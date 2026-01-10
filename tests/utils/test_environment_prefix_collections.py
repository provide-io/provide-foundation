#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for EnvPrefix collection getter methods."""

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


class TestGetList(FoundationTestCase):
    """Test get_list method."""

    def test_get_list_existing_variable(self, clean_env: Any) -> None:
        """Test getting existing list variable."""
        os.environ["APP_HOSTS"] = "host1,host2,host3"
        env = EnvPrefix("app")
        assert env.get_list("hosts") == ["host1", "host2", "host3"]

    def test_get_list_missing_variable_with_default(self, clean_env: Any) -> None:
        """Test getting missing variable with default."""
        env = EnvPrefix("app")
        default_list = ["default1", "default2"]
        assert env.get_list("hosts", default=default_list) == default_list

    def test_get_list_missing_variable_no_default(self, clean_env: Any) -> None:
        """Test getting missing variable without default."""
        env = EnvPrefix("app")
        assert env.get_list("hosts") == []

    def test_get_list_custom_separator(self, clean_env: Any) -> None:
        """Test getting list with custom separator."""
        os.environ["APP_HOSTS"] = "host1:host2:host3"
        env = EnvPrefix("app")
        assert env.get_list("hosts", separator=":") == ["host1", "host2", "host3"]


class TestGetDict(FoundationTestCase):
    """Test get_dict method."""

    def test_get_dict_existing_variable(self, clean_env: Any) -> None:
        """Test getting existing dict variable."""
        os.environ["APP_TAGS"] = "env=prod,version=1.0"
        env = EnvPrefix("app")
        assert env.get_dict("tags") == {"env": "prod", "version": "1.0"}

    def test_get_dict_missing_variable_with_default(self, clean_env: Any) -> None:
        """Test getting missing variable with default."""
        env = EnvPrefix("app")
        default_dict = {"default": "value"}
        assert env.get_dict("tags", default=default_dict) == default_dict

    def test_get_dict_missing_variable_no_default(self, clean_env: Any) -> None:
        """Test getting missing variable without default."""
        env = EnvPrefix("app")
        assert env.get_dict("tags") == {}

    def test_get_dict_custom_separators(self, clean_env: Any) -> None:
        """Test getting dict with custom separators."""
        os.environ["APP_TAGS"] = "env:prod;version:1.0"
        env = EnvPrefix("app")
        result = env.get_dict("tags", item_separator=";", key_value_separator=":")
        assert result == {"env": "prod", "version": "1.0"}


# 🧱🏗️🔚
