"""Tests for configuration manager."""

from __future__ import annotations

from unittest.mock import AsyncMock

from attrs import define
import pytest

from provide.foundation.config.base import BaseConfig
from provide.foundation.config.manager import ConfigManager


@define
class SampleConfig(BaseConfig):
    """Sample configuration class for testing."""

    name: str = "test"
    value: int = 42
    enabled: bool = True


class SampleConfigManager:
    """Test ConfigManager class."""

    async def test_init_manager(self) -> None:
        """Test initializing config manager."""
        manager = ConfigManager()
        assert manager._configs == {}
        assert manager._loaders == {}
        assert manager._schemas == {}
        assert manager._defaults == {}

    async def test_register_config(self) -> None:
        """Test registering a configuration."""
        manager = ConfigManager()
        config = SampleConfig()

        await manager.register("test", config)

        assert "test" in manager._configs
        assert manager._configs["test"] is config

    async def test_get_config(self) -> None:
        """Test getting a configuration."""
        manager = ConfigManager()
        config = SampleConfig()

        await manager.register("test", config)
        retrieved = await manager.get("test")

        assert retrieved is config

    async def test_get_config_not_found(self) -> None:
        """Test getting non-existent configuration."""
        manager = ConfigManager()

        result = await manager.get("nonexistent")
        assert result is None

    async def test_get_config_with_type(self) -> None:
        """Test getting configuration with type checking."""
        manager = ConfigManager()
        config = SampleConfig()

        await manager.register("test", config)
        retrieved = await manager.get("test")

        assert retrieved is config
        assert isinstance(retrieved, SampleConfig)

    async def test_get_all_configs(self) -> None:
        """Test getting all configurations."""
        manager = ConfigManager()
        config1 = SampleConfig(name="config1")
        config2 = SampleConfig(name="config2")

        await manager.register("test1", config1)
        await manager.register("test2", config2)

        all_configs = manager.get_all()
        assert len(all_configs) == 2
        assert all_configs["test1"] is config1
        assert all_configs["test2"] is config2

    async def test_remove_config(self) -> None:
        """Test removing a configuration."""
        manager = ConfigManager()
        config = SampleConfig()

        await manager.register("test", config)
        manager.remove("test")  # remove is sync

        assert "test" not in manager._configs

    async def test_clear_configs(self) -> None:
        """Test clearing all configurations."""
        manager = ConfigManager()
        await manager.register("test1", SampleConfig())
        await manager.register("test2", SampleConfig())

        manager.clear()  # clear is sync

        assert len(manager._configs) == 0

    async def test_load_from_dict(self) -> None:
        """Test loading configuration from dictionary."""
        manager = ConfigManager()

        data = {"name": "updated", "value": 100}
        config = await manager.load_from_dict("test", SampleConfig, data)

        assert config is not None
        assert config.name == "updated"
        assert config.value == 100

    async def test_export_to_dict(self) -> None:
        """Test exporting configuration to dictionary."""
        manager = ConfigManager()
        config = SampleConfig(name="export_test", value=99)
        await manager.register("test", config)

        exported = await manager.export_to_dict()

        assert "test" in exported
        assert exported["test"]["name"] == "export_test"
        assert exported["test"]["value"] == 99

    async def test_reload_configs(self) -> None:
        """Test reloading configurations."""
        manager = ConfigManager()

        # Mock loader
        mock_loader = AsyncMock()
        mock_loader.load.return_value = SampleConfig(name="reloaded")
        manager.add_loader("test", mock_loader)

        config = SampleConfig()
        await manager.register("test", config)

        await manager.reload("test")

        mock_loader.load.assert_called_once()
        # Get the reloaded config
        reloaded = await manager.get("test")
        assert reloaded.name == "reloaded"

    def test_validate_all(self) -> None:
        """Test validating all configurations."""
        manager = ConfigManager()

        config1 = AsyncMock(spec=SampleConfig)
        config2 = AsyncMock(spec=SampleConfig)

        await manager.register("test1", config1)
        await manager.register("test2", config2)

        manager.validate_all()

        config1.validate.assert_called_once()
        config2.validate.assert_called_once()

    async def test_get_or_create(self) -> None:
        """Test get_or_create method."""
        manager = ConfigManager()

        # First call creates
        config1 = await manager.get_or_create("test", SampleConfig)
        assert config1 is not None
        assert isinstance(config1, SampleConfig)

        # Second call gets existing
        config2 = await manager.get_or_create("test", SampleConfig)
        assert config2 is config1

    async def test_update_config(self) -> None:
        """Test updating a configuration."""
        manager = ConfigManager()
        config = SampleConfig()
        await manager.register("test", config)

        await manager.update("test", {"name": "updated", "value": 200})

        assert config.name == "updated"
        assert config.value == 200
