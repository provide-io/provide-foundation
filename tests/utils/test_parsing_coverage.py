"""Comprehensive tests for utils/parsing.py module."""

from __future__ import annotations

from attrs import define, field, fields
from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock
import pytest

from provide.foundation.utils.parsing import (
    auto_parse,
    parse_bool,
    parse_dict,
    parse_list,
    parse_typed_value,
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
        from provide.foundation.utils.parsing import _parse_basic_type

        assert _parse_basic_type("42", int) == 42
        assert _parse_basic_type("3.14", float) == 3.14
        assert _parse_basic_type("hello", str) == "hello"
        assert _parse_basic_type("true", bool) is True
        assert _parse_basic_type("value", object) is None

    def test_parse_list_type(self) -> None:
        """Test _parse_list_type function."""

        from provide.foundation.utils.parsing import _parse_list_type

        # Parameterized list
        result = _parse_list_type("1,2,3", list[int])
        assert result == [1, 2, 3]

        # Non-parameterized list
        result = _parse_list_type("a,b,c", list)
        assert result == ["a", "b", "c"]

    def test_parse_generic_type(self) -> None:
        """Test _parse_generic_type function."""

        from provide.foundation.utils.parsing import _parse_generic_type

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
        from provide.foundation.utils.parsing import _try_converter

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
        from provide.foundation.utils.parsing import _resolve_string_type

        assert _resolve_string_type("int") is int
        assert _resolve_string_type("float") is float
        assert _resolve_string_type("str") is str
        assert _resolve_string_type("bool") is bool
        assert _resolve_string_type("list") is list
        assert _resolve_string_type("dict") is dict
        assert _resolve_string_type("unknown") == "unknown"

    def test_extract_field_type(self) -> None:
        """Test _extract_field_type function."""
        from provide.foundation.utils.parsing import _extract_field_type

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
