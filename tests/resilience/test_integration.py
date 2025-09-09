"""
Integration tests for resilience module with transport middleware and other components.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from provide.foundation.resilience.decorators import retry
from provide.foundation.resilience.retry import BackoffStrategy, RetryExecutor, RetryPolicy
from provide.foundation.transport.base import Request, Response
from provide.foundation.transport.errors import TransportError
from provide.foundation.transport.middleware import RetryMiddleware


class TestRetryMiddlewareIntegration:
    """Test RetryMiddleware using unified retry logic."""

    @pytest.mark.asyncio
    async def test_middleware_with_retry_policy(self):
        """Test middleware configured with RetryPolicy."""
        policy = RetryPolicy(
            max_attempts=3,
            base_delay=0.01,
            backoff=BackoffStrategy.EXPONENTIAL,
            retryable_status_codes={500, 502, 503}
        )
        
        middleware = RetryMiddleware(policy=policy)
        
        request = Request(uri="https://api.example.com/test", method="GET")
        call_count = 0
        
        async def failing_execute(req):
            nonlocal call_count
            call_count += 1
            
            if call_count <= 2:
                # Fail first two attempts
                return Response(status=500, request=req)
            else:
                # Succeed on third attempt
                return Response(status=200, request=req)
        
        response = await middleware.execute_with_retry(failing_execute, request)
        
        assert response.status == 200
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_middleware_with_transport_errors(self):
        """Test middleware retrying transport errors."""
        policy = RetryPolicy(
            max_attempts=3,
            base_delay=0.01,
            retryable_errors=(TransportError,)
        )
        
        middleware = RetryMiddleware(policy=policy)
        
        request = Request(uri="https://api.example.com/test", method="POST")
        call_count = 0
        
        async def failing_execute(req):
            nonlocal call_count
            call_count += 1
            
            if call_count <= 2:
                raise TransportError("Connection failed")
            return Response(status=200, request=req)
        
        response = await middleware.execute_with_retry(failing_execute, request)
        
        assert response.status == 200
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_middleware_non_retryable_status(self):
        """Test middleware doesn't retry non-retryable status codes."""
        policy = RetryPolicy(
            max_attempts=3,
            base_delay=0.01,
            retryable_status_codes={500, 503}
        )
        
        middleware = RetryMiddleware(policy=policy)
        
        request = Request(uri="https://api.example.com/test", method="GET")
        call_count = 0
        
        async def execute_404(req):
            nonlocal call_count
            call_count += 1
            return Response(status=404, request=req)  # Not retryable
        
        response = await middleware.execute_with_retry(execute_404, request)
        
        assert response.status == 404
        assert call_count == 1  # No retries

    @pytest.mark.asyncio
    async def test_middleware_mixed_errors_and_status(self):
        """Test middleware handling both errors and status codes."""
        policy = RetryPolicy(
            max_attempts=5,
            base_delay=0.01,
            retryable_errors=(TransportError,),
            retryable_status_codes={503}
        )
        
        middleware = RetryMiddleware(policy=policy)
        
        request = Request(uri="https://api.example.com/test", method="PUT")
        call_count = 0
        
        async def mixed_failures(req):
            nonlocal call_count
            call_count += 1
            
            if call_count == 1:
                raise TransportError("Connection error")
            elif call_count == 2:
                return Response(status=503, request=req)
            elif call_count == 3:
                raise TransportError("Timeout")
            else:
                return Response(status=200, request=req)
        
        response = await middleware.execute_with_retry(mixed_failures, request)
        
        assert response.status == 200
        assert call_count == 4


class TestDecoratorWithMiddleware:
    """Test @retry decorator working with middleware."""

    @pytest.mark.asyncio
    async def test_decorated_function_calling_middleware(self):
        """Test retry decorator on function that uses middleware."""
        policy = RetryPolicy(
            max_attempts=2,
            base_delay=0.01,
            retryable_status_codes={500}
        )
        
        middleware = RetryMiddleware(policy=policy)
        
        @retry(max_attempts=3, base_delay=0.01)
        async def api_call():
            request = Request(uri="https://api.example.com", method="GET")
            
            async def execute(req):
                # Simulate flaky endpoint
                if not hasattr(api_call, 'attempts'):
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

    def test_nested_retry_decorators(self):
        """Test nested functions with retry decorators."""
        inner_calls = 0
        outer_calls = 0
        
        @retry(max_attempts=2, base_delay=0.01)
        def inner_func():
            nonlocal inner_calls
            inner_calls += 1
            if inner_calls < 2:
                raise ValueError("inner fail")
            return "inner success"
        
        @retry(max_attempts=3, base_delay=0.01)
        def outer_func():
            nonlocal outer_calls
            outer_calls += 1
            
            try:
                result = inner_func()
            except ValueError:
                # Inner func exhausted retries
                if outer_calls < 2:
                    raise ValueError("outer fail")
                return "outer recovered"
            
            return result
        
        # First outer attempt: inner succeeds after retry
        result = outer_func()
        
        # Inner should retry once and succeed
        assert inner_calls == 2
        assert outer_calls == 1
        assert result == "inner success"


class TestRetryExecutorWithRealWorld:
    """Test RetryExecutor with real-world scenarios."""

    @pytest.mark.asyncio
    async def test_database_connection_retry(self):
        """Simulate database connection retry scenario."""
        
        class DatabaseConnection:
            def __init__(self):
                self.connection_attempts = 0
                self.connected = False
            
            async def connect(self):
                self.connection_attempts += 1
                if self.connection_attempts < 3:
                    raise ConnectionError("Database unavailable")
                self.connected = True
                return self
        
        policy = RetryPolicy(
            max_attempts=5,
            base_delay=0.1,
            backoff=BackoffStrategy.EXPONENTIAL,
            retryable_errors=(ConnectionError,)
        )
        
        executor = RetryExecutor(policy)
        db = DatabaseConnection()
        
        with patch('asyncio.sleep'):  # Speed up test
            connection = await executor.execute_async(db.connect)
        
        assert connection.connected
        assert db.connection_attempts == 3

    def test_api_rate_limit_retry(self):
        """Simulate API rate limit retry scenario."""
        
        class RateLimitError(Exception):
            pass
        
        class APIClient:
            def __init__(self):
                self.request_count = 0
            
            def make_request(self, endpoint):
                self.request_count += 1
                if self.request_count < 3:
                    raise RateLimitError("Rate limit exceeded")
                return {"status": "success", "data": endpoint}
        
        policy = RetryPolicy(
            max_attempts=5,
            base_delay=1.0,
            backoff=BackoffStrategy.EXPONENTIAL,
            retryable_errors=(RateLimitError,)
        )
        
        executor = RetryExecutor(policy)
        client = APIClient()
        
        with patch('time.sleep'):  # Speed up test
            result = executor.execute_sync(client.make_request, "/users")
        
        assert result == {"status": "success", "data": "/users"}
        assert client.request_count == 3

    @pytest.mark.asyncio
    async def test_circuit_breaker_with_retry(self):
        """Test circuit breaker pattern combined with retry."""
        
        class CircuitBreaker:
            def __init__(self, failure_threshold=3):
                self.failure_count = 0
                self.failure_threshold = failure_threshold
                self.is_open = False
                self.half_open_attempts = 0
            
            async def call(self, func, *args, **kwargs):
                if self.is_open:
                    if self.half_open_attempts < 1:
                        # Try half-open state
                        self.half_open_attempts += 1
                        try:
                            result = await func(*args, **kwargs)
                            # Success, close circuit
                            self.is_open = False
                            self.failure_count = 0
                            return result
                        except Exception:
                            # Still failing, stay open
                            raise
                    else:
                        raise RuntimeError("Circuit breaker is open")
                
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    self.failure_count += 1
                    if self.failure_count >= self.failure_threshold:
                        self.is_open = True
                    raise
        
        breaker = CircuitBreaker(failure_threshold=2)
        policy = RetryPolicy(
            max_attempts=3,
            base_delay=0.01,
            retryable_errors=(ValueError,)
        )
        executor = RetryExecutor(policy)
        
        call_count = 0
        
        async def flaky_service():
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
        
        # Try again - circuit attempts half-open
        result = await executor.execute_async(breaker.call, flaky_service)
        
        assert result == "success"
        assert not breaker.is_open  # Circuit closed


class TestBackwardCompatibility:
    """Test backward compatibility with existing code."""

    def test_old_retry_on_error_import(self):
        """Test that old import path still works with deprecation warning."""
        with patch('warnings.warn') as mock_warn:
            from provide.foundation.errors.decorators import retry_on_error
            
            mock_warn.assert_called()
            warning_message = str(mock_warn.call_args[0][0])
            assert "deprecated" in warning_message.lower()
            assert "resilience" in warning_message.lower()
        
        # Should still work
        @retry_on_error(max_attempts=2, delay=0.01)
        def func():
            if not hasattr(func, 'called'):
                func.called = True
                raise ValueError("test")
            return "success"
        
        result = func()
        assert result == "success"

    def test_old_retry_policy_import(self):
        """Test that old RetryPolicy import still works."""
        with patch('warnings.warn') as mock_warn:
            from provide.foundation.errors.types import RetryPolicy as OldRetryPolicy
            
            mock_warn.assert_called()
            warning_message = str(mock_warn.call_args[0][0])
            assert "deprecated" in warning_message.lower()
        
        # Should still work
        policy = OldRetryPolicy(max_attempts=3)
        assert policy.max_attempts == 3

    def test_middleware_with_old_policy(self):
        """Test that middleware works with policies from old import."""
        with patch('warnings.warn'):
            from provide.foundation.errors.types import RetryPolicy as OldRetryPolicy
        
        policy = OldRetryPolicy(
            max_attempts=2,
            base_delay=0.01,
            retryable_errors=(ValueError,)
        )
        
        # Should work with middleware
        middleware = RetryMiddleware(policy=policy)
        assert middleware.policy.max_attempts == 2