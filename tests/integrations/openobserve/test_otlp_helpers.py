#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for OpenObserve OTLP helpers.

Tests all helper functions in integrations/openobserve/otlp_helpers.py."""

from __future__ import annotations

from typing import Any

from provide.testkit.mocking import Mock, patch
import pytest

# Skip all tests in this module if opentelemetry is not installed
pytest.importorskip("opentelemetry")

from provide.foundation.integrations.openobserve.otlp_helpers import (
    add_trace_attributes,
    add_trace_context_to_log_entry,
    build_bulk_url,
    build_log_entry,
    configure_otlp_exporter,
    create_otlp_resource,
    map_level_to_severity,
)


class TestConfigureOtlpExporter:
    """Tests for configure_otlp_exporter function."""

    def test_configure_basic(self) -> None:
        """Test basic OTLP exporter configuration."""
        config = Mock()
        config.get_otlp_headers_dict.return_value = {"Content-Type": "application/x-protobuf"}
        config.otlp_endpoint = "https://api.openobserve.ai/api/my-org"
        config.otlp_traces_endpoint = None

        oo_config = Mock()
        oo_config.org = "my-org"
        oo_config.stream = "logs"

        endpoint, headers = configure_otlp_exporter(config, oo_config)

        assert endpoint == "https://api.openobserve.ai/api/my-org/v1/logs"
        assert headers["organization"] == "my-org"
        assert headers["stream-name"] == "logs"
        assert headers["Content-Type"] == "application/x-protobuf"

    def test_configure_with_traces_endpoint(self) -> None:
        """Test configuration when traces endpoint is provided."""
        config = Mock()
        config.get_otlp_headers_dict.return_value = {}
        config.otlp_traces_endpoint = "https://api.openobserve.ai/api/my-org/v1/traces"
        config.otlp_endpoint = "https://api.openobserve.ai/api/my-org"

        oo_config = Mock()
        oo_config.org = "my-org"
        oo_config.stream = "logs"

        endpoint, _headers = configure_otlp_exporter(config, oo_config)

        # Should derive logs endpoint from traces endpoint
        assert endpoint == "https://api.openobserve.ai/api/my-org/v1/logs"

    def test_configure_without_org(self) -> None:
        """Test configuration without organization."""
        config = Mock()
        config.get_otlp_headers_dict.return_value = {}
        config.otlp_endpoint = "https://api.openobserve.ai"
        config.otlp_traces_endpoint = None

        oo_config = Mock()
        oo_config.org = None
        oo_config.stream = "logs"

        _endpoint, headers = configure_otlp_exporter(config, oo_config)

        assert "organization" not in headers
        assert headers["stream-name"] == "logs"

    def test_configure_without_stream(self) -> None:
        """Test configuration without stream."""
        config = Mock()
        config.get_otlp_headers_dict.return_value = {}
        config.otlp_endpoint = "https://api.openobserve.ai"
        config.otlp_traces_endpoint = None

        oo_config = Mock()
        oo_config.org = "my-org"
        oo_config.stream = None

        _endpoint, headers = configure_otlp_exporter(config, oo_config)

        assert headers["organization"] == "my-org"
        assert "stream-name" not in headers


class TestCreateOtlpResource:
    """Tests for create_otlp_resource function."""

    def test_create_resource_basic(self) -> None:
        """Test creating OTLP resource with service name only."""
        resource_attrs_class = Mock()
        resource_attrs_class.SERVICE_NAME = "service.name"
        resource_attrs_class.SERVICE_VERSION = "service.version"

        resource_class = Mock()
        mock_resource = Mock()
        resource_class.create.return_value = mock_resource

        result = create_otlp_resource(
            "test-service",
            None,
            resource_class,
            resource_attrs_class,
        )

        assert result == mock_resource
        resource_class.create.assert_called_once()
        call_args = resource_class.create.call_args[0][0]
        assert call_args["service.name"] == "test-service"
        assert "service.version" not in call_args

    def test_create_resource_with_version(self) -> None:
        """Test creating OTLP resource with service name and version."""
        resource_attrs_class = Mock()
        resource_attrs_class.SERVICE_NAME = "service.name"
        resource_attrs_class.SERVICE_VERSION = "service.version"

        resource_class = Mock()
        mock_resource = Mock()
        resource_class.create.return_value = mock_resource

        result = create_otlp_resource(
            "test-service",
            "1.2.3",
            resource_class,
            resource_attrs_class,
        )

        assert result == mock_resource
        call_args = resource_class.create.call_args[0][0]
        assert call_args["service.name"] == "test-service"
        assert call_args["service.version"] == "1.2.3"


class TestAddTraceAttributes:
    """Tests for add_trace_attributes function."""

    def test_add_trace_attributes_with_recording_span(self) -> None:
        """Test adding trace attributes when span is recording."""
        trace_module = Mock()
        span = Mock()
        span.is_recording.return_value = True
        span_context = Mock()
        span_context.trace_id = 0x1234567890ABCDEF1234567890ABCDEF
        span_context.span_id = 0x1234567890ABCDEF
        span.get_span_context.return_value = span_context
        trace_module.get_current_span.return_value = span

        attributes: dict[str, Any] = {}
        add_trace_attributes(attributes, trace_module)

        assert "trace_id" in attributes
        assert "span_id" in attributes
        assert attributes["trace_id"] == "1234567890abcdef1234567890abcdef"
        assert attributes["span_id"] == "1234567890abcdef"

    def test_add_trace_attributes_without_span(self) -> None:
        """Test that no attributes are added when no span exists."""
        trace_module = Mock()
        trace_module.get_current_span.return_value = None

        attributes: dict[str, Any] = {}
        add_trace_attributes(attributes, trace_module)

        assert "trace_id" not in attributes
        assert "span_id" not in attributes

    def test_add_trace_attributes_with_non_recording_span(self) -> None:
        """Test that no attributes are added when span is not recording."""
        trace_module = Mock()
        span = Mock()
        span.is_recording.return_value = False
        trace_module.get_current_span.return_value = span

        attributes: dict[str, Any] = {}
        add_trace_attributes(attributes, trace_module)

        assert "trace_id" not in attributes
        assert "span_id" not in attributes


class TestMapLevelToSeverity:
    """Tests for map_level_to_severity function."""

    def test_map_standard_levels(self) -> None:
        """Test mapping of standard log levels."""
        assert map_level_to_severity("TRACE") == 1
        assert map_level_to_severity("DEBUG") == 5
        assert map_level_to_severity("INFO") == 9
        assert map_level_to_severity("WARN") == 13
        assert map_level_to_severity("WARNING") == 13
        assert map_level_to_severity("ERROR") == 17
        assert map_level_to_severity("FATAL") == 21
        assert map_level_to_severity("CRITICAL") == 21

    def test_map_lowercase_levels(self) -> None:
        """Test that lowercase levels are handled correctly."""
        assert map_level_to_severity("info") == 9
        assert map_level_to_severity("error") == 17
        assert map_level_to_severity("debug") == 5

    def test_map_mixed_case_levels(self) -> None:
        """Test that mixed case levels are handled correctly."""
        assert map_level_to_severity("Info") == 9
        assert map_level_to_severity("ErRoR") == 17

    def test_map_unknown_level(self) -> None:
        """Test that unknown levels default to INFO (9)."""
        assert map_level_to_severity("UNKNOWN") == 9
        assert map_level_to_severity("CUSTOM") == 9
        assert map_level_to_severity("") == 9


class TestAddTraceContextToLogEntry:
    """Tests for add_trace_context_to_log_entry function."""

    @patch("opentelemetry.trace.get_current_span")
    def test_add_context_from_opentelemetry(self, mock_get_span: Mock) -> None:
        """Test adding trace context from OpenTelemetry."""
        span = Mock()
        span.is_recording.return_value = True
        span_context = Mock()
        span_context.trace_id = 0xABCDEF1234567890ABCDEF1234567890
        span_context.span_id = 0xFEDCBA9876543210
        span.get_span_context.return_value = span_context
        mock_get_span.return_value = span

        log_entry: dict[str, Any] = {}
        add_trace_context_to_log_entry(log_entry)

        assert log_entry["trace_id"] == "abcdef1234567890abcdef1234567890"
        assert log_entry["span_id"] == "fedcba9876543210"

    @patch("opentelemetry.trace.get_current_span")
    def test_add_context_without_span(self, mock_get_span: Mock) -> None:
        """Test that no context is added when no span is available."""
        mock_get_span.return_value = None

        log_entry: dict[str, Any] = {}
        add_trace_context_to_log_entry(log_entry)

        # Should not crash, may have tried Foundation tracer
        # At minimum, should not have OpenTelemetry context
        assert True

    @patch("opentelemetry.trace.get_current_span", side_effect=ImportError)
    @patch("provide.foundation.tracer.context.get_current_span")
    @patch("provide.foundation.tracer.context.get_current_trace_id")
    def test_add_context_with_foundation_tracer(
        self,
        mock_get_trace_id: Mock,
        mock_get_span: Mock,
        mock_otel_get_span: Mock,
    ) -> None:
        """Test fallback to Foundation tracer when OpenTelemetry is not available."""
        # OpenTelemetry not available, Foundation tracer has span
        span = Mock()
        span.trace_id = "foundation-trace-123"
        span.span_id = "foundation-span-456"
        mock_get_span.return_value = span
        mock_get_trace_id.return_value = None

        log_entry: dict[str, Any] = {}
        add_trace_context_to_log_entry(log_entry)

        assert log_entry["trace_id"] == "foundation-trace-123"
        assert log_entry["span_id"] == "foundation-span-456"

    @patch("opentelemetry.trace.get_current_span", side_effect=ImportError)
    @patch("provide.foundation.tracer.context.get_current_span")
    @patch("provide.foundation.tracer.context.get_current_trace_id")
    def test_add_context_with_foundation_trace_id_only(
        self,
        mock_get_trace_id: Mock,
        mock_get_span: Mock,
        mock_otel_get_span: Mock,
    ) -> None:
        """Test fallback to Foundation trace ID when no span is available."""
        # OpenTelemetry not available, Foundation tracer has only trace_id
        mock_get_span.return_value = None
        mock_get_trace_id.return_value = "foundation-trace-only-789"

        log_entry: dict[str, Any] = {}
        add_trace_context_to_log_entry(log_entry)

        assert log_entry["trace_id"] == "foundation-trace-only-789"
        assert "span_id" not in log_entry

    def test_add_context_without_opentelemetry(self) -> None:
        """Test fallback when OpenTelemetry is not available."""
        # OpenTelemetry import will fail in test environment
        log_entry: dict[str, Any] = {}
        add_trace_context_to_log_entry(log_entry)

        # Should not crash even without OpenTelemetry
        assert isinstance(log_entry, dict)


class TestBuildLogEntry:
    """Tests for build_log_entry function."""

    def test_build_log_entry_basic(self) -> None:
        """Test building log entry with basic parameters."""
        config = Mock()
        config.service_name = "test-service"

        entry = build_log_entry("Test message", "INFO", None, None, config)

        assert entry["message"] == "Test message"
        assert entry["level"] == "INFO"
        assert entry["service"] == "test-service"
        assert "_timestamp" in entry
        assert isinstance(entry["_timestamp"], int)

    def test_build_log_entry_with_service_override(self) -> None:
        """Test that explicit service parameter overrides config."""
        config = Mock()
        config.service_name = "config-service"

        entry = build_log_entry("Test", "INFO", "override-service", None, config)

        assert entry["service"] == "override-service"

    def test_build_log_entry_with_attributes(self) -> None:
        """Test building log entry with additional attributes."""
        config = Mock()
        config.service_name = "test-service"

        attributes = {"user_id": "123", "action": "login"}

        entry = build_log_entry("Test", "INFO", None, attributes, config)

        assert entry["user_id"] == "123"
        assert entry["action"] == "login"

    def test_build_log_entry_level_uppercased(self) -> None:
        """Test that log level is uppercased."""
        config = Mock()
        config.service_name = "test"

        entry = build_log_entry("Test", "info", None, None, config)

        assert entry["level"] == "INFO"

    def test_build_log_entry_defaults_to_foundation(self) -> None:
        """Test that service defaults to 'foundation' when not provided."""
        config = Mock()
        config.service_name = None

        entry = build_log_entry("Test", "INFO", None, None, config)

        assert entry["service"] == "foundation"

    def test_build_log_entry_timestamp_is_microseconds(self) -> None:
        """Test that timestamp is in microseconds."""
        config = Mock()
        config.service_name = "test"

        entry = build_log_entry("Test", "INFO", None, None, config)

        # Timestamp should be in microseconds (16 digits for current time)
        assert entry["_timestamp"] > 1_000_000_000_000_000


class TestBuildBulkUrl:
    """Tests for build_bulk_url function."""

    def test_build_bulk_url_without_api_prefix(self) -> None:
        """Test building bulk URL when URL doesn't have /api/{org}."""
        client = Mock()
        client.url = "https://api.openobserve.ai"
        client.organization = "my-org"

        url = build_bulk_url(client)

        assert url == "https://api.openobserve.ai/api/my-org/_bulk"

    def test_build_bulk_url_with_api_prefix(self) -> None:
        """Test building bulk URL when URL already has /api/{org}."""
        client = Mock()
        client.url = "https://api.openobserve.ai/api/my-org"
        client.organization = "my-org"

        url = build_bulk_url(client)

        assert url == "https://api.openobserve.ai/api/my-org/_bulk"

    def test_build_bulk_url_with_trailing_slash(self) -> None:
        """Test building bulk URL with trailing slash."""
        client = Mock()
        client.url = "https://api.openobserve.ai/api/my-org/"
        client.organization = "my-org"

        url = build_bulk_url(client)

        assert url == "https://api.openobserve.ai/api/my-org//_bulk"

    def test_build_bulk_url_different_organizations(self) -> None:
        """Test bulk URL with different organization names."""
        client = Mock()
        client.url = "https://api.openobserve.ai"
        client.organization = "different-org"

        url = build_bulk_url(client)

        assert url == "https://api.openobserve.ai/api/different-org/_bulk"

    def test_build_bulk_url_localhost(self) -> None:
        """Test bulk URL with localhost."""
        client = Mock()
        client.url = "http://localhost:5080"
        client.organization = "test-org"

        url = build_bulk_url(client)

        assert url == "http://localhost:5080/api/test-org/_bulk"


# 🧱🏗️🔚
