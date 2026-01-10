#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for state/config.py.

This module contains comprehensive tests for VersionedConfig and ConfigManager.
Run with: pytest tests/state/test_config.py -v"""

from __future__ import annotations

import threading
import time

from attrs.exceptions import FrozenInstanceError
from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock
import pytest

from provide.foundation.state.base import ImmutableState
from provide.foundation.state.config import ConfigManager, VersionedConfig


class TestVersionedConfig(FoundationTestCase):
    """Tests for VersionedConfig class."""

    def test_versioned_config_initialization(self) -> None:
        """Test VersionedConfig initializes with defaults."""
        config = VersionedConfig()
        assert config.data == {}
        assert config.parent_generation is None
        assert config.config_name == ""  # DEFAULT_STATE_CONFIG_NAME
        assert config.generation == 0

    def test_versioned_config_with_data(self) -> None:
        """Test VersionedConfig with initial data."""
        config = VersionedConfig(data={"key": "value"}, config_name="test")
        assert config.data == {"key": "value"}
        assert config.config_name == "test"

    def test_get_existing_key(self) -> None:
        """Test getting existing configuration value."""
        config = VersionedConfig(data={"foo": "bar"})
        assert config.get("foo") == "bar"

    def test_get_missing_key_returns_default(self) -> None:
        """Test getting missing key returns default."""
        config = VersionedConfig()
        assert config.get("missing") is None
        assert config.get("missing", "default") == "default"

    def test_set_creates_new_config(self) -> None:
        """Test set creates a new config instance."""
        config = VersionedConfig(data={"a": "1"})
        new_config = config.set("b", "2")

        # Original unchanged
        assert config.data == {"a": "1"}
        assert config.generation == 0

        # New config has update
        assert new_config.data == {"a": "1", "b": "2"}
        assert new_config.generation == 1
        assert new_config.parent_generation == 0

    def test_set_updates_existing_key(self) -> None:
        """Test set updates existing key value."""
        config = VersionedConfig(data={"key": "old"})
        new_config = config.set("key", "new")

        assert new_config.data == {"key": "new"}
        assert new_config.generation == 1

    def test_update_multiple_keys(self) -> None:
        """Test update with multiple key-value pairs."""
        config = VersionedConfig(data={"a": "1"})
        new_config = config.update({"b": "2", "c": "3"})

        assert new_config.data == {"a": "1", "b": "2", "c": "3"}
        assert new_config.generation == 1
        assert new_config.parent_generation == 0

    def test_update_overwrites_existing_keys(self) -> None:
        """Test update overwrites existing keys."""
        config = VersionedConfig(data={"a": "1", "b": "2"})
        new_config = config.update({"b": "new", "c": "3"})

        assert new_config.data == {"a": "1", "b": "new", "c": "3"}

    def test_remove_existing_key(self) -> None:
        """Test remove deletes key from config."""
        config = VersionedConfig(data={"a": "1", "b": "2"})
        new_config = config.remove("a")

        assert new_config.data == {"b": "2"}
        assert new_config.generation == 1

    def test_remove_nonexistent_key(self) -> None:
        """Test remove on nonexistent key has no effect."""
        config = VersionedConfig(data={"a": "1"})
        new_config = config.remove("nonexistent")

        assert new_config.data == {"a": "1"}
        assert new_config.generation == 1

    def test_merge_combines_data(self) -> None:
        """Test merge combines data from two configs."""
        config1 = VersionedConfig(data={"a": "1", "b": "2"})
        config2 = VersionedConfig(data={"b": "new", "c": "3"})

        merged = config1.merge(config2)

        assert merged.data == {"a": "1", "b": "new", "c": "3"}

    def test_merge_uses_max_generation(self) -> None:
        """Test merge uses maximum generation from both configs."""
        config1 = VersionedConfig(data={"a": "1"}, generation=5)
        config2 = VersionedConfig(data={"b": "2"}, generation=10)

        merged = config1.merge(config2)

        # Parent generation should be max of both
        assert merged.parent_generation == 10
        # Merged generation is config1.generation + 1 (incremented via with_changes)
        assert merged.generation == 6

    def test_with_changes_increments_generation(self) -> None:
        """Test with_changes increments generation."""
        config = VersionedConfig(data={"a": "1"})
        new_config = config.with_changes(data={"a": "2"})

        assert new_config.generation == 1

    def test_with_changes_explicit_generation(self) -> None:
        """Test with_changes can override generation."""
        config = VersionedConfig()
        new_config = config.with_changes(generation=42)

        assert new_config.generation == 42

    def test_immutability(self) -> None:
        """Test that VersionedConfig is immutable."""
        config = VersionedConfig(data={"a": "1"})

        # Should not be able to modify frozen attributes
        with pytest.raises(FrozenInstanceError):
            config.generation = 5  # type: ignore[misc]


class TestConfigManager(FoundationTestCase):
    """Tests for ConfigManager class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        super().setup_method()
        self.manager = ConfigManager()

    def test_register_config(self) -> None:
        """Test registering a new configuration."""
        config = VersionedConfig(config_name="test")
        self.manager.register_config(config)

        assert "test" in self.manager.list_configs()

    def test_register_duplicate_raises_error(self) -> None:
        """Test registering duplicate config name raises ValueError."""
        config1 = VersionedConfig(config_name="test")
        config2 = VersionedConfig(config_name="test")

        self.manager.register_config(config1)

        with pytest.raises(ValueError, match="already registered"):
            self.manager.register_config(config2)

    def test_get_config_existing(self) -> None:
        """Test getting existing configuration."""
        config = VersionedConfig(config_name="test", data={"key": "value"})
        self.manager.register_config(config)

        retrieved = self.manager.get_config("test")

        assert retrieved is not None
        assert retrieved.config_name == "test"
        assert retrieved.data == {"key": "value"}

    def test_get_config_nonexistent(self) -> None:
        """Test getting nonexistent configuration returns None."""
        result = self.manager.get_config("nonexistent")
        assert result is None

    def test_update_config(self) -> None:
        """Test updating configuration values."""
        config = VersionedConfig(config_name="test", data={"a": "1"})
        self.manager.register_config(config)

        updated = self.manager.update_config("test", b="2", c="3")

        assert updated.data == {"a": "1", "b": "2", "c": "3"}
        assert updated.generation == 1

        # Verify it's persisted
        retrieved = self.manager.get_config("test")
        assert retrieved is not None
        assert retrieved.data == {"a": "1", "b": "2", "c": "3"}

    def test_update_nonexistent_config_raises_error(self) -> None:
        """Test updating nonexistent config raises KeyError."""
        with pytest.raises(KeyError, match="not found"):
            self.manager.update_config("nonexistent", key="value")

    def test_set_config_value(self) -> None:
        """Test setting a single configuration value."""
        config = VersionedConfig(config_name="test", data={"a": "1"})
        self.manager.register_config(config)

        updated = self.manager.set_config_value("test", "b", "2")

        assert updated.data == {"a": "1", "b": "2"}

    def test_set_config_value_nonexistent_raises_error(self) -> None:
        """Test setting value on nonexistent config raises KeyError."""
        with pytest.raises(KeyError, match="not found"):
            self.manager.set_config_value("nonexistent", "key", "value")

    def test_get_config_value_existing(self) -> None:
        """Test getting existing configuration value."""
        config = VersionedConfig(config_name="test", data={"key": "value"})
        self.manager.register_config(config)

        result = self.manager.get_config_value("test", "key")
        assert result == "value"

    def test_get_config_value_missing_key_returns_default(self) -> None:
        """Test getting missing key returns default."""
        config = VersionedConfig(config_name="test")
        self.manager.register_config(config)

        result = self.manager.get_config_value("test", "missing", default="default")
        assert result == "default"

    def test_get_config_value_nonexistent_config_raises_error(self) -> None:
        """Test getting value from nonexistent config raises KeyError."""
        with pytest.raises(KeyError, match="not found"):
            self.manager.get_config_value("nonexistent", "key")

    def test_list_configs(self) -> None:
        """Test listing all registered configurations."""
        config1 = VersionedConfig(config_name="test1")
        config2 = VersionedConfig(config_name="test2")

        self.manager.register_config(config1)
        self.manager.register_config(config2)

        configs = self.manager.list_configs()

        assert len(configs) == 2
        assert "test1" in configs
        assert "test2" in configs

    def test_get_config_generation(self) -> None:
        """Test getting configuration generation."""
        config = VersionedConfig(config_name="test", generation=5)
        self.manager.register_config(config)

        generation = self.manager.get_config_generation("test")
        assert generation == 5

    def test_get_config_generation_nonexistent(self) -> None:
        """Test getting generation of nonexistent config returns None."""
        generation = self.manager.get_config_generation("nonexistent")
        assert generation is None

    def test_reset_config(self) -> None:
        """Test resetting configuration to initial state."""
        config = VersionedConfig(config_name="test", data={"a": "1"})
        self.manager.register_config(config)

        # Make some updates
        self.manager.set_config_value("test", "b", "2")

        # Reset
        self.manager.reset_config("test")

        # Should be back to empty data
        retrieved = self.manager.get_config("test")
        assert retrieved is not None
        assert retrieved.data == {}
        assert retrieved.generation == 0

    def test_reset_nonexistent_config(self) -> None:
        """Test reset on nonexistent config does nothing."""
        # Should not raise
        self.manager.reset_config("nonexistent")

    def test_clear_all(self) -> None:
        """Test clearing all configurations."""
        config1 = VersionedConfig(config_name="test1")
        config2 = VersionedConfig(config_name="test2")

        self.manager.register_config(config1)
        self.manager.register_config(config2)

        self.manager.clear_all()

        assert len(self.manager.list_configs()) == 0

    def test_add_change_listener(self) -> None:
        """Test adding change listener."""
        config = VersionedConfig(config_name="test")
        self.manager.register_config(config)

        listener_called = []

        def listener(old: ImmutableState, new: ImmutableState) -> None:
            listener_called.append((old, new))

        self.manager.add_change_listener("test", listener)

        # Make a change
        self.manager.set_config_value("test", "key", "value")

        # Give listener time to be called
        time.sleep(0.01)

        # Listener should have been called
        assert len(listener_called) == 1

    def test_remove_change_listener(self) -> None:
        """Test removing change listener."""
        config = VersionedConfig(config_name="test")
        self.manager.register_config(config)

        listener_called = []

        def listener(old: ImmutableState, new: ImmutableState) -> None:
            listener_called.append((old, new))

        self.manager.add_change_listener("test", listener)
        self.manager.remove_change_listener("test", listener)

        # Make a change
        self.manager.set_config_value("test", "key", "value")

        # Give time for any listener to be called
        time.sleep(0.01)

        # Listener should not have been called
        assert len(listener_called) == 0

    def test_remove_nonexistent_listener(self) -> None:
        """Test removing nonexistent listener does nothing."""

        def listener(old: ImmutableState, new: ImmutableState) -> None:
            pass

        # Should not raise
        self.manager.remove_change_listener("test", listener)

    def test_listener_exception_suppressed(self) -> None:
        """Test that listener exceptions are suppressed."""
        config = VersionedConfig(config_name="test")
        self.manager.register_config(config)

        def failing_listener(old: ImmutableState, new: ImmutableState) -> None:
            raise ValueError("Listener failed")

        self.manager.add_change_listener("test", failing_listener)

        # Should not raise despite listener failure
        self.manager.set_config_value("test", "key", "value")

    def test_thread_safety(self) -> None:
        """Test thread-safe operations on ConfigManager."""
        config = VersionedConfig(config_name="test")
        self.manager.register_config(config)

        errors: list[Exception] = []

        def update_config(key: str, value: str) -> None:
            try:
                for i in range(10):
                    self.manager.set_config_value("test", key, f"{value}_{i}")
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=update_config, args=(f"key_{i}", f"value_{i}")) for i in range(5)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # No errors should have occurred
        assert len(errors) == 0

        # Final state should have all keys
        final_config = self.manager.get_config("test")
        assert final_config is not None
        assert len(final_config.data) == 5

    def test_notify_listeners_with_non_versioned_config(self) -> None:
        """Test _notify_listeners handles non-VersionedConfig state."""
        # Create a mock non-VersionedConfig ImmutableState
        mock_state = MagicMock(spec=ImmutableState)

        # Should not raise
        self.manager._notify_listeners(mock_state, mock_state)

    def test_update_config_wrong_type_raises_error(self) -> None:
        """Test updating config when current state is wrong type."""
        # This is a bit contrived, but tests the type check
        config = VersionedConfig(config_name="test")
        self.manager.register_config(config)

        # Replace with non-VersionedConfig state (requires direct manipulation)
        mock_state = MagicMock(spec=ImmutableState)
        self.manager._configs["test"]._state = mock_state

        with pytest.raises(TypeError, match="Expected VersionedConfig"):
            self.manager.update_config("test", key="value")

    def test_set_config_value_wrong_type_raises_error(self) -> None:
        """Test set_config_value when current state is wrong type."""
        config = VersionedConfig(config_name="test")
        self.manager.register_config(config)

        # Replace with non-VersionedConfig state
        mock_state = MagicMock(spec=ImmutableState)
        self.manager._configs["test"]._state = mock_state

        with pytest.raises(TypeError, match="Expected VersionedConfig"):
            self.manager.set_config_value("test", "key", "value")

    def test_get_config_returns_none_for_wrong_type(self) -> None:
        """Test get_config returns None when state is not VersionedConfig."""
        config = VersionedConfig(config_name="test")
        self.manager.register_config(config)

        # Replace with non-VersionedConfig state
        mock_state = MagicMock(spec=ImmutableState)
        self.manager._configs["test"]._state = mock_state

        result = self.manager.get_config("test")
        assert result is None

    def test_reset_config_without_config_name_attribute(self) -> None:
        """Test reset_config when current state doesn't have config_name."""
        config = VersionedConfig(config_name="test")
        self.manager.register_config(config)

        # Replace state manager's state with something without config_name
        mock_state = MagicMock(spec=ImmutableState)
        del mock_state.config_name  # Remove config_name attribute
        self.manager._configs["test"]._state = mock_state

        # Should not raise, just do nothing
        self.manager.reset_config("test")


__all__ = [
    "TestConfigManager",
    "TestVersionedConfig",
]

# 🧱🏗️🔚
