#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for utils/formatting.py module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase

from provide.foundation.utils.formatting import (
    format_duration,
    format_number,
    format_percentage,
    format_size,
)


class TestFormatSize(FoundationTestCase):
    """Test format_size function."""

    def test_format_size_zero(self) -> None:
        """Test formatting zero bytes."""
        assert format_size(0) == "0 B"

    def test_format_size_bytes(self) -> None:
        """Test formatting bytes."""
        assert format_size(512) == "512 B"
        assert format_size(1023) == "1023 B"

    def test_format_size_kilobytes(self) -> None:
        """Test formatting kilobytes."""
        assert format_size(1024) == "1.0 KB"
        assert format_size(1536) == "1.5 KB"
        assert format_size(2048) == "2.0 KB"

    def test_format_size_megabytes(self) -> None:
        """Test formatting megabytes."""
        assert format_size(1024 * 1024) == "1.0 MB"
        assert format_size(1.5 * 1024 * 1024) == "1.5 MB"

    def test_format_size_gigabytes(self) -> None:
        """Test formatting gigabytes."""
        assert format_size(1073741824) == "1.0 GB"  # 1024^3
        assert format_size(2 * 1024 * 1024 * 1024) == "2.0 GB"

    def test_format_size_terabytes(self) -> None:
        """Test formatting terabytes."""
        tb = 1024 * 1024 * 1024 * 1024
        assert format_size(tb) == "1.0 TB"
        assert format_size(2.5 * tb) == "2.5 TB"

    def test_format_size_petabytes(self) -> None:
        """Test formatting petabytes."""
        pb = 1024**5
        assert format_size(pb) == "1.0 PB"

    def test_format_size_exabytes(self) -> None:
        """Test formatting exabytes."""
        eb = 1024**6
        assert format_size(eb) == "1.0 EB"

    def test_format_size_precision(self) -> None:
        """Test different precision levels."""
        assert format_size(1536, precision=0) == "2 KB"
        assert format_size(1536, precision=1) == "1.5 KB"
        assert format_size(1536, precision=2) == "1.50 KB"
        assert format_size(1234567, precision=3) == "1.177 MB"

    def test_format_size_negative(self) -> None:
        """Test formatting negative sizes."""
        assert format_size(-1024) == "-1.0 KB"
        assert format_size(-512) == "-512 B"
        assert format_size(-1536) == "-1.5 KB"

    def test_format_size_float_bytes(self) -> None:
        """Test formatting float values that remain in bytes."""
        assert format_size(512.7) == "512 B"
        assert format_size(999.9) == "999 B"

    def test_format_size_very_large(self) -> None:
        """Test formatting very large values (beyond exabytes)."""
        huge = 1024**7  # Larger than exabytes
        result = format_size(huge)
        assert result.endswith(" EB")  # Should cap at EB


class TestFormatDuration(FoundationTestCase):
    """Test format_duration function."""

    def test_format_duration_zero(self) -> None:
        """Test formatting zero duration."""
        assert format_duration(0) == "0 seconds"
        assert format_duration(0, short=True) == "0s"

    def test_format_duration_seconds_only(self) -> None:
        """Test formatting seconds only."""
        assert format_duration(30) == "30 seconds"
        assert format_duration(30, short=True) == "30s"
        assert format_duration(1) == "1 second"
        assert format_duration(1, short=True) == "1s"

    def test_format_duration_minutes_seconds(self) -> None:
        """Test formatting minutes and seconds."""
        assert format_duration(90) == "1 minute 30 seconds"
        assert format_duration(90, short=True) == "1m30s"
        assert format_duration(120) == "2 minutes"
        assert format_duration(120, short=True) == "2m"
        assert format_duration(61) == "1 minute 1 second"
        assert format_duration(61, short=True) == "1m1s"

    def test_format_duration_hours_minutes_seconds(self) -> None:
        """Test formatting hours, minutes, and seconds."""
        assert format_duration(3661) == "1 hour 1 minute 1 second"
        assert format_duration(3661, short=True) == "1h1m1s"
        assert format_duration(3600) == "1 hour"
        assert format_duration(3600, short=True) == "1h"
        assert format_duration(7200) == "2 hours"
        assert format_duration(7200, short=True) == "2h"

    def test_format_duration_days(self) -> None:
        """Test formatting with days."""
        assert format_duration(86400) == "1 day"
        assert format_duration(86400, short=True) == "1d"
        assert format_duration(172800) == "2 days"
        assert format_duration(172800, short=True) == "2d"
        assert format_duration(90061) == "1 day 1 hour 1 minute 1 second"
        assert format_duration(90061, short=True) == "1d1h1m1s"

    def test_format_duration_negative(self) -> None:
        """Test formatting negative durations."""
        assert format_duration(-30) == "-30 seconds"
        assert format_duration(-30, short=True) == "-30s"
        assert format_duration(-90) == "-1 minute 30 seconds"
        assert format_duration(-90, short=True) == "-1m30s"

    def test_format_duration_only_minutes(self) -> None:
        """Test formatting only minutes (no seconds)."""
        assert format_duration(180) == "3 minutes"
        assert format_duration(180, short=True) == "3m"

    def test_format_duration_only_hours(self) -> None:
        """Test formatting only hours (no minutes/seconds)."""
        assert format_duration(7200) == "2 hours"
        assert format_duration(7200, short=True) == "2h"

    def test_format_duration_partial_components(self) -> None:
        """Test various partial component combinations."""
        assert format_duration(3720) == "1 hour 2 minutes"  # 1h 2m 0s
        assert format_duration(3720, short=True) == "1h2m"


class TestFormatNumber(FoundationTestCase):
    """Test format_number function."""

    def test_format_number_integers(self) -> None:
        """Test formatting integers."""
        assert format_number(1234) == "1,234"
        assert format_number(1234567) == "1,234,567"
        assert format_number(123) == "123"

    def test_format_number_floats_auto_precision(self) -> None:
        """Test formatting floats with automatic precision."""
        assert format_number(1234.5) == "1,234.5"
        assert format_number(1234.567890) == "1,234.56789"
        assert format_number(1234.0) == "1,234"
        assert format_number(1234.100000) == "1,234.1"

    def test_format_number_explicit_precision(self) -> None:
        """Test formatting with explicit precision."""
        assert format_number(1234.5678, precision=2) == "1,234.57"
        assert format_number(1234.5, precision=0) == "1,234"
        assert format_number(1234, precision=2) == "1,234.00"

    def test_format_number_negative(self) -> None:
        """Test formatting negative numbers."""
        assert format_number(-1234) == "-1,234"
        assert format_number(-1234.56, precision=1) == "-1,234.6"

    def test_format_number_zero(self) -> None:
        """Test formatting zero."""
        assert format_number(0) == "0"
        assert format_number(0.0) == "0"
        assert format_number(0, precision=2) == "0.00"

    def test_format_number_small_numbers(self) -> None:
        """Test formatting small numbers."""
        assert format_number(12) == "12"
        assert format_number(123) == "123"

    def test_format_number_precision_edge_cases(self) -> None:
        """Test precision edge cases."""
        assert format_number(1234.999, precision=0) == "1,235"
        assert format_number(1234.001, precision=2) == "1,234.00"


class TestFormatPercentage(FoundationTestCase):
    """Test format_percentage function."""

    def test_format_percentage_basic(self) -> None:
        """Test basic percentage formatting."""
        assert format_percentage(0.5) == "50.0%"
        assert format_percentage(0.1234) == "12.3%"
        assert format_percentage(1.0) == "100.0%"

    def test_format_percentage_precision(self) -> None:
        """Test percentage formatting with different precision."""
        assert format_percentage(0.1234, precision=0) == "12%"
        assert format_percentage(0.1234, precision=2) == "12.34%"
        assert format_percentage(0.1234, precision=3) == "12.340%"

    def test_format_percentage_with_sign(self) -> None:
        """Test percentage formatting with sign included."""
        assert format_percentage(0.05, include_sign=True) == "+5.0%"
        assert format_percentage(-0.05, include_sign=True) == "-5.0%"
        assert format_percentage(0.0, include_sign=True) == "0.0%"

    def test_format_percentage_zero(self) -> None:
        """Test formatting zero percentage."""
        assert format_percentage(0.0) == "0.0%"
        assert format_percentage(0.0, include_sign=True) == "0.0%"

    def test_format_percentage_negative(self) -> None:
        """Test formatting negative percentages."""
        assert format_percentage(-0.25) == "-25.0%"
        assert format_percentage(-0.1, precision=0) == "-10%"

    def test_format_percentage_large_values(self) -> None:
        """Test formatting large percentage values."""
        assert format_percentage(2.5) == "250.0%"
        assert format_percentage(10.0) == "1000.0%"

    def test_format_percentage_small_values(self) -> None:
        """Test formatting very small percentage values."""
        assert format_percentage(0.001, precision=3) == "0.100%"
        assert format_percentage(0.0001, precision=4) == "0.0100%"


class TestFormattingEdgeCases:
    """Test edge cases and integration scenarios."""

    def test_all_functions_handle_zero(self) -> None:
        """Test that all functions handle zero appropriately."""
        assert format_size(0) == "0 B"
        assert format_duration(0) == "0 seconds"
        assert format_number(0) == "0"
        assert format_percentage(0.0) == "0.0%"

    def test_all_functions_handle_negative(self) -> None:
        """Test that all functions handle negative values."""
        assert format_size(-1024).startswith("-")
        assert format_duration(-30).startswith("-")
        assert format_number(-1234).startswith("-")
        assert format_percentage(-0.1).startswith("-")

    def test_formatting_consistency(self) -> None:
        """Test formatting consistency across different inputs."""
        # Test that precision is respected consistently
        assert "1.5" in format_size(1536, precision=1)
        assert "12.3" in format_percentage(0.1234, precision=1)
        assert "1,234.5" in format_number(1234.5, precision=1)

    def test_module_exports(self) -> None:
        """Test that all expected functions are exported."""
        from provide.foundation.utils.formatting import __all__

        expected = ["format_duration", "format_number", "format_percentage", "format_size"]
        assert set(__all__) == set(expected)


# Test internal helper functions for completeness
class TestInternalHelpers:
    """Test internal helper functions."""

    def test_format_duration_components(self) -> None:
        """Test _format_duration_components function."""
        from provide.foundation.utils.formatting import _format_duration_components

        result = _format_duration_components(1, 2, 3, 4)
        assert result == (1, 2, 3, 4)

    def test_format_duration_short(self) -> None:
        """Test _format_duration_short function."""
        from provide.foundation.utils.formatting import _format_duration_short

        assert _format_duration_short(1, 2, 3, 4) == "1d2h3m4s"
        assert _format_duration_short(0, 0, 0, 5) == "5s"
        assert _format_duration_short(0, 0, 0, 0) == "0s"
        assert _format_duration_short(1, 0, 0, 0) == "1d"

    def test_format_duration_long(self) -> None:
        """Test _format_duration_long function."""
        from provide.foundation.utils.formatting import _format_duration_long

        assert _format_duration_long(1, 1, 1, 1) == "1 day 1 hour 1 minute 1 second"
        assert _format_duration_long(2, 2, 2, 2) == "2 days 2 hours 2 minutes 2 seconds"
        assert _format_duration_long(0, 0, 0, 5) == "5 seconds"
        assert _format_duration_long(0, 0, 0, 0) == "0 seconds"
        assert _format_duration_long(1, 0, 0, 0) == "1 day"


# 🧱🏗️🔚
