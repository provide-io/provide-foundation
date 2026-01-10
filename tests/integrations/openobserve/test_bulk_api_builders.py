#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for OpenObserve bulk API builder functions.

Tests build_log_entry, build_bulk_url, and build_bulk_request functions."""

from __future__ import annotations

from provide.testkit.mocking import Mock, patch

from provide.foundation.integrations.openobserve.bulk_api import (
    build_bulk_request,
    build_bulk_url,
    build_log_entry,
)
from provide.foundation.integrations.openobserve.client import OpenObserveClient
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
        # Explicitly set service_name to None to avoid environment pollution
        config = TelemetryConfig(service_name=None)

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


# 🧱🏗️🔚
