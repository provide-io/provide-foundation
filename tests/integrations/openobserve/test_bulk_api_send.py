#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for OpenObserve bulk API send_log_bulk function."""

from __future__ import annotations

from provide.testkit.mocking import AsyncMock, Mock, patch
import pytest

from provide.foundation.integrations.openobserve.bulk_api import send_log_bulk
from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.config import OpenObserveConfig
from provide.foundation.logger.config.telemetry import TelemetryConfig
from provide.foundation.serialization import json_loads


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


# 🧱🏗️🔚
