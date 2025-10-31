#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import TypeVar

from provide.foundation.config.base import BaseConfig
from provide.foundation.config.loader import ConfigLoader
from provide.foundation.config.schema import ConfigSchema
from provide.foundation.config.types import ConfigDict, ConfigSource

"""Configuration manager for centralized configuration management."""

T = TypeVar("T", bound=BaseConfig)


class ConfigManager:
    """Centralized configuration manager.

    Manages multiple configuration objects and provides a unified interface.
    """

    def __init__(self) -> None:
        """Initialize configuration manager."""
        self._configs: dict[str, BaseConfig] = {}
        self._schemas: dict[str, ConfigSchema] = {}
        self._loaders: dict[str, ConfigLoader] = {}
        self._defaults: dict[str, ConfigDict] = {}

    def register(
        self,
        name: str,
        config: BaseConfig | None = None,
        schema: ConfigSchema | None = None,
        loader: ConfigLoader | None = None,
        defaults: ConfigDict | None = None,
    ) -> None:
        """Register a configuration.

        Args:
            name: Configuration name
            config: Configuration instance
            schema: Configuration schema
            loader: Configuration loader
            defaults: Default configuration values

        """
        if config is not None:
            self._configs[name] = config

        if schema is not None:
            self._schemas[name] = schema

        if loader is not None:
            self._loaders[name] = loader

        if defaults is not None:
            self._defaults[name] = defaults

    def unregister(self, name: str) -> None:
        """Unregister a configuration.

        Args:
            name: Configuration name

        """
        self._configs.pop(name, None)
        self._schemas.pop(name, None)
        self._loaders.pop(name, None)
        self._defaults.pop(name, None)

    # Alias for unregister
    def remove(self, name: str) -> None:
        """Remove a configuration. Alias for unregister."""
        self.unregister(name)

    def get(self, name: str) -> BaseConfig | None:
        """Get a configuration by name.

        Args:
            name: Configuration name

        Returns:
            Configuration instance or None

        """
        return self._configs.get(name)

    def set(self, name: str, config: BaseConfig) -> None:
        """Set a configuration.

        Args:
            name: Configuration name
            config: Configuration instance

        """
        self._configs[name] = config

    def load(self, name: str, config_class: type[T], loader: ConfigLoader | None = None) -> T:
        """Load a configuration.

        Args:
            name: Configuration name
            config_class: Configuration class
            loader: Optional loader (uses registered if None)

        Returns:
            Configuration instance

        """
        # Use provided loader or registered one
        if loader is None:
            loader = self._loaders.get(name)
            if loader is None:
                raise ValueError(f"No loader registered for configuration: {name}")

        # Load configuration
        config = loader.load(config_class)

        # Apply defaults if available
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(config, key) or getattr(config, key) is None:
                    setattr(config, key, value)

        # Validate against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Store configuration
        self._configs[name] = config

        return config

    def reload(self, name: str) -> BaseConfig:
        """Reload a configuration.

        Args:
            name: Configuration name

        Returns:
            Reloaded configuration instance

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        loader = self._loaders.get(name)

        if loader is None:
            raise ValueError(f"No loader registered for configuration: {name}")

        # Reload from loader
        new_config = loader.load(config.__class__)

        # Apply defaults
        if name in self._defaults:
            defaults_dict = self._defaults[name]
            for key, value in defaults_dict.items():
                if not hasattr(new_config, key) or getattr(new_config, key) is None:
                    setattr(new_config, key, value)

        # Validate
        if name in self._schemas:
            schema = self._schemas[name]
            config_dict = new_config.to_dict(include_sensitive=True)
            schema.validate(config_dict)

        # Update stored configuration
        self._configs[name] = new_config

        return new_config

    def update(
        self,
        name: str,
        updates: ConfigDict,
        source: ConfigSource = ConfigSource.RUNTIME,
    ) -> None:
        """Update a configuration.

        Args:
            name: Configuration name
            updates: Configuration updates
            source: Source of updates

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]

        # Validate updates against schema if available
        if name in self._schemas:
            schema = self._schemas[name]
            # Validate only the updated fields
            for key, value in updates.items():
                if key in schema._field_map:
                    schema._field_map[key].validate(value)

        # Apply updates
        config.update(updates, source)

    def reset(self, name: str) -> None:
        """Reset a configuration to defaults.

        Args:
            name: Configuration name

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        config = self._configs[name]
        config.reset_to_defaults()

        # Apply registered defaults
        if name in self._defaults:
            config.update(self._defaults[name], ConfigSource.DEFAULT)

    def list_configs(self) -> list[str]:
        """List all registered configurations.

        Returns:
            List of configuration names

        """
        return list(self._configs.keys())

    def get_all(self) -> dict[str, BaseConfig]:
        """Get all registered configurations."""
        return self._configs.copy()

    def clear(self) -> None:
        """Clear all configurations."""
        self._configs.clear()
        self._schemas.clear()
        self._loaders.clear()
        self._defaults.clear()

    def export(self, name: str, include_sensitive: bool = False) -> ConfigDict:
        """Export a configuration as dictionary.

        Args:
            name: Configuration name
            include_sensitive: Whether to include sensitive fields

        Returns:
            Configuration dictionary

        """
        if name not in self._configs:
            raise ValueError(f"Configuration not found: {name}")

        return self._configs[name].to_dict(include_sensitive)

    def export_all(self, include_sensitive: bool = False) -> dict[str, ConfigDict]:
        """Export all configurations.

        Args:
            include_sensitive: Whether to include sensitive fields

        Returns:
            Dictionary of all configurations

        """
        result = {}
        for name, config in self._configs.items():
            result[name] = config.to_dict(include_sensitive)
        return result

    # Alias for export_all
    def export_to_dict(self, include_sensitive: bool = False) -> dict[str, ConfigDict]:
        """Export all configs to dict. Alias for export_all."""
        return self.export_all(include_sensitive)

    def load_from_dict(self, name: str, config_class: type[T], data: ConfigDict) -> T:
        """Load config from dictionary."""
        config = config_class.from_dict(data)
        self._configs[name] = config
        return config

    def add_loader(self, name: str, loader: ConfigLoader) -> None:
        """Add a loader for a configuration."""
        self._loaders[name] = loader

    def validate_all(self) -> None:
        """Validate all configurations."""
        for name, config in self._configs.items():
            if hasattr(config, "validate"):
                config.validate()
            if name in self._schemas:
                schema = self._schemas[name]
                config_dict = config.to_dict(include_sensitive=True)
                if hasattr(schema, "validate"):
                    schema.validate(config_dict)

    def get_or_create(self, name: str, config_class: type[T], defaults: ConfigDict | None = None) -> T:
        """Get existing config or create new one with defaults."""
        existing = self.get(name)
        if existing is not None:
            # Type: ignore since we know this is the correct type from how it was registered
            return existing  # type: ignore[return-value]

        # Create new config with defaults
        config = config_class.from_dict(defaults or {})
        self._configs[name] = config
        return config


# Global configuration manager instance
_manager = ConfigManager()


def get_config(name: str) -> BaseConfig | None:
    """Get a configuration from the global manager.

    Args:
        name: Configuration name

    Returns:
        Configuration instance or None

    """
    return _manager.get(name)


def set_config(name: str, config: BaseConfig) -> None:
    """Set a configuration in the global manager.

    Args:
        name: Configuration name
        config: Configuration instance

    """
    _manager.set(name, config)


def register_config(
    name: str,
    config: BaseConfig | None = None,
    schema: ConfigSchema | None = None,
    loader: ConfigLoader | None = None,
    defaults: ConfigDict | None = None,
) -> None:
    """Register a configuration with the global manager.

    Args:
        name: Configuration name
        config: Configuration instance
        schema: Configuration schema
        loader: Configuration loader
        defaults: Default configuration values

    """
    _manager.register(name, config, schema, loader, defaults)


def load_config(name: str, config_class: type[T], loader: ConfigLoader | None = None) -> T:
    """Load a configuration using the global manager.

    Args:
        name: Configuration name
        config_class: Configuration class
        loader: Optional loader

    Returns:
        Configuration instance

    """
    return _manager.load(name, config_class, loader)


# 🧱🏗️🔚
