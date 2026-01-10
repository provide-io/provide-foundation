#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Transport middleware tests."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.time import make_controlled_time
import pytest

from provide.foundation.transport.base import Request, Response
from provide.foundation.transport.middleware import (
    LoggingMiddleware,
    MetricsMiddleware,
    MiddlewarePipeline,
    RetryMiddleware,
)


@pytest.mark.asyncio
async def test_logging_middleware() -> None:
    """Test logging middleware functionality."""
    middleware = LoggingMiddleware(log_requests=True, log_responses=True)

    request = Request(uri="https://api.example.com/test", method="GET")
    response = Response(status=200, elapsed_ms=100.0)

    # Should not modify request/response
    processed_request = await middleware.process_request(request)
    assert processed_request == request

    processed_response = await middleware.process_response(response)
    assert processed_response == response

    # Error processing
    error = Exception("Test error")
    processed_error = await middleware.process_error(error, request)
    assert processed_error == error


@pytest.mark.asyncio
async def test_metrics_middleware() -> None:
    """Test metrics collection middleware."""
    middleware = MetricsMiddleware()

    # Process request (should add start time)
    request = Request(uri="https://api.example.com/test", method="GET")
    processed_request = await middleware.process_request(request)

    assert "start_time" in processed_request.metadata

    # Process response (should record metrics)
    response = Response(status=200, elapsed_ms=100.0, request=processed_request)
    await middleware.process_response(response)

    # Verify middleware has foundation.metrics instances
    assert hasattr(middleware, "_request_counter")
    assert hasattr(middleware, "_request_duration")
    assert hasattr(middleware, "_error_counter")

    # Process error
    error = Exception("Test error")
    await middleware.process_error(error, request)

    # Test passes if no exceptions are raised during metric recording


@pytest.mark.asyncio
async def test_retry_middleware() -> None:
    """Test retry middleware configuration."""
    from provide.foundation.resilience.retry import BackoffStrategy, RetryPolicy

    policy = RetryPolicy(
        max_attempts=3,
        base_delay=0.1,  # Fast for testing
        backoff=BackoffStrategy.EXPONENTIAL,
        retryable_status_codes={500, 503},
    )
    middleware = RetryMiddleware(policy=policy)

    request = Request(uri="https://api.example.com/test", method="GET")

    # Test with non-retryable exception
    class NonRetryableError(Exception):
        pass

    error = NonRetryableError("Not retryable")
    processed_error = await middleware.process_error(error, request)
    assert processed_error == error

    # Test retry logic would be integration tested with actual transport


@pytest.mark.asyncio
async def test_middleware_pipeline() -> None:
    """Test middleware pipeline execution."""
    pipeline = MiddlewarePipeline()

    # Add middleware
    logging_mw = LoggingMiddleware()
    metrics_mw = MetricsMiddleware()

    pipeline.add(logging_mw)
    pipeline.add(metrics_mw)

    assert len(pipeline.middleware) == 2

    # Test request processing
    request = Request(uri="https://api.example.com/test", method="GET")
    processed_request = await pipeline.process_request(request)

    # Should have start_time from metrics middleware
    assert "start_time" in processed_request.metadata

    # Test response processing (reverse order)
    response = Response(status=200, elapsed_ms=100.0, request=processed_request)
    processed_response = await pipeline.process_response(response)

    assert processed_response.status == 200

    # Check that metrics middleware was used
    assert hasattr(metrics_mw, "_request_counter")
    assert hasattr(metrics_mw, "_request_duration")

    # Test error processing
    error = Exception("Test error")
    processed_error = await pipeline.process_error(error, request)
    assert isinstance(processed_error, Exception)


@pytest.mark.asyncio
async def test_middleware_pipeline_removal() -> None:
    """Test middleware removal from pipeline."""
    pipeline = MiddlewarePipeline()

    logging_mw = LoggingMiddleware()
    metrics_mw = MetricsMiddleware()

    pipeline.add(logging_mw)
    pipeline.add(metrics_mw)

    assert len(pipeline.middleware) == 2

    # Remove middleware by class
    removed = pipeline.remove(LoggingMiddleware)
    assert removed is True
    assert len(pipeline.middleware) == 1

    # Try to remove non-existent middleware
    removed = pipeline.remove(RetryMiddleware)
    assert removed is False
    assert len(pipeline.middleware) == 1


class TestMiddleware(FoundationTestCase):
    """Test middleware that tracks calls."""

    def __init__(self) -> None:
        super().__init__()
        self.calls: list[tuple[str, str | int]] = []

    async def process_request(self, request: Request) -> Request:
        self.calls.append(("request", request.method))
        return request

    async def process_response(self, response: Response) -> Response:
        self.calls.append(("response", response.status))
        return response

    async def process_error(self, error: Exception, request: Request) -> Exception:
        self.calls.append(("error", str(error)))
        return error


@pytest.mark.asyncio
async def test_middleware_order() -> None:
    """Test that middleware executes in correct order."""
    pipeline = MiddlewarePipeline()

    mw1 = TestMiddleware()
    mw2 = TestMiddleware()

    pipeline.add(mw1)
    pipeline.add(mw2)

    request = Request(uri="https://example.com", method="POST")
    response = Response(status=201)
    error = Exception("test error")

    # Process request (forward order)
    await pipeline.process_request(request)

    # Process response (reverse order)
    await pipeline.process_response(response)

    # Process error (forward order)
    await pipeline.process_error(error, request)

    # Check call order
    assert mw1.calls == [("request", "POST"), ("response", 201), ("error", "test error")]
    assert mw2.calls == [("request", "POST"), ("response", 201), ("error", "test error")]


@pytest.mark.asyncio
async def test_retry_middleware_execute() -> None:
    """Test retry middleware execute_with_retry method."""
    from provide.foundation.resilience.retry import BackoffStrategy, RetryPolicy

    # Create controlled time for testing retry delays
    get_time, _advance_time, _fake_sleep, fake_async_sleep = make_controlled_time()

    policy = RetryPolicy(
        max_attempts=3,
        base_delay=0.01,  # Very fast for testing
        backoff=BackoffStrategy.EXPONENTIAL,
        retryable_status_codes={500},
    )
    middleware = RetryMiddleware(
        policy=policy,
        time_source=get_time,
        async_sleep_func=fake_async_sleep,
    )

    request = Request(uri="https://api.example.com/test", method="GET")
    call_count = 0

    async def failing_execute(req: Request) -> Response:
        nonlocal call_count
        call_count += 1

        if call_count <= 2:
            # Fail first two attempts with retryable status
            return Response(status=500, request=req)
        # Succeed on third attempt
        return Response(status=200, request=req)

    # Should retry and eventually succeed
    response = await middleware.execute_with_retry(failing_execute, request)

    assert response.status == 200
    assert call_count == 3  # 1 initial + 2 retries


# 🧱🏗️🔚
