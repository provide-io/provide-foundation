#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for EnvPrefix numeric getter methods."""

from __future__ import annotations

from collections.abc import Generator
import os
from pathlib import Path
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


class TestGetStr(FoundationTestCase):
    """Test get_str method."""

    def test_get_str_existing_variable(self, clean_env: Any) -> None:
        """Test getting existing string variable."""
        os.environ["APP_NAME"] = "myapp"
        env = EnvPrefix("app")
        assert env.get_str("name") == "myapp"

    def test_get_str_missing_variable_with_default(self, clean_env: Any) -> None:
        """Test getting missing variable with default."""
        env = EnvPrefix("app")
        assert env.get_str("name", default="default") == "default"

    def test_get_str_missing_variable_no_default(self, clean_env: Any) -> None:
        """Test getting missing variable without default."""
        env = EnvPrefix("app")
        assert env.get_str("name") is None


class TestGetPath(FoundationTestCase):
    """Test get_path method."""

    def test_get_path_existing_variable(self, clean_env: Any) -> None:
        """Test getting existing path variable."""
        os.environ["APP_CONFIG_PATH"] = "/etc/app/config"
        env = EnvPrefix("app")
        result = env.get_path("config_path")
        assert result == Path("/etc/app/config")

    def test_get_path_missing_variable_with_default(self, clean_env: Any) -> None:
        """Test getting missing variable with default."""
        env = EnvPrefix("app")
        default_path = Path("/default/path")
        result = env.get_path("config_path", default=default_path)
        assert result == default_path

    def test_get_path_missing_variable_no_default(self, clean_env: Any) -> None:
        """Test getting missing variable without default."""
        env = EnvPrefix("app")
        assert env.get_path("config_path") is None

    def test_get_path_with_string_default(self, clean_env: Any) -> None:
        """Test getting path with string default."""
        env = EnvPrefix("app")
        result = env.get_path("config_path", default="/default/path")
        assert result == Path("/default/path")


# 🧱🏗️🔚
