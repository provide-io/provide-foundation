#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for auto parsing functionality."""

from __future__ import annotations

from attrs import define, field, fields
from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock
import pytest

from provide.foundation.parsers import auto_parse, parse_bool, parse_dict, parse_list, parse_typed_value


class TestAutoParse(FoundationTestCase):
    """Test auto_parse function."""

    def test_auto_parse_with_converter(self) -> None:
        """Test auto_parse with field converter."""

        @define
        class Config:
            value: str = field(converter=str.upper)

        attr = fields(Config).value
        result = auto_parse(attr, "hello")
        assert result == "HELLO"

    def test_auto_parse_with_metadata_converter(self) -> None:
        """Test auto_parse with converter in metadata."""
        # Create a mock field with metadata converter
        mock_attr = Mock()
        mock_attr.converter = None  # No direct converter
        mock_attr.metadata = {"converter": str.lower}
        mock_attr.type = str

        result = auto_parse(mock_attr, "HELLO")
        assert result == "hello"

    def test_auto_parse_with_type_only(self) -> None:
        """Test auto_parse with type-based parsing."""

        @define
        class Config:
            count: int = field()
            enabled: bool = field()

        # Test int field
        attr = fields(Config).count
        result = auto_parse(attr, "42")
        assert result == 42

        # Test bool field
        attr = fields(Config).enabled
        result = auto_parse(attr, "true")
        assert result is True

    def test_auto_parse_failing_converter(self) -> None:
        """Test auto_parse with failing converter falls back to type parsing."""

        def failing_converter(value: str) -> str:
            raise ValueError("Converter failed")

        mock_attr = Mock()
        mock_attr.converter = failing_converter
        mock_attr.metadata = {}
        mock_attr.type = str

        result = auto_parse(mock_attr, "fallback")
        assert result == "fallback"

    def test_auto_parse_mock_converter(self) -> None:
        """Test auto_parse with mock converter falls back to type parsing."""
        mock_converter = Mock(return_value=Mock(_mock_name="test"))

        mock_attr = Mock()
        mock_attr.converter = mock_converter
        mock_attr.metadata = {}
        mock_attr.type = int

        result = auto_parse(mock_attr, "42")
        assert result == 42

    def test_auto_parse_no_type_info(self) -> None:
        """Test auto_parse without type info returns string."""
        mock_attr = Mock()
        mock_attr.converter = None
        mock_attr.metadata = {}
        mock_attr.type = None

        result = auto_parse(mock_attr, "value")
        assert result == "value"

    def test_auto_parse_no_metadata(self) -> None:
        """Test auto_parse with field that has no metadata."""

        @define
        class Config:
            value: str = field()

        attr = fields(Config).value
        # Remove metadata attribute to test the hasattr check
        if hasattr(attr, "metadata"):
            delattr(attr, "metadata")

        result = auto_parse(attr, "test")
        assert result == "test"

    def test_auto_parse_complex_example(self) -> None:
        """Test auto_parse with complex example from docstring."""

        @define
        class Config:
            count: int = field()
            enabled: bool = field()
            custom: str = field(converter=lambda x: x.upper())

        # Test each field
        count_field = fields(Config).count
        enabled_field = fields(Config).enabled
        custom_field = fields(Config).custom

        assert auto_parse(count_field, "42") == 42
        assert auto_parse(enabled_field, "true") is True
        assert auto_parse(custom_field, "hello") == "HELLO"


class TestEdgeCases:
    """Test edge cases and integration scenarios."""

    def test_empty_string_parsing(self) -> None:
        """Test parsing empty strings."""
        # Empty string is ambiguous for booleans and should raise an error
        with pytest.raises(ValueError, match="Invalid boolean"):
            parse_bool("")
        assert parse_list("") == []
        assert parse_dict("") == {}
        assert parse_typed_value("", str) == ""

    def test_whitespace_only_strings(self) -> None:
        """Test parsing whitespace-only strings."""
        # Whitespace-only strings strip to empty and should raise an error for booleans
        with pytest.raises(ValueError, match="Invalid boolean"):
            parse_bool("   ")
        # parse_list splits on comma, so whitespace-only becomes single empty item
        assert parse_list("   ") == [""]

    def test_special_characters_in_values(self) -> None:
        """Test parsing values with special characters."""
        # Dict value with commas
        result = parse_dict("config=a,b,c", item_separator=";")
        assert result == {"config": "a,b,c"}

        # List with special chars
        result = parse_list("a=1,b=2", separator=",")
        assert result == ["a=1", "b=2"]

    def test_type_conversion_edge_cases(self) -> None:
        """Test edge cases in type conversion."""
        # Float as string to int (raises ValueError in Python)
        with pytest.raises(ValueError):
            parse_typed_value("42.0", int)

        # Valid int conversion
        assert parse_typed_value("42", int) == 42

        # Invalid int conversion
        with pytest.raises(ValueError):
            parse_typed_value("not_a_number", int)

        # Invalid float conversion
        with pytest.raises(ValueError):
            parse_typed_value("not_a_float", float)

    def test_module_docstring_examples(self) -> None:
        """Test examples from module docstring work correctly."""
        # These should match the docstring examples
        assert parse_typed_value("42", int) == 42
        assert parse_typed_value("true", bool) is True
        assert parse_typed_value("a,b,c", list) == ["a", "b", "c"]


# 🧱🏗️🔚
