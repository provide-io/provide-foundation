#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for utils/parsing.py module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.parsers import (
    parse_bool,
    parse_dict,
    parse_list,
)


class TestParseBool(FoundationTestCase):
    """Test parse_bool function."""

    def test_parse_bool_from_bool(self) -> None:
        """Test parsing bool from bool values."""
        assert parse_bool(True) is True
        assert parse_bool(False) is False

    def test_parse_bool_true_values(self) -> None:
        """Test parsing bool from true string values."""
        true_values = ["true", "TRUE", "True", "yes", "YES", "1", "on", "ON", "enabled", "ENABLED"]
        for value in true_values:
            assert parse_bool(value) is True, f"Failed to parse '{value}' as True"

    def test_parse_bool_false_values(self) -> None:
        """Test parsing bool from false string values."""
        false_values = ["false", "FALSE", "False", "no", "NO", "0", "off", "OFF", "disabled", "DISABLED"]
        for value in false_values:
            assert parse_bool(value) is False, f"Failed to parse '{value}' as False"

    def test_parse_bool_with_whitespace(self) -> None:
        """Test parsing bool with whitespace."""
        assert parse_bool("  true  ") is True
        assert parse_bool("  false  ") is False
        assert parse_bool("\ttrue\n") is True

    def test_parse_bool_non_string_types(self) -> None:
        """Test parsing bool from non-string types."""
        # parse_bool_strict accepts int/float for 0 and 1 only
        assert parse_bool(1) is True
        assert parse_bool(0) is False
        assert parse_bool(1.0) is True
        assert parse_bool(0.0) is False

        # Invalid numeric values raise ValueError
        with pytest.raises(ValueError, match="Numeric boolean must be 0 or 1"):
            parse_bool(2)

        # Non-str/bool/int/float types raise TypeError
        with pytest.raises(TypeError, match="Boolean field requires"):
            parse_bool([])
        with pytest.raises(TypeError, match="Boolean field requires"):
            parse_bool([1])

    def test_parse_bool_strict_mode(self) -> None:
        """Test parse_bool with strict mode."""
        # Should work with bool and string
        assert parse_bool(True, strict=True) is True
        assert parse_bool("true", strict=True) is True

        # Should reject non-bool, non-string types
        with pytest.raises(TypeError, match="Cannot convert int to bool"):
            parse_bool(1, strict=True)

        with pytest.raises(TypeError, match="Cannot convert list to bool"):
            parse_bool([], strict=True)

    def test_parse_bool_invalid_values(self) -> None:
        """Test parsing bool from invalid values."""
        invalid_values = ["maybe", "invalid", "2", "unknown"]
        for value in invalid_values:
            with pytest.raises(ValueError, match=f"Invalid boolean '{value}'"):
                parse_bool(value)


class TestParseList(FoundationTestCase):
    """Test parse_list function."""

    def test_parse_list_from_list(self) -> None:
        """Test parsing list from existing list."""
        original = ["a", "b", "c"]
        assert parse_list(original) == original

    def test_parse_list_from_string(self) -> None:
        """Test parsing list from string."""
        assert parse_list("a,b,c") == ["a", "b", "c"]
        assert parse_list("single") == ["single"]

    def test_parse_list_empty_string(self) -> None:
        """Test parsing list from empty string."""
        assert parse_list("") == []
        assert parse_list(None) == []  # Falsy value

    def test_parse_list_custom_separator(self) -> None:
        """Test parsing list with custom separator."""
        assert parse_list("a;b;c", separator=";") == ["a", "b", "c"]
        assert parse_list("a|b|c", separator="|") == ["a", "b", "c"]

    def test_parse_list_with_whitespace(self) -> None:
        """Test parsing list with whitespace."""
        assert parse_list(" a , b , c ") == ["a", "b", "c"]
        assert parse_list("a,  b,   c") == ["a", "b", "c"]

    def test_parse_list_no_strip(self) -> None:
        """Test parsing list without stripping whitespace."""
        assert parse_list(" a , b , c ", strip=False) == [" a ", " b ", " c "]

    def test_parse_list_empty_items(self) -> None:
        """Test parsing list with empty items."""
        assert parse_list("a,,c") == ["a", "", "c"]
        assert parse_list(",b,") == ["", "b", ""]


class TestParseDict(FoundationTestCase):
    """Test parse_dict function."""

    def test_parse_dict_from_dict(self) -> None:
        """Test parsing dict from existing dict."""
        original = {"a": "1", "b": "2"}
        assert parse_dict(original) == original

    def test_parse_dict_from_string(self) -> None:
        """Test parsing dict from string."""
        assert parse_dict("a=1,b=2") == {"a": "1", "b": "2"}
        assert parse_dict("key=value") == {"key": "value"}

    def test_parse_dict_empty_string(self) -> None:
        """Test parsing dict from empty string."""
        assert parse_dict("") == {}
        assert parse_dict(None) == {}

    def test_parse_dict_custom_separators(self) -> None:
        """Test parsing dict with custom separators."""
        assert parse_dict("a:1;b:2", item_separator=";", key_separator=":") == {"a": "1", "b": "2"}

    def test_parse_dict_with_whitespace(self) -> None:
        """Test parsing dict with whitespace."""
        assert parse_dict(" a = 1 , b = 2 ") == {"a": "1", "b": "2"}

    def test_parse_dict_no_strip(self) -> None:
        """Test parsing dict without stripping whitespace."""
        assert parse_dict(" a = 1 ", strip=False) == {" a ": " 1 "}

    def test_parse_dict_invalid_format(self) -> None:
        """Test parsing dict with invalid format."""
        with pytest.raises(ValueError, match="Invalid dict format: 'invalid' missing '='"):
            parse_dict("invalid")

        with pytest.raises(ValueError, match="Invalid dict format: 'no_equals' missing '='"):
            parse_dict("key=value,no_equals")

    def test_parse_dict_value_with_separator(self) -> None:
        """Test parsing dict where value contains the key separator."""
        assert parse_dict("url=http://example.com") == {"url": "http://example.com"}
        assert parse_dict("path=/path/with=equals") == {"path": "/path/with=equals"}

    def test_parse_dict_empty_items(self) -> None:
        """Test parsing dict with empty items."""
        assert parse_dict("a=1,,b=2") == {"a": "1", "b": "2"}  # Empty items are skipped


# 🧱🏗️🔚
