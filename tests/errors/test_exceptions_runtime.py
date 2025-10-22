"""Tests for runtime error classes."""

from __future__ import annotations

from provide.testkit import FoundationTestCase

from provide.foundation.errors.runtime import RuntimeError


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
