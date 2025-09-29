"""Tests for provide.foundation.errors.exceptions module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase

from provide.foundation.errors.auth import AuthenticationError, AuthorizationError
from provide.foundation.errors.base import FoundationError
from provide.foundation.errors.config import ConfigurationError, ValidationError
from provide.foundation.errors.integration import (
    IntegrationError,
    NetworkError,
    TimeoutError,
)
from provide.foundation.errors.resources import (
    AlreadyExistsError,
    NotFoundError,
    ResourceError,
)
from provide.foundation.errors.runtime import ConcurrencyError, RuntimeError, StateError


class TestFoundationError(FoundationTestCase):
    """Test the base FoundationError class."""

    def test_basic_creation(self) -> None:
        """Test basic error creation."""
        error = FoundationError("Test error")
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.code == "PROVIDE_ERROR"
        assert error.context == {}
        assert error.cause is None

    def test_with_code(self) -> None:
        """Test error with custom code."""
        error = FoundationError("Test error", code="CUSTOM_001")
        assert error.code == "CUSTOM_001"

    def test_with_context(self) -> None:
        """Test error with initial context."""
        context = {"key": "value", "number": 42}
        error = FoundationError("Test error", context=context)
        assert error.context == context

    def test_with_cause(self) -> None:
        """Test error with cause."""
        cause = ValueError("Original error")
        error = FoundationError("Wrapped error", cause=cause)
        assert error.cause is cause
        assert error.__cause__ is cause

    def test_with_extra_context(self) -> None:
        """Test error with extra context via kwargs."""
        error = FoundationError(
            "Test error",
            user_id=123,
            request_id="req_456",
            retry_count=3,
        )
        assert error.context == {
            "user_id": 123,
            "request_id": "req_456",
            "retry_count": 3,
        }

    def test_context_merge(self) -> None:
        """Test that extra context merges with provided context."""
        error = FoundationError(
            "Test error",
            context={"existing": "value"},
            new_key="new_value",
            number=42,
        )
        assert error.context == {
            "existing": "value",
            "new_key": "new_value",
            "number": 42,
        }

    def test_add_context(self) -> None:
        """Test adding context after creation."""
        error = FoundationError("Test error")
        error.add_context("key1", "value1")
        error.add_context("key2", 42)

        assert error.context == {"key1": "value1", "key2": 42}

    def test_add_context_chaining(self) -> None:
        """Test that add_context returns self for chaining."""
        error = FoundationError("Test error")
        result = error.add_context("key1", "value1").add_context("key2", "value2")

        assert result is error
        assert error.context == {"key1": "value1", "key2": "value2"}

    def test_to_dict(self) -> None:
        """Test conversion to dictionary."""
        cause = ValueError("Original")
        error = FoundationError(
            "Test error",
            code="TEST_001",
            context={"user_id": 123},
            cause=cause,
            request_id="req_456",
        )

        result = error.to_dict()

        assert result["error.type"] == "FoundationError"
        assert result["error.message"] == "Test error"
        assert result["error.code"] == "TEST_001"
        assert result["error.user_id"] == 123
        assert result["error.request_id"] == "req_456"
        assert result["error.cause"] == "Original"
        assert result["error.cause_type"] == "ValueError"

    def test_to_dict_with_namespaced_context(self) -> None:
        """Test that namespaced context keys are preserved."""
        error = FoundationError("Test error")
        error.add_context("aws.region", "us-east-1")
        error.add_context("http.status", 500)
        error.add_context("simple_key", "value")

        result = error.to_dict()

        assert result["aws.region"] == "us-east-1"
        assert result["http.status"] == 500
        assert result["error.simple_key"] == "value"

    def test_default_code_override(self) -> None:
        """Test that subclasses can override default code."""

        class CustomError(FoundationError):
            def _default_code(self) -> str:
                return "CUSTOM_ERROR"

        error = CustomError("Test")
        assert error.code == "CUSTOM_ERROR"

        # Can still override with explicit code
        error2 = CustomError("Test", code="OVERRIDE")
        assert error2.code == "OVERRIDE"


class TestConfigurationError(FoundationTestCase):
    """Test ConfigurationError class."""

    def test_basic_creation(self) -> None:
        """Test basic ConfigurationError."""
        error = ConfigurationError("Config invalid")
        assert error.message == "Config invalid"
        assert error.code == "CONFIG_ERROR"

    def test_with_config_key(self) -> None:
        """Test with config_key parameter."""
        error = ConfigurationError("Invalid value", config_key="timeout")
        assert error.context["config.key"] == "timeout"

    def test_with_config_source(self) -> None:
        """Test with config_source parameter."""
        error = ConfigurationError("Parse error", config_source="/etc/app.conf")
        assert error.context["config.source"] == "/etc/app.conf"

    def test_with_all_parameters(self) -> None:
        """Test with all specific parameters."""
        error = ConfigurationError(
            "Config error",
            config_key="database.url",
            config_source="environment",
            extra_param="value",
        )
        assert error.context["config.key"] == "database.url"
        assert error.context["config.source"] == "environment"
        assert error.context["extra_param"] == "value"


class TestValidationError(FoundationTestCase):
    """Test ValidationError class."""

    def test_basic_creation(self) -> None:
        """Test basic ValidationError."""
        error = ValidationError("Invalid input")
        assert error.message == "Invalid input"
        assert error.code == "VALIDATION_ERROR"

    def test_with_field(self) -> None:
        """Test with field parameter."""
        error = ValidationError("Required field", field="email")
        assert error.context["validation.field"] == "email"

    def test_with_value(self) -> None:
        """Test with value parameter."""
        error = ValidationError("Invalid format", value="not-an-email")
        assert error.context["validation.value"] == "not-an-email"

    def test_with_rule(self) -> None:
        """Test with rule parameter."""
        error = ValidationError("Failed validation", rule="email_format")
        assert error.context["validation.rule"] == "email_format"

    def test_with_all_parameters(self) -> None:
        """Test with all validation parameters."""
        error = ValidationError(
            "Validation failed",
            field="age",
            value=-1,
            rule="positive_integer",
            max_value=120,
        )
        assert error.context["validation.field"] == "age"
        assert error.context["validation.value"] == "-1"
        assert error.context["validation.rule"] == "positive_integer"
        assert error.context["max_value"] == 120

    def test_value_conversion_to_string(self) -> None:
        """Test that value is converted to string."""
        error = ValidationError("Invalid", value={"complex": "object"})
        assert error.context["validation.value"] == "{'complex': 'object'}"


class TestRuntimeError(FoundationTestCase):
    """Test RuntimeError class."""

    def test_basic_creation(self) -> None:
        """Test basic RuntimeError."""
        error = RuntimeError("Process failed")
        assert error.message == "Process failed"
        assert error.code == "RUNTIME_ERROR"
        assert error.context["runtime.retry_possible"] is False

    def test_with_operation(self) -> None:
        """Test with operation parameter."""
        error = RuntimeError("Lock failed", operation="acquire_lock")
        assert error.context["runtime.operation"] == "acquire_lock"

    def test_with_retry_possible(self) -> None:
        """Test with retry_possible parameter."""
        error = RuntimeError("Temporary failure", retry_possible=True)
        assert error.context["runtime.retry_possible"] is True


class TestIntegrationError(FoundationTestCase):
    """Test IntegrationError class."""

    def test_basic_creation(self) -> None:
        """Test basic IntegrationError."""
        error = IntegrationError("API failed")
        assert error.message == "API failed"
        assert error.code == "INTEGRATION_ERROR"

    def test_with_service(self) -> None:
        """Test with service parameter."""
        error = IntegrationError("Connection failed", service="payment-api")
        assert error.context["integration.service"] == "payment-api"

    def test_with_endpoint(self) -> None:
        """Test with endpoint parameter."""
        error = IntegrationError("Request failed", endpoint="/api/v1/users")
        assert error.context["integration.endpoint"] == "/api/v1/users"

    def test_with_status_code(self) -> None:
        """Test with status_code parameter."""
        error = IntegrationError("HTTP error", status_code=503)
        assert error.context["integration.status_code"] == 503


class TestResourceError(FoundationTestCase):
    """Test ResourceError class."""

    def test_basic_creation(self) -> None:
        """Test basic ResourceError."""
        error = ResourceError("File not found")
        assert error.message == "File not found"
        assert error.code == "RESOURCE_ERROR"

    def test_with_resource_type(self) -> None:
        """Test with resource_type parameter."""
        error = ResourceError("Access denied", resource_type="file")
        assert error.context["resource.type"] == "file"

    def test_with_resource_path(self) -> None:
        """Test with resource_path parameter."""
        error = ResourceError("Not found", resource_path="/data/config.json")
        assert error.context["resource.path"] == "/data/config.json"


class TestNetworkError(FoundationTestCase):
    """Test NetworkError class."""

    def test_basic_creation(self) -> None:
        """Test basic NetworkError."""
        error = NetworkError("Connection refused")
        assert error.message == "Connection refused"
        assert error.code == "NETWORK_ERROR"

    def test_inheritance_from_integration_error(self) -> None:
        """Test that NetworkError inherits from IntegrationError."""
        error = NetworkError("Failed", service="api", status_code=500)
        assert isinstance(error, IntegrationError)
        assert error.context["integration.service"] == "api"
        assert error.context["integration.status_code"] == 500

    def test_with_host(self) -> None:
        """Test with host parameter."""
        error = NetworkError("DNS failed", host="api.example.com")
        assert error.context["network.host"] == "api.example.com"

    def test_with_port(self) -> None:
        """Test with port parameter."""
        error = NetworkError("Port closed", port=8080)
        assert error.context["network.port"] == 8080


class TestTimeoutError(FoundationTestCase):
    """Test TimeoutError class."""

    def test_basic_creation(self) -> None:
        """Test basic TimeoutError."""
        error = TimeoutError("Request timed out")
        assert error.message == "Request timed out"
        assert error.code == "TIMEOUT_ERROR"

    def test_inheritance_from_integration_error(self) -> None:
        """Test that TimeoutError inherits from IntegrationError."""
        error = TimeoutError("Timeout", service="database")
        assert isinstance(error, IntegrationError)
        assert error.context["integration.service"] == "database"

    def test_with_timeout_seconds(self) -> None:
        """Test with timeout_seconds parameter."""
        error = TimeoutError("Exceeded limit", timeout_seconds=30.0)
        assert error.context["timeout.limit"] == 30.0

    def test_with_elapsed_seconds(self) -> None:
        """Test with elapsed_seconds parameter."""
        error = TimeoutError("Too slow", elapsed_seconds=45.5)
        assert error.context["timeout.elapsed"] == 45.5


class TestAuthenticationError(FoundationTestCase):
    """Test AuthenticationError class."""

    def test_basic_creation(self) -> None:
        """Test basic AuthenticationError."""
        error = AuthenticationError("Invalid credentials")
        assert error.message == "Invalid credentials"
        assert error.code == "AUTH_ERROR"

    def test_with_auth_method(self) -> None:
        """Test with auth_method parameter."""
        error = AuthenticationError("Token invalid", auth_method="jwt")
        assert error.context["auth.method"] == "jwt"

    def test_with_realm(self) -> None:
        """Test with realm parameter."""
        error = AuthenticationError("Access denied", realm="admin")
        assert error.context["auth.realm"] == "admin"


class TestAuthorizationError(FoundationTestCase):
    """Test AuthorizationError class."""

    def test_basic_creation(self) -> None:
        """Test basic AuthorizationError."""
        error = AuthorizationError("Permission denied")
        assert error.message == "Permission denied"
        assert error.code == "AUTHZ_ERROR"

    def test_with_required_permission(self) -> None:
        """Test with required_permission parameter."""
        error = AuthorizationError("Forbidden", required_permission="admin:write")
        assert error.context["authz.permission"] == "admin:write"

    def test_with_resource(self) -> None:
        """Test with resource parameter."""
        error = AuthorizationError("Cannot access", resource="/admin/users")
        assert error.context["authz.resource"] == "/admin/users"

    def test_with_actor(self) -> None:
        """Test with actor parameter."""
        error = AuthorizationError("Denied", actor="user:123")
        assert error.context["authz.actor"] == "user:123"


class TestNotFoundError(FoundationTestCase):
    """Test NotFoundError class."""

    def test_basic_creation(self) -> None:
        """Test basic NotFoundError."""
        error = NotFoundError("Resource not found")
        assert error.message == "Resource not found"
        assert error.code == "NOT_FOUND_ERROR"

    def test_with_resource_type(self) -> None:
        """Test with resource_type parameter."""
        error = NotFoundError("Not found", resource_type="user")
        assert error.context["notfound.type"] == "user"

    def test_with_resource_id(self) -> None:
        """Test with resource_id parameter."""
        error = NotFoundError("Missing", resource_id="usr_123")
        assert error.context["notfound.id"] == "usr_123"


class TestAlreadyExistsError(FoundationTestCase):
    """Test AlreadyExistsError class."""

    def test_basic_creation(self) -> None:
        """Test basic AlreadyExistsError."""
        error = AlreadyExistsError("Already exists")
        assert error.message == "Already exists"
        assert error.code == "ALREADY_EXISTS_ERROR"

    def test_with_resource_type(self) -> None:
        """Test with resource_type parameter."""
        error = AlreadyExistsError("Duplicate", resource_type="email")
        assert error.context["exists.type"] == "email"

    def test_with_resource_id(self) -> None:
        """Test with resource_id parameter."""
        error = AlreadyExistsError("Conflict", resource_id="user@example.com")
        assert error.context["exists.id"] == "user@example.com"


class TestStateError(FoundationTestCase):
    """Test StateError class."""

    def test_basic_creation(self) -> None:
        """Test basic StateError."""
        error = StateError("Invalid state")
        assert error.message == "Invalid state"
        assert error.code == "STATE_ERROR"

    def test_with_current_state(self) -> None:
        """Test with current_state parameter."""
        error = StateError("Cannot transition", current_state="pending")
        assert error.context["state.current"] == "pending"

    def test_with_expected_state(self) -> None:
        """Test with expected_state parameter."""
        error = StateError("Wrong state", expected_state="ready")
        assert error.context["state.expected"] == "ready"

    def test_with_transition(self) -> None:
        """Test with transition parameter."""
        error = StateError("Invalid", transition="start->running")
        assert error.context["state.transition"] == "start->running"


class TestConcurrencyError(FoundationTestCase):
    """Test ConcurrencyError class."""

    def test_basic_creation(self) -> None:
        """Test basic ConcurrencyError."""
        error = ConcurrencyError("Lock conflict")
        assert error.message == "Lock conflict"
        assert error.code == "CONCURRENCY_ERROR"

    def test_with_conflict_type(self) -> None:
        """Test with conflict_type parameter."""
        error = ConcurrencyError("Conflict", conflict_type="optimistic_lock")
        assert error.context["concurrency.type"] == "optimistic_lock"

    def test_with_version_expected(self) -> None:
        """Test with version_expected parameter."""
        error = ConcurrencyError("Version mismatch", version_expected=1)
        assert error.context["concurrency.version_expected"] == "1"

    def test_with_version_actual(self) -> None:
        """Test with version_actual parameter."""
        error = ConcurrencyError("Stale", version_actual=3)
        assert error.context["concurrency.version_actual"] == "3"

    def test_version_conversion(self) -> None:
        """Test that versions are converted to strings."""
        error = ConcurrencyError(
            "Version conflict",
            version_expected={"v": 1, "ts": 12345},
            version_actual={"v": 2, "ts": 12346},
        )
        assert "v" in error.context["concurrency.version_expected"]
        assert "v" in error.context["concurrency.version_actual"]


class TestErrorInheritance(FoundationTestCase):
    """Test error inheritance and isinstance checks."""

    def test_all_errors_inherit_from_foundation_error(self) -> None:
        """Test that all error types inherit from FoundationError."""
        errors = [
            ConfigurationError("test"),
            ValidationError("test"),
            RuntimeError("test"),
            IntegrationError("test"),
            ResourceError("test"),
            NetworkError("test"),
            TimeoutError("test"),
            AuthenticationError("test"),
            AuthorizationError("test"),
            NotFoundError("test"),
            AlreadyExistsError("test"),
            StateError("test"),
            ConcurrencyError("test"),
        ]

        for error in errors:
            assert isinstance(error, FoundationError)
            assert isinstance(error, Exception)

    def test_network_and_timeout_inherit_from_integration(self) -> None:
        """Test that network errors inherit from IntegrationError."""
        assert isinstance(NetworkError("test"), IntegrationError)
        assert isinstance(TimeoutError("test"), IntegrationError)
