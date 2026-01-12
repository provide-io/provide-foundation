#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for OpenObserve OTLP adapter.

Tests all functions and classes in integrations/openobserve/otlp_adapter.py."""

from __future__ import annotations

import base64

from provide.testkit.mocking import Mock, patch
import pytest

from provide.foundation.integrations.openobserve.config import OpenObserveConfig
from provide.foundation.integrations.openobserve.otlp_adapter import (
    OpenObserveOTLPClient,
    build_openobserve_headers,
    get_openobserve_otlp_endpoint,
)
from provide.foundation.logger.config.telemetry import TelemetryConfig


class TestGetOpenobserveOtlpEndpoint:
    """Tests for get_openobserve_otlp_endpoint function."""

    def test_endpoint_without_api_prefix(self) -> None:
        """Test endpoint generation from clean base URL."""
        endpoint = get_openobserve_otlp_endpoint(
            "https://api.openobserve.ai",
            "my-org",
        )

        assert endpoint == "https://api.openobserve.ai/api/my-org/v1/logs"

    def test_endpoint_with_api_prefix(self) -> None:
        """Test endpoint generation when URL already has /api/ path."""
        endpoint = get_openobserve_otlp_endpoint(
            "https://api.openobserve.ai/api/my-org",
            "my-org",
        )

        # Should extract base URL and rebuild properly
        assert endpoint == "https://api.openobserve.ai/api/my-org/v1/logs"

    def test_endpoint_with_trailing_slash(self) -> None:
        """Test endpoint generation with trailing slash in URL."""
        endpoint = get_openobserve_otlp_endpoint(
            "https://api.openobserve.ai/",
            "my-org",
        )

        assert endpoint == "https://api.openobserve.ai/api/my-org/v1/logs"

    def test_endpoint_with_trailing_slash_and_api_prefix(self) -> None:
        """Test endpoint generation with both trailing slash and /api/ path."""
        endpoint = get_openobserve_otlp_endpoint(
            "https://api.openobserve.ai/api/my-org/",
            "my-org",
        )

        assert endpoint == "https://api.openobserve.ai/api/my-org/v1/logs"

    def test_endpoint_defaults_to_default_org(self) -> None:
        """Test that org defaults to 'default' when not provided."""
        endpoint = get_openobserve_otlp_endpoint(
            "https://api.openobserve.ai",
            None,
        )

        assert endpoint == "https://api.openobserve.ai/api/default/v1/logs"

    def test_endpoint_with_different_organizations(self) -> None:
        """Test endpoint generation with various organization names."""
        endpoint1 = get_openobserve_otlp_endpoint(
            "https://api.openobserve.ai",
            "org-one",
        )
        assert endpoint1 == "https://api.openobserve.ai/api/org-one/v1/logs"

        endpoint2 = get_openobserve_otlp_endpoint(
            "https://api.openobserve.ai",
            "org-two",
        )
        assert endpoint2 == "https://api.openobserve.ai/api/org-two/v1/logs"

    def test_endpoint_with_localhost(self) -> None:
        """Test endpoint generation with localhost URL."""
        endpoint = get_openobserve_otlp_endpoint(
            "http://localhost:5080",
            "test-org",
        )

        assert endpoint == "http://localhost:5080/api/test-org/v1/logs"

    def test_endpoint_extraction_with_nested_api_path(self) -> None:
        """Test that only the first /api/ occurrence is used for splitting."""
        endpoint = get_openobserve_otlp_endpoint(
            "https://api.openobserve.ai/api/my-org/api/data",
            "my-org",
        )

        # Should split on first /api/ and rebuild
        assert endpoint == "https://api.openobserve.ai/api/my-org/v1/logs"


class TestBuildOpenobserveHeaders:
    """Tests for build_openobserve_headers function."""

    def test_build_headers_basic(self) -> None:
        """Test building headers with minimal configuration."""
        config = OpenObserveConfig(
            org="my-org",
            stream="logs",
            user="admin",
            password="secret",
        )

        headers = build_openobserve_headers(config)

        assert "organization" in headers
        assert headers["organization"] == "my-org"
        assert "stream-name" in headers
        assert headers["stream-name"] == "logs"
        assert "authorization" in headers

    def test_build_headers_with_base_headers(self) -> None:
        """Test that base headers are included in result."""
        config = OpenObserveConfig(
            org="my-org",
            stream="logs",
            user="admin",
            password="secret",
        )

        base_headers = {
            "X-Custom-Header": "value",
            "X-Another-Header": "another-value",
        }

        headers = build_openobserve_headers(config, base_headers)

        assert headers["X-Custom-Header"] == "value"
        assert headers["X-Another-Header"] == "another-value"
        assert headers["organization"] == "my-org"

    def test_build_headers_auth_format(self) -> None:
        """Test that authorization header is properly formatted as Basic auth."""
        config = OpenObserveConfig(
            org="my-org",
            stream="logs",
            user="admin",
            password="secret",
        )

        headers = build_openobserve_headers(config)

        # Verify Basic auth format
        assert headers["authorization"].startswith("Basic ")

        # Decode and verify credentials
        encoded = headers["authorization"].replace("Basic ", "")
        decoded = base64.b64decode(encoded).decode("ascii")
        assert decoded == "admin:secret"

    def test_build_headers_without_org(self) -> None:
        """Test headers when org is not configured."""
        config = OpenObserveConfig(
            org=None,
            stream="logs",
            user="admin",
            password="secret",
        )

        headers = build_openobserve_headers(config)

        assert "organization" not in headers
        assert "stream-name" in headers
        assert "authorization" in headers

    def test_build_headers_without_stream(self) -> None:
        """Test headers when stream is not configured."""
        config = OpenObserveConfig(
            org="my-org",
            stream=None,
            user="admin",
            password="secret",
        )

        headers = build_openobserve_headers(config)

        assert "organization" in headers
        assert "stream-name" not in headers
        assert "authorization" in headers

    def test_build_headers_without_credentials(self) -> None:
        """Test headers when credentials are not provided."""
        config = OpenObserveConfig(
            org="my-org",
            stream="logs",
            user=None,
            password=None,
        )

        headers = build_openobserve_headers(config)

        assert "organization" in headers
        assert "stream-name" in headers
        assert "authorization" not in headers

    def test_build_headers_without_user_only(self) -> None:
        """Test that auth is not added if user is missing."""
        config = OpenObserveConfig(
            org="my-org",
            stream="logs",
            user=None,
            password="secret",
        )

        headers = build_openobserve_headers(config)

        assert "authorization" not in headers

    def test_build_headers_without_password_only(self) -> None:
        """Test that auth is not added if password is missing."""
        config = OpenObserveConfig(
            org="my-org",
            stream="logs",
            user="admin",
            password=None,
        )

        headers = build_openobserve_headers(config)

        assert "authorization" not in headers

    def test_build_headers_with_special_characters_in_credentials(self) -> None:
        """Test that special characters in credentials are properly encoded."""
        config = OpenObserveConfig(
            org="my-org",
            stream="logs",
            user="admin@domain.com",
            password="p@ss:w0rd!",
        )

        headers = build_openobserve_headers(config)

        # Decode and verify
        encoded = headers["authorization"].replace("Basic ", "")
        decoded = base64.b64decode(encoded).decode("ascii")
        assert decoded == "admin@domain.com:p@ss:w0rd!"

    def test_build_headers_empty_config(self) -> None:
        """Test headers with completely empty config."""
        config = OpenObserveConfig()

        headers = build_openobserve_headers(config)

        # Should return empty dict or dict with only base headers
        assert "organization" not in headers
        assert "stream-name" not in headers
        assert "authorization" not in headers


class TestOpenObserveOTLPClient:
    """Tests for OpenObserveOTLPClient class."""

    def test_from_openobserve_config_basic(self) -> None:
        """Test creating client from OpenObserve config."""
        oo_config = OpenObserveConfig(
            url="https://api.openobserve.ai",
            org="my-org",
            user="admin",
            password="secret",
            stream="logs",
        )

        telemetry_config = TelemetryConfig(
            service_name="test-service",
            service_version="1.0.0",
        )

        client = OpenObserveOTLPClient.from_openobserve_config(
            oo_config,
            telemetry_config,
        )

        assert client is not None
        assert client.service_name == "test-service"
        assert client.service_version == "1.0.0"
        assert client.endpoint == "https://api.openobserve.ai/api/my-org/v1/logs"

    def test_from_openobserve_config_headers(self) -> None:
        """Test that client has correct headers from config."""
        oo_config = OpenObserveConfig(
            url="https://api.openobserve.ai",
            org="my-org",
            user="admin",
            password="secret",
            stream="logs",
        )

        telemetry_config = TelemetryConfig(service_name="test-service")

        client = OpenObserveOTLPClient.from_openobserve_config(
            oo_config,
            telemetry_config,
        )

        assert client.headers["organization"] == "my-org"
        assert client.headers["stream-name"] == "logs"
        assert "authorization" in client.headers

    def test_from_openobserve_config_merges_telemetry_headers(self) -> None:
        """Test that telemetry config headers are merged into client headers."""
        oo_config = OpenObserveConfig(
            url="https://api.openobserve.ai",
            org="my-org",
            user="admin",
            password="secret",
        )

        telemetry_config = TelemetryConfig(
            service_name="test-service",
            otlp_headers={"X-Custom-Header": "custom-value"},
        )

        client = OpenObserveOTLPClient.from_openobserve_config(
            oo_config,
            telemetry_config,
        )

        assert client.headers["X-Custom-Header"] == "custom-value"
        assert client.headers["organization"] == "my-org"

    def test_from_openobserve_config_without_url(self) -> None:
        """Test that ValueError is raised when URL is not set."""
        oo_config = OpenObserveConfig(
            url=None,  # No URL
            org="my-org",
            user="admin",
            password="secret",
        )

        telemetry_config = TelemetryConfig(service_name="test-service")

        with pytest.raises(ValueError, match="OpenObserve URL must be set"):
            OpenObserveOTLPClient.from_openobserve_config(
                oo_config,
                telemetry_config,
            )

    def test_from_openobserve_config_defaults_service_name(self) -> None:
        """Test that service name defaults to 'foundation' when not in config."""
        oo_config = OpenObserveConfig(
            url="https://api.openobserve.ai",
            org="my-org",
            user="admin",
            password="secret",
        )

        telemetry_config = TelemetryConfig()  # No service_name

        client = OpenObserveOTLPClient.from_openobserve_config(
            oo_config,
            telemetry_config,
        )

        assert client.service_name == "foundation"

    @patch("provide.foundation.integrations.openobserve.otlp_adapter.OpenObserveConfig")
    @patch("provide.foundation.integrations.openobserve.otlp_adapter.TelemetryConfig")
    def test_from_env_success(
        self,
        mock_telemetry_config_class: Mock,
        mock_oo_config_class: Mock,
    ) -> None:
        """Test creating client from environment variables."""
        # Setup mock configs
        mock_oo_config = Mock(spec=OpenObserveConfig)
        mock_oo_config.is_configured.return_value = True
        mock_oo_config.url = "https://api.openobserve.ai"
        mock_oo_config.org = "my-org"
        mock_oo_config.user = "admin"
        mock_oo_config.password = "secret"
        mock_oo_config.stream = "logs"
        mock_oo_config_class.from_env.return_value = mock_oo_config

        mock_telemetry_config = Mock(spec=TelemetryConfig)
        mock_telemetry_config.service_name = "test-service"
        mock_telemetry_config.service_version = "1.0.0"
        mock_telemetry_config.otlp_headers = None
        mock_telemetry_config_class.from_env.return_value = mock_telemetry_config

        # Call method
        client = OpenObserveOTLPClient.from_env()

        # Verify
        assert client is not None
        mock_oo_config_class.from_env.assert_called_once()
        mock_telemetry_config_class.from_env.assert_called_once()

    @patch("provide.foundation.integrations.openobserve.otlp_adapter.OpenObserveConfig")
    def test_from_env_not_configured(self, mock_oo_config_class: Mock) -> None:
        """Test that None is returned when OpenObserve is not configured."""
        # Setup mock to return not configured
        mock_oo_config = Mock(spec=OpenObserveConfig)
        mock_oo_config.is_configured.return_value = False
        mock_oo_config_class.from_env.return_value = mock_oo_config

        # Call method
        client = OpenObserveOTLPClient.from_env()

        # Should return None
        assert client is None

    @patch("provide.foundation.integrations.openobserve.otlp_adapter.OpenObserveConfig")
    def test_from_env_exception_handling(self, mock_oo_config_class: Mock) -> None:
        """Test that exceptions are caught and None is returned."""
        # Setup mock to raise exception
        mock_oo_config_class.from_env.side_effect = Exception("Config error")

        # Call method
        client = OpenObserveOTLPClient.from_env()

        # Should return None on exception
        assert client is None

    def test_client_inheritance(self) -> None:
        """Test that OpenObserveOTLPClient inherits from OTLPLogClient."""
        from provide.foundation.logger.otlp.client import OTLPLogClient

        oo_config = OpenObserveConfig(
            url="https://api.openobserve.ai",
            org="my-org",
            user="admin",
            password="secret",
        )

        telemetry_config = TelemetryConfig(service_name="test")

        client = OpenObserveOTLPClient.from_openobserve_config(
            oo_config,
            telemetry_config,
        )

        assert isinstance(client, OTLPLogClient)

    def test_from_openobserve_config_with_all_parameters(self) -> None:
        """Test client creation with all possible parameters."""
        oo_config = OpenObserveConfig(
            url="https://api.openobserve.ai/api/custom-org",
            org="custom-org",
            user="user@example.com",
            password="complex-p@ssw0rd!",
            stream="custom-stream",
        )

        telemetry_config = TelemetryConfig(
            service_name="comprehensive-service",
            service_version="2.0.0",
            otlp_headers={
                "X-Custom-1": "value1",
                "X-Custom-2": "value2",
            },
        )

        client = OpenObserveOTLPClient.from_openobserve_config(
            oo_config,
            telemetry_config,
        )

        assert client.service_name == "comprehensive-service"
        assert client.service_version == "2.0.0"
        assert client.headers["organization"] == "custom-org"
        assert client.headers["stream-name"] == "custom-stream"
        assert client.headers["X-Custom-1"] == "value1"
        assert client.headers["X-Custom-2"] == "value2"


# 🧱🏗️🔚
