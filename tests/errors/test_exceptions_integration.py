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

