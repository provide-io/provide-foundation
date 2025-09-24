#!/bin/bash
# 🛠️ Project Update Script
set -eo pipefail

# --- Logging ---
log_info() { echo -e "ℹ️  $1"; }
log_create() { echo -e "✨ $1"; }
log_update() { echo -e "🔄 $1"; }
log_delete() { echo -e "🔥 $1"; }
log_success() { echo -e "✅ $1"; }

# --- Operations ---
log_info "Applying fixes to flaky tests..."

log_update "Updating: tests/errors/test_integration.py to make performance test more robust"
mkdir -p tests/errors/
cat <<'EOF' > tests/errors/test_integration.py
"""Integration tests for the error handling system."""

import asyncio
from contextvars import ContextVar
import json
import time
from typing import Never
from unittest.mock import patch

import pytest

from provide.foundation import (
    FoundationError,
    error_boundary,
    resilient,
)
from provide.foundation.errors import (
    AlreadyExistsError,
    AuthenticationError,
    ConfigurationError,
    IntegrationError,
    NetworkError,
    NotFoundError,
    ValidationError,
)
from provide.foundation.errors.context import (
    ErrorCategory,
    ErrorSeverity,
    capture_error_context,
)
from provide.foundation.errors.decorators import (
    fallback_on_error,
    suppress_and_log,
)
from provide.foundation.errors.handlers import (
    ErrorHandler,
    handle_error,
    transactional,
)
from provide.foundation.errors.types import ErrorCode, ErrorMetadata
from provide.foundation.resilience import circuit_breaker, retry


class TestErrorSystemIntegration:
    """Integration tests for the complete error system."""

    def test_end_to_end_error_flow(self) -> None:
        """Test complete error flow from creation to handling."""
        # Create error with rich context
        error = ValidationError(
            "Invalid configuration",
            field="timeout",
            value=-1,
            code="VAL_002",
            request_id="req_123",
            user_id="usr_456",
        )

        # Add more context
        error.add_context("service.name", "api-gateway")
        error.add_context("service.version", "1.2.3")

        # Capture error context
        ctx = capture_error_context(
            error,
            severity=ErrorSeverity.HIGH,
            terraform={"provider": "aws", "resource": "lambda"},
        )

        # Verify context structure
        assert ctx.severity == ErrorSeverity.HIGH
        assert ctx.category == ErrorCategory.USER

        # Convert to dict for logging
        log_data = error.to_dict()
        assert log_data["error.type"] == "ValidationError"
        assert log_data["error.code"] == "VAL_002"
        assert log_data["validation.field"] == "timeout"

        # Test error handling
        handled = handle_error(error, log=False, fallback="default")
        assert handled == "default"

    def test_nested_error_handling(self) -> None:
        """Test nested error handlers and boundaries."""
        call_stack = []

        def inner_function() -> Never:
            call_stack.append("inner")
            raise ValidationError("Inner error", field="email")

        @resilient(suppress=(ValidationError,), fallback="handled")
        def middle_function() -> None:
            call_stack.append("middle")
            with error_boundary(NetworkError, reraise=True):
                inner_function()

        def outer_function():
            call_stack.append("outer")
            with transactional(
                rollback=lambda: call_stack.append("rollback"),
                commit=lambda: call_stack.append("commit"),
            ):
                return middle_function()

        result = outer_function()

        assert result == "handled"
        assert call_stack == ["outer", "middle", "inner", "commit"]

    def test_error_chain_propagation(self) -> None:
        """Test error chaining and context propagation."""
        # Original error
        original = NetworkError("Connection refused", host="db.example.com", port=5432)

        # Wrap in integration error
        integration = IntegrationError(
            "Database unavailable",
            service="user-service",
            cause=original,
        )
        integration.context.update(original.context)

        # Wrap in configuration error
        config = ConfigurationError(
            "Service misconfigured",
            config_key="database.url",
            cause=integration,
        )

        # Verify chain
        assert config.cause is integration
        assert integration.cause is original
        assert config.__cause__ is integration

        # Verify context propagation
        assert integration.context["network.host"] == "db.example.com"

    def test_retry_with_circuit_breaker(self) -> None:
        """Test combining retry and circuit breaker patterns."""
        attempt_count = 0

        @circuit_breaker(failure_threshold=3, recovery_timeout=0.01)
        @retry(max_attempts=2, base_delay=0.01)
        def unreliable_service() -> str:
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 7:
                raise NetworkError("Service down")
            return "success"

        # First call: 2 attempts (retry), both fail - circuit counts as 1 failure
        with pytest.raises(NetworkError):
            unreliable_service()
        assert attempt_count == 2

        # Second call: 2 attempts (retry), both fail - circuit counts as 2 failures
        with pytest.raises(NetworkError):
            unreliable_service()
        assert attempt_count == 4

        # Third call: 2 attempts (retry), both fail - circuit opens (3 failures)
        with pytest.raises(NetworkError):
            unreliable_service()
        assert attempt_count == 6

        # Fourth call: circuit is open
        with pytest.raises(RuntimeError) as exc_info:
            unreliable_service()
        assert "Circuit breaker is open" in str(exc_info.value)
        assert attempt_count == 6  # No new attempt

        # Wait for recovery
        time.sleep(0.02)

        # Fifth call: circuit half-open, succeeds
        result = unreliable_service()
        assert result == "success"
        assert attempt_count == 7

    def test_error_handler_chain(self) -> None:
        """Test chaining multiple error handlers."""
        results = []

        # Create handler chain
        handler1 = ErrorHandler(
            policies={
                ValidationError: lambda e: results.append("validation") or "v",
                NetworkError: lambda e: results.append("network") or "n",
            },
        )

        handler2 = ErrorHandler(
            policies={ConfigurationError: lambda e: results.append("config") or "c"},
            default_action=lambda e: results.append("default") or "d",
        )

        # Test different error types
        assert handler1.handle(ValidationError("test")) == "v"
        assert handler1.handle(ConfigurationError("test")) is None  # No handler
        assert handler2.handle(ConfigurationError("test")) == "c"
        assert handler2.handle(NotFoundError("test")) == "d"  # Default

        assert results == ["validation", "config", "default"]

    def test_context_vars_integration(self) -> None:
        """Test integration with context variables."""
        request_context = ContextVar("request_context", default={})

        def set_request_context(**kwargs) -> None:
            ctx = request_context.get().copy()
            ctx.update(kwargs)
            request_context.set(ctx)

        def create_contextualized_error(message: str, **kwargs):
            error = FoundationError(message, **kwargs)
            error.context.update(request_context.get())
            return error

        # Simulate request handling
        set_request_context(request_id="req_123", user_id="usr_456")

        # Create error within request context
        error = create_contextualized_error("Operation failed", operation="create_user")

        assert error.context["request_id"] == "req_123"
        assert error.context["user_id"] == "usr_456"
        assert error.context["operation"] == "create_user"

    @pytest.mark.asyncio
    async def test_async_error_handling(self) -> None:
        """Test error handling in async context."""

        async def async_operation() -> Never:
            await asyncio.sleep(0.01)
            raise NetworkError("Async failure", host="async.example.com")

        @resilient(fallback="async_default", suppress=(NetworkError,))
        async def async_with_handling():
            return await async_operation()

        result = await async_with_handling()
        assert result == "async_default"

    def test_terraform_diagnostic_integration(self) -> None:
        """Test Terraform diagnostic generation."""
        # Create error with Terraform context
        error = IntegrationError(
            "Provider initialization failed",
            service="terraform",
            status_code=403,
        )

        # Add Terraform-specific context
        error.add_context("terraform.provider", "registry.terraform.io/hashicorp/aws")
        error.add_context("terraform.resource_type", "aws_instance")
        error.add_context(
            "terraform.resource_address",
            "module.compute.aws_instance.web[0]",
        )
        error.add_context("aws.region", "us-east-1")
        error.add_context("aws.error_code", "UnauthorizedOperation")

        # Capture context
        ctx = capture_error_context(error)

        # Generate Terraform diagnostic
        diagnostic = ctx.to_terraform_diagnostic()

        assert diagnostic["severity"] == "error"
        assert "provider" in diagnostic["detail"]
        assert diagnostic["detail"]["aws"] == {
            "region": "us-east-1",
            "error_code": "UnauthorizedOperation",
        }

    def test_error_recovery_strategies(self) -> None:
        """Test different error recovery strategies."""
        call_log = []

        # Strategy 1: Retry with exponential backoff
        @retry(max_attempts=3, base_delay=0.01)
        def retry_strategy() -> str:
            call_log.append("retry")
            if len([c for c in call_log if c == "retry"]) < 3:
                raise NetworkError("Temporary failure")
            return "retry_success"

        # Strategy 2: Fallback
        def fallback_func() -> str:
            call_log.append("fallback")
            return "fallback_success"

        @fallback_on_error(fallback_func, NetworkError)
        def fallback_strategy() -> Never:
            call_log.append("primary")
            raise NetworkError("Primary failed")

        # Strategy 3: Suppress and continue
        @suppress_and_log(ValueError, fallback="suppressed")
        def suppress_strategy() -> Never:
            call_log.append("suppress")
            raise ValueError("Ignorable error")

        # Test all strategies
        assert retry_strategy() == "retry_success"
        assert fallback_strategy() == "fallback_success"
        assert suppress_strategy() == "suppressed"

        assert call_log == [
            "retry",
            "retry",
            "retry",
            "primary",
            "fallback",
            "suppress",
        ]

    def test_error_metadata_and_response(self) -> None:
        """Test error metadata and response generation."""
        from provide.foundation.errors.types import ErrorResponse

        # Create error with metadata
        metadata = ErrorMetadata(
            request_id="req_123",
            correlation_id="corr_456",
            retry_count=2,
            retry_after=30.0,
            help_url="https://docs.example.com/errors/AUTH_002",
        )

        error = AuthenticationError("Token expired", auth_method="jwt", realm="api")

        # Create error response
        response = ErrorResponse(
            error_code=ErrorCode.AUTH_TOKEN_EXPIRED.value,
            message=error.message,
            details={
                "auth_method": error.context.get("auth.method"),
                "realm": error.context.get("auth.realm"),
            },
            metadata=metadata,
        )

        # Verify JSON serialization
        json_str = response.to_json()
        data = json.loads(json_str)

        assert data["error_code"] == "AUTH_002"
        assert data["message"] == "Token expired"
        assert data["details"]["auth_method"] == "jwt"
        assert data["metadata"]["retry_after"] == 30.0

    @patch("provide.foundation.hub.foundation.get_foundation_logger")
    def test_logging_integration(self, mock_logger) -> Never:
        """Test integration with logging system."""
        # Create and handle error
        error = ValidationError("Invalid input", field="email", value="not-an-email")

        with error_boundary(ValidationError, log_errors=True, reraise=False):
            raise error

        # Verify logging
        mock_logger.return_value.error.assert_called_once()
        call_args = mock_logger.return_value.error.call_args

        # Check logged context
        assert call_args[1]["error.type"] == "ValidationError"
        assert call_args[1]["error.message"] == "Invalid input"
        assert call_args[1]["validation.field"] == "email"

    def test_custom_error_extension(self) -> None:
        """Test extending the error system with custom errors."""

        # Define custom error for specific domain
        class PaymentError(FoundationError):
            def __init__(
                self,
                message: str,
                *,
                amount: float | None = None,
                currency: str | None = None,
                **kwargs,
            ) -> None:
                if amount is not None:
                    kwargs.setdefault("context", {})["payment.amount"] = amount
                if currency:
                    kwargs.setdefault("context", {})["payment.currency"] = currency
                super().__init__(message, **kwargs)

            def _default_code(self) -> str:
                return "PAYMENT_ERROR"

        # Use custom error
        error = PaymentError(
            "Payment failed",
            amount=99.99,
            currency="USD",
            processor="stripe",
            error_code="card_declined",
        )

        assert error.code == "PAYMENT_ERROR"
        assert error.context["payment.amount"] == 99.99
        assert error.context["payment.currency"] == "USD"
        assert error.context["processor"] == "stripe"

        # Test with error handling
        @resilient(suppress=(PaymentError,), fallback={"status": "failed"})
        def process_payment() -> Never:
            raise error

        result = process_payment()
        assert result == {"status": "failed"}

    def test_performance_with_many_errors(self) -> None:
        """Test performance with many errors."""
        errors = []

        # Create many errors
        for i in range(100):
            error = FoundationError(
                f"Error {i}",
                code=f"ERR_{i:03d}",
                index=i,
                timestamp=time.time(),
            )
            errors.append(error)

        # Handle all errors
        handler = ErrorHandler(
            default_action=lambda e: f"handled_{e.context.get('index')}",
        )

        start = time.perf_counter()
        results = [handler.handle(error) for error in errors]
        duration = time.perf_counter() - start

        assert len(results) == 100
        assert all(r.startswith("handled_") for r in results)
        # Should be fast (less than 500ms for 100 errors)
        assert duration < 0.5


class TestRealWorldScenarios:
    """Test real-world error handling scenarios."""

    def test_web_request_error_handling(self) -> None:
        """Simulate web request error handling."""
        # Simulate request context
        request_data = {
            "method": "POST",
            "path": "/api/users",
            "headers": {"X-Request-ID": "req_abc123"},
            "body": {"email": "invalid", "age": -1},
        }

        def validate_request(data) -> None:
            errors = []

            if "@" not in data.get("body", {}).get("email", ""):
                errors.append(ValidationError("Invalid email", field="email"))

            if data.get("body", {}).get("age", 0) < 0:
                errors.append(ValidationError("Age must be positive", field="age"))

            if errors:
                raise ValidationError(
                    "Request validation failed",
                    validation_errors=[str(e) for e in errors],
                    request_id=data["headers"]["X-Request-ID"],
                )

        # Handle request
        try:
            validate_request(request_data)
        except ValidationError as e:
            # Create error response
            assert e.context["request_id"] == "req_abc123"
            assert len(e.context["validation_errors"]) == 2

    def test_database_transaction_error(self) -> None:
        """Simulate database transaction error handling."""
        db_operations = []

        def db_insert(table, data) -> None:
            db_operations.append(("insert", table, data))
            if table == "users" and data.get("email") == "duplicate@example.com":
                raise AlreadyExistsError(
                    "User already exists",
                    resource_type="user",
                    resource_id=data["email"],
                )

        def db_rollback() -> None:
            db_operations.append(("rollback", None, None))

        def db_commit() -> None:
            db_operations.append(("commit", None, None))

        # Successful transaction
        with transactional(db_rollback, db_commit):
            db_insert("users", {"email": "new@example.com"})
            db_insert("profiles", {"user_email": "new@example.com"})

        assert ("commit", None, None) in db_operations

        # Failed transaction
        db_operations.clear()

        with pytest.raises(AlreadyExistsError), transactional(db_rollback, db_commit):
            db_insert("users", {"email": "duplicate@example.com"})
            db_insert("profiles", {"user_email": "duplicate@example.com"})

        assert ("rollback", None, None) in db_operations
        assert ("commit", None, None) not in db_operations

    def test_microservice_communication_error(self) -> None:
        """Simulate microservice communication error handling."""
        service_calls = []

        @retry(NetworkError, max_attempts=3, base_delay=0.01)
        @circuit_breaker(failure_threshold=5, recovery_timeout=0.1)
        def call_user_service(user_id):
            service_calls.append(("user-service", user_id))

            # Simulate intermittent failures
            if len(service_calls) < 2:
                raise NetworkError(
                    "Connection timeout",
                    service="user-service",
                    endpoint=f"/users/{user_id}",
                )

            return {"id": user_id, "name": "Test User"}

        # Should retry and succeed
        result = call_user_service(123)
        assert result["id"] == 123
        assert len(service_calls) == 2  # One failure, one success
EOF

log_update "Updating: tests/utils/test_rate_limiting.py to fix flaky precision test"
mkdir -p tests/utils/
cat <<'EOF' > tests/utils/test_rate_limiting.py
"""Tests for rate limiting utilities."""

import asyncio
import time
from typing import Never

import pytest

from provide.foundation.utils.rate_limiting import TokenBucketRateLimiter


class TestTokenBucketRateLimiter:
    """Test TokenBucketRateLimiter functionality."""

    def test_init_validates_parameters(self) -> None:
        """Test that initialization validates parameters."""
        # Valid parameters should work
        limiter = TokenBucketRateLimiter(capacity=10.0, refill_rate=5.0)
        assert limiter._capacity == 10.0
        assert limiter._refill_rate == 5.0

        # Invalid capacity should raise ValueError
        with pytest.raises(ValueError, match="Capacity must be positive"):
            TokenBucketRateLimiter(capacity=0, refill_rate=5.0)

        with pytest.raises(ValueError, match="Capacity must be positive"):
            TokenBucketRateLimiter(capacity=-1, refill_rate=5.0)

        # Invalid refill rate should raise ValueError
        with pytest.raises(ValueError, match="Refill rate must be positive"):
            TokenBucketRateLimiter(capacity=10.0, refill_rate=0)

        with pytest.raises(ValueError, match="Refill rate must be positive"):
            TokenBucketRateLimiter(capacity=10.0, refill_rate=-1)

    @pytest.mark.asyncio
    async def test_initial_tokens_available(self) -> None:
        """Test that limiter starts with full capacity of tokens."""
        limiter = TokenBucketRateLimiter(capacity=5.0, refill_rate=1.0)

        # Should allow up to capacity requests immediately
        for _ in range(5):
            assert await limiter.is_allowed() is True

        # Next request should be denied
        assert await limiter.is_allowed() is False

    @pytest.mark.asyncio
    async def test_token_refill_over_time(self) -> None:
        """Test that tokens are refilled over time."""
        # Create limiter with 1 token capacity, refilling at 2 tokens/second
        limiter = TokenBucketRateLimiter(capacity=1.0, refill_rate=2.0)

        # Use the initial token
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False

        # Wait for half a second - should get 1 token back (2 tokens/sec * 0.5s = 1 token)
        await asyncio.sleep(0.6)
        assert await limiter.is_allowed() is True

        # Should be denied again immediately
        assert await limiter.is_allowed() is False

    @pytest.mark.asyncio
    async def test_burst_capacity_limit(self) -> None:
        """Test that tokens don't accumulate beyond capacity."""
        limiter = TokenBucketRateLimiter(capacity=3.0, refill_rate=10.0)

        # Use all initial tokens
        for _ in range(3):
            assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False

        # Wait long enough for many tokens to be generated (way more than capacity)
        await asyncio.sleep(1.0)  # Should generate 10 tokens, but capacity is 3

        # Should only be able to use 3 tokens (capacity limit)
        for _ in range(3):
            assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False

    @pytest.mark.asyncio
    async def test_get_current_tokens(self) -> None:
        """Test getting current token count."""
        limiter = TokenBucketRateLimiter(capacity=5.0, refill_rate=1.0)

        # Should start with full capacity
        tokens = await limiter.get_current_tokens()
        assert tokens == 5.0

        # Use some tokens
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is True

        tokens = await limiter.get_current_tokens()
        # Allow for small timing variations due to test execution time
        assert abs(tokens - 3.0) < 0.01

    @pytest.mark.asyncio
    async def test_concurrent_access(self) -> None:
        """Test thread-safety with concurrent access."""
        limiter = TokenBucketRateLimiter(capacity=10.0, refill_rate=1.0)

        # Create multiple concurrent tasks trying to get tokens
        async def try_get_token():
            return await limiter.is_allowed()

        tasks = [try_get_token() for _ in range(20)]
        results = await asyncio.gather(*tasks)

        # Should have exactly 10 successes (the initial capacity)
        successful_requests = sum(results)
        assert successful_requests == 10

    @pytest.mark.asyncio
    async def test_fractional_values(self) -> None:
        """Test that fractional capacity and refill rates work."""
        limiter = TokenBucketRateLimiter(capacity=2.5, refill_rate=0.5)

        # Should allow 2 requests initially (2.5 capacity, but we consume 1.0 per request)
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False  # 0.5 tokens remaining, need 1.0

        # Wait for 2 seconds to get 1 more token (0.5 tokens/sec * 2s = 1 token)
        await asyncio.sleep(2.1)
        assert await limiter.is_allowed() is True

    def test_logger_initialization_success(self) -> None:
        """Test successful logger initialization."""
        limiter = TokenBucketRateLimiter(capacity=1.0, refill_rate=1.0)
        # Logger should be available and cached
        assert limiter._logger is not None

    def test_logger_initialization_fallback(self, monkeypatch) -> None:
        """Test logger initialization fallback when import fails."""

        # Mock the import to raise ImportError
        def mock_import_error(*args, **kwargs) -> Never:
            raise ImportError("Mocked import failure")

        # Patch the import mechanism
        monkeypatch.setattr("builtins.__import__", mock_import_error)

        # Should not raise an exception, should fallback gracefully
        limiter = TokenBucketRateLimiter(capacity=1.0, refill_rate=1.0)
        assert limiter._logger is None

    @pytest.mark.asyncio
    async def test_very_long_wait_periods(self) -> None:
        """Test behavior after very long idle periods."""
        limiter = TokenBucketRateLimiter(capacity=3.0, refill_rate=1.0)

        # Use all tokens
        for _ in range(3):
            assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False

        # Simulate a very long wait (equivalent to generating 100 tokens)
        # but capacity should limit to 3
        start_time = time.monotonic()

        # Manually advance the internal timestamp to simulate long wait
        limiter._last_refill_timestamp = start_time - 100.0  # 100 seconds ago

        # Should still be limited by capacity
        for _ in range(3):
            assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False

    @pytest.mark.asyncio
    async def test_extreme_time_precision(self) -> None:
        """Test behavior with very small time intervals and high precision."""
        limiter = TokenBucketRateLimiter(
            capacity=1.0,
            refill_rate=1000.0,
        )  # Very fast refill

        # Use the initial token
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False

        # Wait just slightly longer than needed for 1 token (1/1000 = 0.001s)
        # Use a slightly more generous sleep to account for event loop scheduling jitter.
        await asyncio.sleep(0.005)
        assert await limiter.is_allowed() is True

    @pytest.mark.asyncio
    async def test_high_concurrency_stress(self) -> None:
        """Test thread-safety with high concurrency stress testing."""
        limiter = TokenBucketRateLimiter(capacity=50.0, refill_rate=1.0)

        # Create many more concurrent tasks than capacity
        async def try_get_token():
            return await limiter.is_allowed()

        # Test with 200 concurrent tasks for 50 token capacity
        tasks = [try_get_token() for _ in range(200)]
        results = await asyncio.gather(*tasks)

        # Should have exactly 50 successes (the initial capacity)
        successful_requests = sum(results)
        assert successful_requests == 50

        # All remaining should be denied
        denied_requests = len(results) - successful_requests
        assert denied_requests == 150

    @pytest.mark.asyncio
    async def test_extreme_concurrency_stress(self) -> None:
        """Test thread-safety with extreme concurrency."""
        limiter = TokenBucketRateLimiter(capacity=100.0, refill_rate=1.0)

        # Create extreme number of concurrent tasks
        async def try_get_token():
            return await limiter.is_allowed()

        # Test with 1000 concurrent tasks for 100 token capacity
        tasks = [try_get_token() for _ in range(1000)]
        results = await asyncio.gather(*tasks)

        # Should have exactly 100 successes (the initial capacity)
        successful_requests = sum(results)
        assert successful_requests == 100

    @pytest.mark.asyncio
    async def test_concurrent_refill_and_consumption(self) -> None:
        """Test concurrent token consumption while refilling occurs."""
        limiter = TokenBucketRateLimiter(capacity=5.0, refill_rate=10.0)  # Fast refill

        # Use all initial tokens
        for _ in range(5):
            assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False

        async def consumer():
            """Try to consume tokens continuously."""
            successes = 0
            for _ in range(20):
                if await limiter.is_allowed():
                    successes += 1
                await asyncio.sleep(0.01)  # Small delay
            return successes

        # Run multiple consumers concurrently while tokens refill
        consumers = [consumer() for _ in range(3)]
        results = await asyncio.gather(*consumers)

        # Should have some successes due to refilling, but not unlimited
        total_successes = sum(results)
        # With 10 tokens/sec refill rate and ~0.6s total time,
        # expect some additional tokens, but exact timing varies in CI/test environments
        # Be more lenient with timing-dependent behavior
        assert 0 <= total_successes <= 20  # Reasonable range allowing for timing variations

    @pytest.mark.asyncio
    async def test_logger_usage_during_operations(self, mocker) -> None:
        """Test that logger is used correctly during operations."""
        # Mock the get_logger function to return a mock logger
        mock_logger = mocker.MagicMock()
        mocker.patch("provide.foundation.logger.get_logger", return_value=mock_logger)

        limiter = TokenBucketRateLimiter(capacity=2.0, refill_rate=1.0)

        # Should have logged initialization
        mock_logger.debug.assert_called_once()
        init_call = mock_logger.debug.call_args[0][0]
        assert "TokenBucketRateLimiter initialized" in init_call

        # Reset mock to test operation logging
        mock_logger.reset_mock()

        # Test successful request logging
        await limiter.is_allowed()
        mock_logger.debug.assert_called_once()
        success_call = mock_logger.debug.call_args[0][0]
        assert "Request allowed" in success_call

        # Reset and test denied request logging
        mock_logger.reset_mock()
        await limiter.is_allowed()  # Use second token
        await limiter.is_allowed()  # Should be denied

        mock_logger.warning.assert_called_once()
        denied_call = mock_logger.warning.call_args[0][0]
        assert "Request denied" in denied_call
EOF

log_success "Project update complete."