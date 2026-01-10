#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Additional tests for transport middleware to improve coverage."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch
from provide.testkit.time import make_controlled_time
import pytest

from provide.foundation.transport.base import Request, Response
from provide.foundation.transport.errors import TransportError
from provide.foundation.transport.middleware import (
    LoggingMiddleware,
    MetricsMiddleware,
    MiddlewarePipeline,
    RetryMiddleware,
    create_default_pipeline,
    get_middleware_by_category,
    register_middleware,
)


class TestLoggingMiddlewareEdgeCases(FoundationTestCase):
    """Test edge cases in LoggingMiddleware."""

    @pytest.mark.asyncio
    async def test_logging_middleware_disabled_logging(self) -> None:
        """Test LoggingMiddleware with logging disabled."""
        middleware = LoggingMiddleware(log_requests=False, log_responses=False, log_bodies=False)

        request = Request(uri="https://api.example.com/test", method="GET", body="test body")
        response = Response(status=200, elapsed_ms=100.0, body="response body", request=request)

        # Should not log anything but still return the same objects
        processed_request = await middleware.process_request(request)
        assert processed_request == request

        processed_response = await middleware.process_response(response)
        assert processed_response == response

    @pytest.mark.asyncio
    async def test_logging_middleware_body_logging(self) -> None:
        """Test LoggingMiddleware with body logging enabled."""
        middleware = LoggingMiddleware(log_requests=True, log_responses=True, log_bodies=True)

        request = Request(uri="https://api.example.com/test", method="POST", body="request body")
        response = Response(status=200, elapsed_ms=100.0, body="response body", request=request)

        # Should log bodies
        processed_request = await middleware.process_request(request)
        assert processed_request == request

        processed_response = await middleware.process_response(response)
        assert processed_response == response

    @pytest.mark.asyncio
    async def test_logging_middleware_no_body(self) -> None:
        """Test LoggingMiddleware with no request/response body."""
        middleware = LoggingMiddleware(log_requests=True, log_responses=True, log_bodies=True)

        request = Request(uri="https://api.example.com/test", method="GET")
        response = Response(status=200, elapsed_ms=100.0, request=request)

        # Should handle missing bodies gracefully
        processed_request = await middleware.process_request(request)
        assert processed_request == request

        processed_response = await middleware.process_response(response)
        assert processed_response == response

    def test_status_emoji_generation(self) -> None:
        """Test status emoji generation for different status codes."""
        middleware = LoggingMiddleware()

        # 2xx success

        # 3xx redirect
        assert middleware._get_status_emoji(301) == "↩️"
        assert middleware._get_status_emoji(302) == "↩️"
        assert middleware._get_status_emoji(399) == "↩️"

        # 4xx client error
        assert middleware._get_status_emoji(400) == "⚠️"
        assert middleware._get_status_emoji(404) == "⚠️"
        assert middleware._get_status_emoji(499) == "⚠️"

        # 5xx server error
        assert middleware._get_status_emoji(500) == "❌"
        assert middleware._get_status_emoji(503) == "❌"
        assert middleware._get_status_emoji(599) == "❌"

        # Unknown status codes
        assert middleware._get_status_emoji(100) == "❓"
        assert middleware._get_status_emoji(600) == "❓"
        assert middleware._get_status_emoji(999) == "❓"

    @pytest.mark.asyncio
    async def test_logging_middleware_no_headers(self) -> None:
        """Test LoggingMiddleware with objects that don't have headers."""
        middleware = LoggingMiddleware(log_requests=True, log_responses=True)

        # Create request/response without headers attribute
        request = Request(uri="https://api.example.com/test", method="GET")
        response = Response(status=200, elapsed_ms=100.0, request=request)

        # Remove headers if they exist
        if hasattr(request, "headers"):
            delattr(request, "headers")
        if hasattr(response, "headers"):
            delattr(response, "headers")

        # Should handle missing headers gracefully
        await middleware.process_request(request)
        await middleware.process_response(response)

    @pytest.mark.asyncio
    async def test_logging_middleware_response_no_request(self) -> None:
        """Test LoggingMiddleware with response that has no request."""
        middleware = LoggingMiddleware(log_responses=True)

        response = Response(status=200, elapsed_ms=100.0)  # No request attached

        # Should handle missing request gracefully
        processed_response = await middleware.process_response(response)
        assert processed_response == response


class TestRetryMiddlewareEdgeCases(FoundationTestCase):
    """Test edge cases in RetryMiddleware."""

    @pytest.mark.asyncio
    async def test_retry_middleware_non_retryable_error(self) -> None:
        """Test RetryMiddleware with non-retryable errors."""
        from provide.foundation.resilience.retry import RetryPolicy

        # Create controlled time for testing
        get_time, _advance_time, _fake_sleep, fake_async_sleep = make_controlled_time()

        policy = RetryPolicy(max_attempts=3, retryable_errors=(ValueError,))
        middleware = RetryMiddleware(
            policy=policy,
            time_source=get_time,
            async_sleep_func=fake_async_sleep,
        )

        request = Request(uri="https://api.example.com/test", method="GET")

        # Test with non-retryable error
        error = TypeError("Not retryable")
        processed_error = await middleware.process_error(error, request)
        assert processed_error == error

    @pytest.mark.asyncio
    async def test_retry_middleware_execute_success_first_try(self) -> None:
        """Test RetryMiddleware when request succeeds on first try."""
        # Create controlled time for testing
        get_time, _advance_time, _fake_sleep, fake_async_sleep = make_controlled_time()

        middleware = RetryMiddleware(
            time_source=get_time,
            async_sleep_func=fake_async_sleep,
        )
        request = Request(uri="https://api.example.com/test", method="GET")

        async def success_execute(req: Request) -> Response:
            return Response(status=200, request=req)

        response = await middleware.execute_with_retry(success_execute, request)
        assert response.status == 200

    @pytest.mark.asyncio
    async def test_retry_middleware_execute_retryable_status_exhausted(self) -> None:
        """Test RetryMiddleware when retries are exhausted."""
        from provide.foundation.resilience.retry import RetryPolicy

        # Create controlled time for testing
        get_time, _advance_time, _fake_sleep, fake_async_sleep = make_controlled_time()

        policy = RetryPolicy(max_attempts=2, base_delay=0.01, retryable_status_codes={500})
        middleware = RetryMiddleware(
            policy=policy,
            time_source=get_time,
            async_sleep_func=fake_async_sleep,
        )
        request = Request(uri="https://api.example.com/test", method="GET")

        async def always_fail_execute(req: Request) -> Response:
            return Response(status=500, request=req)

        # Should eventually raise TransportError after exhausting retries
        with pytest.raises(TransportError, match="Retryable HTTP status: 500"):
            await middleware.execute_with_retry(always_fail_execute, request)

    @pytest.mark.asyncio
    async def test_retry_middleware_execute_transport_error_passthrough(self) -> None:
        """Test RetryMiddleware passes through non-synthetic TransportError."""
        # Create controlled time for testing
        get_time, _advance_time, _fake_sleep, fake_async_sleep = make_controlled_time()

        middleware = RetryMiddleware(
            time_source=get_time,
            async_sleep_func=fake_async_sleep,
        )
        request = Request(uri="https://api.example.com/test", method="GET")

        async def error_execute(req: Request) -> Response:
            raise TransportError("Network error")

        # Should pass through the original TransportError
        with pytest.raises(TransportError, match="Network error"):
            await middleware.execute_with_retry(error_execute, request)


class TestMetricsMiddlewareEdgeCases(FoundationTestCase):
    """Test edge cases in MetricsMiddleware."""

    @pytest.mark.asyncio
    async def test_metrics_middleware_response_no_start_time(self) -> None:
        """Test MetricsMiddleware when response request has no start_time."""
        middleware = MetricsMiddleware()

        request = Request(uri="https://api.example.com/test", method="GET")
        # Don't set start_time in metadata
        response = Response(status=200, elapsed_ms=100.0, request=request)

        # Should handle missing start_time gracefully
        processed_response = await middleware.process_response(response)
        assert processed_response == response

    @pytest.mark.asyncio
    async def test_metrics_middleware_response_no_request(self) -> None:
        """Test MetricsMiddleware when response has no request."""
        middleware = MetricsMiddleware()

        response = Response(status=200, elapsed_ms=100.0)  # No request attached

        # Should handle missing request gracefully
        processed_response = await middleware.process_response(response)
        assert processed_response == response

    @pytest.mark.asyncio
    async def test_metrics_middleware_different_error_types(self) -> None:
        """Test MetricsMiddleware with different error types."""
        middleware = MetricsMiddleware()
        request = Request(uri="https://api.example.com/test", method="POST")

        # Test different error types
        errors = [
            ValueError("Value error"),
            TypeError("Type error"),
            ConnectionError("Connection error"),
            TransportError("Transport error"),
        ]

        for error in errors:
            processed_error = await middleware.process_error(error, request)
            assert processed_error == error


class TestMiddlewarePipelineEdgeCases(FoundationTestCase):
    """Test edge cases in MiddlewarePipeline."""

    @pytest.mark.asyncio
    async def test_empty_pipeline(self) -> None:
        """Test MiddlewarePipeline with no middleware."""
        pipeline = MiddlewarePipeline()

        request = Request(uri="https://api.example.com/test", method="GET")
        response = Response(status=200, elapsed_ms=100.0)
        error = Exception("Test error")

        # Should pass through unchanged
        processed_request = await pipeline.process_request(request)
        assert processed_request == request

        processed_response = await pipeline.process_response(response)
        assert processed_response == response

        processed_error = await pipeline.process_error(error, request)
        assert processed_error == error

    def test_middleware_pipeline_add_tracking(self) -> None:
        """Test that MiddlewarePipeline properly tracks added middleware."""
        pipeline = MiddlewarePipeline()

        middleware1 = LoggingMiddleware()
        middleware2 = MetricsMiddleware()

        # Initially empty
        assert len(pipeline.middleware) == 0

        # Add middleware
        pipeline.add(middleware1)
        assert len(pipeline.middleware) == 1
        assert pipeline.middleware[0] == middleware1

        pipeline.add(middleware2)
        assert len(pipeline.middleware) == 2
        assert pipeline.middleware[1] == middleware2

    def test_middleware_pipeline_remove_nonexistent(self) -> None:
        """Test removing middleware that doesn't exist."""
        pipeline = MiddlewarePipeline()
        pipeline.add(LoggingMiddleware())

        # Try to remove middleware not in pipeline
        result = pipeline.remove(RetryMiddleware)
        assert result is False
        assert len(pipeline.middleware) == 1


class TestMiddlewareRegistration(FoundationTestCase):
    """Test middleware registration functions."""

    def test_register_middleware_basic(self) -> None:
        """Test basic middleware registration."""
        with patch("provide.foundation.transport.middleware.get_component_registry") as mock_registry:
            mock_reg = Mock()
            mock_registry.return_value = mock_reg

            register_middleware("test", LoggingMiddleware)

            mock_reg.register.assert_called_once()
            _args, kwargs = mock_reg.register.call_args
            assert kwargs["name"] == "test"
            assert kwargs["value"] == LoggingMiddleware
            assert kwargs["dimension"] == "transport.middleware"
            assert kwargs["replace"] is True

    def test_register_middleware_with_metadata(self) -> None:
        """Test middleware registration with custom metadata."""
        with patch("provide.foundation.transport.middleware.get_component_registry") as mock_registry:
            mock_reg = Mock()
            mock_registry.return_value = mock_reg

            register_middleware("test", LoggingMiddleware, category="custom", priority=50, extra="value")

            mock_reg.register.assert_called_once()
            _args, kwargs = mock_reg.register.call_args
            assert kwargs["dimension"] == "custom"
            assert kwargs["metadata"]["priority"] == 50
            assert kwargs["metadata"]["extra"] == "value"

    def test_get_middleware_by_category(self) -> None:
        """Test getting middleware by category."""
        with patch("provide.foundation.transport.middleware.get_component_registry") as mock_registry:
            # Mock registry entries
            mock_entry1 = Mock()
            mock_entry1.dimension = "transport.middleware"
            mock_entry1.value = LoggingMiddleware
            mock_entry1.metadata = {"priority": 20}

            mock_entry2 = Mock()
            mock_entry2.dimension = "transport.middleware"
            mock_entry2.value = MetricsMiddleware
            mock_entry2.metadata = {"priority": 10}

            mock_entry3 = Mock()
            mock_entry3.dimension = "other.category"
            mock_entry3.value = RetryMiddleware
            mock_entry3.metadata = {"priority": 30}

            # Mock the registry as an iterable
            mock_registry.return_value = [mock_entry1, mock_entry2, mock_entry3]

            result = get_middleware_by_category("transport.middleware")

            # Should return only matching category, sorted by priority
            assert len(result) == 2
            assert result[0] == MetricsMiddleware  # Priority 10 (higher priority)
            assert result[1] == LoggingMiddleware  # Priority 20

    def test_get_middleware_by_category_default_priority(self) -> None:
        """Test getting middleware with default priority."""
        with patch("provide.foundation.transport.middleware.get_component_registry") as mock_registry:
            # Mock entry without priority metadata
            mock_entry = Mock()
            mock_entry.dimension = "transport.middleware"
            mock_entry.value = LoggingMiddleware
            mock_entry.metadata = {}  # No priority

            # Mock the registry as an iterable
            mock_registry.return_value = [mock_entry]

            result = get_middleware_by_category("transport.middleware")
            assert len(result) == 1
            assert result[0] == LoggingMiddleware


class TestDefaultPipeline(FoundationTestCase):
    """Test default pipeline creation."""

    def test_create_default_pipeline(self) -> None:
        """Test creating default middleware pipeline."""
        pipeline = create_default_pipeline()

        assert isinstance(pipeline, MiddlewarePipeline)
        assert len(pipeline.middleware) == 3

        # Check middleware types
        middleware_types = [type(mw) for mw in pipeline.middleware]
        assert RetryMiddleware in middleware_types
        assert LoggingMiddleware in middleware_types
        assert MetricsMiddleware in middleware_types


class TestBuiltinRegistration(FoundationTestCase):
    """Test builtin middleware registration."""

    def test_builtin_registration_import_error(self) -> None:
        """Test builtin middleware registration handles ImportError."""
        with patch(
            "provide.foundation.transport.middleware.register_middleware",
            side_effect=ImportError("Registry not available"),
        ):
            # Should not raise exception
            from provide.foundation.transport.middleware import _register_builtin_middleware

            _register_builtin_middleware()

    def test_builtin_registration_success(self) -> None:
        """Test successful builtin middleware registration."""
        with patch("provide.foundation.transport.middleware.register_middleware") as mock_register:
            from provide.foundation.transport.middleware import _register_builtin_middleware

            _register_builtin_middleware()

            # Should register all three builtin middleware
            assert mock_register.call_count == 3

            # Check registration calls
            calls = mock_register.call_args_list
            middleware_names = [call[0][0] for call in calls]
            assert "logging" in middleware_names
            assert "retry" in middleware_names
            assert "metrics" in middleware_names


# 🧱🏗️🔚
