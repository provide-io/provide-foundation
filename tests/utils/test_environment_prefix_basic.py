#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for utils/environment/prefix.py module."""

from __future__ import annotations

from collections.abc import Generator
import os
from typing import Any

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.utils.environment.prefix import EnvPrefix


@pytest.fixture
def clean_env() -> Generator[None, None, None]:
    """Fixture to clean up environment variables after each test."""
    original_env = os.environ.copy()
    yield
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


class TestEnvPrefixInit(FoundationTestCase):
    """Test EnvPrefix initialization."""

    def test_init_default_separator(self, clean_env: Any) -> None:
        """Test initialization with default separator."""
        env = EnvPrefix("myapp")
        assert env.prefix == "MYAPP"
        assert env.separator == "_"

    def test_init_custom_separator(self, clean_env: Any) -> None:
        """Test initialization with custom separator."""
        env = EnvPrefix("myapp", separator=":")
        assert env.prefix == "MYAPP"
        assert env.separator == ":"

    def test_init_prefix_case_conversion(self, clean_env: Any) -> None:
        """Test that prefix is converted to uppercase."""
        env = EnvPrefix("MyApp")
        assert env.prefix == "MYAPP"

        env = EnvPrefix("lowercase")
        assert env.prefix == "LOWERCASE"

    def test_init_prefix_with_numbers(self, clean_env: Any) -> None:
        """Test prefix with numbers and special chars."""
        env = EnvPrefix("app123")
        assert env.prefix == "APP123"
        assert env.separator == "_"


class TestMakeName(FoundationTestCase):
    """Test _make_name method."""

    def test_make_name_basic(self, clean_env: Any) -> None:
        """Test basic name creation."""
        env = EnvPrefix("app")
        assert env._make_name("debug") == "APP_DEBUG"
        assert env._make_name("database_url") == "APP_DATABASE_URL"

    def test_make_name_case_conversion(self, clean_env: Any) -> None:
        """Test that names are converted to uppercase."""
        env = EnvPrefix("app")
        assert env._make_name("Debug") == "APP_DEBUG"
        assert env._make_name("DATABASE_url") == "APP_DATABASE_URL"

    def test_make_name_separator_replacement(self, clean_env: Any) -> None:
        """Test replacement of common separators."""
        env = EnvPrefix("app")
        assert env._make_name("database-url") == "APP_DATABASE_URL"
        assert env._make_name("log.level") == "APP_LOG_LEVEL"
        assert env._make_name("cache-timeout.value") == "APP_CACHE_TIMEOUT_VALUE"

    def test_make_name_custom_separator(self, clean_env: Any) -> None:
        """Test name creation with custom separator."""
        env = EnvPrefix("app", separator=":")
        assert env._make_name("debug") == "APP:DEBUG"
        assert env._make_name("database-url") == "APP:DATABASE_URL"

    def test_make_name_empty_name(self, clean_env: Any) -> None:
        """Test name creation with empty name."""
        env = EnvPrefix("app")
        assert env._make_name("") == "APP_"


class TestGetBool(FoundationTestCase):
    """Test get_bool method."""

    def test_get_bool_existing_variable(self, clean_env: Any) -> None:
        """Test getting existing boolean variable."""
        os.environ["APP_DEBUG"] = "true"
        env = EnvPrefix("app")
        assert env.get_bool("debug") is True

    def test_get_bool_missing_variable_with_default(self, clean_env: Any) -> None:
        """Test getting missing variable with default."""
        env = EnvPrefix("app")
        assert env.get_bool("debug", default=False) is False

    def test_get_bool_missing_variable_no_default(self, clean_env: Any) -> None:
        """Test getting missing variable without default."""
        env = EnvPrefix("app")
        assert env.get_bool("debug") is None

    def test_get_bool_with_separator_replacement(self, clean_env: Any) -> None:
        """Test boolean with separator replacement."""
        os.environ["APP_ENABLE_DEBUG"] = "true"
        env = EnvPrefix("app")
        assert env.get_bool("enable-debug") is True


class TestGetInt(FoundationTestCase):
    """Test get_int method."""

    def test_get_int_existing_variable(self, clean_env: Any) -> None:
        """Test getting existing integer variable."""
        os.environ["APP_PORT"] = "8080"
        env = EnvPrefix("app")
        assert env.get_int("port") == 8080

    def test_get_int_missing_variable_with_default(self, clean_env: Any) -> None:
        """Test getting missing variable with default."""
        env = EnvPrefix("app")
        assert env.get_int("port", default=3000) == 3000

    def test_get_int_missing_variable_no_default(self, clean_env: Any) -> None:
        """Test getting missing variable without default."""
        env = EnvPrefix("app")
        assert env.get_int("port") is None


class TestGetFloat(FoundationTestCase):
    """Test get_float method."""

    def test_get_float_existing_variable(self, clean_env: Any) -> None:
        """Test getting existing float variable."""
        os.environ["APP_TIMEOUT"] = "30.5"
        env = EnvPrefix("app")
        assert env.get_float("timeout") == 30.5

    def test_get_float_missing_variable_with_default(self, clean_env: Any) -> None:
        """Test getting missing variable with default."""
        env = EnvPrefix("app")
        assert env.get_float("timeout", default=10.0) == 10.0

    def test_get_float_missing_variable_no_default(self, clean_env: Any) -> None:
        """Test getting missing variable without default."""
        env = EnvPrefix("app")
        assert env.get_float("timeout") is None


# 🧱🏗️🔚
