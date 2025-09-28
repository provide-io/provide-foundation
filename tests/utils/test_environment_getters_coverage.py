"""Comprehensive tests for utils/environment/getters.py module."""

from __future__ import annotations

from collections.abc import Generator
import os
from pathlib import Path
from typing import Any, get_origin
from unittest.mock import Mock, patch

from provide.testkit import reset_foundation_setup_for_testing
import pytest

from provide.foundation.errors.config import ValidationError
from provide.foundation.utils.environment.getters import (
    _get_logger,
    _parse_complex_type,
    _parse_simple_type,
    get_bool,
    get_dict,
    get_float,
    get_int,
    get_list,
    get_path,
    get_str,
    require,
)


@pytest.fixture(autouse=True)
def reset_foundation() -> None:
    """Reset Foundation state before each test."""
    reset_foundation_setup_for_testing()


@pytest.fixture
def clean_env() -> Generator[None, None, None]:
    """Fixture to clean up environment variables after each test."""
    original_env = os.environ.copy()
    yield
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


class TestGetLogger:
    """Test _get_logger function."""

    def test_get_logger_returns_logger(self) -> None:
        """Test that _get_logger returns a logger instance."""
        logger = _get_logger()
        assert logger is not None
        assert hasattr(logger, "info")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")
        assert hasattr(logger, "debug")


class TestGetBool:
    """Test get_bool function edge cases."""

    def test_get_bool_validation_error_details(self, clean_env: Any) -> None:
        """Test get_bool ValidationError contains proper details."""
        os.environ["TEST_BOOL"] = "invalid_value"

        with pytest.raises(ValidationError) as exc_info:
            get_bool("TEST_BOOL")

        error = exc_info.value
        assert error.context["validation.field"] == "TEST_BOOL"
        assert error.context["validation.value"] == "invalid_value"
        assert error.context["validation.rule"] == "boolean"
        assert "Invalid boolean value for TEST_BOOL" in str(error)

    def test_get_bool_edge_cases(self, clean_env: Any) -> None:
        """Test get_bool with various edge cases."""
        # Test with empty string
        os.environ["TEST_BOOL"] = ""
        assert get_bool("TEST_BOOL") is False

        # Test with whitespace
        os.environ["TEST_BOOL"] = "  true  "
        assert get_bool("TEST_BOOL") is True

        # Test case sensitivity
        os.environ["TEST_BOOL"] = "TRUE"
        assert get_bool("TEST_BOOL") is True

        os.environ["TEST_BOOL"] = "False"
        assert get_bool("TEST_BOOL") is False


class TestGetInt:
    """Test get_int function edge cases."""

    def test_get_int_validation_error_details(self, clean_env: Any) -> None:
        """Test get_int ValidationError contains proper details."""
        os.environ["TEST_INT"] = "not_a_number"

        with pytest.raises(ValidationError) as exc_info:
            get_int("TEST_INT")

        error = exc_info.value
        assert error.context["validation.field"] == "TEST_INT"
        assert error.context["validation.value"] == "not_a_number"
        assert error.context["validation.rule"] == "integer"
        assert "Invalid integer value for TEST_INT" in str(error)

    def test_get_int_edge_cases(self, clean_env: Any) -> None:
        """Test get_int with various edge cases."""
        # Test negative numbers
        os.environ["TEST_INT"] = "-42"
        assert get_int("TEST_INT") == -42

        # Test zero
        os.environ["TEST_INT"] = "0"
        assert get_int("TEST_INT") == 0

        # Test with whitespace
        os.environ["TEST_INT"] = "  123  "
        assert get_int("TEST_INT") == 123

        # Test scientific notation (should fail)
        os.environ["TEST_INT"] = "1e5"
        with pytest.raises(ValidationError):
            get_int("TEST_INT")

        # Test float value (should fail)
        os.environ["TEST_INT"] = "123.45"
        with pytest.raises(ValidationError):
            get_int("TEST_INT")


class TestGetFloat:
    """Test get_float function edge cases."""

    def test_get_float_validation_error_details(self, clean_env: Any) -> None:
        """Test get_float ValidationError contains proper details."""
        os.environ["TEST_FLOAT"] = "not_a_float"

        with pytest.raises(ValidationError) as exc_info:
            get_float("TEST_FLOAT")

        error = exc_info.value
        assert error.context["validation.field"] == "TEST_FLOAT"
        assert error.context["validation.value"] == "not_a_float"
        assert error.context["validation.rule"] == "float"
        assert "Invalid float value for TEST_FLOAT" in str(error)

    def test_get_float_edge_cases(self, clean_env: Any) -> None:
        """Test get_float with various edge cases."""
        # Test negative numbers
        os.environ["TEST_FLOAT"] = "-3.14"
        assert get_float("TEST_FLOAT") == -3.14

        # Test zero
        os.environ["TEST_FLOAT"] = "0.0"
        assert get_float("TEST_FLOAT") == 0.0

        # Test integer format
        os.environ["TEST_FLOAT"] = "42"
        assert get_float("TEST_FLOAT") == 42.0

        # Test scientific notation
        os.environ["TEST_FLOAT"] = "1.5e-4"
        assert get_float("TEST_FLOAT") == 1.5e-4

        # Test infinity
        os.environ["TEST_FLOAT"] = "inf"
        result = get_float("TEST_FLOAT")
        assert result == float("inf")

        # Test negative infinity
        os.environ["TEST_FLOAT"] = "-inf"
        result = get_float("TEST_FLOAT")
        assert result == float("-inf")


class TestGetStr:
    """Test get_str function edge cases."""

    def test_get_str_empty_string(self, clean_env: Any) -> None:
        """Test get_str with empty string."""
        os.environ["TEST_STR"] = ""
        assert get_str("TEST_STR") == ""

    def test_get_str_with_special_characters(self, clean_env: Any) -> None:
        """Test get_str with special characters."""
        os.environ["TEST_STR"] = "hello\nworld\ttab"
        assert get_str("TEST_STR") == "hello\nworld\ttab"

    def test_get_str_unicode(self, clean_env: Any) -> None:
        """Test get_str with unicode characters."""
        os.environ["TEST_STR"] = "héllo wørld 🌍"
        assert get_str("TEST_STR") == "héllo wørld 🌍"


class TestGetPath:
    """Test get_path function edge cases."""

    def test_get_path_environment_variable_expansion(self, clean_env: Any) -> None:
        """Test get_path with environment variable expansion."""
        os.environ["BASE_DIR"] = "/base/path"
        os.environ["TEST_PATH"] = "$BASE_DIR/subdir"

        result = get_path("TEST_PATH")
        assert result == Path("/base/path/subdir")

    def test_get_path_home_expansion(self, clean_env: Any) -> None:
        """Test get_path with home directory expansion."""
        os.environ["TEST_PATH"] = "~/test"

        result = get_path("TEST_PATH")
        assert result is not None
        assert str(result).startswith(str(Path.home()))
        assert result.name == "test"

    def test_get_path_default_types(self, clean_env: Any) -> None:
        """Test get_path with different default types."""
        # Test with string default
        result = get_path("MISSING_PATH", "/default/string")
        assert result == Path("/default/string")

        # Test with Path default
        path_default = Path("/default/path")
        result = get_path("MISSING_PATH", path_default)
        assert result == path_default
        assert result is path_default  # Should be the same instance

    def test_get_path_complex_expansion(self, clean_env: Any) -> None:
        """Test get_path with complex environment expansion."""
        os.environ["VAR1"] = "first"
        os.environ["VAR2"] = "second"
        os.environ["TEST_PATH"] = "/$VAR1/${VAR2}/path"

        result = get_path("TEST_PATH")
        assert result == Path("/first/second/path")


class TestGetList:
    """Test get_list function edge cases."""

    def test_get_list_empty_items_filtered(self, clean_env: Any) -> None:
        """Test get_list filters empty items."""
        os.environ["TEST_LIST"] = "a,,b,,"
        result = get_list("TEST_LIST")
        assert result == ["a", "b"]

    def test_get_list_only_separators(self, clean_env: Any) -> None:
        """Test get_list with only separators."""
        os.environ["TEST_LIST"] = ",,,"
        result = get_list("TEST_LIST")
        assert result == []

    def test_get_list_custom_separator(self, clean_env: Any) -> None:
        """Test get_list with custom separator."""
        os.environ["TEST_LIST"] = "a|b|c"
        result = get_list("TEST_LIST", separator="|")
        assert result == ["a", "b", "c"]

    def test_get_list_whitespace_handling(self, clean_env: Any) -> None:
        """Test get_list whitespace handling."""
        os.environ["TEST_LIST"] = " a , b , c "
        result = get_list("TEST_LIST")
        assert result == ["a", "b", "c"]

    def test_get_list_single_item(self, clean_env: Any) -> None:
        """Test get_list with single item."""
        os.environ["TEST_LIST"] = "single"
        result = get_list("TEST_LIST")
        assert result == ["single"]


class TestGetDict:
    """Test get_dict function edge cases."""

    def test_get_dict_invalid_format_warning(self, clean_env: Any) -> None:
        """Test get_dict logs warning for invalid format and returns partial result."""
        os.environ["TEST_DICT"] = "key1=val1,invalid_item,key2=val2"

        with patch("provide.foundation.utils.environment.getters._get_logger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            result = get_dict("TEST_DICT")

            # Should return valid items and skip invalid ones
            assert result == {"key1": "val1", "key2": "val2"}

            # Should log warning about invalid format
            mock_logger.warning.assert_called_once()
            call_args = mock_logger.warning.call_args
            assert "Invalid dictionary format" in call_args[0][0]

    def test_get_dict_custom_separators(self, clean_env: Any) -> None:
        """Test get_dict with custom separators."""
        os.environ["TEST_DICT"] = "key1:val1;key2:val2"
        result = get_dict("TEST_DICT", item_separator=";", key_value_separator=":")
        assert result == {"key1": "val1", "key2": "val2"}

    def test_get_dict_empty_items_skipped(self, clean_env: Any) -> None:
        """Test get_dict skips empty items."""
        os.environ["TEST_DICT"] = "key1=val1,,key2=val2,"
        result = get_dict("TEST_DICT")
        assert result == {"key1": "val1", "key2": "val2"}

    def test_get_dict_whitespace_handling(self, clean_env: Any) -> None:
        """Test get_dict handles whitespace correctly."""
        os.environ["TEST_DICT"] = " key1 = val1 , key2 = val2 "
        result = get_dict("TEST_DICT")
        assert result == {"key1": "val1", "key2": "val2"}

    def test_get_dict_no_separator_items_skipped(self, clean_env: Any) -> None:
        """Test get_dict skips items without key-value separator."""
        os.environ["TEST_DICT"] = "key1=val1,invalid_item,key2=val2"
        result = get_dict("TEST_DICT")
        assert result == {"key1": "val1", "key2": "val2"}

    def test_get_dict_multiple_separators(self, clean_env: Any) -> None:
        """Test get_dict with multiple separators in value."""
        os.environ["TEST_DICT"] = "key1=val=with=equals,key2=val2"
        result = get_dict("TEST_DICT")
        assert result == {"key1": "val=with=equals", "key2": "val2"}


class TestParseSimpleType:
    """Test _parse_simple_type function."""

    def test_parse_simple_type_bool(self, clean_env: Any) -> None:
        """Test _parse_simple_type with bool type."""
        os.environ["TEST_VAR"] = "true"
        result = _parse_simple_type("TEST_VAR", bool)
        assert result is True

    def test_parse_simple_type_int(self, clean_env: Any) -> None:
        """Test _parse_simple_type with int type."""
        os.environ["TEST_VAR"] = "42"
        result = _parse_simple_type("TEST_VAR", int)
        assert result == 42

    def test_parse_simple_type_float(self, clean_env: Any) -> None:
        """Test _parse_simple_type with float type."""
        os.environ["TEST_VAR"] = "3.14"
        result = _parse_simple_type("TEST_VAR", float)
        assert result == 3.14

    def test_parse_simple_type_str(self, clean_env: Any) -> None:
        """Test _parse_simple_type with str type."""
        os.environ["TEST_VAR"] = "hello"
        result = _parse_simple_type("TEST_VAR", str)
        assert result == "hello"

    def test_parse_simple_type_path(self, clean_env: Any) -> None:
        """Test _parse_simple_type with Path type."""
        os.environ["TEST_VAR"] = "/test/path"
        result = _parse_simple_type("TEST_VAR", Path)
        assert result == Path("/test/path")

    def test_parse_simple_type_unknown(self, clean_env: Any) -> None:
        """Test _parse_simple_type with unknown type falls back to string."""
        os.environ["TEST_VAR"] = "fallback_value"

        class UnknownType:
            pass

        result = _parse_simple_type("TEST_VAR", UnknownType)
        assert result == "fallback_value"

    def test_parse_simple_type_missing_var(self, clean_env: Any) -> None:
        """Test _parse_simple_type with missing variable for unknown type."""
        with pytest.raises(KeyError):
            _parse_simple_type("MISSING_VAR", object)


class TestParseComplexType:
    """Test _parse_complex_type function."""

    def test_parse_complex_type_list(self, clean_env: Any) -> None:
        """Test _parse_complex_type with list origin."""
        os.environ["TEST_VAR"] = "a,b,c"
        result = _parse_complex_type("TEST_VAR", list)
        assert result == ["a", "b", "c"]

    def test_parse_complex_type_dict(self, clean_env: Any) -> None:
        """Test _parse_complex_type with dict origin."""
        os.environ["TEST_VAR"] = "key1=val1,key2=val2"
        result = _parse_complex_type("TEST_VAR", dict)
        assert result == {"key1": "val1", "key2": "val2"}

    def test_parse_complex_type_unknown(self, clean_env: Any) -> None:
        """Test _parse_complex_type with unknown type falls back to string."""
        os.environ["TEST_VAR"] = "fallback_value"

        class UnknownOrigin:
            pass

        result = _parse_complex_type("TEST_VAR", UnknownOrigin)
        assert result == "fallback_value"

    def test_parse_complex_type_missing_var(self, clean_env: Any) -> None:
        """Test _parse_complex_type with missing variable for unknown type."""
        with pytest.raises(KeyError):
            _parse_complex_type("MISSING_VAR", object)


class TestRequire:
    """Test require function edge cases."""

    def test_require_missing_variable(self, clean_env: Any) -> None:
        """Test require with missing variable."""
        with pytest.raises(ValidationError) as exc_info:
            require("MISSING_VAR")

        error = exc_info.value
        assert error.context["validation.field"] == "MISSING_VAR"
        assert error.context["validation.rule"] == "required"
        assert "Required environment variable not set: MISSING_VAR" in str(error)

    def test_require_no_type_hint(self, clean_env: Any) -> None:
        """Test require without type hint returns string."""
        os.environ["TEST_VAR"] = "value"
        result = require("TEST_VAR")
        assert result == "value"

    def test_require_with_simple_types(self, clean_env: Any) -> None:
        """Test require with various simple type hints."""
        # Test bool
        os.environ["TEST_BOOL"] = "true"
        assert require("TEST_BOOL", bool) is True

        # Test int
        os.environ["TEST_INT"] = "42"
        assert require("TEST_INT", int) == 42

        # Test float
        os.environ["TEST_FLOAT"] = "3.14"
        assert require("TEST_FLOAT", float) == 3.14

        # Test str
        os.environ["TEST_STR"] = "hello"
        assert require("TEST_STR", str) == "hello"

        # Test Path
        os.environ["TEST_PATH"] = "/test"
        assert require("TEST_PATH", Path) == Path("/test")

    def test_require_with_complex_types(self, clean_env: Any) -> None:
        """Test require with complex type hints."""
        # Test list
        os.environ["TEST_LIST"] = "a,b,c"
        result = require("TEST_LIST", list[str])
        assert result == ["a", "b", "c"]

        # Test dict
        os.environ["TEST_DICT"] = "key=val"
        result = require("TEST_DICT", dict[str, str])
        assert result == {"key": "val"}

    def test_require_get_origin_none(self, clean_env: Any) -> None:
        """Test require when get_origin returns None."""
        os.environ["TEST_VAR"] = "test_value"

        # For simple types, get_origin returns None
        result = require("TEST_VAR", str)
        assert result == "test_value"

    def test_require_get_origin_not_none(self, clean_env: Any) -> None:
        """Test require when get_origin returns a value."""
        os.environ["TEST_VAR"] = "a,b,c"

        # For list[str], get_origin returns list
        result = require("TEST_VAR", list[str])
        assert result == ["a", "b", "c"]


class TestIntegrationScenarios:
    """Test integration scenarios and edge cases."""

    def test_all_functions_handle_missing_vars(self, clean_env: Any) -> None:
        """Test all getter functions handle missing variables correctly."""
        assert get_bool("MISSING") is None
        assert get_int("MISSING") is None
        assert get_float("MISSING") is None
        assert get_str("MISSING") is None
        assert get_path("MISSING") is None
        assert get_list("MISSING") == []
        assert get_dict("MISSING") == {}

    def test_all_functions_with_defaults(self, clean_env: Any) -> None:
        """Test all getter functions with default values."""
        assert get_bool("MISSING", True) is True
        assert get_int("MISSING", 42) == 42
        assert get_float("MISSING", 3.14) == 3.14
        assert get_str("MISSING", "default") == "default"
        assert get_path("MISSING", "/default") == Path("/default")
        assert get_list("MISSING", ["a", "b"]) == ["a", "b"]
        assert get_dict("MISSING", {"key": "val"}) == {"key": "val"}

    def test_concurrent_access(self, clean_env: Any) -> None:
        """Test concurrent access to environment getters."""
        import threading

        os.environ["CONCURRENT_VAR"] = "test_value"
        os.environ["CONCURRENT_BOOL"] = "true"
        results = []
        errors = []

        def get_env_vars() -> None:
            try:
                results.extend(
                    [
                        get_str("CONCURRENT_VAR"),
                        get_bool("CONCURRENT_BOOL"),
                        get_list("CONCURRENT_VAR"),
                    ]
                )
            except Exception as e:
                errors.append(e)

        # Run multiple threads
        threads = [threading.Thread(target=get_env_vars) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        # All should succeed
        assert len(errors) == 0
        assert len(results) == 15  # 3 calls * 5 threads

    def test_module_constants_and_imports(self) -> None:
        """Test module-level constants and imports."""
        from provide.foundation.utils.environment import getters

        # Check that expected functions are available
        expected_functions = [
            "get_bool",
            "get_int",
            "get_float",
            "get_str",
            "get_path",
            "get_list",
            "get_dict",
            "require",
        ]

        for func_name in expected_functions:
            assert hasattr(getters, func_name)
            assert callable(getattr(getters, func_name))

    def test_type_hint_integration(self, clean_env: Any) -> None:
        """Test integration with typing system."""
        os.environ["TYPE_TEST"] = "value"

        # Test that get_origin works correctly
        origin = get_origin(list[str])
        assert origin is list

        origin = get_origin(dict[str, str])
        assert origin is dict

        origin = get_origin(str)
        assert origin is None
