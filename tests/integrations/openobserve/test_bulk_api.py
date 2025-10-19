"""Comprehensive tests for OpenObserve bulk API functionality.

Tests all functions in integrations/openobserve/bulk_api.py with unit and integration tests.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, Mock, patch

import pytest

from provide.foundation.integrations.openobserve.bulk_api import (
    build_bulk_request,
    build_bulk_url,
    build_log_entry,
    send_log_bulk,
)
from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.config import OpenObserveConfig
from provide.foundation.logger.config.telemetry import TelemetryConfig
from provide.foundation.serialization import json_loads


class TestBuildLogEntry:
    """Tests for build_log_entry function."""

    def test_build_log_entry_basic(self) -> None:
        """Test building log entry with basic parameters."""
        config = TelemetryConfig(service_name="test-service")

        entry = build_log_entry(
            message="Test message",
            level="INFO",
            service_name=None,
            attributes=None,
            config=config,
        )

        assert entry["message"] == "Test message"
        assert entry["level"] == "INFO"
        assert entry["service"] == "test-service"
        assert "_timestamp" in entry
        assert isinstance(entry["_timestamp"], int)
        assert entry["_timestamp"] > 0

    def test_build_log_entry_with_service_name_override(self) -> None:
        """Test that explicit service_name parameter overrides config."""
        config = TelemetryConfig(service_name="config-service")

        entry = build_log_entry(
            message="Test",
            level="INFO",
            service_name="override-service",
            attributes=None,
            config=config,
        )

        assert entry["service"] == "override-service"

    def test_build_log_entry_with_attributes(self) -> None:
        """Test building log entry with additional attributes."""
        config = TelemetryConfig(service_name="test-service")
        attributes = {
            "user_id": "123",
            "request_id": "abc-def",
            "environment": "production",
        }

        entry = build_log_entry(
            message="Test",
            level="INFO",
            service_name=None,
            attributes=attributes,
            config=config,
        )

        assert entry["user_id"] == "123"
        assert entry["request_id"] == "abc-def"
        assert entry["environment"] == "production"

    def test_build_log_entry_level_uppercased(self) -> None:
        """Test that log level is uppercased."""
        config = TelemetryConfig(service_name="test")

        entry = build_log_entry("Test", "info", None, None, config)
        assert entry["level"] == "INFO"

        entry = build_log_entry("Test", "debug", None, None, config)
        assert entry["level"] == "DEBUG"

    def test_build_log_entry_defaults_to_foundation_service(self) -> None:
        """Test that service defaults to 'foundation' when not in config."""
        config = TelemetryConfig()  # No service_name

        entry = build_log_entry("Test", "INFO", None, None, config)

        assert entry["service"] == "foundation"

    @patch("provide.foundation.integrations.openobserve.bulk_api.add_trace_context_to_attributes")
    def test_build_log_entry_adds_trace_context(self, mock_add_trace: Mock) -> None:
        """Test that trace context is added to log entry."""
        config = TelemetryConfig(service_name="test")

        build_log_entry("Test", "INFO", None, None, config)

        mock_add_trace.assert_called_once()
        call_args = mock_add_trace.call_args[0][0]
        assert isinstance(call_args, dict)

    def test_build_log_entry_timestamp_is_microseconds(self) -> None:
        """Test that timestamp is in microseconds (OpenObserve format)."""
        config = TelemetryConfig(service_name="test")

        entry = build_log_entry("Test", "INFO", None, None, config)

        # Timestamp should be in microseconds (16 digits for current time)
        assert entry["_timestamp"] > 1_000_000_000_000_000


class TestBuildBulkUrl:
    """Tests for build_bulk_url function."""

    def test_build_bulk_url_without_api_prefix(self) -> None:
        """Test building bulk URL when URL doesn't have /api/{org}."""
        client = Mock(spec=OpenObserveClient)
        client.url = "https://api.openobserve.ai"
        client.organization = "my-org"

        url = build_bulk_url(client)

        assert url == "https://api.openobserve.ai/api/my-org/_bulk"

    def test_build_bulk_url_with_api_prefix(self) -> None:
        """Test building bulk URL when URL already has /api/{org}."""
        client = Mock(spec=OpenObserveClient)
        client.url = "https://api.openobserve.ai/api/my-org"
        client.organization = "my-org"

        url = build_bulk_url(client)

        assert url == "https://api.openobserve.ai/api/my-org/_bulk"

    def test_build_bulk_url_with_trailing_slash(self) -> None:
        """Test building bulk URL with trailing slash in client URL."""
        client = Mock(spec=OpenObserveClient)
        client.url = "https://api.openobserve.ai/api/my-org/"
        client.organization = "my-org"

        url = build_bulk_url(client)

        assert url == "https://api.openobserve.ai/api/my-org//_bulk"

    def test_build_bulk_url_different_organizations(self) -> None:
        """Test that organization name is used in URL construction."""
        client = Mock(spec=OpenObserveClient)
        client.url = "https://api.openobserve.ai"
        client.organization = "different-org"

        url = build_bulk_url(client)

        assert url == "https://api.openobserve.ai/api/different-org/_bulk"


class TestBuildBulkRequest:
    """Tests for build_bulk_request function."""

    def test_build_bulk_request_basic(self) -> None:
        """Test building NDJSON bulk request."""
        config = TelemetryConfig(service_name="test")

        bulk_request = build_bulk_request(
            message="Test message",
            level="INFO",
            service_name=None,
            attributes=None,
            config=config,
            stream="default",
        )

        # Should be NDJSON format (two lines with newline at end)
        lines = bulk_request.split("\n")
        assert len(lines) == 3  # index line, data line, trailing newline
        assert lines[2] == ""  # Trailing newline results in empty string

    def test_build_bulk_request_index_line(self) -> None:
        """Test that index line is correctly formatted."""
        config = TelemetryConfig(service_name="test")

        bulk_request = build_bulk_request(
            message="Test",
            level="INFO",
            service_name=None,
            attributes=None,
            config=config,
            stream="my-stream",
        )

        lines = bulk_request.split("\n")
        index_line = json_loads(lines[0])

        assert "index" in index_line
        assert index_line["index"]["_index"] == "my-stream"

    def test_build_bulk_request_data_line(self) -> None:
        """Test that data line contains log entry."""
        config = TelemetryConfig(service_name="test")

        bulk_request = build_bulk_request(
            message="Test message",
            level="INFO",
            service_name=None,
            attributes=None,
            config=config,
            stream="default",
        )

        lines = bulk_request.split("\n")
        data_line = json_loads(lines[1])

        assert data_line["message"] == "Test message"
        assert data_line["level"] == "INFO"
        assert data_line["service"] == "test"

    def test_build_bulk_request_with_attributes(self) -> None:
        """Test bulk request includes attributes in data line."""
        config = TelemetryConfig(service_name="test")
        attributes = {"user_id": "123", "action": "login"}

        bulk_request = build_bulk_request(
            message="User login",
            level="INFO",
            service_name=None,
            attributes=attributes,
            config=config,
            stream="default",
        )

        lines = bulk_request.split("\n")
        data_line = json_loads(lines[1])

        assert data_line["user_id"] == "123"
        assert data_line["action"] == "login"

    def test_build_bulk_request_custom_stream(self) -> None:
        """Test bulk request with custom stream name."""
        config = TelemetryConfig(service_name="test")

        bulk_request = build_bulk_request(
            message="Test",
            level="INFO",
            service_name=None,
            attributes=None,
            config=config,
            stream="custom-logs",
        )

        lines = bulk_request.split("\n")
        index_line = json_loads(lines[0])

        assert index_line["index"]["_index"] == "custom-logs"


class TestSendLogBulk:
    """Tests for send_log_bulk function."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock OpenObserve client."""
        client = Mock(spec=OpenObserveClient)
        client.url = "https://api.openobserve.ai"
        client.organization = "test-org"

        # Mock the async client
        mock_response = AsyncMock()
        mock_response.is_success.return_value = True
        mock_response.status = 200

        client._client = AsyncMock()
        client._client.request = AsyncMock(return_value=mock_response)

        return client

    @patch("provide.foundation.integrations.openobserve.bulk_api.OpenObserveClient")
    @patch("provide.foundation.integrations.openobserve.bulk_api.get_hub")
    @patch("provide.foundation.integrations.openobserve.bulk_api.OpenObserveConfig")
    def test_send_log_bulk_success(
        self,
        mock_oo_config_class: Mock,
        mock_get_hub: Mock,
        mock_client_class: Mock,
        mock_client: Mock,
    ) -> None:
        """Test successful log sending via bulk API."""
        # Setup mocks
        mock_client_class.from_config.return_value = mock_client

        mock_hub = Mock()
        mock_hub.get_foundation_config.return_value = TelemetryConfig(service_name="test")
        mock_get_hub.return_value = mock_hub

        mock_oo_config = Mock(spec=OpenObserveConfig)
        mock_oo_config.stream = "default"
        mock_oo_config_class.from_env.return_value = mock_oo_config

        # Call function
        result = send_log_bulk("Test message", "INFO")

        # Verify
        assert result is True
        mock_client._client.request.assert_called_once()

    @patch("provide.foundation.integrations.openobserve.bulk_api.OpenObserveClient")
    @patch("provide.foundation.integrations.openobserve.bulk_api.get_hub")
    @patch("provide.foundation.integrations.openobserve.bulk_api.OpenObserveConfig")
    def test_send_log_bulk_with_provided_client(
        self,
        mock_oo_config_class: Mock,
        mock_get_hub: Mock,
        mock_client_class: Mock,
        mock_client: Mock,
    ) -> None:
        """Test sending log with provided client (doesn't create new one)."""
        # Setup mocks
        mock_hub = Mock()
        mock_hub.get_foundation_config.return_value = TelemetryConfig(service_name="test")
        mock_get_hub.return_value = mock_hub

        mock_oo_config = Mock(spec=OpenObserveConfig)
        mock_oo_config.stream = "default"
        mock_oo_config_class.from_env.return_value = mock_oo_config

        # Call with provided client
        result = send_log_bulk("Test", "INFO", client=mock_client)

        # Should not call from_config
        mock_client_class.from_config.assert_not_called()
        assert result is True

    @patch("provide.foundation.integrations.openobserve.bulk_api.OpenObserveClient")
    @patch("provide.foundation.integrations.openobserve.bulk_api.get_hub")
    @patch("provide.foundation.integrations.openobserve.bulk_api.OpenObserveConfig")
    @patch("provide.foundation.integrations.openobserve.bulk_api.TelemetryConfig")
    def test_send_log_bulk_fallback_to_env_config(
        self,
        mock_telemetry_config_class: Mock,
        mock_oo_config_class: Mock,
        mock_get_hub: Mock,
        mock_client_class: Mock,
        mock_client: Mock,
    ) -> None:
        """Test that it falls back to TelemetryConfig.from_env() when hub has no config."""
        # Setup mocks
        mock_client_class.from_config.return_value = mock_client

        mock_hub = Mock()
        mock_hub.get_foundation_config.return_value = None  # No config in hub
        mock_get_hub.return_value = mock_hub

        mock_telemetry_config_class.from_env.return_value = TelemetryConfig(service_name="test")

        mock_oo_config = Mock(spec=OpenObserveConfig)
        mock_oo_config.stream = "default"
        mock_oo_config_class.from_env.return_value = mock_oo_config

        # Call function
        result = send_log_bulk("Test", "INFO")

        # Verify fallback was used
        mock_telemetry_config_class.from_env.assert_called_once()
        assert result is True

    @patch("provide.foundation.integrations.openobserve.bulk_api.OpenObserveClient")
    @patch("provide.foundation.integrations.openobserve.bulk_api.get_hub")
    @patch("provide.foundation.integrations.openobserve.bulk_api.OpenObserveConfig")
    def test_send_log_bulk_request_details(
        self,
        mock_oo_config_class: Mock,
        mock_get_hub: Mock,
        mock_client_class: Mock,
        mock_client: Mock,
    ) -> None:
        """Test the details of the HTTP request made to bulk API."""
        # Setup mocks
        mock_client_class.from_config.return_value = mock_client

        mock_hub = Mock()
        mock_hub.get_foundation_config.return_value = TelemetryConfig(service_name="test")
        mock_get_hub.return_value = mock_hub

        mock_oo_config = Mock(spec=OpenObserveConfig)
        mock_oo_config.stream = "test-stream"
        mock_oo_config_class.from_env.return_value = mock_oo_config

        # Call function
        send_log_bulk("Test message", "INFO", attributes={"key": "value"})

        # Verify request details
        call_kwargs = mock_client._client.request.call_args[1]
        assert call_kwargs["method"] == "POST"
        assert call_kwargs["uri"] == "https://api.openobserve.ai/api/test-org/_bulk"
        assert call_kwargs["headers"]["Content-Type"] == "application/x-ndjson"
        assert isinstance(call_kwargs["body"], str)
        assert "\n" in call_kwargs["body"]  # NDJSON format

    @patch("provide.foundation.integrations.openobserve.bulk_api.OpenObserveClient")
    @patch("provide.foundation.integrations.openobserve.bulk_api.get_hub")
    @patch("provide.foundation.integrations.openobserve.bulk_api.OpenObserveConfig")
    def test_send_log_bulk_failure_response(
        self,
        mock_oo_config_class: Mock,
        mock_get_hub: Mock,
        mock_client_class: Mock,
        mock_client: Mock,
    ) -> None:
        """Test handling of failed response from bulk API."""
        # Setup failure response
        mock_response = AsyncMock()
        mock_response.is_success = Mock(return_value=False)  # Mock as callable
        mock_response.status = 500
        mock_client._client.request = AsyncMock(return_value=mock_response)

        mock_client_class.from_config.return_value = mock_client

        mock_hub = Mock()
        mock_hub.get_foundation_config.return_value = TelemetryConfig(service_name="test")
        mock_get_hub.return_value = mock_hub

        mock_oo_config = Mock(spec=OpenObserveConfig)
        mock_oo_config.stream = "default"
        mock_oo_config_class.from_env.return_value = mock_oo_config

        # Call function
        result = send_log_bulk("Test", "INFO")

        # Should return False on failure
        assert result is False

    @patch("provide.foundation.integrations.openobserve.bulk_api.OpenObserveClient")
    @patch("provide.foundation.integrations.openobserve.bulk_api.get_hub")
    def test_send_log_bulk_exception_handling(
        self,
        mock_get_hub: Mock,
        mock_client_class: Mock,
    ) -> None:
        """Test that exceptions are caught and return False."""
        # Setup to raise exception
        mock_client_class.from_config.side_effect = Exception("Connection error")

        # Call function
        result = send_log_bulk("Test", "INFO")

        # Should return False on exception
        assert result is False

    @patch("provide.foundation.integrations.openobserve.bulk_api.OpenObserveClient")
    @patch("provide.foundation.integrations.openobserve.bulk_api.get_hub")
    @patch("provide.foundation.integrations.openobserve.bulk_api.OpenObserveConfig")
    def test_send_log_bulk_uses_default_stream(
        self,
        mock_oo_config_class: Mock,
        mock_get_hub: Mock,
        mock_client_class: Mock,
        mock_client: Mock,
    ) -> None:
        """Test that 'default' stream is used when not configured."""
        # Setup mocks
        mock_client_class.from_config.return_value = mock_client

        mock_hub = Mock()
        mock_hub.get_foundation_config.return_value = TelemetryConfig(service_name="test")
        mock_get_hub.return_value = mock_hub

        mock_oo_config = Mock(spec=OpenObserveConfig)
        mock_oo_config.stream = None  # No stream configured
        mock_oo_config_class.from_env.return_value = mock_oo_config

        # Call function
        send_log_bulk("Test", "INFO")

        # Verify 'default' stream is used
        call_kwargs = mock_client._client.request.call_args[1]
        body_lines = call_kwargs["body"].split("\n")
        index_line = json_loads(body_lines[0])
        assert index_line["index"]["_index"] == "default"

    @patch("provide.foundation.integrations.openobserve.bulk_api.OpenObserveClient")
    @patch("provide.foundation.integrations.openobserve.bulk_api.get_hub")
    @patch("provide.foundation.integrations.openobserve.bulk_api.OpenObserveConfig")
    def test_send_log_bulk_with_all_parameters(
        self,
        mock_oo_config_class: Mock,
        mock_get_hub: Mock,
        mock_client_class: Mock,
        mock_client: Mock,
    ) -> None:
        """Test sending log with all optional parameters."""
        # Setup mocks
        mock_client_class.from_config.return_value = mock_client

        mock_hub = Mock()
        mock_hub.get_foundation_config.return_value = TelemetryConfig(service_name="test")
        mock_get_hub.return_value = mock_hub

        mock_oo_config = Mock(spec=OpenObserveConfig)
        mock_oo_config.stream = "default"
        mock_oo_config_class.from_env.return_value = mock_oo_config

        # Call with all parameters
        result = send_log_bulk(
            message="Test message",
            level="ERROR",
            service_name="custom-service",
            attributes={"error_code": "500", "user": "admin"},
            client=mock_client,
        )

        assert result is True

        # Verify request body contains all data
        call_kwargs = mock_client._client.request.call_args[1]
        body_lines = call_kwargs["body"].split("\n")
        data_line = json_loads(body_lines[1])

        assert data_line["message"] == "Test message"
        assert data_line["level"] == "ERROR"
        assert data_line["service"] == "custom-service"
        assert data_line["error_code"] == "500"
        assert data_line["user"] == "admin"


# <3 🧱🤝🔌🪄
