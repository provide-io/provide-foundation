"""Comprehensive coverage tests for config manager module."""

import pytest
from unittest.mock import AsyncMock, Mock
from attrs import define

from provide.foundation.config.base import BaseConfig, field
from provide.foundation.config.manager import (
    ConfigManager,
    get_config,
    set_config,
    register_config,
    load_config,
    _manager,
)
from provide.foundation.config.loader import ConfigLoader
from provide.foundation.config.schema import ConfigSchema, SchemaField
from provide.foundation.config.types import ConfigSource, ConfigDict


@define
class TestConfigClass(BaseConfig):
    """Test configuration for comprehensive testing."""
    name: str = field(default="test_name")
    count: int = field(default=0)
    enabled: bool = field(default=False)
    data: str = field(default="")


@define
class AnotherTestConfig(BaseConfig):
    """Another test config class."""
    value: str = field(default="default")
    number: int = field(default=100)


class TestConfigManagerComprehensive:
    """Comprehensive tests for ConfigManager functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.manager = ConfigManager()
        self.test_config = TestConfigClass(name="test", count=5, enabled=True)
    
    @pytest.mark.asyncio
    async def test_register_with_all_components(self):
        """Test register with all components: config, schema, loader, defaults."""
        # Create schema
        schema = ConfigSchema([
            SchemaField("name", str, required=True),
            SchemaField("count", int, required=False)
        ])
        
        # Create loader
        loader = Mock(spec=ConfigLoader)
        loader.load = AsyncMock(return_value=self.test_config)
        
        # Create defaults
        defaults = {"name": "default_name", "count": 10}
        
        await self.manager.register(
            name="full_test",
            config=self.test_config,
            schema=schema,
            loader=loader,
            defaults=defaults
        )
        
        assert "full_test" in self.manager._configs
        assert "full_test" in self.manager._schemas
        assert "full_test" in self.manager._loaders
        assert "full_test" in self.manager._defaults
        assert self.manager._configs["full_test"] is self.test_config
        assert self.manager._schemas["full_test"] is schema
        assert self.manager._loaders["full_test"] is loader
        assert self.manager._defaults["full_test"] == defaults
    
    @pytest.mark.asyncio
    async def test_register_partial_components(self):
        """Test register with only some components."""
        schema = ConfigSchema([SchemaField("name", str)])
        
        await self.manager.register(name="partial", schema=schema)
        
        assert "partial" not in self.manager._configs
        assert "partial" in self.manager._schemas
        assert "partial" not in self.manager._loaders
        assert "partial" not in self.manager._defaults
    
    def test_unregister_config(self):
        """Test unregistering configuration and all associated components."""
        # Set up all components
        self.manager._configs["test"] = self.test_config
        self.manager._schemas["test"] = Mock()
        self.manager._loaders["test"] = Mock()
        self.manager._defaults["test"] = {}
        
        self.manager.unregister("test")
        
        assert "test" not in self.manager._configs
        assert "test" not in self.manager._schemas
        assert "test" not in self.manager._loaders
        assert "test" not in self.manager._defaults
    
    def test_remove_alias(self):
        """Test remove method as alias for unregister."""
        self.manager._configs["test"] = self.test_config
        
        self.manager.remove("test")
        
        assert "test" not in self.manager._configs
    
    @pytest.mark.asyncio
    async def test_get_existing_config(self):
        """Test getting existing configuration."""
        self.manager._configs["test"] = self.test_config
        
        result = await self.manager.get("test")
        
        assert result is self.test_config
    
    @pytest.mark.asyncio
    async def test_get_nonexistent_config(self):
        """Test getting non-existent configuration."""
        result = await self.manager.get("nonexistent")
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_set_config(self):
        """Test setting a configuration."""
        await self.manager.set("new_config", self.test_config)
        
        assert "new_config" in self.manager._configs
        assert self.manager._configs["new_config"] is self.test_config
    
    @pytest.mark.asyncio
    async def test_load_with_registered_loader(self):
        """Test loading configuration with registered loader."""
        # Set up loader
        loader = Mock(spec=ConfigLoader)
        loader.load = AsyncMock(return_value=self.test_config)
        self.manager._loaders["test"] = loader
        
        result = await self.manager.load("test", TestConfigClass)
        
        assert result is self.test_config
        loader.load.assert_called_once_with(TestConfigClass)
        assert self.manager._configs["test"] is self.test_config
    
    @pytest.mark.asyncio
    async def test_load_with_provided_loader(self):
        """Test loading configuration with provided loader."""
        loader = Mock(spec=ConfigLoader)
        loader.load = AsyncMock(return_value=self.test_config)
        
        result = await self.manager.load("test", TestConfigClass, loader=loader)
        
        assert result is self.test_config
        loader.load.assert_called_once_with(TestConfigClass)
    
    @pytest.mark.asyncio
    async def test_load_with_no_loader(self):
        """Test loading configuration with no loader available."""
        with pytest.raises(ValueError, match="No loader registered for configuration"):
            await self.manager.load("test", TestConfigClass)
    
    @pytest.mark.asyncio
    async def test_load_with_defaults(self):
        """Test loading configuration and applying defaults."""
        # Create config with None values for some fields
        config_with_nones = TestConfigClass(name="loaded", count=None, enabled=None)
        
        loader = Mock(spec=ConfigLoader)
        loader.load = AsyncMock(return_value=config_with_nones)
        
        defaults = {"count": 99, "enabled": True}
        self.manager._defaults["test"] = defaults
        
        result = await self.manager.load("test", TestConfigClass, loader=loader)
        
        assert result.name == "loaded"  # Original value preserved
        assert result.count == 99  # Default applied
        assert result.enabled is True  # Default applied
    
    @pytest.mark.asyncio
    async def test_load_with_schema_validation(self):
        """Test loading configuration with schema validation."""
        # Use Mock config instead of attrs class for method mocking
        mock_config = Mock(spec=BaseConfig)
        mock_config.to_dict = Mock(return_value={"name": "test", "count": 5})
        
        loader = Mock(spec=ConfigLoader)
        loader.load = AsyncMock(return_value=mock_config)
        
        # Mock schema validation
        schema = Mock(spec=ConfigSchema)
        schema.validate = AsyncMock()
        self.manager._schemas["test"] = schema
        
        result = await self.manager.load("test", TestConfigClass, loader=loader)
        
        schema.validate.assert_called_once()
        mock_config.to_dict.assert_called_once_with(include_sensitive=True)
        assert result is mock_config
    
    @pytest.mark.asyncio
    async def test_reload_config(self):
        """Test reloading an existing configuration."""
        # Set up existing config and loader
        old_config = TestConfigClass(name="old", count=1)
        new_config = TestConfigClass(name="new", count=2)
        
        loader = Mock(spec=ConfigLoader)
        loader.load = AsyncMock(return_value=new_config)
        
        self.manager._configs["test"] = old_config
        self.manager._loaders["test"] = loader
        
        result = await self.manager.reload("test")
        
        assert result is new_config
        assert self.manager._configs["test"] is new_config
        loader.load.assert_called_once_with(TestConfigClass)
    
    @pytest.mark.asyncio
    async def test_reload_nonexistent_config(self):
        """Test reloading a non-existent configuration."""
        with pytest.raises(ValueError, match="Configuration not found"):
            await self.manager.reload("nonexistent")
    
    @pytest.mark.asyncio
    async def test_reload_no_loader(self):
        """Test reloading with no loader registered."""
        self.manager._configs["test"] = self.test_config
        
        with pytest.raises(ValueError, match="No loader registered for configuration"):
            await self.manager.reload("test")
    
    @pytest.mark.asyncio
    async def test_reload_with_defaults(self):
        """Test reloading with defaults application."""
        old_config = TestConfigClass(name="old")
        new_config = TestConfigClass(name="new", count=None)
        
        loader = Mock(spec=ConfigLoader)
        loader.load = AsyncMock(return_value=new_config)
        
        defaults = {"count": 50}
        self.manager._configs["test"] = old_config
        self.manager._loaders["test"] = loader
        self.manager._defaults["test"] = defaults
        
        result = await self.manager.reload("test")
        
        assert result.count == 50  # Default applied
    
    @pytest.mark.asyncio
    async def test_reload_with_schema_validation(self):
        """Test reloading with schema validation."""
        old_config = TestConfigClass(name="old")
        
        # Use Mock for new config to allow method mocking
        new_config = Mock(spec=BaseConfig)
        new_config.to_dict = Mock(return_value={"name": "new", "count": 0})
        
        loader = Mock(spec=ConfigLoader)
        loader.load = AsyncMock(return_value=new_config)
        
        schema = Mock(spec=ConfigSchema)
        schema.validate = AsyncMock()
        
        self.manager._configs["test"] = old_config
        self.manager._loaders["test"] = loader
        self.manager._schemas["test"] = schema
        
        result = await self.manager.reload("test")
        
        schema.validate.assert_called_once()
        new_config.to_dict.assert_called_once_with(include_sensitive=True)
        assert result is new_config
    
    @pytest.mark.asyncio
    async def test_update_config(self):
        """Test updating a configuration."""
        mock_config = Mock(spec=BaseConfig)
        mock_config.update = Mock()
        
        self.manager._configs["test"] = mock_config
        
        updates = {"name": "updated", "count": 10}
        
        await self.manager.update("test", updates, ConfigSource.RUNTIME)
        
        mock_config.update.assert_called_once_with(updates, ConfigSource.RUNTIME)
    
    @pytest.mark.asyncio
    async def test_update_nonexistent_config(self):
        """Test updating non-existent configuration."""
        with pytest.raises(ValueError, match="Configuration not found"):
            await self.manager.update("nonexistent", {})
    
    @pytest.mark.asyncio
    async def test_update_with_schema_validation(self):
        """Test updating configuration with schema validation."""
        # Create schema with field validation
        field_mock = Mock()
        field_mock.validate = AsyncMock()
        
        schema = Mock(spec=ConfigSchema)
        schema._field_map = {"name": field_mock}
        
        mock_config = Mock(spec=BaseConfig)
        mock_config.update = Mock()
        
        self.manager._configs["test"] = mock_config
        self.manager._schemas["test"] = schema
        
        updates = {"name": "validated"}
        
        await self.manager.update("test", updates)
        
        field_mock.validate.assert_called_once_with("validated")
        mock_config.update.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_reset_config(self):
        """Test resetting configuration to defaults."""
        mock_config = Mock(spec=BaseConfig)
        mock_config.reset_to_defaults = Mock()
        mock_config.update = Mock()
        
        self.manager._configs["test"] = mock_config
        
        defaults = {"name": "reset_name", "count": 0}
        self.manager._defaults["test"] = defaults
        
        await self.manager.reset("test")
        
        mock_config.reset_to_defaults.assert_called_once()
        mock_config.update.assert_called_once_with(defaults, ConfigSource.DEFAULT)
    
    @pytest.mark.asyncio
    async def test_reset_nonexistent_config(self):
        """Test resetting non-existent configuration."""
        with pytest.raises(ValueError, match="Configuration not found"):
            await self.manager.reset("nonexistent")
    
    def test_list_configs(self):
        """Test listing all configurations."""
        self.manager._configs["config1"] = Mock()
        self.manager._configs["config2"] = Mock()
        
        result = self.manager.list_configs()
        
        assert set(result) == {"config1", "config2"}
    
    def test_get_all_configs(self):
        """Test getting all configurations."""
        config1 = Mock()
        config2 = Mock()
        
        self.manager._configs["config1"] = config1
        self.manager._configs["config2"] = config2
        
        result = self.manager.get_all()
        
        assert result == {"config1": config1, "config2": config2}
        # Should be a copy, not the same dict
        assert result is not self.manager._configs
    
    def test_clear_all(self):
        """Test clearing all configurations and associated data."""
        self.manager._configs["test"] = Mock()
        self.manager._schemas["test"] = Mock()
        self.manager._loaders["test"] = Mock()
        self.manager._defaults["test"] = Mock()
        
        self.manager.clear()
        
        assert len(self.manager._configs) == 0
        assert len(self.manager._schemas) == 0
        assert len(self.manager._loaders) == 0
        assert len(self.manager._defaults) == 0
    
    @pytest.mark.asyncio
    async def test_export_config(self):
        """Test exporting configuration as dictionary."""
        mock_config = Mock(spec=BaseConfig)
        mock_config.to_dict = Mock(return_value={"name": "test", "count": 5})
        self.manager._configs["test"] = mock_config
        
        result = await self.manager.export("test", include_sensitive=True)
        
        mock_config.to_dict.assert_called_once_with(True)
        assert result == {"name": "test", "count": 5}
    
    @pytest.mark.asyncio
    async def test_export_nonexistent_config(self):
        """Test exporting non-existent configuration."""
        with pytest.raises(ValueError, match="Configuration not found"):
            await self.manager.export("nonexistent")
    
    @pytest.mark.asyncio
    async def test_export_all_configs(self):
        """Test exporting all configurations."""
        config1 = Mock()
        config1.to_dict = Mock(return_value={"key1": "value1"})
        config2 = Mock()
        config2.to_dict = Mock(return_value={"key2": "value2"})
        
        self.manager._configs["config1"] = config1
        self.manager._configs["config2"] = config2
        
        result = await self.manager.export_all(include_sensitive=False)
        
        config1.to_dict.assert_called_once_with(False)
        config2.to_dict.assert_called_once_with(False)
        assert result == {"config1": {"key1": "value1"}, "config2": {"key2": "value2"}}
    
    @pytest.mark.asyncio
    async def test_export_to_dict_alias(self):
        """Test export_to_dict as alias for export_all."""
        config1 = Mock()
        config1.to_dict = Mock(return_value={"key1": "value1"})
        
        self.manager._configs["config1"] = config1
        
        result = await self.manager.export_to_dict(include_sensitive=True)
        
        config1.to_dict.assert_called_once_with(True)
        assert result == {"config1": {"key1": "value1"}}
    
    @pytest.mark.asyncio
    async def test_load_from_dict(self):
        """Test loading configuration from dictionary."""
        data = {"name": "from_dict", "count": 42}
        
        result = await self.manager.load_from_dict("test", TestConfigClass, data)
        
        assert isinstance(result, TestConfigClass)
        assert result.name == "from_dict"
        assert result.count == 42
        assert self.manager._configs["test"] is result
    
    def test_add_loader(self):
        """Test adding a loader for configuration."""
        loader = Mock(spec=ConfigLoader)
        
        self.manager.add_loader("test", loader)
        
        assert self.manager._loaders["test"] is loader
    
    @pytest.mark.asyncio
    async def test_validate_all_configs(self):
        """Test validating all configurations."""
        # Config with validate method
        config1 = Mock()
        config1.validate = AsyncMock()
        config1.to_dict = Mock(return_value={"key": "value"})
        
        # Config without validate method
        config2 = Mock(spec=[])
        config2.to_dict = Mock(return_value={"key2": "value2"})
        
        # Schema with validate method
        schema1 = Mock()
        schema1.validate = AsyncMock()
        
        # Schema without validate method  
        schema2 = Mock(spec=[])
        
        self.manager._configs["config1"] = config1
        self.manager._configs["config2"] = config2
        self.manager._schemas["config1"] = schema1
        self.manager._schemas["config2"] = schema2
        
        await self.manager.validate_all()
        
        config1.validate.assert_called_once()
        schema1.validate.assert_called_once_with({"key": "value"})
        # config2 and schema2 validate methods should not be called
    
    @pytest.mark.asyncio
    async def test_get_or_create_existing(self):
        """Test get_or_create with existing configuration."""
        existing_config = TestConfigClass(name="existing")
        self.manager._configs["test"] = existing_config
        
        result = await self.manager.get_or_create("test", TestConfigClass, {"name": "new"})
        
        assert result is existing_config
        assert result.name == "existing"  # Should not be overwritten
    
    @pytest.mark.asyncio
    async def test_get_or_create_new(self):
        """Test get_or_create creating new configuration."""
        defaults = {"name": "created", "count": 100}
        
        result = await self.manager.get_or_create("new_test", TestConfigClass, defaults)
        
        assert isinstance(result, TestConfigClass)
        assert result.name == "created"
        assert result.count == 100
        assert self.manager._configs["new_test"] is result
    
    @pytest.mark.asyncio
    async def test_get_or_create_no_defaults(self):
        """Test get_or_create with no defaults provided."""
        result = await self.manager.get_or_create("empty_test", TestConfigClass)
        
        assert isinstance(result, TestConfigClass)
        assert result.name == "test_name"  # Default from class
        assert self.manager._configs["empty_test"] is result


class TestGlobalFunctions:
    """Test global configuration manager functions."""
    
    def setup_method(self):
        """Set up test environment."""
        # Reset global manager
        _manager.clear()
        self.test_config = TestConfigClass(name="global_test")
    
    @pytest.mark.asyncio
    async def test_get_config_global(self):
        """Test global get_config function."""
        _manager._configs["test"] = self.test_config
        
        result = await get_config("test")
        
        assert result is self.test_config
    
    @pytest.mark.asyncio
    async def test_set_config_global(self):
        """Test global set_config function."""
        await set_config("test", self.test_config)
        
        assert _manager._configs["test"] is self.test_config
    
    @pytest.mark.asyncio
    async def test_register_config_global(self):
        """Test global register_config function."""
        schema = Mock(spec=ConfigSchema)
        loader = Mock(spec=ConfigLoader)
        defaults = {"name": "default"}
        
        await register_config("test", self.test_config, schema, loader, defaults)
        
        assert _manager._configs["test"] is self.test_config
        assert _manager._schemas["test"] is schema
        assert _manager._loaders["test"] is loader
        assert _manager._defaults["test"] == defaults
    
    @pytest.mark.asyncio
    async def test_load_config_global(self):
        """Test global load_config function."""
        loader = Mock(spec=ConfigLoader)
        loader.load = AsyncMock(return_value=self.test_config)
        
        result = await load_config("test", TestConfigClass, loader)
        
        assert result is self.test_config
        loader.load.assert_called_once_with(TestConfigClass)