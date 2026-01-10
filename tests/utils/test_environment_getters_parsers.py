#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for environment parser functions and integration.

Tests _parse_simple_type, _parse_complex_type, require, and integration scenarios."""

from __future__ import annotations

from collections.abc import Generator
import os
from pathlib import Path
from typing import Any, get_origin

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.errors.config import ValidationError
from provide.foundation.utils.environment.getters import (
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


@pytest.fixture
def clean_env() -> Generator[None, None, None]:
    """Fixture to clean up environment variables after each test."""
    original_env = os.environ.copy()
    yield
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


class TestParseSimpleType(FoundationTestCase):
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


class TestParseComplexType(FoundationTestCase):
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


class TestParseComplexTypeExtended(FoundationTestCase):
    """Test _parse_complex_type with tuple and set types."""

    def test_parse_complex_type_tuple(self, clean_env: Any) -> None:
        """Test _parse_complex_type with tuple origin."""
        os.environ["TEST_VAR"] = "a,b,c"
        result = _parse_complex_type("TEST_VAR", tuple)
        assert result == ("a", "b", "c")
        assert isinstance(result, tuple)

    def test_parse_complex_type_set(self, clean_env: Any) -> None:
        """Test _parse_complex_type with set origin."""
        os.environ["TEST_VAR"] = "a,b,a,c"
        result = _parse_complex_type("TEST_VAR", set)
        assert result == {"a", "b", "c"}
        assert isinstance(result, set)

    def test_parse_complex_type_tuple_empty(self, clean_env: Any) -> None:
        """Test _parse_complex_type with tuple for empty value."""
        os.environ["TEST_VAR"] = ""
        result = _parse_complex_type("TEST_VAR", tuple)
        assert result == ()

    def test_parse_complex_type_set_empty(self, clean_env: Any) -> None:
        """Test _parse_complex_type with set for empty value."""
        os.environ["TEST_VAR"] = ""
        result = _parse_complex_type("TEST_VAR", set)
        assert result == set()


class TestRequire(FoundationTestCase):
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


class TestIntegrationScenarios(FoundationTestCase):
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
        threads = [threading.Thread(daemon=True, target=get_env_vars) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10.0)

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


# 🧱🏗️🔚
