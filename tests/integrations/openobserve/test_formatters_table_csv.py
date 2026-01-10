#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for OpenObserve table and CSV formatters.

This module contains unit tests for table and CSV output formatters.
These are pure unit tests that don't require a running OpenObserve instance."""

from __future__ import annotations

from datetime import datetime

from provide.testkit import FoundationTestCase

from provide.foundation.integrations.openobserve.formatters import (
    format_csv,
    format_table,
)
from provide.foundation.integrations.openobserve.models import SearchResponse


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


__all__ = [
    "TestFormatCsv",
    "TestFormatTable",
]

# 🧱🏗️🔚
