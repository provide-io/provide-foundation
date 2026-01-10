#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for EnvPrefix integration scenarios and edge cases."""

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


class TestIntegrationScenarios(FoundationTestCase):
    """Test integration scenarios."""

    def test_real_world_configuration_scenario(self, clean_env: Any) -> None:
        """Test a real-world configuration scenario."""
        # Set up a typical application configuration
        os.environ["MYAPP_DEBUG"] = "true"
        os.environ["MYAPP_DATABASE_URL"] = "postgres://localhost/mydb"
        os.environ["MYAPP_CACHE_TTL"] = "300"
        os.environ["MYAPP_ALLOWED_HOSTS"] = "localhost,127.0.0.1,example.com"
        os.environ["MYAPP_FEATURE_FLAGS"] = "feature1=on,feature2=off"

        env = EnvPrefix("myapp")

        # Test various getter methods
        assert env.get_bool("debug") is True
        assert env.get_str("database-url") == "postgres://localhost/mydb"
        assert env.get_int("cache.ttl") == 300
        assert env.get_list("allowed_hosts") == ["localhost", "127.0.0.1", "example.com"]
        assert env.get_dict("feature_flags") == {"feature1": "on", "feature2": "off"}

        # Test subscript access
        assert env["database-url"] == "postgres://localhost/mydb"

        # Test containment
        assert "debug" in env
        assert "nonexistent" not in env

        # Test getting all variables
        all_vars = env.all_with_prefix()
        assert len(all_vars) == 5
        assert "DEBUG" in all_vars
        assert "DATABASE_URL" in all_vars

    def test_multiple_prefixes_isolated(self, clean_env: Any) -> None:
        """Test that multiple prefixes work independently."""
        os.environ["APP1_DEBUG"] = "true"
        os.environ["APP2_DEBUG"] = "false"
        os.environ["APP1_PORT"] = "8080"
        os.environ["APP2_PORT"] = "9090"

        env1 = EnvPrefix("app1")
        env2 = EnvPrefix("app2")

        assert env1.get_bool("debug") is True
        assert env2.get_bool("debug") is False
        assert env1.get_int("port") == 8080
        assert env2.get_int("port") == 9090

        # Each should only see their own variables
        all_vars1 = env1.all_with_prefix()
        all_vars2 = env2.all_with_prefix()

        assert len(all_vars1) == 2
        assert len(all_vars2) == 2
        assert all_vars1["DEBUG"] == "true"
        assert all_vars2["DEBUG"] == "false"

    def test_error_propagation(self, clean_env: Any) -> None:
        """Test that errors from underlying getters propagate correctly."""
        os.environ["APP_INVALID_INT"] = "not_a_number"

        env = EnvPrefix("app")

        # ValidationError should propagate from get_int
        with pytest.raises(ValidationError):
            env.get_int("invalid_int")


class TestEdgeCases(FoundationTestCase):
    """Test edge cases and boundary conditions."""

    def test_empty_prefix(self, clean_env: Any) -> None:
        """Test with empty prefix."""
        os.environ["_DEBUG"] = "true"
        env = EnvPrefix("", separator="_")
        assert env.get_bool("debug") is True

    def test_prefix_only_separator(self, clean_env: Any) -> None:
        """Test with prefix that's only separator characters."""
        os.environ["___DEBUG"] = "true"
        env = EnvPrefix("__", separator="_")
        assert env.get_bool("debug") is True

    def test_special_characters_in_names(self, clean_env: Any) -> None:
        """Test handling of special characters in variable names."""
        os.environ["APP_VAR_WITH_NUMBERS123"] = "value"
        env = EnvPrefix("app")
        assert env.get_str("var_with_numbers123") == "value"

    def test_unicode_handling(self, clean_env: Any) -> None:
        """Test basic unicode handling in values."""
        os.environ["APP_UNICODE"] = "café"
        env = EnvPrefix("app")
        assert env.get_str("unicode") == "café"


class TestModuleIntegration(FoundationTestCase):
    """Test module-level integration."""

    def test_class_importable(self) -> None:
        """Test that EnvPrefix class is importable."""
        from provide.foundation.utils.environment.prefix import EnvPrefix

        assert EnvPrefix is not None
        assert callable(EnvPrefix)

    def test_type_var_importable(self) -> None:
        """Test that TypeVar is properly imported."""
        from provide.foundation.utils.environment.prefix import T

        # Just verify it exists and is a TypeVar
        assert T is not None
        assert hasattr(T, "__name__")


# 🧱🏗️🔚
