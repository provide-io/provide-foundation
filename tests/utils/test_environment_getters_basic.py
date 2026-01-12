#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for basic environment getter functions.

Tests get_bool, get_int, get_float, get_str, get_path, and _get_logger."""

from __future__ import annotations

from collections.abc import Generator
import os
from pathlib import Path
from typing import Any

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.errors.config import ValidationError
from provide.foundation.utils.environment.getters import (
    _get_logger,
    get_bool,
    get_float,
    get_int,
    get_path,
    get_str,
)


@pytest.fixture
def clean_env() -> Generator[None, None, None]:
    """Fixture to clean up environment variables after each test."""
    original_env = os.environ.copy()
    yield
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


class TestGetLogger(FoundationTestCase):
    """Test _get_logger function."""

    def test_get_logger_returns_logger(self) -> None:
        """Test that _get_logger returns a logger instance."""
        logger = _get_logger()
        assert logger is not None
        assert hasattr(logger, "info")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")
        assert hasattr(logger, "debug")


class TestGetBool(FoundationTestCase):
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
        # Test with empty string - returns None with warning
        os.environ["TEST_BOOL"] = ""
        assert get_bool("TEST_BOOL") is None

        # Test with whitespace
        os.environ["TEST_BOOL"] = "  true  "
        assert get_bool("TEST_BOOL") is True

        # Test case sensitivity
        os.environ["TEST_BOOL"] = "TRUE"
        assert get_bool("TEST_BOOL") is True

        os.environ["TEST_BOOL"] = "False"
        assert get_bool("TEST_BOOL") is False


class TestGetInt(FoundationTestCase):
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


class TestGetFloat(FoundationTestCase):
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


class TestGetStr(FoundationTestCase):
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


class TestGetPath(FoundationTestCase):
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


# 🧱🏗️🔚
