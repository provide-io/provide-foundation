#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for special config converters."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.parsers.primitives import parse_bool_strict
from provide.foundation.parsers.structured import parse_module_levels
from provide.foundation.parsers.telemetry import parse_foundation_log_output


class TestFoundationLogOutputParsing(FoundationTestCase):
    """Test foundation log output destination parsing."""

    def test_parse_foundation_log_output_valid(self) -> None:
        """Test parsing valid output destinations."""
        assert parse_foundation_log_output("stderr") == "stderr"
        assert parse_foundation_log_output("stdout") == "stdout"
        assert parse_foundation_log_output("main") == "main"

        # Case insensitive
        assert parse_foundation_log_output("STDERR") == "stderr"
        assert parse_foundation_log_output("StdOut") == "stdout"
        assert parse_foundation_log_output("MAIN") == "main"

    def test_parse_foundation_log_output_empty(self) -> None:
        """Test parsing empty string defaults to stderr."""
        assert parse_foundation_log_output("") == "stderr"
        assert parse_foundation_log_output(None) == "stderr"

    def test_parse_foundation_log_output_whitespace(self) -> None:
        """Test whitespace handling."""
        assert parse_foundation_log_output("  stderr  ") == "stderr"
        assert parse_foundation_log_output("  STDOUT  ") == "stdout"

    def test_parse_foundation_log_output_invalid(self) -> None:
        """Test parsing invalid destinations raises error."""
        with pytest.raises(ValueError, match="Invalid foundation_log_output"):
            parse_foundation_log_output("invalid")

        with pytest.raises(ValueError, match="Invalid foundation_log_output"):
            parse_foundation_log_output("console")


class TestBoolStrictParsing(FoundationTestCase):
    """Test strict boolean parsing."""

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
        ],
    )
    def test_parse_bool_strict_valid(self, value, expected) -> None:
        """Test parsing valid boolean representations."""
        assert parse_bool_strict(value) == expected

    def test_parse_bool_strict_bool_input(self) -> None:
        """Test parsing actual bool values."""
        assert parse_bool_strict(True) is True
        assert parse_bool_strict(False) is False

    def test_parse_bool_strict_numeric_input(self) -> None:
        """Test parsing numeric boolean values (int and float)."""
        # Valid numeric booleans
        assert parse_bool_strict(1) is True
        assert parse_bool_strict(0) is False
        assert parse_bool_strict(1.0) is True
        assert parse_bool_strict(0.0) is False

        # Invalid numeric values
        with pytest.raises(ValueError, match="Numeric boolean must be 0 or 1"):
            parse_bool_strict(42)

        with pytest.raises(ValueError, match="Numeric boolean must be 0 or 1"):
            parse_bool_strict(-1)

        with pytest.raises(ValueError, match="Numeric boolean must be 0 or 1"):
            parse_bool_strict(2.0)

        with pytest.raises(ValueError, match="Numeric boolean must be 0 or 1"):
            parse_bool_strict(0.5)

    def test_parse_bool_strict_invalid_value(self) -> None:
        """Test strict parsing rejects invalid string values."""
        with pytest.raises(ValueError, match="Invalid boolean"):
            parse_bool_strict("invalid")

        with pytest.raises(ValueError, match="Invalid boolean"):
            parse_bool_strict("")

        with pytest.raises(ValueError, match="Invalid boolean"):
            parse_bool_strict("maybe")

    def test_parse_bool_strict_invalid_type(self) -> None:
        """Test strict parsing rejects invalid types."""
        with pytest.raises(TypeError, match="Boolean field requires str, bool, int, or float"):
            parse_bool_strict([])

        with pytest.raises(TypeError, match="Boolean field requires str, bool, int, or float"):
            parse_bool_strict(None)

        with pytest.raises(TypeError, match="Boolean field requires str, bool, int, or float"):
            parse_bool_strict({"key": "value"})

    def test_parse_bool_strict_whitespace(self) -> None:
        """Test whitespace handling in strict mode."""
        assert parse_bool_strict("  true  ") is True
        assert parse_bool_strict("  false  ") is False


class TestModuleLevelsDictInput(FoundationTestCase):
    """Test module levels parsing with dict input."""

    def test_parse_module_levels_dict_valid(self) -> None:
        """Test parsing dict input with valid levels."""
        input_dict = {"auth": "debug", "database": "ERROR", "api": "Info"}
        result = parse_module_levels(input_dict)
        assert result == {"auth": "DEBUG", "database": "ERROR", "api": "INFO"}

    def test_parse_module_levels_dict_invalid(self) -> None:
        """Test dict input with some invalid levels."""
        input_dict = {"auth": "DEBUG", "bad": "INVALID_LEVEL", "api": "INFO"}
        result = parse_module_levels(input_dict)
        assert result == {"auth": "DEBUG", "api": "INFO"}  # Invalid level skipped

    def test_parse_module_levels_dict_empty(self) -> None:
        """Test parsing empty dict."""
        assert parse_module_levels({}) == {}


# 🧱🏗️🔚
