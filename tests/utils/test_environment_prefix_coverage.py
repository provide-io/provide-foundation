"""Comprehensive tests for utils/environment/prefix.py module."""

from __future__ import annotations

from collections.abc import Generator
import os
from pathlib import Path
from typing import Any

from provide.testkit import reset_foundation_setup_for_testing
import pytest

from provide.foundation.errors.config import ValidationError
from provide.foundation.utils.environment.prefix import EnvPrefix


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


class TestEnvPrefixInit:
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


class TestMakeName:
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


class TestGetBool:
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


class TestGetInt:
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


class TestGetFloat:
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


class TestGetStr:
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


class TestGetPath:
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


class TestGetList:
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


class TestGetDict:
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


class TestRequire:
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


class TestSubscriptNotation:
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


class TestContains:
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


class TestAllWithPrefix:
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


class TestIntegrationScenarios:
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


class TestEdgeCases:
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


class TestModuleIntegration:
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
