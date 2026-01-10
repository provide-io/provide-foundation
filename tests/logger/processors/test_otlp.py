#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for logger OTLP processor.

Tests all functions in logger/processors/otlp.py including timestamp conversion,
processor creation, log flushing, and provider reset."""

from __future__ import annotations

from collections.abc import Generator
import sys

from provide.testkit.mocking import Mock, patch
import pytest

# Skip all tests in this module if opentelemetry is not installed
pytest.importorskip("opentelemetry")

from provide.foundation.logger.processors.otlp import (
    create_otlp_processor,
    flush_otlp_logs,
    reset_otlp_provider,
)


@pytest.fixture(autouse=True)
def reset_otlp_provider_fixture() -> Generator[None]:
    """Reset OTLP provider before each test."""
    # Get module reference from sys.modules
    otlp_mod = sys.modules.get("provide.foundation.logger.processors.otlp")
    if otlp_mod:
        # Reset the global provider before each test
        otlp_mod._OTLP_LOGGER_PROVIDER = None
    yield
    # Clean up after test
    if otlp_mod:
        otlp_mod._OTLP_LOGGER_PROVIDER = None


class TestConvertTimestampToNanos:
    """Tests for _convert_timestamp_to_nanos helper function."""

    def test_convert_none_timestamp(self) -> None:
        """Test that None timestamp returns None."""
        from provide.foundation.logger.processors.otlp import _convert_timestamp_to_nanos

        result = _convert_timestamp_to_nanos(None)

        assert result is None

    def test_convert_empty_string(self) -> None:
        """Test that empty string returns None."""
        from provide.foundation.logger.processors.otlp import _convert_timestamp_to_nanos

        result = _convert_timestamp_to_nanos("")

        assert result is None

    def test_convert_iso_timestamp_utc(self) -> None:
        """Test converting ISO format timestamp with Z suffix."""
        from provide.foundation.logger.processors.otlp import _convert_timestamp_to_nanos

        # 2024-01-01T00:00:00Z = 1704067200 seconds = 1704067200000000000 nanos
        result = _convert_timestamp_to_nanos("2024-01-01T00:00:00Z")

        assert result == 1704067200000000000

    def test_convert_iso_timestamp_with_offset(self) -> None:
        """Test converting ISO format timestamp with timezone offset."""
        from provide.foundation.logger.processors.otlp import _convert_timestamp_to_nanos

        # 2024-01-01T00:00:00+00:00 = 1704067200 seconds
        result = _convert_timestamp_to_nanos("2024-01-01T00:00:00+00:00")

        assert result == 1704067200000000000

    def test_convert_float_seconds(self) -> None:
        """Test converting float timestamp in seconds."""
        from provide.foundation.logger.processors.otlp import _convert_timestamp_to_nanos

        # Small value (< 10 billion) is treated as seconds
        result = _convert_timestamp_to_nanos(1704067200.0)

        assert result == 1704067200000000000

    def test_convert_int_seconds(self) -> None:
        """Test converting integer timestamp in seconds."""
        from provide.foundation.logger.processors.otlp import _convert_timestamp_to_nanos

        result = _convert_timestamp_to_nanos(1704067200)

        assert result == 1704067200000000000

    def test_convert_already_nanos(self) -> None:
        """Test that large timestamp (already in nanos) is returned as-is."""
        from provide.foundation.logger.processors.otlp import _convert_timestamp_to_nanos

        # Large value (>= 10 billion) is treated as already in nanos
        nanos = 1704067200000000000
        result = _convert_timestamp_to_nanos(nanos)

        assert result == nanos

    def test_convert_float_with_subsecond_precision(self) -> None:
        """Test converting float with subsecond precision."""
        from provide.foundation.logger.processors.otlp import _convert_timestamp_to_nanos

        # 1.5 seconds should become 1500000000 nanos
        result = _convert_timestamp_to_nanos(1.5)

        assert result == 1500000000


class TestCreateOtlpProcessor:
    """Tests for create_otlp_processor function."""

    def test_create_without_endpoint(self) -> None:
        """Test that None is returned when no OTLP endpoint is configured."""
        config = Mock()
        config.otlp_endpoint = None

        result = create_otlp_processor(config)

        assert result is None

    @patch("provide.foundation.logger.processors.otlp.OTLPLogClient")
    def test_create_when_client_not_available(self, mock_client_class: Mock) -> None:
        """Test that None is returned when OTLP client is not available."""
        config = Mock()
        config.otlp_endpoint = "https://api.example.com"

        mock_client = Mock()
        mock_client.is_available.return_value = False
        mock_client_class.from_config.return_value = mock_client

        result = create_otlp_processor(config)

        assert result is None

    @patch("provide.foundation.logger.processors.otlp.OTLPLogClient")
    def test_create_when_provider_creation_fails(self, mock_client_class: Mock) -> None:
        """Test that None is returned when logger provider creation fails."""
        config = Mock()
        config.otlp_endpoint = "https://api.example.com"

        mock_client = Mock()
        mock_client.is_available.return_value = True
        mock_client.create_logger_provider.return_value = None
        mock_client_class.from_config.return_value = mock_client

        result = create_otlp_processor(config)

        assert result is None

    @patch("provide.foundation.logger.processors.otlp.OTLPLogClient")
    def test_create_success(self, mock_client_class: Mock) -> None:
        """Test successful creation of OTLP processor."""
        config = Mock()
        config.otlp_endpoint = "https://api.example.com"

        mock_provider = Mock()
        mock_provider.get_logger.return_value = Mock()
        mock_provider.resource = Mock()

        mock_client = Mock()
        mock_client.is_available.return_value = True
        mock_client.create_logger_provider.return_value = mock_provider
        mock_client_class.from_config.return_value = mock_client

        result = create_otlp_processor(config)

        assert result is not None
        assert callable(result)

    @patch("provide.foundation.logger.processors.otlp.OTLPLogClient")
    def test_create_reuses_existing_provider(self, mock_client_class: Mock) -> None:
        """Test that existing logger provider is reused."""
        config = Mock()
        config.otlp_endpoint = "https://api.example.com"

        mock_provider = Mock()
        mock_provider.get_logger.return_value = Mock()
        mock_provider.resource = Mock()

        mock_client = Mock()
        mock_client.is_available.return_value = True
        mock_client.create_logger_provider.return_value = mock_provider
        mock_client_class.from_config.return_value = mock_client

        # Create first processor
        result1 = create_otlp_processor(config)
        assert result1 is not None

        # Create second processor - should reuse provider
        result2 = create_otlp_processor(config)
        assert result2 is not None

        # Should only create client once
        assert mock_client_class.from_config.call_count == 1

    @patch("provide.foundation.logger.processors.otlp.OTLPLogClient")
    def test_create_handles_exception(self, mock_client_class: Mock) -> None:
        """Test that exceptions during creation return None."""
        config = Mock()
        config.otlp_endpoint = "https://api.example.com"

        mock_client_class.from_config.side_effect = Exception("Setup failed")

        result = create_otlp_processor(config)

        assert result is None


class TestOtlpProcessor:
    """Tests for the OTLP processor function."""

    @patch("provide.foundation.logger.processors.otlp.map_level_to_severity")
    @patch("provide.foundation.logger.processors.otlp.OTLPLogClient")
    @patch("opentelemetry.sdk._logs._internal.LogRecord")
    @patch("opentelemetry.sdk._logs._internal.SeverityNumber")
    def test_processor_sends_log(
        self,
        mock_severity_class: Mock,
        mock_log_record_class: Mock,
        mock_client_class: Mock,
        mock_map_level: Mock,
    ) -> None:
        """Test that processor sends log to OTLP."""
        config = Mock()
        config.otlp_endpoint = "https://api.example.com"

        mock_logger = Mock()
        mock_provider = Mock()
        mock_provider.get_logger.return_value = mock_logger
        mock_provider.resource = Mock()

        mock_client = Mock()
        mock_client.is_available.return_value = True
        mock_client.create_logger_provider.return_value = mock_provider
        mock_client_class.from_config.return_value = mock_client

        mock_map_level.return_value = 9  # INFO level

        processor = create_otlp_processor(config)
        assert processor is not None

        # Call processor
        event_dict = {
            "event": "Test message",
            "level": "info",
            "timestamp": 1704067200.0,
            "key": "value",
        }

        result = processor(Mock(), "info", event_dict)

        # Should return event_dict unchanged
        assert result == event_dict
        # Should emit log record
        mock_logger.emit.assert_called_once()

    @patch("provide.foundation.logger.processors.otlp.OTLPLogClient")
    def test_processor_skips_if_flagged(self, mock_client_class: Mock) -> None:
        """Test that processor skips OTLP if _skip_otlp flag is set."""
        config = Mock()
        config.otlp_endpoint = "https://api.example.com"

        mock_logger = Mock()
        mock_provider = Mock()
        mock_provider.get_logger.return_value = mock_logger
        mock_provider.resource = Mock()

        mock_client = Mock()
        mock_client.is_available.return_value = True
        mock_client.create_logger_provider.return_value = mock_provider
        mock_client_class.from_config.return_value = mock_client

        processor = create_otlp_processor(config)
        assert processor is not None

        # Call processor with skip flag
        event_dict = {
            "event": "Test message",
            "level": "info",
            "_skip_otlp": True,
        }

        result = processor(Mock(), "info", event_dict)

        # Should return event_dict without _skip_otlp flag
        assert "_skip_otlp" not in result
        # Should NOT emit log
        mock_logger.emit.assert_not_called()

    @patch("provide.foundation.logger.processors.otlp.map_level_to_severity")
    @patch("provide.foundation.logger.processors.otlp.OTLPLogClient")
    @patch("opentelemetry.sdk._logs._internal.LogRecord")
    @patch("opentelemetry.sdk._logs._internal.SeverityNumber")
    def test_processor_handles_exception_silently(
        self,
        mock_severity_class: Mock,
        mock_log_record_class: Mock,
        mock_client_class: Mock,
        mock_map_level: Mock,
    ) -> None:
        """Test that processor handles exceptions without breaking logging."""
        config = Mock()
        config.otlp_endpoint = "https://api.example.com"

        mock_logger = Mock()
        mock_logger.emit.side_effect = Exception("OTLP failed")

        mock_provider = Mock()
        mock_provider.get_logger.return_value = mock_logger
        mock_provider.resource = Mock()

        mock_client = Mock()
        mock_client.is_available.return_value = True
        mock_client.create_logger_provider.return_value = mock_provider
        mock_client_class.from_config.return_value = mock_client

        mock_map_level.return_value = 9

        processor = create_otlp_processor(config)
        assert processor is not None

        # Call processor - should not raise
        event_dict = {
            "event": "Test message",
            "level": "info",
        }

        result = processor(Mock(), "info", event_dict)

        # Should return event_dict unchanged despite error
        assert result == event_dict

    @patch("provide.foundation.logger.processors.otlp.map_level_to_severity")
    @patch("provide.foundation.logger.processors.otlp.OTLPLogClient")
    @patch("opentelemetry._logs.LogRecord")
    @patch("opentelemetry._logs.SeverityNumber")
    def test_processor_builds_attributes_correctly(
        self,
        mock_severity_class: Mock,
        mock_api_log_record_class: Mock,
        mock_client_class: Mock,
        mock_map_level: Mock,
    ) -> None:
        """Test that processor correctly builds log attributes."""
        config = Mock()
        config.otlp_endpoint = "https://api.example.com"

        mock_logger = Mock()
        mock_provider = Mock()
        mock_provider.get_logger.return_value = mock_logger
        mock_provider.resource = Mock()

        mock_client = Mock()
        mock_client.is_available.return_value = True
        mock_client.create_logger_provider.return_value = mock_provider
        mock_client_class.from_config.return_value = mock_client

        mock_map_level.return_value = 9

        processor = create_otlp_processor(config)
        assert processor is not None

        # Call processor with various attributes
        event_dict = {
            "event": "Test message",
            "level": "info",
            "timestamp": 1704067200.0,
            "user_id": "123",
            "action": "login",
        }

        processor(Mock(), "info", event_dict)

        # Verify APILogRecord was created with correct attributes
        call_kwargs = mock_api_log_record_class.call_args[1]
        attributes = call_kwargs["attributes"]

        assert attributes["message"] == "Test message"
        assert attributes["level"] == "INFO"
        assert attributes["user_id"] == "123"
        assert attributes["action"] == "login"
        assert "timestamp" not in attributes  # Should be excluded
        assert "event" not in attributes  # Should be excluded


class TestFlushOtlpLogs:
    """Tests for flush_otlp_logs function."""

    def test_flush_without_provider(self) -> None:
        """Test that flush works when no provider exists."""
        # Should not raise
        flush_otlp_logs()

    def test_flush_with_provider(self) -> None:
        """Test that flush calls force_flush on provider."""
        import sys

        otlp_mod = sys.modules["provide.foundation.logger.processors.otlp"]
        mock_provider = Mock()
        otlp_mod._OTLP_LOGGER_PROVIDER = mock_provider

        flush_otlp_logs()

        mock_provider.force_flush.assert_called_once_with(timeout_millis=5000)

    def test_flush_handles_exception(self) -> None:
        """Test that flush handles exceptions silently."""
        import sys

        otlp_mod = sys.modules["provide.foundation.logger.processors.otlp"]
        mock_provider = Mock()
        mock_provider.force_flush.side_effect = Exception("Flush failed")
        otlp_mod._OTLP_LOGGER_PROVIDER = mock_provider

        # Should not raise
        flush_otlp_logs()


class TestResetOtlpProvider:
    """Tests for reset_otlp_provider function."""

    def test_reset_without_provider(self) -> None:
        """Test that reset works when no provider exists."""
        import sys

        # Should not raise
        reset_otlp_provider()

        otlp_mod = sys.modules["provide.foundation.logger.processors.otlp"]
        assert otlp_mod._OTLP_LOGGER_PROVIDER is None

    def test_reset_with_provider(self) -> None:
        """Test that reset flushes and clears provider."""
        import sys

        otlp_mod = sys.modules["provide.foundation.logger.processors.otlp"]
        mock_provider = Mock()
        otlp_mod._OTLP_LOGGER_PROVIDER = mock_provider

        reset_otlp_provider()

        # Should flush before resetting
        mock_provider.force_flush.assert_called_once()
        # Should clear provider
        assert otlp_mod._OTLP_LOGGER_PROVIDER is None

    def test_reset_handles_flush_exception(self) -> None:
        """Test that reset handles flush exceptions."""
        import sys

        otlp_mod = sys.modules["provide.foundation.logger.processors.otlp"]
        mock_provider = Mock()
        mock_provider.force_flush.side_effect = Exception("Flush failed")
        otlp_mod._OTLP_LOGGER_PROVIDER = mock_provider

        # Should not raise
        reset_otlp_provider()

        # Should still clear provider despite flush error
        assert otlp_mod._OTLP_LOGGER_PROVIDER is None


# 🧱🏗️🔚
