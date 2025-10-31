#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Callable
import contextlib
import threading
import time
from typing import Any

from attrs import define, field

from provide.foundation.config.defaults import DEFAULT_STATE_CONFIG_NAME
from provide.foundation.state.base import ImmutableState, StateManager

"""Immutable configuration management with versioning."""


@define(frozen=True, slots=True, kw_only=True)
class VersionedConfig(ImmutableState):
    """Immutable configuration with generation tracking.

    All Foundation configurations should inherit from this to ensure
    immutability and proper change tracking.
    """

    data: dict[str, Any] = field(factory=dict)
    parent_generation: int | None = field(default=None)
    config_name: str = field(default=DEFAULT_STATE_CONFIG_NAME)

    def with_changes(self, **changes: Any) -> VersionedConfig:
        """Create a new state instance with the specified changes.

        Args:
            **changes: Field updates to apply

        Returns:
            New state instance with updated generation
        """
        # Increment generation for change tracking
        if "generation" not in changes:
            changes["generation"] = self.generation + 1

        # For attrs classes with slots, use attrs.evolve instead of __dict__
        import attrs

        return attrs.evolve(self, **changes)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> VersionedConfig:
        """Create a new config with the specified key-value pair.

        Args:
            key: Configuration key
            value: Configuration value

        Returns:
            New configuration instance
        """
        new_data = {**self.data, key: value}
        return self.with_changes(
            data=new_data,
            parent_generation=self.generation,
        )

    def update(self, updates: dict[str, Any]) -> VersionedConfig:
        """Create a new config with multiple updates.

        Args:
            updates: Dictionary of key-value pairs to update

        Returns:
            New configuration instance
        """
        new_data = {**self.data, **updates}
        return self.with_changes(
            data=new_data,
            parent_generation=self.generation,
        )

    def remove(self, key: str) -> VersionedConfig:
        """Create a new config with the specified key removed.

        Args:
            key: Configuration key to remove

        Returns:
            New configuration instance
        """
        new_data = {k: v for k, v in self.data.items() if k != key}
        return self.with_changes(
            data=new_data,
            parent_generation=self.generation,
        )

    def merge(self, other: VersionedConfig) -> VersionedConfig:
        """Merge with another configuration.

        Args:
            other: Configuration to merge with

        Returns:
            New configuration instance with merged data
        """
        new_data = {**self.data, **other.data}
        return self.with_changes(
            data=new_data,
            parent_generation=max(self.generation, other.generation),
        )


@define(kw_only=True, slots=True)
class ConfigManager:
    """Thread-safe manager for versioned configurations.

    Provides atomic updates and change tracking for configurations.
    """

    _configs: dict[str, StateManager] = field(factory=dict)
    _lock: threading.RLock = field(factory=threading.RLock, init=False)
    _change_listeners: dict[str, list[Callable[[ImmutableState, ImmutableState], None]]] = field(
        factory=dict, init=False
    )

    def register_config(self, config: VersionedConfig) -> None:
        """Register a new configuration.

        Args:
            config: Configuration to register
        """
        with self._lock:
            if config.config_name in self._configs:
                raise ValueError(f"Configuration '{config.config_name}' already registered")

            manager = StateManager(state=config)
            self._configs[config.config_name] = manager
            self._change_listeners[config.config_name] = []

            # Add observer for change notifications
            manager.add_observer(self._notify_listeners)

    def get_config(self, name: str) -> VersionedConfig | None:
        """Get a configuration by name.

        Args:
            name: Configuration name

        Returns:
            Configuration instance or None if not found
        """
        with self._lock:
            manager = self._configs.get(name)
            if manager:
                state = manager.current_state
                return state if isinstance(state, VersionedConfig) else None
            return None

    def update_config(self, name: str, **updates: Any) -> VersionedConfig:
        """Update a configuration with new values.

        Args:
            name: Configuration name
            **updates: Key-value pairs to update

        Returns:
            Updated configuration instance

        Raises:
            KeyError: If configuration not found
        """
        with self._lock:
            manager = self._configs.get(name)
            if not manager:
                raise KeyError(f"Configuration '{name}' not found")

            current_config = manager.current_state
            if not isinstance(current_config, VersionedConfig):
                raise TypeError(f"Expected VersionedConfig, got {type(current_config)}")
            new_config = current_config.update(updates)
            manager.replace_state(new_config)
            return new_config

    def set_config_value(self, name: str, key: str, value: Any) -> VersionedConfig:
        """Set a single configuration value.

        Args:
            name: Configuration name
            key: Configuration key
            value: Configuration value

        Returns:
            Updated configuration instance

        Raises:
            KeyError: If configuration not found
        """
        with self._lock:
            manager = self._configs.get(name)
            if not manager:
                raise KeyError(f"Configuration '{name}' not found")

            current_config = manager.current_state
            if not isinstance(current_config, VersionedConfig):
                raise TypeError(f"Expected VersionedConfig, got {type(current_config)}")
            new_config = current_config.set(key, value)
            manager.replace_state(new_config)
            return new_config

    def get_config_value(self, name: str, key: str, default: Any = None) -> Any:
        """Get a single configuration value.

        Args:
            name: Configuration name
            key: Configuration key
            default: Default value if not found

        Returns:
            Configuration value or default

        Raises:
            KeyError: If configuration not found
        """
        config = self.get_config(name)
        if not config:
            raise KeyError(f"Configuration '{name}' not found")
        return config.get(key, default)

    def add_change_listener(
        self, name: str, listener: Callable[[ImmutableState, ImmutableState], None]
    ) -> None:
        """Add a change listener for a configuration.

        Args:
            name: Configuration name
            listener: Function called when configuration changes
        """
        with self._lock:
            if name not in self._change_listeners:
                self._change_listeners[name] = []
            self._change_listeners[name].append(listener)

    def remove_change_listener(
        self, name: str, listener: Callable[[ImmutableState, ImmutableState], None]
    ) -> None:
        """Remove a change listener for a configuration.

        Args:
            name: Configuration name
            listener: Listener function to remove
        """
        with self._lock:
            listeners = self._change_listeners.get(name, [])
            with contextlib.suppress(ValueError):
                listeners.remove(listener)

    def list_configs(self) -> list[str]:
        """List all registered configuration names.

        Returns:
            List of configuration names
        """
        with self._lock:
            return list(self._configs.keys())

    def get_config_generation(self, name: str) -> int | None:
        """Get the current generation of a configuration.

        Args:
            name: Configuration name

        Returns:
            Configuration generation or None if not found
        """
        config = self.get_config(name)
        return config.generation if config else None

    def reset_config(self, name: str) -> None:
        """Reset a configuration to its initial state.

        Args:
            name: Configuration name
        """
        with self._lock:
            manager = self._configs.get(name)
            if manager:
                # Find the root configuration (generation 0)
                current = manager.current_state
                if hasattr(current, "config_name"):
                    initial_config = VersionedConfig(
                        config_name=current.config_name,
                        data={},
                        generation=0,
                        created_at=time.time(),
                    )
                    manager.replace_state(initial_config)

    def clear_all(self) -> None:
        """Clear all configurations."""
        with self._lock:
            self._configs.clear()
            self._change_listeners.clear()

    def _notify_listeners(self, old_state: ImmutableState, new_state: ImmutableState) -> None:
        """Notify change listeners of configuration updates."""
        if not isinstance(new_state, VersionedConfig):
            return

        config_name = new_state.config_name
        listeners = self._change_listeners.get(config_name, [])

        for listener in listeners:
            with contextlib.suppress(Exception):
                listener(old_state, new_state)


# 🧱🏗️🔚
