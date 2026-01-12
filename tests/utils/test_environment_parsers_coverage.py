#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for utils/environment/parsers.py module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.errors.config import ValidationError
from provide.foundation.utils.environment.parsers import parse_duration, parse_size


class TestParseDuration(FoundationTestCase):
    """Test parse_duration function."""

    def test_parse_duration_plain_seconds(self) -> None:
        """Test parsing plain numeric seconds."""
        assert parse_duration("30") == 30
        assert parse_duration("0") == 0
        assert parse_duration("123") == 123

    def test_parse_duration_seconds_unit(self) -> None:
        """Test parsing durations with seconds unit."""
        assert parse_duration("30s") == 30
        assert parse_duration("0s") == 0
        assert parse_duration("1s") == 1
        assert parse_duration("999s") == 999

    def test_parse_duration_minutes_unit(self) -> None:
        """Test parsing durations with minutes unit."""
        assert parse_duration("1m") == 60
        assert parse_duration("5m") == 300
        assert parse_duration("60m") == 3600

    def test_parse_duration_hours_unit(self) -> None:
        """Test parsing durations with hours unit."""
        assert parse_duration("1h") == 3600
        assert parse_duration("2h") == 7200
        assert parse_duration("24h") == 86400

    def test_parse_duration_days_unit(self) -> None:
        """Test parsing durations with days unit."""
        assert parse_duration("1d") == 86400
        assert parse_duration("2d") == 172800
        assert parse_duration("7d") == 604800

    def test_parse_duration_combined_units(self) -> None:
        """Test parsing combined duration units."""
        # 1 hour 30 minutes = 3600 + 1800 = 5400
        assert parse_duration("1h30m") == 5400

        # 2 days 5 hours 30 minutes = 172800 + 18000 + 1800 = 192600
        assert parse_duration("2d5h30m") == 192600

        # 1 day 1 hour 1 minute 1 second = 86400 + 3600 + 60 + 1 = 90061
        assert parse_duration("1d1h1m1s") == 90061

    def test_parse_duration_case_insensitive(self) -> None:
        """Test that duration parsing is case insensitive."""
        assert parse_duration("30S") == 30
        assert parse_duration("5M") == 300
        assert parse_duration("2H") == 7200
        assert parse_duration("1D") == 86400
        assert parse_duration("1H30M") == 5400

    def test_parse_duration_mixed_case(self) -> None:
        """Test parsing with mixed case."""
        assert parse_duration("1H30m") == 5400
        assert parse_duration("2D5h") == 190800  # 2*86400 + 5*3600 = 172800 + 18000
        assert parse_duration("5m30S") == 330

    def test_parse_duration_with_spaces(self) -> None:
        """Test parsing durations with spaces (should fail)."""
        # The current implementation doesn't handle spaces
        with pytest.raises(ValidationError, match="Invalid duration format"):
            parse_duration("1 h")

        with pytest.raises(ValidationError, match="Invalid duration format"):
            parse_duration("30 s")

    def test_parse_duration_invalid_format(self) -> None:
        """Test parsing invalid duration formats."""
        with pytest.raises(ValidationError) as exc_info:
            parse_duration("invalid")

        error = exc_info.value
        assert error.context["validation.value"] == "invalid"
        assert error.context["validation.rule"] == "duration"
        assert "Invalid duration format" in str(error)

    def test_parse_duration_empty_string(self) -> None:
        """Test parsing empty string."""
        with pytest.raises(ValidationError, match="Invalid duration format"):
            parse_duration("")

    def test_parse_duration_invalid_unit(self) -> None:
        """Test parsing with invalid unit."""
        with pytest.raises(ValidationError) as exc_info:
            parse_duration("30x")

        error = exc_info.value
        assert error.context["validation.value"] == "30x"
        assert error.context["validation.rule"] == "duration"
        assert "Invalid duration format" in str(error)

    def test_parse_duration_no_numeric_value(self) -> None:
        """Test parsing with no numeric value."""
        with pytest.raises(ValidationError, match="Invalid duration format"):
            parse_duration("s")

        with pytest.raises(ValidationError, match="Invalid duration format"):
            parse_duration("m")

    def test_parse_duration_zero_values(self) -> None:
        """Test parsing with zero values."""
        assert parse_duration("0s") == 0
        assert parse_duration("0m") == 0
        assert parse_duration("0h") == 0
        assert parse_duration("0d") == 0
        assert parse_duration("0h0m0s") == 0

    def test_parse_duration_large_values(self) -> None:
        """Test parsing large duration values."""
        assert parse_duration("365d") == 31536000  # 1 year in seconds
        assert parse_duration("1000h") == 3600000
        assert parse_duration("999999s") == 999999

    def test_parse_duration_repeated_units(self) -> None:
        """Test parsing with repeated units."""
        # Multiple same units should be additive
        assert parse_duration("1h1h") == 7200  # 2 hours
        assert parse_duration("30m30m") == 3600  # 1 hour
        assert parse_duration("1d1d") == 172800  # 2 days


class TestParseSize(FoundationTestCase):
    """Test parse_size function."""

    def test_parse_size_plain_bytes(self) -> None:
        """Test parsing plain numeric bytes."""
        assert parse_size("1024") == 1024
        assert parse_size("0") == 0
        assert parse_size("512") == 512

    def test_parse_size_bytes_unit(self) -> None:
        """Test parsing with explicit bytes unit."""
        assert parse_size("1024B") == 1024
        assert parse_size("512B") == 512
        assert parse_size("0B") == 0

    def test_parse_size_kilobytes(self) -> None:
        """Test parsing kilobytes."""
        assert parse_size("1KB") == 1024
        assert parse_size("2KB") == 2048
        assert parse_size("1K") == 1024
        assert parse_size("2K") == 2048

    def test_parse_size_megabytes(self) -> None:
        """Test parsing megabytes."""
        assert parse_size("1MB") == 1024 * 1024
        assert parse_size("2MB") == 2 * 1024 * 1024
        assert parse_size("1M") == 1024 * 1024
        assert parse_size("10M") == 10 * 1024 * 1024

    def test_parse_size_gigabytes(self) -> None:
        """Test parsing gigabytes."""
        assert parse_size("1GB") == 1024 * 1024 * 1024
        assert parse_size("2GB") == 2 * 1024 * 1024 * 1024
        assert parse_size("1G") == 1024 * 1024 * 1024

    def test_parse_size_terabytes(self) -> None:
        """Test parsing terabytes."""
        assert parse_size("1TB") == 1024 * 1024 * 1024 * 1024
        assert parse_size("1T") == 1024 * 1024 * 1024 * 1024

    def test_parse_size_decimal_values(self) -> None:
        """Test parsing decimal size values."""
        assert parse_size("1.5KB") == int(1.5 * 1024)
        assert parse_size("2.5MB") == int(2.5 * 1024 * 1024)
        assert parse_size("0.5GB") == int(0.5 * 1024 * 1024 * 1024)

    def test_parse_size_case_insensitive(self) -> None:
        """Test that size parsing is case insensitive."""
        assert parse_size("1kb") == 1024
        assert parse_size("1mb") == 1024 * 1024
        assert parse_size("1gb") == 1024 * 1024 * 1024
        assert parse_size("1tb") == 1024 * 1024 * 1024 * 1024

    def test_parse_size_mixed_case(self) -> None:
        """Test parsing with mixed case."""
        assert parse_size("1Kb") == 1024
        assert parse_size("1mB") == 1024 * 1024
        assert parse_size("1Gb") == 1024 * 1024 * 1024

    def test_parse_size_with_spaces(self) -> None:
        """Test parsing sizes with spaces."""
        assert parse_size("1 KB") == 1024
        assert parse_size("10 MB") == 10 * 1024 * 1024
        assert parse_size("1.5 GB") == int(1.5 * 1024 * 1024 * 1024)

    def test_parse_size_invalid_format(self) -> None:
        """Test parsing invalid size formats."""
        with pytest.raises(ValidationError) as exc_info:
            parse_size("invalid")

        error = exc_info.value
        assert error.context["validation.value"] == "invalid"
        assert error.context["validation.rule"] == "size"
        assert "Invalid size format" in str(error)

    def test_parse_size_empty_string(self) -> None:
        """Test parsing empty string."""
        with pytest.raises(ValidationError, match="Invalid size format"):
            parse_size("")

    def test_parse_size_invalid_unit(self) -> None:
        """Test parsing with invalid unit."""
        with pytest.raises(ValidationError) as exc_info:
            parse_size("100XB")

        error = exc_info.value
        assert error.context["validation.value"] == "100XB"
        assert error.context["validation.rule"] == "size"
        assert "Invalid size format" in str(error)

    def test_parse_size_no_numeric_value(self) -> None:
        """Test parsing with no numeric value."""
        with pytest.raises(ValidationError, match="Invalid size format"):
            parse_size("KB")

        with pytest.raises(ValidationError, match="Invalid size format"):
            parse_size("MB")

    def test_parse_size_zero_values(self) -> None:
        """Test parsing with zero values."""
        assert parse_size("0KB") == 0
        assert parse_size("0MB") == 0
        assert parse_size("0GB") == 0
        assert parse_size("0TB") == 0

    def test_parse_size_large_values(self) -> None:
        """Test parsing large size values."""
        assert parse_size("1000TB") == 1000 * 1024 * 1024 * 1024 * 1024
        assert parse_size("999GB") == 999 * 1024 * 1024 * 1024

    def test_parse_size_edge_case_units(self) -> None:
        """Test edge cases for size units."""
        # Test units without 'B' suffix
        assert parse_size("1K") == 1024
        assert parse_size("1M") == 1024 * 1024
        assert parse_size("1G") == 1024 * 1024 * 1024
        assert parse_size("1T") == 1024 * 1024 * 1024 * 1024

    def test_parse_size_fractional_bytes(self) -> None:
        """Test parsing fractional bytes (should be converted to int)."""
        # 1.5KB = 1536 bytes
        assert parse_size("1.5KB") == 1536
        # 2.7MB
        assert parse_size("2.7MB") == int(2.7 * 1024 * 1024)

    def test_parse_size_validation_error_details(self) -> None:
        """Test that ValidationError contains proper details."""
        with pytest.raises(ValidationError) as exc_info:
            parse_size("invalid_size")

        error = exc_info.value
        assert hasattr(error, "context")
        assert "validation.value" in error.context
        assert "validation.rule" in error.context
        assert error.context["validation.value"] == "invalid_size"
        assert error.context["validation.rule"] == "size"


class TestParseDurationValidationErrorDetails(FoundationTestCase):
    """Test ValidationError details for parse_duration."""

    def test_parse_duration_validation_error_has_context(self) -> None:
        """Test that ValidationError has proper context."""
        with pytest.raises(ValidationError) as exc_info:
            parse_duration("invalid_duration")

        error = exc_info.value
        assert hasattr(error, "context")
        assert "validation.value" in error.context
        assert "validation.rule" in error.context
        assert error.context["validation.value"] == "invalid_duration"
        assert error.context["validation.rule"] == "duration"

    def test_parse_duration_unit_error_has_context(self) -> None:
        """Test ValidationError for invalid units has proper context."""
        with pytest.raises(ValidationError) as exc_info:
            parse_duration("30z")

        error = exc_info.value
        assert error.context["validation.value"] == "30z"
        assert error.context["validation.rule"] == "duration"


class TestModuleIntegration(FoundationTestCase):
    """Test module-level integration scenarios."""

    def test_all_functions_importable(self) -> None:
        """Test that all public functions are importable."""
        from provide.foundation.utils.environment.parsers import parse_duration, parse_size

        assert callable(parse_duration)
        assert callable(parse_size)

    def test_functions_work_together(self) -> None:
        """Test that functions can be used together."""
        # Test that both functions work independently
        duration = parse_duration("1h30m")
        size = parse_size("10MB")

        assert duration == 5400  # 1.5 hours in seconds
        assert size == 10485760  # 10MB in bytes

    def test_error_handling_consistency(self) -> None:
        """Test that error handling is consistent across functions."""
        # Both should raise ValidationError for invalid input
        with pytest.raises(ValidationError):
            parse_duration("invalid")

        with pytest.raises(ValidationError):
            parse_size("invalid")

        # Both should handle empty strings consistently
        with pytest.raises(ValidationError):
            parse_duration("")

        with pytest.raises(ValidationError):
            parse_size("")


class TestEdgeCasesAndRegressions(FoundationTestCase):
    """Test edge cases and potential regression scenarios."""

    def test_parse_duration_regex_edge_cases(self) -> None:
        """Test regex edge cases for duration parsing."""
        # Test that only valid patterns match - these actually work because regex finds h and s
        assert parse_duration("1hour") == 3600  # finds 'h' in 'hour'
        assert parse_duration("1sec") == 1  # finds 's' in 'sec'

        # Test patterns that actually fail
        with pytest.raises(ValidationError):
            parse_duration("1xyz")  # No valid units

        with pytest.raises(ValidationError):
            parse_duration("abc")  # No digits

    def test_parse_size_regex_edge_cases(self) -> None:
        """Test regex edge cases for size parsing."""
        # Test patterns that might confuse the regex
        with pytest.raises(ValidationError):
            parse_size("1.2.3GB")  # Multiple dots

        with pytest.raises(ValidationError):
            parse_size("GB1")  # Unit before number

    def test_boundary_values(self) -> None:
        """Test boundary values for both functions."""
        # Minimum values
        assert parse_duration("1s") == 1
        assert parse_size("1B") == 1

        # Zero values
        assert parse_duration("0") == 0
        assert parse_size("0") == 0


# 🧱🏗️🔚
