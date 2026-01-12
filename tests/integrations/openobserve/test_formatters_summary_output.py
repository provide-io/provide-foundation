#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for OpenObserve summary and output dispatcher formatters.

This module contains unit tests for summary formatting and the output dispatcher.
These are pure unit tests that don't require a running OpenObserve instance."""

from __future__ import annotations

from datetime import datetime

from provide.testkit import FoundationTestCase

from provide.foundation.integrations.openobserve.formatters import (
    format_output,
    format_summary,
)
from provide.foundation.integrations.openobserve.models import SearchResponse


class TestFormatSummary(FoundationTestCase):
    """Tests for format_summary function."""

    def test_format_summary_basic(self) -> None:
        """Test basic summary formatting."""
        response = SearchResponse(
            hits=[{"message": "Test"}],
            total=100,
            took=42,
            scan_size=1024000,
        )

        result = format_summary(response)

        assert "Total hits: 100" in result
        assert "Returned: 1" in result
        assert "Query time: 42ms" in result
        assert "Scan size: 1,024,000 bytes" in result

    def test_format_summary_with_trace_id(self) -> None:
        """Test summary with trace ID."""
        response = SearchResponse(
            hits=[],
            total=0,
            took=10,
            scan_size=0,
            trace_id="abc123def456",
        )

        result = format_summary(response)

        assert "Trace ID: abc123def456" in result

    def test_format_summary_partial_results(self) -> None:
        """Test summary with partial results flag."""
        response = SearchResponse(
            hits=[{"message": "Test"}],
            total=1000,
            took=100,
            scan_size=5000,
            is_partial=True,
        )

        result = format_summary(response)

        assert "partial" in result.lower()

    def test_format_summary_with_errors(self) -> None:
        """Test summary with function errors."""
        response = SearchResponse(
            hits=[],
            total=0,
            took=5,
            scan_size=0,
            function_error=["Error 1", "Error 2"],
        )

        result = format_summary(response)

        assert "Errors:" in result
        assert "Error 1" in result
        assert "Error 2" in result

    def test_format_summary_level_distribution(self) -> None:
        """Test summary includes level distribution."""
        response = SearchResponse(
            hits=[
                {"level": "INFO"},
                {"level": "INFO"},
                {"level": "ERROR"},
                {"level": "WARN"},
            ],
            total=4,
            took=10,
            scan_size=1024,
        )

        result = format_summary(response)

        assert "Level distribution:" in result
        assert "INFO: 2" in result
        assert "ERROR: 1" in result
        assert "WARN: 1" in result

    def test_format_summary_unknown_level(self) -> None:
        """Test summary handles entries without level field."""
        response = SearchResponse(
            hits=[
                {"message": "No level"},
            ],
            total=1,
            took=5,
            scan_size=512,
        )

        result = format_summary(response)

        assert "UNKNOWN: 1" in result


class TestFormatOutput(FoundationTestCase):
    """Tests for format_output dispatcher function."""

    def test_format_output_json(self) -> None:
        """Test format_output with JSON format."""
        response = SearchResponse(
            hits=[{"message": "Test"}],
            total=1,
            took=10,
            scan_size=1024,
        )

        result = format_output(response, format_type="json")

        assert '"hits"' in result
        assert '"total"' in result

    def test_format_output_log(self) -> None:
        """Test format_output with log format."""
        response = SearchResponse(
            hits=[
                {"_timestamp": 1609459200000000, "level": "INFO", "message": "Test"},
            ],
            total=1,
            took=10,
            scan_size=1024,
        )

        result = format_output(response, format_type="log")

        # Timestamp converted to local time
        dt = datetime.fromtimestamp(1609459200000000 / 1_000_000)
        expected_date = dt.strftime("%Y-%m-%d")
        assert expected_date in result
        assert "INFO" in result
        assert "Test" in result

    def test_format_output_table(self) -> None:
        """Test format_output with table format."""
        response = SearchResponse(
            hits=[{"level": "INFO", "message": "Test"}],
            total=1,
            took=10,
            scan_size=1024,
        )

        result = format_output(response, format_type="table")

        assert "level" in result or "level" in result.lower()
        assert "message" in result or "message" in result.lower()

    def test_format_output_csv(self) -> None:
        """Test format_output with CSV format."""
        response = SearchResponse(
            hits=[{"level": "INFO", "message": "Test"}],
            total=1,
            took=10,
            scan_size=1024,
        )

        result = format_output(response, format_type="csv")

        assert "level" in result
        assert "message" in result
        assert "INFO" in result

    def test_format_output_summary(self) -> None:
        """Test format_output with summary format."""
        response = SearchResponse(
            hits=[{"message": "Test"}],
            total=100,
            took=42,
            scan_size=1024,
        )

        result = format_output(response, format_type="summary")

        assert "Total hits: 100" in result
        assert "Query time: 42ms" in result

    def test_format_output_unknown_format(self) -> None:
        """Test format_output with unknown format defaults to log."""
        response = SearchResponse(
            hits=[
                {"_timestamp": 1609459200000000, "level": "INFO", "message": "Test"},
            ],
            total=1,
            took=10,
            scan_size=1024,
        )

        result = format_output(response, format_type="unknown")

        # Should default to log format (timestamp converted to local time)
        dt = datetime.fromtimestamp(1609459200000000 / 1_000_000)
        expected_date = dt.strftime("%Y-%m-%d")
        assert expected_date in result
        assert "INFO" in result

    def test_format_output_case_insensitive(self) -> None:
        """Test format_output handles case-insensitive format types."""
        response = SearchResponse(
            hits=[{"message": "Test"}],
            total=1,
            took=10,
            scan_size=1024,
        )

        result1 = format_output(response, format_type="JSON")
        result2 = format_output(response, format_type="Json")
        result3 = format_output(response, format_type="json")

        # All should produce JSON output
        assert '"hits"' in result1
        assert '"hits"' in result2
        assert '"hits"' in result3

    def test_format_output_dict_json(self) -> None:
        """Test format_output with dict input and JSON format."""
        entry = {"message": "Test", "level": "INFO"}

        result = format_output(entry, format_type="json")

        assert '"message": "Test"' in result
        assert '"level": "INFO"' in result

    def test_format_output_dict_log(self) -> None:
        """Test format_output with dict input and log format."""
        entry = {
            "_timestamp": 1609459200000000,
            "level": "ERROR",
            "message": "Error occurred",
        }

        result = format_output(entry, format_type="log")

        # Timestamp converted to local time
        dt = datetime.fromtimestamp(1609459200000000 / 1_000_000)
        expected_date = dt.strftime("%Y-%m-%d")
        assert expected_date in result
        assert "ERROR" in result
        assert "Error occurred" in result

    def test_format_output_dict_table(self) -> None:
        """Test format_output with dict input and table format."""
        entry = {"level": "INFO", "message": "Test"}

        result = format_output(entry, format_type="table")

        # Should create single-entry table
        assert "level" in result or "level" in result.lower()
        assert "message" in result or "message" in result.lower()

    def test_format_output_dict_csv(self) -> None:
        """Test format_output with dict input and CSV format."""
        entry = {"level": "INFO", "message": "Test"}

        result = format_output(entry, format_type="csv")

        lines = result.strip().split("\n")
        # Header + 1 data row
        assert len(lines) == 2
        assert "level" in lines[0]
        assert "INFO" in result

    def test_format_output_dict_summary(self) -> None:
        """Test format_output with dict input and summary format."""
        entry = {"message": "Test"}

        result = format_output(entry, format_type="summary")

        # Should indicate it's a single entry
        assert "Single log entry" in result

    def test_format_output_with_kwargs(self) -> None:
        """Test format_output passes kwargs to formatters."""
        response = SearchResponse(
            hits=[{"message": "Test"}],
            total=1,
            took=10,
            scan_size=1024,
        )

        # Test JSON with pretty=False
        result = format_output(response, format_type="json", pretty=False)

        # Should be compact JSON
        assert "\n" not in result


__all__ = [
    "TestFormatOutput",
    "TestFormatSummary",
]

# 🧱🏗️🔚
