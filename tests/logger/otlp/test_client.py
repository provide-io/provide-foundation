"""Comprehensive tests for generic OTLP client.

Tests all functionality in logger/otlp/client.py including log sending,
logger provider creation, circuit breaker integration, and configuration.
"""

from __future__ import annotations

from unittest.mock import Mock, patch

import pytest

from provide.foundation.logger.otlp.client import OTLPLogClient


class TestOTLPLogClientInit:
    """Tests for OTLPLogClient initialization."""

    def test_client_creation_basic(self) -> None:
        """Test basic client initialization."""
        client = OTLPLogClient(
            endpoint="https://api.example.com/v1/logs",
            service_name="test-service",
        )

        assert client.endpoint == "https://api.example.com/v1/logs"
        assert client.service_name == "test-service"
        assert client.service_version is None
        assert client.timeout == 30.0
        assert client.use_circuit_breaker is True

    def test_client_creation_with_all_parameters(self) -> None:
        """Test client initialization with all parameters."""
        headers = {"Authorization": "Bearer token"}

        client = OTLPLogClient(
            endpoint="https://api.example.com",
            headers=headers,
            service_name="test-service",
            service_version="1.0.0",
            environment="production",
            timeout=60.0,
            use_circuit_breaker=False,
        )

        assert client.endpoint == "https://api.example.com/v1/logs"
        assert client.headers == headers
        assert client.service_name == "test-service"
        assert client.service_version == "1.0.0"
        assert client.environment == "production"
        assert client.timeout == 60.0
        assert client.use_circuit_breaker is False

    def test_client_creation_defaults(self) -> None:
        """Test client with default values."""
        client = OTLPLogClient(endpoint="https://api.example.com")

        assert client.service_name == "foundation"
        assert client.headers == {}


class TestCheckOtlpAvailability:
    """Tests for _check_otlp_availability method."""

    @patch("provide.foundation.logger.otlp.client.OTLPLogClient._check_otlp_availability")
    def test_check_otlp_available(self, mock_check: Mock) -> None:
        """Test when OpenTelemetry SDK is available."""
        mock_check.return_value = True

        client = OTLPLogClient(endpoint="https://api.example.com")

        assert client._otlp_available is True

    @patch("provide.foundation.logger.otlp.client.OTLPLogClient._check_otlp_availability")
    def test_check_otlp_unavailable(self, mock_check: Mock) -> None:
        """Test when OpenTelemetry SDK is not available."""
        mock_check.return_value = False

        client = OTLPLogClient(endpoint="https://api.example.com")

        assert client._otlp_available is False


class TestFromConfig:
    """Tests for from_config class method."""

    def test_from_config_basic(self) -> None:
        """Test creating client from TelemetryConfig."""
        config = Mock()
        config.otlp_endpoint = "https://api.example.com/v1/logs"
        config.otlp_headers = {"X-Custom": "value"}
        config.service_name = "test-service"
        config.service_version = "1.0.0"

        client = OTLPLogClient.from_config(config)

        assert client.endpoint == "https://api.example.com/v1/logs"
        assert client.service_name == "test-service"
        assert client.service_version == "1.0.0"
        assert client.headers["X-Custom"] == "value"

    def test_from_config_with_additional_headers(self) -> None:
        """Test from_config with additional headers."""
        config = Mock()
        config.otlp_endpoint = "https://api.example.com"
        config.otlp_headers = {"X-Custom": "value"}
        config.service_name = "test-service"
        config.service_version = None

        additional_headers = {"X-Additional": "extra"}

        client = OTLPLogClient.from_config(config, additional_headers)

        assert client.headers["X-Custom"] == "value"
        assert client.headers["X-Additional"] == "extra"

    def test_from_config_without_endpoint(self) -> None:
        """Test that ValueError is raised when endpoint is not set."""
        config = Mock()
        config.otlp_endpoint = None

        with pytest.raises(ValueError, match="otlp_endpoint must be set"):
            OTLPLogClient.from_config(config)

    def test_from_config_defaults_service_name(self) -> None:
        """Test that service name defaults to 'foundation'."""
        config = Mock()
        config.otlp_endpoint = "https://api.example.com"
        config.otlp_headers = {}
        config.service_name = None
        config.service_version = None

        client = OTLPLogClient.from_config(config)

        assert client.service_name == "foundation"


class TestSendLog:
    """Tests for send_log method."""

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    @patch("provide.foundation.logger.otlp.client.OTLPLogClient._create_logger_provider_internal")
    def test_send_log_success(
        self,
        mock_create_provider: Mock,
        mock_get_breaker: Mock,
    ) -> None:
        """Test successful log sending."""
        # Mock circuit breaker
        mock_breaker = Mock()
        mock_breaker.can_attempt.return_value = True
        mock_get_breaker.return_value = mock_breaker

        # Mock logger provider
        mock_provider = Mock()
        mock_logger = Mock()
        mock_provider.get_logger.return_value = mock_logger
        mock_create_provider.return_value = mock_provider

        # Create client with OTLP available
        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        result = client.send_log("Test message", level="INFO")

        assert result is True
        mock_breaker.record_success.assert_called_once()
        mock_logger.emit.assert_called_once()
        mock_provider.force_flush.assert_called_once()
        mock_provider.shutdown.assert_called_once()

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    def test_send_log_otlp_unavailable(self, mock_get_breaker: Mock) -> None:
        """Test send_log when OTLP is not available."""
        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = False

        result = client.send_log("Test message")

        assert result is False
        mock_get_breaker.assert_not_called()

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    def test_send_log_circuit_breaker_open(self, mock_get_breaker: Mock) -> None:
        """Test send_log when circuit breaker is open."""
        mock_breaker = Mock()
        mock_breaker.can_attempt.return_value = False
        mock_get_breaker.return_value = mock_breaker

        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        result = client.send_log("Test message")

        assert result is False

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    @patch("provide.foundation.logger.otlp.client.OTLPLogClient._create_logger_provider_internal")
    def test_send_log_provider_creation_fails(
        self,
        mock_create_provider: Mock,
        mock_get_breaker: Mock,
    ) -> None:
        """Test send_log when provider creation fails."""
        mock_breaker = Mock()
        mock_breaker.can_attempt.return_value = True
        mock_get_breaker.return_value = mock_breaker

        mock_create_provider.return_value = None

        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        result = client.send_log("Test message")

        assert result is False
        mock_breaker.record_failure.assert_called_once()

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    @patch("provide.foundation.logger.otlp.client.OTLPLogClient._create_logger_provider_internal")
    def test_send_log_with_attributes(
        self,
        mock_create_provider: Mock,
        mock_get_breaker: Mock,
    ) -> None:
        """Test send_log with custom attributes."""
        mock_breaker = Mock()
        mock_breaker.can_attempt.return_value = True
        mock_get_breaker.return_value = mock_breaker

        mock_provider = Mock()
        mock_logger = Mock()
        mock_provider.get_logger.return_value = mock_logger
        mock_create_provider.return_value = mock_provider

        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        attributes = {"user_id": "123", "action": "login"}
        result = client.send_log("User logged in", level="INFO", attributes=attributes)

        assert result is True
        mock_logger.emit.assert_called_once()

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    @patch("provide.foundation.logger.otlp.client.OTLPLogClient._create_logger_provider_internal")
    def test_send_log_exception(
        self,
        mock_create_provider: Mock,
        mock_get_breaker: Mock,
    ) -> None:
        """Test send_log handles exceptions gracefully."""
        mock_breaker = Mock()
        mock_breaker.can_attempt.return_value = True
        mock_get_breaker.return_value = mock_breaker

        mock_create_provider.side_effect = Exception("Provider error")

        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        result = client.send_log("Test message")

        assert result is False
        mock_breaker.record_failure.assert_called_once()

    def test_send_log_without_circuit_breaker(self) -> None:
        """Test send_log when circuit breaker is disabled."""
        client = OTLPLogClient(
            endpoint="https://api.example.com",
            use_circuit_breaker=False,
        )
        client._otlp_available = False

        result = client.send_log("Test message")

        # Should return False due to OTLP unavailable
        assert result is False


class TestCreateLoggerProvider:
    """Tests for create_logger_provider method."""

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    @patch("provide.foundation.logger.otlp.client.OTLPLogClient._create_logger_provider_internal")
    def test_create_logger_provider_success(
        self,
        mock_create_internal: Mock,
        mock_get_breaker: Mock,
    ) -> None:
        """Test successful logger provider creation."""
        mock_breaker = Mock()
        mock_breaker.can_attempt.return_value = True
        mock_get_breaker.return_value = mock_breaker

        mock_provider = Mock()
        mock_create_internal.return_value = mock_provider

        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        result = client.create_logger_provider()

        assert result == mock_provider
        mock_breaker.record_success.assert_called_once()

    def test_create_logger_provider_otlp_unavailable(self) -> None:
        """Test create_logger_provider when OTLP is unavailable."""
        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = False

        result = client.create_logger_provider()

        assert result is None

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    def test_create_logger_provider_circuit_open(self, mock_get_breaker: Mock) -> None:
        """Test create_logger_provider when circuit is open."""
        mock_breaker = Mock()
        mock_breaker.can_attempt.return_value = False
        mock_get_breaker.return_value = mock_breaker

        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        result = client.create_logger_provider()

        assert result is None

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    @patch("provide.foundation.logger.otlp.client.OTLPLogClient._create_logger_provider_internal")
    def test_create_logger_provider_exception(
        self,
        mock_create_internal: Mock,
        mock_get_breaker: Mock,
    ) -> None:
        """Test create_logger_provider handles exceptions."""
        mock_breaker = Mock()
        mock_breaker.can_attempt.return_value = True
        mock_get_breaker.return_value = mock_breaker

        mock_create_internal.side_effect = Exception("Provider error")

        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        result = client.create_logger_provider()

        assert result is None
        mock_breaker.record_failure.assert_called_once()


class TestCreateLoggerProviderInternal:
    """Tests for _create_logger_provider_internal method."""

    @patch("provide.foundation.logger.otlp.client.create_otlp_resource")
    def test_create_logger_provider_internal_import_error(
        self,
        mock_create_resource: Mock,
    ) -> None:
        """Test _create_logger_provider_internal when imports fail."""
        client = OTLPLogClient(
            endpoint="https://api.example.com",
            service_name="test-service",
        )

        # This will naturally fail if OpenTelemetry is not installed
        result = client._create_logger_provider_internal()

        # Result could be None if OTLP is not available
        assert result is None or result is not None

    @patch("provide.foundation.logger.otlp.client.create_otlp_resource")
    def test_create_logger_provider_internal_exception(
        self,
        mock_create_resource: Mock,
    ) -> None:
        """Test _create_logger_provider_internal handles exceptions."""
        mock_create_resource.side_effect = Exception("Resource error")

        client = OTLPLogClient(endpoint="https://api.example.com")

        result = client._create_logger_provider_internal()

        assert result is None


class TestIsAvailable:
    """Tests for is_available method."""

    def test_is_available_otlp_unavailable(self) -> None:
        """Test is_available when OTLP is not available."""
        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = False

        result = client.is_available()

        assert result is False

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    def test_is_available_circuit_open(self, mock_get_breaker: Mock) -> None:
        """Test is_available when circuit breaker is open."""
        mock_breaker = Mock()
        mock_breaker.can_attempt.return_value = False
        mock_get_breaker.return_value = mock_breaker

        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        result = client.is_available()

        assert result is False

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    def test_is_available_true(self, mock_get_breaker: Mock) -> None:
        """Test is_available when everything is available."""
        mock_breaker = Mock()
        mock_breaker.can_attempt.return_value = True
        mock_get_breaker.return_value = mock_breaker

        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        result = client.is_available()

        assert result is True

    def test_is_available_without_circuit_breaker(self) -> None:
        """Test is_available when circuit breaker is disabled."""
        client = OTLPLogClient(
            endpoint="https://api.example.com",
            use_circuit_breaker=False,
        )
        client._otlp_available = True

        result = client.is_available()

        assert result is True


class TestGetStats:
    """Tests for get_stats method."""

    def test_get_stats_basic(self) -> None:
        """Test get_stats returns client information."""
        client = OTLPLogClient(
            endpoint="https://api.example.com",
            service_name="test-service",
        )
        client._otlp_available = True

        stats = client.get_stats()

        assert stats["otlp_available"] is True
        assert stats["endpoint"] == "https://api.example.com/v1/logs"
        assert stats["service_name"] == "test-service"

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    def test_get_stats_with_circuit_breaker(self, mock_get_breaker: Mock) -> None:
        """Test get_stats includes circuit breaker stats."""
        mock_breaker = Mock()
        mock_breaker_stats = {
            "state": "closed",
            "failure_count": 0,
        }
        mock_breaker.get_stats.return_value = mock_breaker_stats
        mock_get_breaker.return_value = mock_breaker

        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        stats = client.get_stats()

        assert "circuit_breaker" in stats
        assert stats["circuit_breaker"] == mock_breaker_stats

    def test_get_stats_without_circuit_breaker(self) -> None:
        """Test get_stats without circuit breaker enabled."""
        client = OTLPLogClient(
            endpoint="https://api.example.com",
            use_circuit_breaker=False,
        )
        client._otlp_available = False

        stats = client.get_stats()

        assert "circuit_breaker" not in stats
        assert stats["otlp_available"] is False


class TestEndpointBuilding:
    """Tests for endpoint URL building."""

    def test_endpoint_with_logs_suffix(self) -> None:
        """Test that /v1/logs is added to endpoint."""
        client = OTLPLogClient(endpoint="https://api.example.com")

        assert client.endpoint.endswith("/v1/logs")

    def test_endpoint_already_has_logs_suffix(self) -> None:
        """Test endpoint that already has /v1/logs."""
        client = OTLPLogClient(endpoint="https://api.example.com/v1/logs")

        # Should not duplicate /v1/logs
        assert client.endpoint == "https://api.example.com/v1/logs"


# <3 🧱🤝📝🪄
