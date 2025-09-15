"""Additional tests for parsing utilities to improve code coverage."""

from unittest.mock import Mock

import pytest

from provide.foundation.utils.parsing import (
    auto_parse,
    parse_bool,
    parse_dict,
    parse_list,
    parse_typed_value,
)


class TestParsingCoverage:
    """Test parsing utilities for improved coverage."""

    def test_parse_bool_with_strict_mode_non_string(self) -> None:
        """Test parse_bool with strict mode rejects non-string types."""
        with pytest.raises(TypeError) as exc_info:
            parse_bool(123, strict=True)
        assert "Cannot convert int to bool" in str(exc_info.value)

    def test_parse_bool_invalid_string_value(self) -> None:
        """Test parse_bool with invalid string value."""
        with pytest.raises(ValueError) as exc_info:
            parse_bool("maybe")
        assert "Cannot parse 'maybe' as boolean" in str(exc_info.value)

    def test_parse_bool_with_empty_string(self) -> None:
        """Test parse_bool with empty string returns False."""
        assert parse_bool("") is False

    def test_parse_bool_with_whitespace(self) -> None:
        """Test parse_bool handles whitespace properly."""
        assert parse_bool("  TRUE  ") is True
        assert parse_bool("  false  ") is False

    def test_parse_bool_case_insensitive(self) -> None:
        """Test parse_bool handles different cases."""
        assert parse_bool("TRUE") is True
        assert parse_bool("False") is False
        assert parse_bool("YES") is True
        assert parse_bool("No") is False

    def test_parse_list_with_no_strip(self) -> None:
        """Test parse_list without stripping whitespace."""
        result = parse_list("  a  , b ,c  ", strip=False)
        assert result == ["  a  ", " b ", "c  "]

    def test_parse_list_with_empty_string(self) -> None:
        """Test parse_list with empty string."""
        assert parse_list("") == []
        assert parse_list(None) == []

    def test_parse_list_with_custom_separator(self) -> None:
        """Test parse_list with custom separator."""
        result = parse_list("a|b|c", separator="|")
        assert result == ["a", "b", "c"]

    def test_parse_list_already_list(self) -> None:
        """Test parse_list with already parsed list."""
        original = ["a", "b", "c"]
        result = parse_list(original)
        assert result == original
        assert result is original  # Should return same object

    def test_parse_dict_with_empty_items(self) -> None:
        """Test parse_dict handles empty items."""
        result = parse_dict("a=1,,b=2")
        assert result == {"a": "1", "b": "2"}

    def test_parse_dict_missing_separator(self) -> None:
        """Test parse_dict with missing key separator."""
        with pytest.raises(ValueError) as exc_info:
            parse_dict("a=1,invalid_item,c=3")
        assert "Invalid dict format: 'invalid_item' missing '='" in str(exc_info.value)

    def test_parse_dict_with_no_strip(self) -> None:
        """Test parse_dict without stripping whitespace."""
        result = parse_dict("  a = 1 , b = 2  ", strip=False)
        assert result == {"  a ": " 1 ", " b ": " 2  "}

    def test_parse_dict_with_custom_separators(self) -> None:
        """Test parse_dict with custom separators."""
        result = parse_dict("a:1;b:2", item_separator=";", key_separator=":")
        assert result == {"a": "1", "b": "2"}

    def test_parse_dict_with_empty_string(self) -> None:
        """Test parse_dict with empty string."""
        assert parse_dict("") == {}
        assert parse_dict(None) == {}

    def test_parse_dict_already_dict(self) -> None:
        """Test parse_dict with already parsed dict."""
        original = {"a": "1", "b": "2"}
        result = parse_dict(original)
        assert result == original
        assert result is original  # Should return same object

    def test_parse_dict_with_multiple_equals_in_value(self) -> None:
        """Test parse_dict handles multiple equals signs in value."""
        result = parse_dict("url=http://example.com/path?a=1&b=2")
        assert result == {"url": "http://example.com/path?a=1&b=2"}

    def test_parse_typed_value_with_none(self) -> None:
        """Test parse_typed_value handles None value."""
        assert parse_typed_value(None, str) is None

    def test_parse_typed_value_with_int_and_float(self) -> None:
        """Test parse_typed_value with numeric types."""
        assert parse_typed_value("42", int) == 42
        assert parse_typed_value("3.14", float) == 3.14

    def test_parse_typed_value_with_typed_list(self) -> None:
        """Test parse_typed_value with typed list."""
        # Test list[int]

        result = parse_typed_value("1,2,3", list[int])
        assert result == [1, 2, 3]

    def test_parse_typed_value_with_typed_list_conversion_error(self) -> None:
        """Test parse_typed_value with list conversion error."""
        with pytest.raises(ValueError) as exc_info:
            parse_typed_value("a,b,c", list[int])
        assert "Cannot convert list items to int" in str(exc_info.value)

    def test_parse_typed_value_with_untyped_list(self) -> None:
        """Test parse_typed_value with untyped list."""
        result = parse_typed_value("a,b,c", list)
        assert result == ["a", "b", "c"]

    def test_parse_typed_value_with_dict_type(self) -> None:
        """Test parse_typed_value with dict types."""
        # Test with typing origin

        result = parse_typed_value("a=1,b=2", dict[str, str])
        assert result == {"a": "1", "b": "2"}

        # Test with plain dict
        result = parse_typed_value("a=1,b=2", dict)
        assert result == {"a": "1", "b": "2"}

    def test_parse_typed_value_unknown_type(self) -> None:
        """Test parse_typed_value with unknown type returns string."""

        class CustomType:
            pass

        result = parse_typed_value("test", CustomType)
        assert result == "test"

    def test_auto_parse_with_type_attribute(self) -> None:
        """Test auto_parse with attrs field having type."""
        # Mock an attrs field
        mock_field = Mock()
        mock_field.type = int

        result = auto_parse(mock_field, "42")
        assert result == 42

    def test_auto_parse_with_string_type_name(self) -> None:
        """Test auto_parse with string type name."""
        mock_field = Mock()
        mock_field.type = "int"

        result = auto_parse(mock_field, "42")
        assert result == 42

    def test_auto_parse_with_unknown_string_type(self) -> None:
        """Test auto_parse with unknown string type name."""
        mock_field = Mock()
        mock_field.type = "unknown_type"

        result = auto_parse(mock_field, "test")
        assert result == "test"

    def test_auto_parse_without_type(self) -> None:
        """Test auto_parse without type returns string."""
        mock_field = Mock()
        mock_field.type = None

        result = auto_parse(mock_field, "test")
        assert result == "test"

    def test_auto_parse_without_type_attribute(self) -> None:
        """Test auto_parse without type attribute returns string."""
        mock_field = Mock(spec=[])  # No type attribute

        result = auto_parse(mock_field, "test")
        assert result == "test"

    def test_parse_typed_value_list_without_args(self) -> None:
        """Test parse_typed_value with list type that has no generic args."""
        # Create a mock type that looks like list but without args

        # Test with typing.List that might not have args in some cases
        result = parse_typed_value("a,b,c", list)
        assert result == ["a", "b", "c"]

    def test_auto_parse_all_string_type_mappings(self) -> None:
        """Test auto_parse with all supported string type mappings."""
        mappings = [
            ("int", "42", 42),
            ("float", "3.14", 3.14),
            ("str", "test", "test"),
            ("bool", "true", True),
            ("list", "a,b,c", ["a", "b", "c"]),
            ("dict", "a=1,b=2", {"a": "1", "b": "2"}),
        ]

        for type_str, value, expected in mappings:
            mock_field = Mock()
            mock_field.type = type_str
            result = auto_parse(mock_field, value)
            assert result == expected, f"Failed for type {type_str}"
