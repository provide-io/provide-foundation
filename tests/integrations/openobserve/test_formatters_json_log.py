#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for OpenObserve JSON and log formatters.

This module contains unit tests for JSON and log line formatting.
These are pure unit tests that don't require a running OpenObserve instance."""

from __future__ import annotations

from datetime import datetime

from provide.testkit import FoundationTestCase

from provide.foundation.integrations.openobserve.formatters import (
    format_json,
    format_log_line,
)
from provide.foundation.integrations.openobserve.models import SearchResponse


class TestFormatJson(FoundationTestCase):
    """Tests for format_json function."""

    def test_format_json_search_response_pretty(self) -> None:
        """Test JSON formatting of SearchResponse with pretty printing."""
        response = SearchResponse(
            hits=[{"message": "test", "level": "INFO"}],
            total=1,
            took=10,
            scan_size=1024,
        )

        result = format_json(response, pretty=True)

        assert '"hits"' in result
        assert '"total": 1' in result
        assert '"took": 10' in result
        assert '"scan_size": 1024' in result
        # Pretty print should have indentation
        assert "\n" in result
        assert "  " in result

    def test_format_json_search_response_compact(self) -> None:
        """Test JSON formatting of SearchResponse without pretty printing."""
        response = SearchResponse(
            hits=[{"message": "test"}],
            total=1,
            took=5,
            scan_size=512,
        )

        result = format_json(response, pretty=False)

        assert '"hits"' in result
        assert '"total": 1' in result  # Python's json.dumps includes space after colon
        # Compact format should not have extra whitespace (no indentation)
        assert "\n" not in result

    def test_format_json_dict(self) -> None:
        """Test JSON formatting of plain dict."""
        data = {"message": "test", "level": "ERROR", "timestamp": 12345}

        result = format_json(data, pretty=True)

        assert '"message": "test"' in result
        assert '"level": "ERROR"' in result
        assert '"timestamp": 12345' in result

    def test_format_json_empty_response(self) -> None:
        """Test JSON formatting of empty SearchResponse."""
        response = SearchResponse(
            hits=[],
            total=0,
            took=0,
            scan_size=0,
        )

        result = format_json(response, pretty=True)

        assert '"hits": []' in result
        assert '"total": 0' in result


class TestFormatLogLine(FoundationTestCase):
    """Tests for format_log_line function."""

    def test_format_log_line_complete(self) -> None:
        """Test formatting log line with all fields."""
        entry = {
            "_timestamp": 1609459200000000,  # 2021-01-01 00:00:00 UTC
            "level": "INFO",
            "message": "Test message",
            "service": "test-service",
        }

        result = format_log_line(entry)

        # Timestamp will be converted to local time
        dt = datetime.fromtimestamp(1609459200000000 / 1_000_000)
        expected_date = dt.strftime("%Y-%m-%d")
        assert expected_date in result
        assert "[INFO ]" in result
        assert "Test message" in result
        assert "[test-service]" in result

    def test_format_log_line_minimal(self) -> None:
        """Test formatting log line with minimal fields."""
        entry = {"message": "Simple message"}

        result = format_log_line(entry)

        assert "unknown" in result  # No timestamp
        assert "[INFO ]" in result  # Default level
        assert "Simple message" in result

    def test_format_log_line_with_extra_fields(self) -> None:
        """Test formatting log line with extra fields."""
        entry = {
            "_timestamp": 1609459200000000,
            "level": "ERROR",
            "message": "Error occurred",
            "error_code": 500,
            "user_id": "123",
        }

        result = format_log_line(entry)

        assert "ERROR" in result
        assert "Error occurred" in result
        # Extra fields should appear as key=value
        assert "error_code=500" in result
        assert "user_id=123" in result

    def test_format_log_line_excludes_internal_fields(self) -> None:
        """Test that internal fields are excluded from extra fields."""
        entry = {
            "_timestamp": 1609459200000000,
            "level": "INFO",
            "message": "Test",
            "_p": "internal",
            "custom": "value",
        }

        result = format_log_line(entry)

        # _p should be excluded
        assert "_p" not in result
        # Custom field should be included
        assert "custom=value" in result

    def test_format_log_line_timestamp_formatting(self) -> None:
        """Test timestamp formatting with microseconds."""
        timestamp = 1609459200123456  # Microseconds precision
        entry = {
            "_timestamp": timestamp,
            "message": "Test",
        }

        result = format_log_line(entry)

        # Should format with milliseconds precision (converted to local time)
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        expected_time = dt.strftime("%H:%M:%S.%f")[:-3]
        assert expected_time in result


__all__ = [
    "TestFormatJson",
    "TestFormatLogLine",
]

# 🧱🏗️🔚
