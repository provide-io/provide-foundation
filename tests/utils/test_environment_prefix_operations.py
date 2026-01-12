#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for EnvPrefix operations."""

from __future__ import annotations

from collections.abc import Generator
import os
from typing import Any

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.errors.config import ValidationError
from provide.foundation.utils.environment.prefix import EnvPrefix


@pytest.fixture
def clean_env() -> Generator[None, None, None]:
    """Fixture to clean up environment variables after each test."""
    original_env = os.environ.copy()
    yield
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


class TestRequire(FoundationTestCase):
    """Test require method."""

    def test_require_existing_variable(self, clean_env: Any) -> None:
        """Test requiring existing variable."""
        os.environ["APP_SECRET"] = "mysecret"
        env = EnvPrefix("app")
        assert env.require("secret") == "mysecret"

    def test_require_missing_variable(self, clean_env: Any) -> None:
        """Test requiring missing variable."""
        env = EnvPrefix("app")
        with pytest.raises(ValidationError, match="Required environment variable not set: APP_SECRET"):
            env.require("secret")

    def test_require_with_type_hint(self, clean_env: Any) -> None:
        """Test requiring variable with type hint."""
        os.environ["APP_PORT"] = "8080"
        env = EnvPrefix("app")
        result = env.require("port", type_hint=int)
        assert result == 8080

    def test_require_separator_replacement(self, clean_env: Any) -> None:
        """Test require with separator replacement."""
        os.environ["APP_API_KEY"] = "mykey"
        env = EnvPrefix("app")
        assert env.require("api-key") == "mykey"


class TestSubscriptNotation(FoundationTestCase):
    """Test __getitem__ method (subscript notation)."""

    def test_getitem_existing_variable(self, clean_env: Any) -> None:
        """Test subscript access to existing variable."""
        os.environ["APP_NAME"] = "myapp"
        env = EnvPrefix("app")
        assert env["name"] == "myapp"

    def test_getitem_missing_variable(self, clean_env: Any) -> None:
        """Test subscript access to missing variable."""
        env = EnvPrefix("app")
        assert env["name"] is None

    def test_getitem_separator_replacement(self, clean_env: Any) -> None:
        """Test subscript access with separator replacement."""
        os.environ["APP_DATABASE_URL"] = "postgres://localhost"
        env = EnvPrefix("app")
        assert env["database-url"] == "postgres://localhost"


class TestContains(FoundationTestCase):
    """Test __contains__ method (in operator)."""

    def test_contains_existing_variable(self, clean_env: Any) -> None:
        """Test 'in' operator with existing variable."""
        os.environ["APP_DEBUG"] = "true"
        env = EnvPrefix("app")
        assert "debug" in env

    def test_contains_missing_variable(self, clean_env: Any) -> None:
        """Test 'in' operator with missing variable."""
        env = EnvPrefix("app")
        assert "debug" not in env

    def test_contains_separator_replacement(self, clean_env: Any) -> None:
        """Test 'in' operator with separator replacement."""
        os.environ["APP_API_KEY"] = "mykey"
        env = EnvPrefix("app")
        assert "api-key" in env
        assert "api.key" in env


class TestAllWithPrefix(FoundationTestCase):
    """Test all_with_prefix method."""

    def test_all_with_prefix_multiple_variables(self, clean_env: Any) -> None:
        """Test getting all variables with prefix."""
        os.environ["APP_DEBUG"] = "true"
        os.environ["APP_PORT"] = "8080"
        os.environ["APP_NAME"] = "myapp"
        os.environ["OTHER_VAR"] = "ignored"

        env = EnvPrefix("app")
        result = env.all_with_prefix()

        expected = {
            "DEBUG": "true",
            "PORT": "8080",
            "NAME": "myapp",
        }
        assert result == expected

    def test_all_with_prefix_no_variables(self, clean_env: Any) -> None:
        """Test getting all variables when none exist."""
        env = EnvPrefix("app")
        result = env.all_with_prefix()
        assert result == {}

    def test_all_with_prefix_custom_separator(self, clean_env: Any) -> None:
        """Test getting all variables with custom separator."""
        os.environ["APP:DEBUG"] = "true"
        os.environ["APP:PORT"] = "8080"
        os.environ["APP_OTHER"] = "ignored"  # Wrong separator

        env = EnvPrefix("app", separator=":")
        result = env.all_with_prefix()

        expected = {
            "DEBUG": "true",
            "PORT": "8080",
        }
        assert result == expected

    def test_all_with_prefix_overlapping_prefixes(self, clean_env: Any) -> None:
        """Test with overlapping prefixes."""
        os.environ["APP_DEBUG"] = "true"
        os.environ["APPA_DEBUG"] = "ignored"  # Similar but different prefix
        os.environ["AP_DEBUG"] = "ignored"  # Shorter prefix

        env = EnvPrefix("app")
        result = env.all_with_prefix()

        expected = {
            "DEBUG": "true",
        }
        assert result == expected

    def test_all_with_prefix_empty_prefix_part(self, clean_env: Any) -> None:
        """Test with prefix followed directly by separator."""
        os.environ["APP_"] = "empty_name"
        os.environ["APP_DEBUG"] = "true"

        env = EnvPrefix("app")
        result = env.all_with_prefix()

        expected = {
            "": "empty_name",
            "DEBUG": "true",
        }
        assert result == expected


# 🧱🏗️🔚
