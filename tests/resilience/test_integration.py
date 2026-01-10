#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Integration tests for resilience module with transport middleware and other components."""

from __future__ import annotations

from typing import Any

from provide.testkit import FoundationTestCase
from provide.testkit.time import make_controlled_time
import pytest

from provide.foundation.resilience.decorators import retry
from provide.foundation.resilience.retry import (
    BackoffStrategy,
    RetryExecutor,
    RetryPolicy,
)
from provide.foundation.transport.base import Request, Response
from provide.foundation.transport.errors import TransportError
from provide.foundation.transport.middleware import RetryMiddleware


class TestRetryMiddlewareIntegration(FoundationTestCase):
    """Test RetryMiddleware using unified retry logic."""

    @pytest.mark.asyncio
    async def test_middleware_with_retry_policy(self) -> None:
        """Test middleware configured with RetryPolicy using controlled time."""
        get_time, _advance_time, _fake_sleep, fake_async_sleep = make_controlled_time()

        policy = RetryPolicy(
            max_attempts=3,
            base_delay=0.01,
            backoff=BackoffStrategy.EXPONENTIAL,
            retryable_status_codes={500, 502, 503},
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
                # Fail first two attempts
                return Response(status=500, request=req)
            # Succeed on third attempt
            return Response(status=200, request=req)

        response = await middleware.execute_with_retry(failing_execute, request)

        assert response.status == 200
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_middleware_with_transport_errors(self) -> None:
        """Test middleware retrying transport errors using controlled time."""
        get_time, _advance_time, _fake_sleep, fake_async_sleep = make_controlled_time()

        policy = RetryPolicy(
            max_attempts=3,
            base_delay=0.01,
            retryable_errors=(TransportError,),
        )

        middleware = RetryMiddleware(
            policy=policy,
            time_source=get_time,
            async_sleep_func=fake_async_sleep,
        )

        request = Request(uri="https://api.example.com/test", method="POST")
        call_count = 0

        async def failing_execute(req: Request) -> Response:
            nonlocal call_count
            call_count += 1

            if call_count <= 2:
                raise TransportError("Connection failed")
            return Response(status=200, request=req)

        response = await middleware.execute_with_retry(failing_execute, request)

        assert response.status == 200
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_middleware_non_retryable_status(self) -> None:
        """Test middleware doesn't retry non-retryable status codes using controlled time."""
        get_time, _advance_time, _fake_sleep, fake_async_sleep = make_controlled_time()

        policy = RetryPolicy(
            max_attempts=3,
            base_delay=0.01,
            retryable_status_codes={500, 503},
        )

        middleware = RetryMiddleware(
            policy=policy,
            time_source=get_time,
            async_sleep_func=fake_async_sleep,
        )

        request = Request(uri="https://api.example.com/test", method="GET")
        call_count = 0

        async def execute_404(req: Request) -> Response:
            nonlocal call_count
            call_count += 1
            return Response(status=404, request=req)  # Not retryable

        response = await middleware.execute_with_retry(execute_404, request)

        assert response.status == 404
        assert call_count == 1  # No retries

    @pytest.mark.asyncio
    async def test_middleware_mixed_errors_and_status(self) -> None:
        """Test middleware handling both errors and status codes using controlled time."""
        get_time, _advance_time, _fake_sleep, fake_async_sleep = make_controlled_time()

        policy = RetryPolicy(
            max_attempts=5,
            base_delay=0.01,
            retryable_errors=(TransportError,),
            retryable_status_codes={503},
        )

        middleware = RetryMiddleware(
            policy=policy,
            time_source=get_time,
            async_sleep_func=fake_async_sleep,
        )

        request = Request(uri="https://api.example.com/test", method="PUT")
        call_count = 0

        async def mixed_failures(req: Request) -> Response:
            nonlocal call_count
            call_count += 1

            if call_count == 1:
                raise TransportError("Connection error")
            if call_count == 2:
                return Response(status=503, request=req)
            if call_count == 3:
                raise TransportError("Timeout")
            return Response(status=200, request=req)

        response = await middleware.execute_with_retry(mixed_failures, request)

        assert response.status == 200
        assert call_count == 4


class TestDecoratorWithMiddleware(FoundationTestCase):
    """Test @retry decorator working with middleware."""

    @pytest.mark.asyncio
    async def test_decorated_function_calling_middleware(self) -> None:
        """Test retry decorator on function that uses middleware using controlled time."""
        get_time, _advance_time, _fake_sleep, fake_async_sleep = make_controlled_time()

        policy = RetryPolicy(
            max_attempts=2,
            base_delay=0.01,
            retryable_status_codes={500},
        )

        middleware = RetryMiddleware(
            policy=policy,
            time_source=get_time,
            async_sleep_func=fake_async_sleep,
        )

        @retry(max_attempts=3, base_delay=0.01, time_source=get_time, async_sleep_func=fake_async_sleep)
        async def api_call() -> Response:
            request = Request(uri="https://api.example.com", method="GET")

            async def execute(req: Request) -> Response:
                # Simulate flaky endpoint
                if not hasattr(api_call, "attempts"):
                    api_call.attempts = 0
                api_call.attempts += 1

                if api_call.attempts < 4:
                    return Response(status=500, request=req)
                return Response(status=200, request=req)

            # Middleware handles HTTP retries
            response = await middleware.execute_with_retry(execute, request)

            # Function handles business logic retries
            if response.status != 200:
                raise ValueError(f"Unexpected status: {response.status}")

            return response

        result = await api_call()
        assert result.status == 200

    def test_nested_retry_decorators(self) -> None:
        """Test nested functions with retry decorators using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()

        inner_calls = 0
        outer_calls = 0

        @retry(max_attempts=2, base_delay=0.01, time_source=get_time, sleep_func=fake_sleep)
        def inner_func() -> str:
            nonlocal inner_calls
            inner_calls += 1
            if inner_calls < 2:
                raise ValueError("inner fail")
            return "inner success"

        @retry(max_attempts=3, base_delay=0.01, time_source=get_time, sleep_func=fake_sleep)
        def outer_func() -> str:
            nonlocal outer_calls
            outer_calls += 1

            try:
                result = inner_func()
            except ValueError as e:
                # Inner func exhausted retries
                if outer_calls < 2:
                    raise ValueError("outer fail") from e
                return "outer recovered"

            return result

        # First outer attempt: inner succeeds after retry
        result = outer_func()

        # Inner should retry once and succeed
        assert inner_calls == 2
        assert outer_calls == 1
        assert result == "inner success"


class TestRetryExecutorWithRealWorld(FoundationTestCase):
    """Test RetryExecutor with real-world scenarios."""

    @pytest.mark.asyncio
    async def test_database_connection_retry(self) -> None:
        """Simulate database connection retry scenario using controlled time."""
        get_time, _advance_time, _fake_sleep, fake_async_sleep = make_controlled_time()

        class DatabaseConnection:
            def __init__(self) -> None:
                self.connection_attempts = 0
                self.connected = False

            async def connect(self) -> DatabaseConnection:
                self.connection_attempts += 1
                if self.connection_attempts < 3:
                    raise ConnectionError("Database unavailable")
                self.connected = True
                return self

        policy = RetryPolicy(
            max_attempts=5,
            base_delay=0.01,
            backoff=BackoffStrategy.EXPONENTIAL,
            retryable_errors=(ConnectionError,),
        )

        executor = RetryExecutor(
            policy,
            time_source=get_time,
            async_sleep_func=fake_async_sleep,
        )
        db = DatabaseConnection()

        connection = await executor.execute_async(db.connect)

        assert connection.connected
        assert db.connection_attempts == 3

    def test_api_rate_limit_retry(self) -> None:
        """Simulate API rate limit retry scenario using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()

        class RateLimitError(Exception):
            pass

        class APIClient:
            def __init__(self) -> None:
                self.request_count = 0

            def make_request(self, endpoint: str) -> dict[str, Any]:
                self.request_count += 1
                if self.request_count < 3:
                    raise RateLimitError("Rate limit exceeded")
                return {"status": "success", "data": endpoint}

        policy = RetryPolicy(
            max_attempts=5,
            base_delay=0.01,
            backoff=BackoffStrategy.EXPONENTIAL,
            retryable_errors=(RateLimitError,),
        )

        executor = RetryExecutor(
            policy,
            time_source=get_time,
            sleep_func=fake_sleep,
        )
        client = APIClient()

        result = executor.execute_sync(client.make_request, "/users")

        assert result == {"status": "success", "data": "/users"}
        assert client.request_count == 3

    @pytest.mark.asyncio
    async def test_circuit_breaker_with_retry(self) -> None:
        """Test circuit breaker pattern combined with retry using controlled time."""
        get_time, _advance_time, _fake_sleep, fake_async_sleep = make_controlled_time()

        class CircuitBreaker:
            def __init__(self, failure_threshold: int = 3) -> None:
                self.failure_count = 0
                self.failure_threshold = failure_threshold
                self.is_open = False
                self.half_open_attempts = 0

            async def call(self, func: Any, *args: Any, **kwargs: Any) -> Any:
                if self.is_open:
                    if self.half_open_attempts < 1:
                        # Try half-open state
                        self.half_open_attempts += 1
                        try:
                            result = await func(*args, **kwargs)
                            # Success, close circuit
                            self.is_open = False
                            self.failure_count = 0
                            self.half_open_attempts = 0  # Reset half-open counter
                            return result
                        except Exception:
                            # Still failing, stay open
                            raise
                    else:
                        raise RuntimeError("Circuit breaker is open")

                try:
                    result = await func(*args, **kwargs)
                    # Success, reset failure count
                    self.failure_count = 0
                    return result
                except Exception:
                    self.failure_count += 1
                    if self.failure_count >= self.failure_threshold:
                        self.is_open = True
                        self.half_open_attempts = 0  # Reset when opening
                    raise

        breaker = CircuitBreaker(failure_threshold=2)
        policy = RetryPolicy(
            max_attempts=3,
            base_delay=0.01,
            retryable_errors=(ValueError, RuntimeError),
        )
        executor = RetryExecutor(
            policy,
            time_source=get_time,
            async_sleep_func=fake_async_sleep,
        )

        call_count = 0

        async def flaky_service() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 4:
                raise ValueError("Service error")
            return "success"

        # First call will fail and open the circuit after retries
        with pytest.raises(ValueError):
            await executor.execute_async(breaker.call, flaky_service)

        # Circuit should be open now
        assert breaker.is_open

        # Reset for recovery test
        call_count = 3  # Next call will succeed
        breaker.half_open_attempts = 0  # Reset half-open attempts for clean recovery test

        # Try again - circuit attempts half-open
        result = await executor.execute_async(breaker.call, flaky_service)

        assert result == "success"
        assert not breaker.is_open  # Circuit closed


# 🧱🏗️🔚
