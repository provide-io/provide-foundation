#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for OTLP client initialization, configuration, and setup.

Tests OTLPLogClient initialization, from_config class method, availability checking,
and endpoint building."""

from __future__ import annotations

from provide.testkit.mocking import Mock, patch
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


# 🧱🏗️🔚
