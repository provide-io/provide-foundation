#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for typed value parsing functionality."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock
import pytest

from provide.foundation.parsers import (
    parse_typed_value,
)


class TestParseTypedValue(FoundationTestCase):
    """Test parse_typed_value function."""

    def test_parse_typed_value_none(self) -> None:
        """Test parsing None value."""
        assert parse_typed_value(None, str) is None
        assert parse_typed_value(None, int) is None

    def test_parse_typed_value_basic_types(self) -> None:
        """Test parsing basic types."""
        assert parse_typed_value("42", int) == 42
        assert parse_typed_value("3.14", float) == 3.14
        assert parse_typed_value("hello", str) == "hello"
        assert parse_typed_value("true", bool) is True

    def test_parse_typed_value_list(self) -> None:
        """Test parsing list types."""
        assert parse_typed_value("a,b,c", list) == ["a", "b", "c"]

    def test_parse_typed_value_dict(self) -> None:
        """Test parsing dict types."""
        assert parse_typed_value("a=1,b=2", dict) == {"a": "1", "b": "2"}

    def test_parse_typed_value_parameterized_list(self) -> None:
        """Test parsing parameterized list types."""

        # list[int]
        result = parse_typed_value("1,2,3", list[int])
        assert result == [1, 2, 3]

        # list[bool]
        result = parse_typed_value("true,false,1", list[bool])
        assert result == [True, False, True]

    def test_parse_typed_value_parameterized_list_conversion_error(self) -> None:
        """Test parsing parameterized list with conversion errors."""

        with pytest.raises(ValueError, match="Cannot convert list items to int"):
            parse_typed_value("1,invalid,3", list[int])

    def test_parse_typed_value_unknown_type(self) -> None:
        """Test parsing with unknown type."""

        class CustomType:
            pass

        # Should fall back to string
        assert parse_typed_value("value", CustomType) == "value"

    def test_parse_typed_value_fallback_to_string(self) -> None:
        """Test that unknown types fall back to string."""
        result = parse_typed_value("fallback", object)
        assert result == "fallback"


class TestInternalHelpers:
    """Test internal helper functions."""

    def test_parse_basic_type(self) -> None:
        """Test _parse_basic_type function."""
        from provide.foundation.parsers import _parse_basic_type

        assert _parse_basic_type("42", int) == 42
        assert _parse_basic_type("3.14", float) == 3.14
        assert _parse_basic_type("hello", str) == "hello"
        assert _parse_basic_type("true", bool) is True
        assert _parse_basic_type("value", object) is None

    def test_parse_list_type(self) -> None:
        """Test _parse_list_type function."""

        from provide.foundation.parsers import _parse_list_type

        # Parameterized list
        result = _parse_list_type("1,2,3", list[int])
        assert result == [1, 2, 3]

        # Non-parameterized list
        result = _parse_list_type("a,b,c", list)
        assert result == ["a", "b", "c"]

    def test_parse_generic_type(self) -> None:
        """Test _parse_generic_type function."""

        from provide.foundation.parsers import _parse_generic_type

        # Parameterized list
        result = _parse_generic_type("1,2,3", list[int])
        assert result == [1, 2, 3]

        # Dict
        result = _parse_generic_type("a=1,b=2", dict[str, str])
        assert result == {"a": "1", "b": "2"}

        # Non-generic types
        result = _parse_generic_type("a,b,c", list)
        assert result == ["a", "b", "c"]

        result = _parse_generic_type("a=1", dict)
        assert result == {"a": "1"}

        # Unknown type
        result = _parse_generic_type("value", str)
        assert result is None

    def test_try_converter(self) -> None:
        """Test _try_converter function."""
        from provide.foundation.parsers import _try_converter

        # Successful converter
        success, result = _try_converter(str.upper, "hello")
        assert success is True
        assert result == "HELLO"

        # Failed converter
        def failing_converter(value: str) -> int:
            raise ValueError("Failed")

        success, result = _try_converter(failing_converter, "value")
        assert success is False
        assert result is None

        # No converter
        success, result = _try_converter(None, "value")
        assert success is False

        # Non-callable converter
        success, result = _try_converter("not_callable", "value")
        assert success is False

        # Mock converter (special case)
        mock_converter = Mock(return_value=Mock(_mock_name="test"))
        success, result = _try_converter(mock_converter, "value")
        assert success is False

    def test_resolve_string_type(self) -> None:
        """Test _resolve_string_type function."""
        from provide.foundation.parsers import _resolve_string_type

        assert _resolve_string_type("int") is int
        assert _resolve_string_type("float") is float
        assert _resolve_string_type("str") is str
        assert _resolve_string_type("bool") is bool
        assert _resolve_string_type("list") is list
        assert _resolve_string_type("dict") is dict
        assert _resolve_string_type("unknown") == "unknown"

    def test_extract_field_type(self) -> None:
        """Test _extract_field_type function."""
        from provide.foundation.parsers import _extract_field_type

        # Mock attrs field
        field_with_type = Mock()
        field_with_type.type = int
        assert _extract_field_type(field_with_type) is int

        # Field with string type
        field_with_string_type = Mock()
        field_with_string_type.type = "int"
        assert _extract_field_type(field_with_string_type) is int

        # Field with unknown string type
        field_with_unknown_type = Mock()
        field_with_unknown_type.type = "unknown"
        assert _extract_field_type(field_with_unknown_type) is None

        # Field without type
        field_without_type = Mock()
        field_without_type.type = None
        assert _extract_field_type(field_without_type) is None

        # Field missing type attribute
        field_missing_type = Mock(spec=[])
        assert _extract_field_type(field_missing_type) is None


# 🧱🏗️🔚
