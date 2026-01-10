#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for FileConfigLoader."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch
import pytest

from provide.foundation.config.base import BaseConfig
from provide.foundation.config.loader import FileConfigLoader
from provide.foundation.config.types import ConfigFormat, ConfigSource
from provide.foundation.errors.config import ConfigurationError
from provide.foundation.errors.resources import NotFoundError


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


class TestFileConfigLoader(FoundationTestCase):
    """Test FileConfigLoader class."""

    def test_init_with_explicit_format(self) -> None:
        """Test initialization with explicit format."""
        loader = FileConfigLoader("config.json", format=ConfigFormat.JSON)
        assert loader.format == ConfigFormat.JSON
        assert loader.path == Path("config.json")
        assert loader.encoding == "utf-8"

    def test_init_auto_detect_format(self) -> None:
        """Test automatic format detection."""
        loader = FileConfigLoader("config.yaml")
        assert loader.format == ConfigFormat.YAML

    def test_init_unknown_format_error(self) -> None:
        """Test error for unknown format."""
        with pytest.raises(ConfigurationError) as exc_info:
            FileConfigLoader("config.unknown")

        assert "Cannot determine format" in str(exc_info.value)
        assert exc_info.value.code == "CONFIG_FORMAT_UNKNOWN"

    def test_exists_true(self, tmp_path: Path) -> None:
        """Test exists returns True for existing file."""
        config_file = tmp_path / "config.json"
        config_file.write_text("{}")

        loader = FileConfigLoader(config_file)
        assert loader.exists() is True

    def test_exists_false(self) -> None:
        """Test exists returns False for non-existent file."""
        loader = FileConfigLoader("nonexistent.json")
        assert loader.exists() is False

    def test_load_json_file(self, tmp_path: Path) -> None:
        """Test loading JSON configuration."""
        config_file = tmp_path / "config.json"
        data = {"name": "json_test", "value": 100, "enabled": False}
        config_file.write_text(json.dumps(data))

        loader = FileConfigLoader(config_file)
        config = loader.load(TestConfig)

        assert config.name == "json_test"
        assert config.value == 100
        assert config.enabled is False

    def test_load_yaml_file(self, tmp_path: Path) -> None:
        """Test loading YAML configuration."""
        pytest.importorskip("yaml")

        config_file = tmp_path / "config.yaml"
        config_file.write_text("name: yaml_test\nvalue: 200\nenabled: true\n")

        loader = FileConfigLoader(config_file)
        config = loader.load(TestConfig)

        assert config.name == "yaml_test"
        assert config.value == 200
        assert config.enabled is True

    def test_load_toml_file(self, tmp_path: Path) -> None:
        """Test loading TOML configuration."""
        config_file = tmp_path / "config.toml"
        config_file.write_text('name = "toml_test"\nvalue = 300\nenabled = false\n')

        loader = FileConfigLoader(config_file)
        config = loader.load(TestConfig)

        assert config.name == "toml_test"
        assert config.value == 300
        assert config.enabled is False

    def test_load_ini_file(self, tmp_path: Path) -> None:
        """Test loading INI configuration."""
        config_file = tmp_path / "config.ini"
        config_file.write_text("[section1]\nkey1 = value1\nkey2 = value2\n")

        loader = FileConfigLoader(config_file)
        data = loader._read_file()

        assert "section1" in data
        section1 = cast(dict[str, Any], data["section1"])
        assert section1["key1"] == "value1"
        assert section1["key2"] == "value2"

    def test_load_env_file(self, tmp_path: Path) -> None:
        """Test loading .env file."""
        config_file = tmp_path / "config.env"
        config_file.write_text('NAME="env_test"\nVALUE=400\nENABLED=true\n# Comment\n\n')

        loader = FileConfigLoader(config_file)
        data = loader._read_file()

        assert data["name"] == "env_test"  # Lowercase conversion
        assert data["value"] == "400"
        assert data["enabled"] == "true"

    def test_load_file_not_found_error(self) -> None:
        """Test error when file not found."""
        loader = FileConfigLoader("nonexistent.json")

        with pytest.raises(NotFoundError) as exc_info:
            loader.load(TestConfig)

        assert "Configuration file not found" in str(exc_info.value)
        assert exc_info.value.code == "CONFIG_FILE_NOT_FOUND"

    def test_load_empty_file_error(self, tmp_path: Path) -> None:
        """Test error when file is empty."""
        config_file = tmp_path / "empty.json"
        config_file.write_text("")

        loader = FileConfigLoader(config_file)

        with pytest.raises(ConfigurationError) as exc_info:
            loader.load(TestConfig)

        assert "Failed to read config file" in str(exc_info.value)
        assert exc_info.value.code == "CONFIG_READ_ERROR"

    def test_load_unsupported_format_error(self, tmp_path: Path) -> None:
        """Test error for unsupported format."""
        config_file = tmp_path / "config.json"
        config_file.write_text("{}")

        loader = FileConfigLoader(config_file)
        loader.format = "UNSUPPORTED"  # type: ignore[assignment]

        with pytest.raises(ConfigurationError) as exc_info:
            loader.load(TestConfig)

        assert "Unsupported format" in str(exc_info.value)
        assert exc_info.value.code == "CONFIG_FORMAT_UNSUPPORTED"

    @patch("provide.foundation.file.safe.safe_read_text")
    def test_load_resilient_decorator(self, mock_read: Mock, tmp_path: Path) -> None:
        """Test resilient decorator catches errors."""
        config_file = tmp_path / "config.json"

        # Don't write the file, just patch the read function
        mock_read.side_effect = OSError("File read error")

        loader = FileConfigLoader(config_file)

        # Mock the exists method to return True so we get to the read error
        with patch.object(loader, "exists", return_value=True):
            with pytest.raises(ConfigurationError) as exc_info:
                loader.load(TestConfig)

            assert "Failed to read config file" in str(exc_info.value)
            assert exc_info.value.code == "CONFIG_READ_ERROR"

    def test_parse_env_file_with_quotes(self, tmp_path: Path) -> None:
        """Test parsing .env file with quoted values."""
        config_file = tmp_path / "config.env"
        config_file.write_text("QUOTED_DOUBLE=\"value with spaces\"\nQUOTED_SINGLE='single quotes'\n")

        loader = FileConfigLoader(config_file)
        data = loader._read_file()

        assert data["quoted_double"] == "value with spaces"
        assert data["quoted_single"] == "single quotes"

    def test_ini_to_dict_with_defaults(self, tmp_path: Path) -> None:
        """Test INI to dict conversion with DEFAULT section."""
        config_file = tmp_path / "config.ini"
        config_file.write_text("[DEFAULT]\ndefault_key = default_value\n[section1]\nkey1 = value1\n")

        loader = FileConfigLoader(config_file)
        data = loader._read_file()

        assert "DEFAULT" in data
        default_section = cast(dict[str, Any], data["DEFAULT"])
        section1 = cast(dict[str, Any], data["section1"])
        assert default_section["default_key"] == "default_value"
        assert section1["key1"] == "value1"


# 🧱🏗️🔚
