#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for environment variable utilities."""

from pathlib import Path

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.errors import ValidationError
from provide.foundation.utils.environment import (
    EnvPrefix,
    get_bool,
    get_dict,
    get_float,
    get_int,
    get_list,
    get_path,
    get_str,
    parse_duration,
    parse_size,
    require,
)


class TestBasicGetters(FoundationTestCase):
    """Test basic environment variable getters."""

    def test_get_bool(self, monkeypatch) -> None:
        """Test boolean parsing."""
        # True values
        for value in ["true", "True", "1", "yes", "YES", "on", "ON", "enabled"]:
            monkeypatch.setenv("TEST_BOOL", value)
            assert get_bool("TEST_BOOL") is True

        # False values
        for value in ["false", "False", "0", "no", "NO", "off", "OFF", "disabled"]:
            monkeypatch.setenv("TEST_BOOL", value)
            assert get_bool("TEST_BOOL") is False

        # Empty string returns None with warning
        monkeypatch.setenv("TEST_BOOL", "")
        assert get_bool("TEST_BOOL") is None

        # Invalid value
        monkeypatch.setenv("TEST_BOOL", "invalid")
        with pytest.raises(ValidationError) as exc_info:
            get_bool("TEST_BOOL")
        assert "Invalid boolean value" in str(exc_info.value)

        # Missing with default
        monkeypatch.delenv("TEST_BOOL", raising=False)
        assert get_bool("TEST_BOOL", True) is True
        assert get_bool("TEST_BOOL", False) is False
        assert get_bool("TEST_BOOL") is None

    def test_get_int(self, monkeypatch) -> None:
        """Test integer parsing."""
        monkeypatch.setenv("TEST_INT", "42")
        assert get_int("TEST_INT") == 42

        monkeypatch.setenv("TEST_INT", "-100")
        assert get_int("TEST_INT") == -100

        monkeypatch.setenv("TEST_INT", "0")
        assert get_int("TEST_INT") == 0

        # Invalid value
        monkeypatch.setenv("TEST_INT", "not_a_number")
        with pytest.raises(ValidationError) as exc_info:
            get_int("TEST_INT")
        assert "Invalid integer value" in str(exc_info.value)

        # Missing with default
        monkeypatch.delenv("TEST_INT", raising=False)
        assert get_int("TEST_INT", 99) == 99
        assert get_int("TEST_INT") is None

    def test_get_float(self, monkeypatch) -> None:
        """Test float parsing."""
        monkeypatch.setenv("TEST_FLOAT", "3.14")
        assert get_float("TEST_FLOAT") == 3.14

        monkeypatch.setenv("TEST_FLOAT", "-2.5")
        assert get_float("TEST_FLOAT") == -2.5

        monkeypatch.setenv("TEST_FLOAT", "0")
        assert get_float("TEST_FLOAT") == 0.0

        # Scientific notation
        monkeypatch.setenv("TEST_FLOAT", "1.23e-4")
        assert get_float("TEST_FLOAT") == 1.23e-4

        # Invalid value
        monkeypatch.setenv("TEST_FLOAT", "not_a_float")
        with pytest.raises(ValidationError) as exc_info:
            get_float("TEST_FLOAT")
        assert "Invalid float value" in str(exc_info.value)

        # Missing with default
        monkeypatch.delenv("TEST_FLOAT", raising=False)
        assert get_float("TEST_FLOAT", 1.5) == 1.5
        assert get_float("TEST_FLOAT") is None

    def test_get_str(self, monkeypatch) -> None:
        """Test string getter."""
        monkeypatch.setenv("TEST_STR", "hello world")
        assert get_str("TEST_STR") == "hello world"

        monkeypatch.setenv("TEST_STR", "")
        assert get_str("TEST_STR") == ""

        # Missing with default
        monkeypatch.delenv("TEST_STR", raising=False)
        assert get_str("TEST_STR", "default") == "default"
        assert get_str("TEST_STR") is None

    def test_get_path(self, monkeypatch) -> None:
        """Test path parsing."""
        monkeypatch.setenv("TEST_PATH", "/tmp/test")
        path = get_path("TEST_PATH")
        assert path == Path("/tmp/test")

        # User expansion
        monkeypatch.setenv("TEST_PATH", "~/test")
        path = get_path("TEST_PATH")
        assert str(path).startswith(str(Path.home()))

        # Environment variable expansion
        monkeypatch.setenv("BASE_DIR", "/base")
        monkeypatch.setenv("TEST_PATH", "$BASE_DIR/test")
        path = get_path("TEST_PATH")
        assert path == Path("/base/test")

        # Missing with default
        monkeypatch.delenv("TEST_PATH", raising=False)
        assert get_path("TEST_PATH", "/default") == Path("/default")
        assert get_path("TEST_PATH", Path("/default")) == Path("/default")
        assert get_path("TEST_PATH") is None

    def test_get_list(self, monkeypatch) -> None:
        """Test list parsing."""
        monkeypatch.setenv("TEST_LIST", "a,b,c")
        assert get_list("TEST_LIST") == ["a", "b", "c"]

        # With spaces
        monkeypatch.setenv("TEST_LIST", "a, b , c")
        assert get_list("TEST_LIST") == ["a", "b", "c"]

        # Custom separator
        monkeypatch.setenv("TEST_LIST", "a:b:c")
        assert get_list("TEST_LIST", separator=":") == ["a", "b", "c"]

        # Empty string
        monkeypatch.setenv("TEST_LIST", "")
        assert get_list("TEST_LIST") == []

        # Empty items filtered
        monkeypatch.setenv("TEST_LIST", "a,,b,")
        assert get_list("TEST_LIST") == ["a", "b"]

        # Missing with default
        monkeypatch.delenv("TEST_LIST", raising=False)
        assert get_list("TEST_LIST", ["x", "y"]) == ["x", "y"]
        assert get_list("TEST_LIST") == []

    def test_get_dict(self, monkeypatch) -> None:
        """Test dictionary parsing."""
        monkeypatch.setenv("TEST_DICT", "key1=val1,key2=val2")
        assert get_dict("TEST_DICT") == {"key1": "val1", "key2": "val2"}

        # With spaces
        monkeypatch.setenv("TEST_DICT", "key1 = val1 , key2 = val2")
        assert get_dict("TEST_DICT") == {"key1": "val1", "key2": "val2"}

        # Custom separators
        monkeypatch.setenv("TEST_DICT", "key1:val1;key2:val2")
        assert get_dict("TEST_DICT", item_separator=";", key_value_separator=":") == {
            "key1": "val1",
            "key2": "val2",
        }

        # Empty string
        monkeypatch.setenv("TEST_DICT", "")
        assert get_dict("TEST_DICT") == {}

        # Invalid items logged but skipped
        monkeypatch.setenv("TEST_DICT", "key1=val1,invalid,key2=val2")
        result = get_dict("TEST_DICT")
        assert result == {"key1": "val1", "key2": "val2"}

        # Missing with default
        monkeypatch.delenv("TEST_DICT", raising=False)
        assert get_dict("TEST_DICT", {"a": "b"}) == {"a": "b"}
        assert get_dict("TEST_DICT") == {}


class TestRequire(FoundationTestCase):
    """Test require function."""

    def test_require_present(self, monkeypatch) -> None:
        """Test requiring present variable."""
        monkeypatch.setenv("REQUIRED", "value")
        assert require("REQUIRED") == "value"

    def test_require_missing(self, monkeypatch) -> None:
        """Test requiring missing variable."""
        monkeypatch.delenv("REQUIRED", raising=False)
        with pytest.raises(ValidationError) as exc_info:
            require("REQUIRED")
        assert "Required environment variable not set" in str(exc_info.value)

    def test_require_with_type(self, monkeypatch) -> None:
        """Test requiring with type hints."""
        monkeypatch.setenv("REQUIRED", "true")
        assert require("REQUIRED", bool) is True

        monkeypatch.setenv("REQUIRED", "42")
        assert require("REQUIRED", int) == 42

        monkeypatch.setenv("REQUIRED", "3.14")
        assert require("REQUIRED", float) == 3.14

        monkeypatch.setenv("REQUIRED", "hello")
        assert require("REQUIRED", str) == "hello"

        monkeypatch.setenv("REQUIRED", "/tmp")
        assert require("REQUIRED", Path) == Path("/tmp")

        monkeypatch.setenv("REQUIRED", "a,b,c")
        assert require("REQUIRED", list[str]) == ["a", "b", "c"]

        monkeypatch.setenv("REQUIRED", "k=v")
        assert require("REQUIRED", dict[str, str]) == {"k": "v"}


class TestEnvPrefix(FoundationTestCase):
    """Test EnvPrefix class."""

    def test_prefix_basic(self, monkeypatch) -> None:
        """Test basic prefix functionality."""
        env = EnvPrefix("MYAPP")

        monkeypatch.setenv("MYAPP_DEBUG", "true")
        assert env.get_bool("debug") is True
        assert env.get_bool("DEBUG") is True

        monkeypatch.setenv("MYAPP_PORT", "8080")
        assert env.get_int("port") == 8080

        monkeypatch.setenv("MYAPP_HOST", "localhost")
        assert env.get_str("host") == "localhost"

    def test_prefix_subscript(self, monkeypatch) -> None:
        """Test subscript notation."""
        env = EnvPrefix("TEST")

        monkeypatch.setenv("TEST_KEY", "value")
        assert env["key"] == "value"
        assert "key" in env

        monkeypatch.delenv("TEST_KEY")
        assert env["key"] is None
        assert "key" not in env

    def test_prefix_name_normalization(self, monkeypatch) -> None:
        """Test name normalization."""
        env = EnvPrefix("APP")

        monkeypatch.setenv("APP_SOME_KEY", "value")
        assert env.get_str("some-key") == "value"
        assert env.get_str("some.key") == "value"
        assert env.get_str("some_key") == "value"

    def test_prefix_all_with_prefix(self, monkeypatch) -> None:
        """Test getting all variables with prefix."""
        env = EnvPrefix("PREFIX")

        monkeypatch.setenv("PREFIX_VAR1", "val1")
        monkeypatch.setenv("PREFIX_VAR2", "val2")
        monkeypatch.setenv("OTHER_VAR", "val3")

        all_vars = env.all_with_prefix()
        assert all_vars == {"VAR1": "val1", "VAR2": "val2"}

    def test_prefix_custom_separator(self, monkeypatch) -> None:
        """Test custom separator."""
        env = EnvPrefix("APP", separator="__")

        monkeypatch.setenv("APP__DEBUG", "true")
        assert env.get_bool("debug") is True


class TestParsers(FoundationTestCase):
    """Test parsing functions."""

    def test_parse_duration(self) -> None:
        """Test duration parsing."""
        assert parse_duration("30") == 30
        assert parse_duration("30s") == 30
        assert parse_duration("5m") == 300
        assert parse_duration("2h") == 7200
        assert parse_duration("1d") == 86400

        # Combined
        assert parse_duration("1h30m") == 5400
        assert parse_duration("1d2h3m4s") == 93784

        # Case insensitive
        assert parse_duration("1H30M") == 5400

        # Invalid
        with pytest.raises(ValidationError) as exc_info:
            parse_duration("invalid")
        assert "Invalid duration format" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            parse_duration("10x")
        # Since 'x' is not a valid unit, the regex won't match at all
        assert "Invalid duration format" in str(exc_info.value)

    def test_parse_size(self) -> None:
        """Test size parsing."""
        assert parse_size("1024") == 1024
        assert parse_size("1KB") == 1024
        assert parse_size("1K") == 1024
        assert parse_size("10MB") == 10 * 1024 * 1024
        assert parse_size("10M") == 10 * 1024 * 1024
        assert parse_size("1GB") == 1024**3
        assert parse_size("1G") == 1024**3
        assert parse_size("1TB") == 1024**4
        assert parse_size("1T") == 1024**4

        # With decimals
        assert parse_size("1.5GB") == int(1.5 * 1024**3)

        # With spaces
        assert parse_size("10 MB") == 10 * 1024 * 1024

        # Case insensitive
        assert parse_size("10mb") == 10 * 1024 * 1024

        # Invalid
        with pytest.raises(ValidationError) as exc_info:
            parse_size("invalid")
        assert "Invalid size format" in str(exc_info.value)

        # Test completely invalid format (XB is not in the units dict)
        with pytest.raises(ValidationError) as exc_info:
            parse_size("invalid")
        assert "Invalid size format" in str(exc_info.value)


# 🧱🏗️🔚
