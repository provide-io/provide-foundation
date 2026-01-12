#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for configuration field converters."""

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.config.converters import (
    parse_bool_extended,
    parse_console_formatter,
    parse_float_with_validation,
    parse_log_level,
    parse_module_levels,
    parse_rate_limits,
)


class TestLogLevelParsing(FoundationTestCase):
    """Test log level parsing and validation."""

    def test_parse_log_level_valid(self) -> None:
        """Test parsing valid log levels."""
        assert parse_log_level("debug") == "DEBUG"
        assert parse_log_level("INFO") == "INFO"
        assert parse_log_level("Warning") == "WARNING"
        assert parse_log_level("ERROR") == "ERROR"
        assert parse_log_level("critical") == "CRITICAL"
        assert parse_log_level("TRACE") == "TRACE"

    def test_parse_log_level_invalid(self) -> None:
        """Test parsing invalid log levels raises error."""
        with pytest.raises(ValueError, match="Invalid log_level"):
            parse_log_level("INVALID")

        with pytest.raises(ValueError, match="Invalid log_level"):
            parse_log_level("")


class TestConsoleFormatterParsing(FoundationTestCase):
    """Test console formatter parsing."""

    def test_parse_console_formatter_valid(self) -> None:
        """Test parsing valid formatters."""
        assert parse_console_formatter("KEY_VALUE") == "key_value"
        assert parse_console_formatter("json") == "json"
        assert parse_console_formatter("JSON") == "json"

    def test_parse_console_formatter_invalid(self) -> None:
        """Test parsing invalid formatters raises error."""
        with pytest.raises(ValueError, match="Invalid console_formatter"):
            parse_console_formatter("xml")

        with pytest.raises(ValueError, match="Invalid console_formatter"):
            parse_console_formatter("yaml")


class TestModuleLevelsParsing(FoundationTestCase):
    """Test module-specific log levels parsing."""

    def test_parse_module_levels_valid(self) -> None:
        """Test parsing valid module:level pairs."""
        result = parse_module_levels("auth:DEBUG,database:ERROR")
        assert result == {"auth": "DEBUG", "database": "ERROR"}

        result = parse_module_levels("auth.service:TRACE, db.queries:WARNING")
        assert result == {"auth.service": "TRACE", "db.queries": "WARNING"}

    def test_parse_module_levels_empty(self) -> None:
        """Test parsing empty string returns empty dict."""
        assert parse_module_levels("") == {}
        assert parse_module_levels("   ") == {}

    def test_parse_module_levels_invalid_format(self) -> None:
        """Test invalid formats are skipped silently."""
        result = parse_module_levels("auth:DEBUG,invalid_no_colon,db:INFO")
        assert result == {"auth": "DEBUG", "db": "INFO"}

        result = parse_module_levels("auth:INVALID_LEVEL,db:ERROR")
        assert result == {"db": "ERROR"}  # Invalid level skipped

    def test_parse_module_levels_whitespace(self) -> None:
        """Test whitespace handling."""
        result = parse_module_levels(" auth : DEBUG , database : ERROR ")
        assert result == {"auth": "DEBUG", "database": "ERROR"}


class TestRateLimitsParsing(FoundationTestCase):
    """Test rate limits parsing."""

    def test_parse_rate_limits_valid(self) -> None:
        """Test parsing valid logger:rate:capacity triplets."""
        result = parse_rate_limits("api:10.0:100.0,worker:5:50")
        assert result == {
            "api": (10.0, 100.0),
            "worker": (5.0, 50.0),
        }

    def test_parse_rate_limits_empty(self) -> None:
        """Test parsing empty string returns empty dict."""
        assert parse_rate_limits("") == {}
        assert parse_rate_limits("   ") == {}

    def test_parse_rate_limits_invalid_format(self) -> None:
        """Test invalid formats are skipped silently."""
        result = parse_rate_limits("api:10:100,invalid:format,worker:5:50")
        assert result == {
            "api": (10.0, 100.0),
            "worker": (5.0, 50.0),
        }

        result = parse_rate_limits("api:not_a_number:100")
        assert result == {}  # Invalid number skipped


class TestBoolExtendedParsing(FoundationTestCase):
    """Test extended boolean parsing."""

    @pytest.mark.parametrize(
        "value,expected",
        [
            ("true", True),
            ("True", True),
            ("TRUE", True),
            ("yes", True),
            ("Yes", True),
            ("1", True),
            ("on", True),
            ("ON", True),
            ("false", False),
            ("False", False),
            ("no", False),
            ("0", False),
            ("off", False),
            ("OFF", False),
            ("", False),
            ("anything_else", False),
        ],
    )
    def test_parse_bool_extended(self, value, expected) -> None:
        """Test parsing various boolean representations."""
        assert parse_bool_extended(value) == expected


class TestFloatValidationParsing(FoundationTestCase):
    """Test float parsing with validation."""

    def test_parse_float_with_validation_valid(self) -> None:
        """Test parsing valid floats."""
        assert parse_float_with_validation("3.14") == 3.14
        assert parse_float_with_validation("10") == 10.0
        assert parse_float_with_validation("-5.5") == -5.5

    def test_parse_float_with_validation_range(self) -> None:
        """Test parsing with range validation."""
        assert parse_float_with_validation("5.0", min_val=0.0, max_val=10.0) == 5.0

        with pytest.raises(ValueError, match="must be >= 0.0"):
            parse_float_with_validation("-1.0", min_val=0.0)

        with pytest.raises(ValueError, match="must be <= 10.0"):
            parse_float_with_validation("11.0", max_val=10.0)

    def test_parse_float_with_validation_invalid(self) -> None:
        """Test parsing invalid floats raises error."""
        with pytest.raises(ValueError, match="Invalid float"):
            parse_float_with_validation("not_a_number")


# 🧱🏗️🔚
