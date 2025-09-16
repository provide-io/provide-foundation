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
    with_error_handling,
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

        @with_error_handling(suppress=(ValidationError,), fallback="handled")
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

        @with_error_handling(fallback="async_default", suppress=(NetworkError,))
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
        @with_error_handling(suppress=(PaymentError,), fallback={"status": "failed"})
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
        # Should be fast (less than 100ms for 100 errors)
        assert duration < 0.1


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
