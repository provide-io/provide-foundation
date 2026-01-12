#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive coverage tests for config manager module."""

from attrs import define
from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock
import pytest

from provide.foundation.config.base import BaseConfig, field
from provide.foundation.config.loader import ConfigLoader
from provide.foundation.config.manager import (
    ConfigManager,
)
from provide.foundation.config.schema import ConfigSchema, SchemaField
from provide.foundation.config.types import ConfigSource


@define
class SampleConfigClass(BaseConfig):
    """Sample configuration class for testing."""

    name: str = field(default="test")
    count: int | None = field(default=None)
    enabled: bool = field(default=False)


class TestConfigManagerComprehensive(FoundationTestCase):
    """Comprehensive tests for ConfigManager functionality."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.manager = ConfigManager()
        self.test_config = SampleConfigClass(name="test", count=5, enabled=True)

    def test_register_with_all_components(self) -> None:
        """Test register with all components: config, schema, loader, defaults."""
        # Create schema
        schema = ConfigSchema(
            [
                SchemaField("name", str, required=True),
                SchemaField("count", int, required=False),
            ],
        )

        # Create loader
        loader = Mock(spec=ConfigLoader)
        loader.load = Mock(return_value=self.test_config)

        # Create defaults
        defaults = {"name": "default_name", "count": 10}

        self.manager.register(
            name="full_test",
            config=self.test_config,
            schema=schema,
            loader=loader,
            defaults=defaults,
        )

        assert "full_test" in self.manager._configs
        assert "full_test" in self.manager._schemas
        assert "full_test" in self.manager._loaders
        assert "full_test" in self.manager._defaults
        assert self.manager._configs["full_test"] is self.test_config
        assert self.manager._schemas["full_test"] is schema
        assert self.manager._loaders["full_test"] is loader
        assert self.manager._defaults["full_test"] == defaults

    def test_register_partial_components(self) -> None:
        """Test register with only some components."""
        schema = ConfigSchema([SchemaField("name", str)])

        self.manager.register(name="partial", schema=schema)

        assert "partial" not in self.manager._configs
        assert "partial" in self.manager._schemas
        assert "partial" not in self.manager._loaders
        assert "partial" not in self.manager._defaults

    def test_unregister_config(self) -> None:
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

    def test_remove_alias(self) -> None:
        """Test remove method as alias for unregister."""
        self.manager._configs["test"] = self.test_config

        self.manager.remove("test")

        assert "test" not in self.manager._configs

    def test_get_existing_config(self) -> None:
        """Test getting existing configuration."""
        self.manager._configs["test"] = self.test_config

        result = self.manager.get("test")

        assert result is self.test_config

    def test_get_nonexistent_config(self) -> None:
        """Test getting non-existent configuration."""
        result = self.manager.get("nonexistent")

        assert result is None

    def test_set_config(self) -> None:
        """Test setting a configuration."""
        self.manager.set("new_config", self.test_config)

        assert "new_config" in self.manager._configs
        assert self.manager._configs["new_config"] is self.test_config

    def test_load_with_registered_loader(self) -> None:
        """Test loading configuration with registered loader."""
        # Set up loader
        loader = Mock(spec=ConfigLoader)
        loader.load = Mock(return_value=self.test_config)
        self.manager._loaders["test"] = loader

        result = self.manager.load("test", SampleConfigClass)

        assert result is self.test_config
        loader.load.assert_called_once_with(SampleConfigClass)
        assert self.manager._configs["test"] is self.test_config

    def test_load_with_provided_loader(self) -> None:
        """Test loading configuration with provided loader."""
        loader = Mock(spec=ConfigLoader)
        loader.load = Mock(return_value=self.test_config)

        result = self.manager.load("test", SampleConfigClass, loader=loader)

        assert result is self.test_config
        loader.load.assert_called_once_with(SampleConfigClass)

    def test_load_with_no_loader(self) -> None:
        """Test loading configuration with no loader available."""
        with pytest.raises(ValueError, match="No loader registered for configuration"):
            self.manager.load("test", SampleConfigClass)

    def test_load_with_defaults(self) -> None:
        """Test loading configuration and applying defaults."""
        # Create config with None values for some fields
        config_with_nones = SampleConfigClass(name="loaded", count=None, enabled=None)

        loader = Mock(spec=ConfigLoader)
        loader.load = Mock(return_value=config_with_nones)

        defaults = {"count": 99, "enabled": True}
        self.manager._defaults["test"] = defaults

        result = self.manager.load("test", SampleConfigClass, loader=loader)

        assert result.name == "loaded"  # Original value preserved
        assert result.count == 99  # Default applied
        assert result.enabled is True  # Default applied

    def test_load_with_schema_validation(self) -> None:
        """Test loading configuration with schema validation."""
        # Use Mock config instead of attrs class for method mocking
        mock_config = Mock(spec=BaseConfig)
        mock_config.to_dict = Mock(return_value={"name": "test", "count": 5})

        loader = Mock(spec=ConfigLoader)
        loader.load = Mock(return_value=mock_config)

        # Mock schema validation
        schema = Mock(spec=ConfigSchema)
        schema.validate = Mock()
        self.manager._schemas["test"] = schema

        result = self.manager.load("test", SampleConfigClass, loader=loader)

        schema.validate.assert_called_once()
        mock_config.to_dict.assert_called_once_with(include_sensitive=True)
        assert result is mock_config

    def test_reload_config(self) -> None:
        """Test reloading an existing configuration."""
        # Set up existing config and loader
        old_config = SampleConfigClass(name="old", count=1)
        new_config = SampleConfigClass(name="new", count=2)

        loader = Mock(spec=ConfigLoader)
        loader.load = Mock(return_value=new_config)

        self.manager._configs["test"] = old_config
        self.manager._loaders["test"] = loader

        result = self.manager.reload("test")

        assert result is new_config
        assert self.manager._configs["test"] is new_config
        loader.load.assert_called_once_with(SampleConfigClass)

    def test_reload_nonexistent_config(self) -> None:
        """Test reloading a non-existent configuration."""
        with pytest.raises(ValueError, match="Configuration not found"):
            self.manager.reload("nonexistent")

    def test_reload_no_loader(self) -> None:
        """Test reloading with no loader registered."""
        self.manager._configs["test"] = self.test_config

        with pytest.raises(ValueError, match="No loader registered for configuration"):
            self.manager.reload("test")

    def test_reload_with_defaults(self) -> None:
        """Test reloading with defaults application."""
        old_config = SampleConfigClass(name="old")
        new_config = SampleConfigClass(name="new", count=None)

        loader = Mock(spec=ConfigLoader)
        loader.load = Mock(return_value=new_config)

        defaults = {"count": 50}
        self.manager._configs["test"] = old_config
        self.manager._loaders["test"] = loader
        self.manager._defaults["test"] = defaults

        result = self.manager.reload("test")

        assert result.count == 50  # Default applied

    def test_reload_with_schema_validation(self) -> None:
        """Test reloading with schema validation."""
        old_config = SampleConfigClass(name="old")

        # Use Mock for new config to allow method mocking
        new_config = Mock(spec=BaseConfig)
        new_config.to_dict = Mock(return_value={"name": "new", "count": 0})

        loader = Mock(spec=ConfigLoader)
        loader.load = Mock(return_value=new_config)

        schema = Mock(spec=ConfigSchema)
        schema.validate = Mock()

        self.manager._configs["test"] = old_config
        self.manager._loaders["test"] = loader
        self.manager._schemas["test"] = schema

        result = self.manager.reload("test")

        schema.validate.assert_called_once()
        new_config.to_dict.assert_called_once_with(include_sensitive=True)
        assert result is new_config

    def test_update_config(self) -> None:
        """Test updating a configuration."""
        mock_config = Mock(spec=BaseConfig)
        mock_config.update = Mock()

        self.manager._configs["test"] = mock_config

        updates = {"name": "updated", "count": 10}

        self.manager.update("test", updates, ConfigSource.RUNTIME)

        mock_config.update.assert_called_once_with(updates, ConfigSource.RUNTIME)

    def test_update_nonexistent_config(self) -> None:
        """Test updating non-existent configuration."""
        with pytest.raises(ValueError, match="Configuration not found"):
            self.manager.update("nonexistent", {})

    def test_update_with_schema_validation(self) -> None:
        """Test updating configuration with schema validation."""
        # Create schema with field validation
        field_mock = Mock()
        field_mock.validate = Mock()

        schema = Mock(spec=ConfigSchema)
        schema._field_map = {"name": field_mock}

        mock_config = Mock(spec=BaseConfig)
        mock_config.update = Mock()

        self.manager._configs["test"] = mock_config
        self.manager._schemas["test"] = schema

        updates = {"name": "validated"}

        self.manager.update("test", updates)

        field_mock.validate.assert_called_once_with("validated")
        mock_config.update.assert_called_once()

    def test_reset_config(self) -> None:
        """Test resetting configuration to defaults."""
        mock_config = Mock(spec=BaseConfig)
        mock_config.reset_to_defaults = Mock()
        mock_config.update = Mock()

        self.manager._configs["test"] = mock_config

        defaults = {"name": "reset_name", "count": 0}
        self.manager._defaults["test"] = defaults

        self.manager.reset("test")

        mock_config.reset_to_defaults.assert_called_once()
        mock_config.update.assert_called_once_with(defaults, ConfigSource.DEFAULT)

    def test_reset_nonexistent_config(self) -> None:
        """Test resetting non-existent configuration."""
        with pytest.raises(ValueError, match="Configuration not found"):
            self.manager.reset("nonexistent")

    def test_list_configs(self) -> None:
        """Test listing all configurations."""
        self.manager._configs["config1"] = Mock()
        self.manager._configs["config2"] = Mock()

        result = self.manager.list_configs()

        assert set(result) == {"config1", "config2"}

    def test_get_all_configs(self) -> None:
        """Test getting all configurations."""
        config1 = Mock()
        config2 = Mock()

        self.manager._configs["config1"] = config1
        self.manager._configs["config2"] = config2

        result = self.manager.get_all()

        assert result == {"config1": config1, "config2": config2}
        # Should be a copy, not the same dict
        assert result is not self.manager._configs

    def test_clear_all(self) -> None:
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

    def test_export_config(self) -> None:
        """Test exporting configuration as dictionary."""
        mock_config = Mock(spec=BaseConfig)
        mock_config.to_dict = Mock(return_value={"name": "test", "count": 5})
        self.manager._configs["test"] = mock_config

        result = self.manager.export("test", include_sensitive=True)

        mock_config.to_dict.assert_called_once_with(True)
        assert result == {"name": "test", "count": 5}

    def test_export_nonexistent_config(self) -> None:
        """Test exporting non-existent configuration."""
        with pytest.raises(ValueError, match="Configuration not found"):
            self.manager.export("nonexistent")

    def test_export_all_configs(self) -> None:
        """Test exporting all configurations."""
        config1 = Mock()
        config1.to_dict = Mock(return_value={"key1": "value1"})
        config2 = Mock()
        config2.to_dict = Mock(return_value={"key2": "value2"})

        self.manager._configs["config1"] = config1
        self.manager._configs["config2"] = config2

        result = self.manager.export_all(include_sensitive=False)

        config1.to_dict.assert_called_once_with(False)
        config2.to_dict.assert_called_once_with(False)
        assert result == {"config1": {"key1": "value1"}, "config2": {"key2": "value2"}}

    def test_export_to_dict_alias(self) -> None:
        """Test export_to_dict as alias for export_all."""
        config1 = Mock()
        config1.to_dict = Mock(return_value={"key1": "value1"})

        self.manager._configs["config1"] = config1

        result = self.manager.export_to_dict(include_sensitive=True)

        config1.to_dict.assert_called_once_with(True)
        assert result == {"config1": {"key1": "value1"}}

    def test_load_from_dict(self) -> None:
        """Test loading configuration from dictionary."""
        data = {"name": "from_dict", "count": 42}

        result = self.manager.load_from_dict("test", SampleConfigClass, data)

        assert isinstance(result, SampleConfigClass)
        assert result.name == "from_dict"
        assert result.count == 42
        assert self.manager._configs["test"] is result

    def test_add_loader(self) -> None:
        """Test adding a loader for configuration."""
        loader = Mock(spec=ConfigLoader)

        self.manager.add_loader("test", loader)

        assert self.manager._loaders["test"] is loader

    def test_validate_all_configs(self) -> None:
        """Test validating all configurations."""
        # Config with validate method
        config1 = Mock()
        config1.validate = Mock()
        config1.to_dict = Mock(return_value={"key": "value"})

        # Config without validate method
        config2 = Mock(spec=[])
        config2.to_dict = Mock(return_value={"key2": "value2"})

        # Schema with validate method
        schema1 = Mock()
        schema1.validate = Mock()

        # Schema without validate method
        schema2 = Mock(spec=[])

        self.manager._configs["config1"] = config1
        self.manager._configs["config2"] = config2
        self.manager._schemas["config1"] = schema1
        self.manager._schemas["config2"] = schema2

        self.manager.validate_all()

        config1.validate.assert_called_once()
        schema1.validate.assert_called_once_with({"key": "value"})
        # config2 and schema2 validate methods should not be called

    def test_get_or_create_existing(self) -> None:
        """Test get_or_create with existing configuration."""
        existing_config = SampleConfigClass(name="existing")
        self.manager._configs["test"] = existing_config

        result = self.manager.get_or_create(
            "test",
            SampleConfigClass,
            {"name": "new"},
        )

        assert result is existing_config
        assert result.name == "existing"  # Should not be overwritten

    def test_get_or_create_new(self) -> None:
        """Test get_or_create creating new configuration."""
        defaults = {"name": "created", "count": 100}

        result = self.manager.get_or_create("new_test", SampleConfigClass, defaults)

        assert isinstance(result, SampleConfigClass)
        assert result.name == "created"
        assert result.count == 100
        assert self.manager._configs["new_test"] is result

    def test_get_or_create_no_defaults(self) -> None:
        """Test get_or_create with no defaults provided."""
        result = self.manager.get_or_create("empty_test", SampleConfigClass)

        assert isinstance(result, SampleConfigClass)
        assert result.name == "test"  # Default from class
        assert self.manager._configs["empty_test"] is result


# 🧱🏗️🔚
