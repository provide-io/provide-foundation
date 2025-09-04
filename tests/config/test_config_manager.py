"""Tests for configuration manager."""

from __future__ import annotations

from pathlib import Path
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from provide.foundation.config.manager import ConfigManager
from provide.foundation.config.base import BaseConfig
from provide.foundation.config.types import ConfigDict, ConfigSource
from attrs import define


@define
class TestConfig(BaseConfig):
    """Test configuration class."""
    
    name: str = "test"
    value: int = 42
    enabled: bool = True


class TestConfigManager:
    """Test ConfigManager class."""

    @pytest.mark.asyncio
    async def test_init_manager(self) -> None:
        """Test initializing config manager."""
        manager = ConfigManager()
        assert manager._configs == {}
        assert manager._loaders == {}
        assert manager._schemas == {}
        assert manager._defaults == {}

    @pytest.mark.asyncio
    async def test_register_config(self) -> None:
        """Test registering a configuration."""
        manager = ConfigManager()
        config = TestConfig()
        
        await manager.register("test", config)
        
        assert "test" in manager._configs
        assert manager._configs["test"] is config

    @pytest.mark.asyncio
    async def test_get_config(self) -> None:
        """Test getting a configuration."""
        manager = ConfigManager()
        config = TestConfig()
        
        await manager.register("test", config)
        retrieved = await manager.get("test")
        
        assert retrieved is config

    @pytest.mark.asyncio
    async def test_get_config_not_found(self) -> None:
        """Test getting non-existent configuration."""
        manager = ConfigManager()
        
        result = await manager.get("nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_config_with_type(self) -> None:
        """Test getting configuration with type checking."""
        manager = ConfigManager()
        config = TestConfig()
        
        await manager.register("test", config)
        retrieved = await manager.get("test")
        
        assert retrieved is config
        assert isinstance(retrieved, TestConfig)

    @pytest.mark.asyncio
    async def test_get_all_configs(self) -> None:
        """Test getting all configurations."""
        manager = ConfigManager()
        config1 = TestConfig(name="config1")
        config2 = TestConfig(name="config2")
        
        await manager.register("test1", config1)
        await manager.register("test2", config2)
        
        all_configs = manager.get_all()
        assert len(all_configs) == 2
        assert all_configs["test1"] is config1
        assert all_configs["test2"] is config2

    @pytest.mark.asyncio
    async def test_remove_config(self) -> None:
        """Test removing a configuration."""
        manager = ConfigManager()
        config = TestConfig()
        
        await manager.register("test", config)
        manager.remove("test")  # remove is sync
        
        assert "test" not in manager._configs

    @pytest.mark.asyncio
    async def test_clear_configs(self) -> None:
        """Test clearing all configurations."""
        manager = ConfigManager()
        await manager.register("test1", TestConfig())
        await manager.register("test2", TestConfig())
        
        manager.clear()  # clear is sync
        
        assert len(manager._configs) == 0

    @pytest.mark.asyncio
    async def test_load_from_dict(self) -> None:
        """Test loading configuration from dictionary."""
        manager = ConfigManager()
        
        data = {"name": "updated", "value": 100}
        config = await manager.load_from_dict("test", TestConfig, data)
        
        assert config is not None
        assert config.name == "updated"
        assert config.value == 100

    @pytest.mark.asyncio
    async def test_export_to_dict(self) -> None:
        """Test exporting configuration to dictionary."""
        manager = ConfigManager()
        config = TestConfig(name="export_test", value=99)
        await manager.register("test", config)
        
        exported = await manager.export_to_dict()
        
        assert "test" in exported
        assert exported["test"]["name"] == "export_test"
        assert exported["test"]["value"] == 99

    @pytest.mark.asyncio
    async def test_reload_configs(self) -> None:
        """Test reloading configurations."""
        manager = ConfigManager()
        
        # Mock loader
        mock_loader = AsyncMock()
        mock_loader.load.return_value = {"test": {"name": "reloaded"}}
        manager.add_loader(mock_loader)
        
        config = TestConfig()
        manager.register("test", config)
        
        await manager.reload()
        
        mock_loader.load.assert_called_once()
        assert config.name == "reloaded"

    @pytest.mark.asyncio
    async def test_validate_all(self) -> None:
        """Test validating all configurations."""
        manager = ConfigManager()
        
        config1 = AsyncMock(spec=TestConfig)
        config2 = AsyncMock(spec=TestConfig)
        
        manager.register("test1", config1)
        manager.register("test2", config2)
        
        await manager.validate_all()
        
        config1.validate.assert_called_once()
        config2.validate.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_or_create(self) -> None:
        """Test get_or_create method."""
        manager = ConfigManager()
        
        # First call creates
        config1 = await manager.get_or_create("test", TestConfig)
        assert config1 is not None
        assert isinstance(config1, TestConfig)
        
        # Second call gets existing
        config2 = await manager.get_or_create("test", TestConfig)
        assert config2 is config1

    @pytest.mark.asyncio
    async def test_update_config(self) -> None:
        """Test updating a configuration."""
        manager = ConfigManager()
        config = TestConfig()
        await manager.register("test", config)
        
        await manager.update("test", {"name": "updated", "value": 200})
        
        assert config.name == "updated"
        assert config.value == 200