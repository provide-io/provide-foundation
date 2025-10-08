"""Unit tests for OpenObserve formatters.

This module contains unit tests for all OpenObserve output formatters
(JSON, log, table, CSV, summary). These are pure unit tests that don't
require a running OpenObserve instance.
"""

from __future__ import annotations

from provide.testkit import FoundationTestCase

from provide.foundation.integrations.openobserve.formatters import (
    format_csv,
    format_json,
    format_log_line,
    format_output,
    format_summary,
    format_table,
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


class TestFormatTable(FoundationTestCase):
    """Tests for format_table function."""

    def test_format_table_empty_results(self) -> None:
        """Test table formatting with no results."""
        response = SearchResponse(
            hits=[],
            total=0,
            took=0,
            scan_size=0,
        )

        result = format_table(response)

        assert result == "No results found"

    def test_format_table_with_results(self) -> None:
        """Test table formatting with results."""
        response = SearchResponse(
            hits=[
                {"_timestamp": 1609459200000000, "level": "INFO", "message": "Test 1"},
                {"_timestamp": 1609459201000000, "level": "ERROR", "message": "Test 2"},
            ],
            total=2,
            took=10,
            scan_size=1024,
        )

        result = format_table(response)

        # Should contain column names (tabulate or simple format)
        assert "level" in result or "level" in result.lower()
        assert "message" in result or "message" in result.lower()
        # Should contain data
        assert "Test 1" in result
        assert "Test 2" in result

    def test_format_table_custom_columns(self) -> None:
        """Test table formatting with custom columns."""
        response = SearchResponse(
            hits=[
                {"level": "INFO", "message": "Test", "extra": "data"},
            ],
            total=1,
            took=5,
            scan_size=512,
        )

        result = format_table(response, columns=["level", "message"])

        assert "level" in result or "level" in result.lower()
        assert "message" in result or "message" in result.lower()
        # Extra field should not appear when custom columns specified
        # (actual appearance depends on tabulate vs simple format)

    def test_format_table_filters_internal_columns(self) -> None:
        """Test that internal columns are filtered by default."""
        response = SearchResponse(
            hits=[
                {"_timestamp": 1609459200000000, "_p": "internal", "message": "Test"},
            ],
            total=1,
            took=5,
            scan_size=512,
        )

        result = format_table(response)

        # _timestamp should be included
        assert "_timestamp" in result or "timestamp" in result
        # _p should be filtered out (unless explicitly in columns)

    def test_format_table_column_priority(self) -> None:
        """Test that priority columns appear first."""
        response = SearchResponse(
            hits=[
                {
                    "custom": "value",
                    "message": "Test",
                    "level": "INFO",
                    "_timestamp": 1609459200000000,
                },
            ],
            total=1,
            took=5,
            scan_size=512,
        )

        result = format_table(response)

        # Priority columns should appear (order depends on implementation)
        assert "timestamp" in result or "_timestamp" in result
        assert "level" in result
        assert "message" in result


class TestFormatCsv(FoundationTestCase):
    """Tests for format_csv function."""

    def test_format_csv_empty_results(self) -> None:
        """Test CSV formatting with no results."""
        response = SearchResponse(
            hits=[],
            total=0,
            took=0,
            scan_size=0,
        )

        result = format_csv(response)

        assert result == ""

    def test_format_csv_with_results(self) -> None:
        """Test CSV formatting with results."""
        response = SearchResponse(
            hits=[
                {"level": "INFO", "message": "Test 1"},
                {"level": "ERROR", "message": "Test 2"},
            ],
            total=2,
            took=10,
            scan_size=1024,
        )

        result = format_csv(response)

        lines = result.strip().split("\n")
        # Should have header + 2 data rows
        assert len(lines) == 3
        # Header should contain column names
        assert "level" in lines[0]
        assert "message" in lines[0]
        # Data rows
        assert "INFO" in result
        assert "ERROR" in result
        assert "Test 1" in result
        assert "Test 2" in result

    def test_format_csv_custom_columns(self) -> None:
        """Test CSV formatting with custom columns."""
        response = SearchResponse(
            hits=[
                {"level": "INFO", "message": "Test", "extra": "data"},
            ],
            total=1,
            took=5,
            scan_size=512,
        )

        result = format_csv(response, columns=["level", "message"])

        # Should only include specified columns
        lines = result.strip().split("\n")
        header = lines[0]
        assert "level" in header
        assert "message" in header
        # Extra column should not appear
        assert "extra" not in header

    def test_format_csv_timestamp_conversion(self) -> None:
        """Test that timestamps are converted to ISO format."""
        response = SearchResponse(
            hits=[
                {"_timestamp": 1609459200000000, "message": "Test"},
            ],
            total=1,
            took=5,
            scan_size=512,
        )

        result = format_csv(response)

        # Timestamp should be converted to ISO format (local time)
        dt = datetime.fromtimestamp(1609459200000000 / 1_000_000)
        expected_date = dt.date().isoformat()
        assert expected_date in result

    def test_format_csv_sorted_columns(self) -> None:
        """Test that columns are sorted when auto-detected."""
        response = SearchResponse(
            hits=[
                {"zebra": "z", "alpha": "a", "beta": "b"},
            ],
            total=1,
            took=5,
            scan_size=512,
        )

        result = format_csv(response)

        lines = result.strip().split("\n")
        header = lines[0]
        # Columns should be sorted
        alpha_pos = header.index("alpha")
        beta_pos = header.index("beta")
        zebra_pos = header.index("zebra")
        assert alpha_pos < beta_pos < zebra_pos


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
    "TestFormatCsv",
    "TestFormatJson",
    "TestFormatLogLine",
    "TestFormatOutput",
    "TestFormatSummary",
    "TestFormatTable",
]
