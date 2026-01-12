#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for RuntimeConfigLoader and DictConfigLoader."""

from __future__ import annotations

import os
from typing import Any

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.config.base import BaseConfig
from provide.foundation.config.env import RuntimeConfig
from provide.foundation.config.loader import (
    DictConfigLoader,
    RuntimeConfigLoader,
)
from provide.foundation.config.types import ConfigSource


# Test configuration class (shared across test files)
class TestConfig(BaseConfig):
    """Test configuration class."""

    def __init__(self, name: str = "test", value: int = 42, enabled: bool = True) -> None:
        self.name = name
        self.value = value
        self.enabled = enabled

    @classmethod
    def from_dict(cls, data: dict[str, Any], source: ConfigSource = ConfigSource.RUNTIME) -> TestConfig:
        """Create config from dictionary."""
        # Use provided data or fallback to defaults
        return cls(
            name=data.get("name", "test"), value=data.get("value", 42), enabled=data.get("enabled", True)
        )

    def to_dict(self, include_sensitive: bool = False) -> dict[str, Any]:
        """Convert to dictionary."""
        return {"name": self.name, "value": self.value, "enabled": self.enabled}

    def get_source(self, key: str) -> ConfigSource | None:
        """Get source for a field."""
        # Only return source for fields that were actually set
        if key in ("name", "value", "enabled"):
            return ConfigSource.RUNTIME
        return None

    def update(
        self,
        updates: dict[str, str | int | float | bool | list[Any] | dict[str, Any] | None],
        source: ConfigSource = ConfigSource.RUNTIME,
    ) -> None:
        """Update configuration."""
        for key, value in updates.items():
            if hasattr(self, key):
                setattr(self, key, value)


class TestRuntimeConfig(RuntimeConfig):
    """Test runtime configuration class."""

    def __init__(self, name: str = "runtime", debug: bool = False) -> None:
        super().__init__()
        self.name = name
        self.debug = debug

    @classmethod
    def from_env(
        cls,
        prefix: str = "",
        delimiter: str = "_",
        case_sensitive: bool = False,
    ) -> TestRuntimeConfig:
        """Create from environment variables."""
        config = cls()
        prefix_key = f"{prefix}{delimiter}" if prefix else ""

        # Look for NAME and DEBUG env vars
        name_key = f"{prefix_key}NAME" if not case_sensitive else f"{prefix_key}name"
        debug_key = f"{prefix_key}DEBUG" if not case_sensitive else f"{prefix_key}debug"

        if name_key in os.environ:
            config.name = os.environ[name_key]
        if debug_key in os.environ:
            config.debug = os.environ[debug_key].lower() in ("true", "1", "yes")

        return config


class TestRuntimeConfigLoader(FoundationTestCase):
    """Test RuntimeConfigLoader class."""

    def test_init_defaults(self) -> None:
        """Test initialization with defaults."""
        loader = RuntimeConfigLoader()
        assert loader.prefix == ""
        assert loader.delimiter == "_"
        assert loader.case_sensitive is False

    def test_init_custom_values(self) -> None:
        """Test initialization with custom values."""
        loader = RuntimeConfigLoader(prefix="APP", delimiter="__", case_sensitive=True)
        assert loader.prefix == "APP"
        assert loader.delimiter == "__"
        assert loader.case_sensitive is True

    def test_exists_with_prefix(self) -> None:
        """Test exists with prefix."""
        with patch.dict(os.environ, {"TEST_NAME": "value"}):
            loader = RuntimeConfigLoader(prefix="TEST")
            assert loader.exists() is True

    def test_exists_without_prefix(self) -> None:
        """Test exists without prefix."""
        loader = RuntimeConfigLoader()
        # Should return True since environment always has some variables
        assert loader.exists() is True

    def test_exists_no_matching_vars(self) -> None:
        """Test exists when no matching variables found."""
        loader = RuntimeConfigLoader(prefix="NONEXISTENT")
        assert loader.exists() is False

    def test_load_runtime_config(self) -> None:
        """Test loading runtime configuration."""
        with patch.dict(os.environ, {"TEST_NAME": "runtime_test", "TEST_DEBUG": "true"}):
            loader = RuntimeConfigLoader(prefix="TEST")
            config = loader.load(TestRuntimeConfig)

            assert config.name == "runtime_test"
            assert config.debug is True

    def test_load_non_runtime_config_error(self) -> None:
        """Test error when config class is not RuntimeConfig."""
        loader = RuntimeConfigLoader()

        with pytest.raises(TypeError) as exc_info:
            loader.load(TestConfig)

        assert "must inherit from RuntimeConfig" in str(exc_info.value)


class TestDictConfigLoader(FoundationTestCase):
    """Test DictConfigLoader class."""

    def test_init_defaults(self) -> None:
        """Test initialization with defaults."""
        data: dict[str, Any] = {"name": "dict_test"}
        loader = DictConfigLoader(data)
        assert loader.data == data
        assert loader.source == ConfigSource.RUNTIME

    def test_init_custom_source(self) -> None:
        """Test initialization with custom source."""
        data: dict[str, Any] = {"name": "dict_test"}
        loader = DictConfigLoader(data, source=ConfigSource.FILE)
        assert loader.source == ConfigSource.FILE

    def test_exists_true(self) -> None:
        """Test exists returns True for non-None data."""
        loader = DictConfigLoader({"key": "value"})
        assert loader.exists() is True

    def test_exists_false(self) -> None:
        """Test exists returns False for None data."""
        loader = DictConfigLoader(None)  # type: ignore[arg-type]
        assert loader.exists() is False

    def test_load_config(self) -> None:
        """Test loading configuration from dictionary."""
        data: dict[str, Any] = {"name": "dict_config", "value": 500, "enabled": True}
        loader = DictConfigLoader(data)
        config = loader.load(TestConfig)

        assert config.name == "dict_config"
        assert config.value == 500
        assert config.enabled is True


# 🧱🏗️🔚
