#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for environment variable configuration."""

from __future__ import annotations

from attrs import define
from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.config.base import field
from provide.foundation.config.env import (
    RuntimeConfig,
    env_field,
    get_env,
)
from provide.foundation.parsers import (
    parse_bool,
    parse_dict,
    parse_list,
)


class TestEnvUtilities(FoundationTestCase):
    """Test environment variable utilities."""

    def test_get_env_existing(self, monkeypatch) -> None:
        """Test getting existing environment variable."""
        monkeypatch.setenv("TEST_VAR", "test_value")
        assert get_env("TEST_VAR") == "test_value"

    def test_get_env_missing_with_default(self) -> None:
        """Test getting missing variable with default."""
        assert get_env("MISSING_VAR", default="default") == "default"

    def test_get_env_missing_required(self) -> None:
        """Test getting missing required variable."""
        with pytest.raises(ValueError, match="Required environment variable"):
            get_env("MISSING_VAR", required=True)

    def test_get_env_file_secret(self, tmp_path, monkeypatch) -> None:
        """Test reading secret from file."""
        secret_file = tmp_path / "secret.txt"
        secret_file.write_text("secret_value\n")

        monkeypatch.setenv("SECRET_VAR", f"file://{secret_file}")
        assert get_env("SECRET_VAR") == "secret_value"

    def test_get_env_file_secret_missing(self, monkeypatch) -> None:
        """Test reading secret from missing file."""
        monkeypatch.setenv("SECRET_VAR", "file:///nonexistent/file")

        with pytest.raises(ValueError, match="Failed to read secret"):
            get_env("SECRET_VAR")

    def test_parse_bool_true_values(self) -> None:
        """Test parsing true boolean values."""
        assert parse_bool("true") is True
        assert parse_bool("True") is True
        assert parse_bool("TRUE") is True
        assert parse_bool("1") is True
        assert parse_bool("yes") is True
        assert parse_bool("on") is True
        assert parse_bool("enabled") is True
        assert parse_bool(True) is True

    def test_parse_bool_false_values(self) -> None:
        """Test parsing false boolean values."""
        assert parse_bool("false") is False
        assert parse_bool("False") is False
        assert parse_bool("FALSE") is False
        assert parse_bool("0") is False
        assert parse_bool("no") is False
        assert parse_bool("off") is False
        assert parse_bool("disabled") is False
        assert parse_bool(False) is False

    def test_parse_bool_invalid(self) -> None:
        """Test parsing invalid boolean values."""
        with pytest.raises(ValueError):
            parse_bool("invalid")

    def test_parse_list_from_string(self) -> None:
        """Test parsing list from string."""
        assert parse_list("a,b,c") == ["a", "b", "c"]
        assert parse_list("a, b, c") == ["a", "b", "c"]
        assert parse_list("") == []

    def test_parse_list_from_list(self) -> None:
        """Test parsing list from list."""
        assert parse_list(["a", "b", "c"]) == ["a", "b", "c"]

    def test_parse_list_custom_separator(self) -> None:
        """Test parsing list with custom separator."""
        assert parse_list("a|b|c", separator="|") == ["a", "b", "c"]

    def test_parse_list_no_strip(self) -> None:
        """Test parsing list without stripping."""
        assert parse_list("a , b , c ", strip=False) == ["a ", " b ", " c "]

    def test_parse_dict_from_string(self) -> None:
        """Test parsing dictionary from string."""
        assert parse_dict("key1=value1,key2=value2") == {
            "key1": "value1",
            "key2": "value2",
        }

    def test_parse_dict_from_dict(self) -> None:
        """Test parsing dictionary from dictionary."""
        d = {"key1": "value1"}
        assert parse_dict(d) == d

    def test_parse_dict_empty(self) -> None:
        """Test parsing empty dictionary."""
        assert parse_dict("") == {}

    def test_parse_dict_custom_separators(self) -> None:
        """Test parsing dictionary with custom separators."""
        assert parse_dict("key1:value1;key2:value2", ";", ":") == {
            "key1": "value1",
            "key2": "value2",
        }

    def test_parse_dict_invalid(self) -> None:
        """Test parsing invalid dictionary."""
        with pytest.raises(ValueError, match="Invalid dict format"):
            parse_dict("invalid_format")


@define
class TestRuntimeConfig(RuntimeConfig):
    """Test configuration that loads from environment."""

    app_name: str = env_field(default="test_app")
    port: int = env_field(default=8080, parser=int)
    debug: bool = env_field(default=False, parser=parse_bool)
    hosts: list[str] = env_field(factory=list, parser=parse_list)
    metadata: dict[str, str] = env_field(factory=dict, parser=parse_dict)
    custom_var: str = env_field(env_var="CUSTOM_ENV_VAR", default="")


class TestRuntimeConfigClass(FoundationTestCase):
    """Test RuntimeConfig class functionality."""

    def test_from_env_with_prefix(self, monkeypatch) -> None:
        """Test loading from environment with prefix."""
        monkeypatch.setenv("TEST_APP_NAME", "my_app")
        monkeypatch.setenv("TEST_PORT", "3000")
        monkeypatch.setenv("TEST_DEBUG", "true")
        monkeypatch.setenv("TEST_HOSTS", "host1,host2")
        monkeypatch.setenv("TEST_METADATA", "key1=val1,key2=val2")

        config = TestRuntimeConfig.from_env(prefix="TEST")

        assert config.app_name == "my_app"
        assert config.port == 3000
        assert config.debug is True
        assert config.hosts == ["host1", "host2"]
        assert config.metadata == {"key1": "val1", "key2": "val2"}

    def test_from_env_custom_var(self, monkeypatch) -> None:
        """Test loading with custom environment variable name."""
        monkeypatch.setenv("CUSTOM_ENV_VAR", "custom_value")

        config = TestRuntimeConfig.from_env()
        assert config.custom_var == "custom_value"

    def test_from_env_defaults(self) -> None:
        """Test loading with default values."""
        config = TestRuntimeConfig.from_env()

        assert config.app_name == "test_app"
        assert config.port == 8080
        assert config.debug is False
        assert config.hosts == []
        assert config.metadata == {}

    def test_to_env_dict(self) -> None:
        """Test converting to environment variable dictionary."""
        config = TestRuntimeConfig(
            app_name="my_app",
            port=3000,
            debug=True,
            hosts=["host1", "host2"],
            metadata={"key": "value"},
        )

        env_dict = config.to_env_dict(prefix="APP")

        assert env_dict["APP_APP_NAME"] == "my_app"
        assert env_dict["APP_PORT"] == "3000"
        assert env_dict["APP_DEBUG"] == "true"
        assert env_dict["APP_HOSTS"] == "host1,host2"
        assert env_dict["APP_METADATA"] == "key=value"

    def test_to_env_dict_custom_delimiter(self) -> None:
        """Test converting with custom delimiter."""
        config = TestRuntimeConfig(app_name="test")
        env_dict = config.to_env_dict(prefix="APP", delimiter="__")

        assert "APP__APP_NAME" in env_dict

    def test_auto_parse_types(self, monkeypatch) -> None:
        """Test automatic type parsing."""

        @define
        class AutoParseConfig(RuntimeConfig):
            str_val: str = field(default="")
            int_val: int = field(default=0)
            float_val: float = field(default=0.0)
            bool_val: bool = field(default=False)

        monkeypatch.setenv("STR_VAL", "test")
        monkeypatch.setenv("INT_VAL", "42")
        monkeypatch.setenv("FLOAT_VAL", "3.14")
        monkeypatch.setenv("BOOL_VAL", "true")

        config = AutoParseConfig.from_env()

        assert config.str_val == "test"
        assert config.int_val == 42
        assert config.float_val == 3.14
        assert config.bool_val is True


# 🧱🏗️🔚
