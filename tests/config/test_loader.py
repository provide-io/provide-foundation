"""Tests for configuration loaders."""

from __future__ import annotations

import json
import pytest
from pathlib import Path
from attrs import define

from provide.foundation.config.base import BaseConfig, field
from provide.foundation.config.env import EnvConfig, env_field, parse_bool
from provide.foundation.config.loader import (
    ChainedLoader,
    DictConfigLoader,
    EnvConfigLoader,
    FileConfigLoader,
    MultiSourceLoader,
)
from provide.foundation.config.types import ConfigFormat, ConfigSource


@define
class TestConfig(BaseConfig):
    """Test configuration."""

    name: str = field(default="test")
    port: int = field(default=8080)
    debug: bool = field(default=False)


@define
class TestEnvConfig(EnvConfig):
    """Test environment configuration."""

    name: str = env_field(default="test")
    port: int = env_field(default=8080, parser=int)
    debug: bool = env_field(default=False, parser=parse_bool)


class TestFileConfigLoader:
    """Test FileConfigLoader."""

    def test_load_json(self, tmp_path):
        """Test loading JSON configuration."""
        config_file = tmp_path / "config.json"
        config_file.write_text(
            json.dumps({"name": "json_config", "port": 3000, "debug": True})
        )

        loader = FileConfigLoader(config_file)
        assert loader.exists()

        config = loader.load(TestConfig)
        assert config.name == "json_config"
        assert config.port == 3000
        assert config.debug is True
        assert config.get_source("name") == ConfigSource.FILE

    def test_load_yaml(self, tmp_path):
        """Test loading YAML configuration."""
        pytest.importorskip("yaml")

        config_file = tmp_path / "config.yaml"
        config_file.write_text("""
name: yaml_config
port: 4000
debug: true
""")

        loader = FileConfigLoader(config_file)
        config = loader.load(TestConfig)

        assert config.name == "yaml_config"
        assert config.port == 4000
        assert config.debug is True

    def test_load_toml(self, tmp_path):
        """Test loading TOML configuration."""
        config_file = tmp_path / "config.toml"
        config_file.write_text("""
name = "toml_config"
port = 5000
debug = false
""")

        loader = FileConfigLoader(config_file)
        config = loader.load(TestConfig)

        assert config.name == "toml_config"
        assert config.port == 5000
        assert config.debug is False

    def test_load_env_file(self, tmp_path):
        """Test loading .env file configuration."""
        config_file = tmp_path / ".env"
        config_file.write_text("""
# Comment line
NAME=env_config
PORT=6000
DEBUG=true

# Another comment
EXTRA_VAR="quoted value"
""")

        loader = FileConfigLoader(config_file)
        config = loader.load(TestConfig)

        # Note: .env files return string values, need proper parsing
        assert config.name == "env_config"

    def test_auto_detect_format(self, tmp_path):
        """Test automatic format detection."""
        json_file = tmp_path / "config.json"
        json_file.write_text('{"name": "test"}')

        loader = FileConfigLoader(json_file)
        assert loader.format == ConfigFormat.JSON

    def test_unknown_format(self, tmp_path):
        """Test error with unknown format."""
        config_file = tmp_path / "config.unknown"
        config_file.touch()

        with pytest.raises(ValueError, match="Cannot determine format"):
            FileConfigLoader(config_file)

    @pytest.mark.asyncio
    async def test_file_not_found(self, tmp_path):
        """Test error when file doesn't exist."""
        loader = FileConfigLoader(tmp_path / "nonexistent.json")
        assert not loader.exists()

        with pytest.raises(FileNotFoundError):
            await loader.load(TestConfig)


class TestEnvConfigLoader:
    """Test EnvConfigLoader."""

    def test_load_with_prefix(self, monkeypatch):
        """Test loading with prefix."""
        monkeypatch.setenv("APP_NAME", "env_app")
        monkeypatch.setenv("APP_PORT", "7000")
        monkeypatch.setenv("APP_DEBUG", "true")

        loader = EnvConfigLoader(prefix="APP")
        assert loader.exists()

        config = loader.load(TestEnvConfig)
        assert config.name == "env_app"
        assert config.port == 7000
        assert config.debug is True

    def test_load_without_prefix(self, monkeypatch):
        """Test loading without prefix."""
        monkeypatch.setenv("NAME", "no_prefix")
        monkeypatch.setenv("PORT", "8000")

        loader = EnvConfigLoader()
        config = loader.load(TestEnvConfig)

        assert config.name == "no_prefix"
        assert config.port == 8000

    def test_non_env_config(self):
        """Test error with non-EnvConfig class."""
        loader = EnvConfigLoader()

        with pytest.raises(TypeError, match="must inherit from EnvConfig"):
            loader.load(TestConfig)


class TestDictConfigLoader:
    """Test DictConfigLoader."""

    @pytest.mark.asyncio
    async def test_load_from_dict(self):
        """Test loading from dictionary."""
        data = {"name": "dict_config", "port": 9000, "debug": True}

        loader = DictConfigLoader(data)
        assert loader.exists()

        config = await loader.load(TestConfig)
        assert config.name == "dict_config"
        assert config.port == 9000
        assert config.debug is True
        assert await config.get_source("name") == ConfigSource.RUNTIME

    @pytest.mark.asyncio
    async def test_custom_source(self):
        """Test with custom source."""
        loader = DictConfigLoader({}, source=ConfigSource.DEFAULT)
        config = await loader.load(TestConfig)
        assert await config.get_source("name") is None  # Uses default values


class TestMultiSourceLoader:
    """Test MultiSourceLoader."""

    @pytest.mark.asyncio
    async def test_merge_multiple_sources(self, tmp_path, monkeypatch):
        """Test merging from multiple sources."""
        # File source
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({"name": "file_name", "port": 3000}))

        # Environment source
        monkeypatch.setenv("PORT", "4000")
        monkeypatch.setenv("DEBUG", "true")

        # Create loaders
        file_loader = FileConfigLoader(config_file)
        env_loader = EnvConfigLoader()
        dict_loader = DictConfigLoader({"name": "runtime_name"})

        # Multi-source loader (order matters - later overrides earlier)
        loader = MultiSourceLoader(file_loader, env_loader, dict_loader)
        assert loader.exists()

        config = await loader.load(TestEnvConfig)

        # Should have merged values with proper precedence
        assert config.name == "runtime_name"  # From dict (last)
        assert config.port == 4000  # From env
        assert config.debug is True  # From env

    @pytest.mark.asyncio
    async def test_no_sources_available(self):
        """Test error when no sources exist."""
        loader = MultiSourceLoader()
        assert not loader.exists()

        with pytest.raises(ValueError, match="No configuration sources"):
            await loader.load(TestConfig)


class TestChainedLoader:
    """Test ChainedLoader."""

    @pytest.mark.asyncio
    async def test_first_available_source(self, tmp_path):
        """Test loading from first available source."""
        # Create two config files
        primary = tmp_path / "primary.json"
        fallback = tmp_path / "fallback.json"

        primary.write_text(json.dumps({"name": "primary"}))
        fallback.write_text(json.dumps({"name": "fallback"}))

        # Chain loaders
        loader = ChainedLoader(FileConfigLoader(primary), FileConfigLoader(fallback))

        config = await loader.load(TestConfig)
        assert config.name == "primary"  # From first available

    @pytest.mark.asyncio
    async def test_fallback_source(self, tmp_path):
        """Test falling back when primary doesn't exist."""
        primary = tmp_path / "nonexistent.json"
        fallback = tmp_path / "fallback.json"
        fallback.write_text(json.dumps({"name": "fallback"}))

        loader = ChainedLoader(FileConfigLoader(primary), FileConfigLoader(fallback))

        config = await loader.load(TestConfig)
        assert config.name == "fallback"

    @pytest.mark.asyncio
    async def test_no_source_available(self, tmp_path):
        """Test error when no source is available."""
        loader = ChainedLoader(
            FileConfigLoader(tmp_path / "missing1.json"),
            FileConfigLoader(tmp_path / "missing2.json"),
        )

        assert not loader.exists()

        with pytest.raises(ValueError, match="No configuration source"):
            await loader.load(TestConfig)
