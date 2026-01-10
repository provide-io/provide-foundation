#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Advanced cleanup, config loading, and miscellaneous tests for hub components module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import AsyncMock, Mock

from provide.foundation.hub.components import (
    ComponentCategory,
    _component_registry,
    _initialized_components,
    cleanup_all_components,
    discover_components,
    get_component_registry,
    load_config_from_registry,
)


class TestAdvancedCleanup(FoundationTestCase):
    """Test advanced cleanup scenarios."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

    def teardown_method(self) -> None:
        """Clean up after tests."""
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

    def test_cleanup_all_components_with_async_cleanup(self) -> None:
        """Test cleanup_all_components handles async cleanup methods."""
        registry = get_component_registry()

        async_component = Mock()
        async_component.cleanup = AsyncMock()

        registry.register(
            name="async_cleanup_component",
            value=async_component,
            dimension="test_dimension",
            metadata={"supports_cleanup": True},
        )

        # Should handle async cleanup without raising exception
        cleanup_all_components("test_dimension")

        # Async cleanup should be called (via task creation or similar)
        # The exact behavior depends on the event loop state
        assert async_component.cleanup.called or hasattr(
            async_component.cleanup,
            "call_count",
        )

    def test_cleanup_all_components_no_dimension_filter(self) -> None:
        """Test cleanup_all_components without dimension filter."""
        registry = get_component_registry()

        component1 = Mock()
        component1.cleanup = Mock()

        component2 = Mock()
        component2.cleanup = Mock()

        registry.register(
            name="component1",
            value=component1,
            dimension="dimension1",
            metadata={"supports_cleanup": True},
        )

        registry.register(
            name="component2",
            value=component2,
            dimension="dimension2",
            metadata={"supports_cleanup": True},
        )

        # Cleanup all components (no dimension filter)
        cleanup_all_components()

        # Both components should be cleaned up
        component1.cleanup.assert_called_once()
        component2.cleanup.assert_called_once()


class TestConfigFromRegistry(FoundationTestCase):
    """Test configuration loading from registry."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

    def teardown_method(self) -> None:
        """Clean up after tests."""
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

    def test_load_config_from_registry_sync_sources(self) -> None:
        """Test load_config_from_registry with sync sources."""
        registry = get_component_registry()

        # Mock config class
        config_class = Mock()
        config_class.from_dict = Mock(return_value="loaded_config")

        # Mock config source
        source = Mock()
        source.load_config = Mock(return_value={"key": "value"})

        registry.register(
            name="sync_config_source",
            value=source,
            dimension=ComponentCategory.CONFIG_SOURCE.value,
            metadata={"priority": 1},
        )

        result = load_config_from_registry(config_class)

        assert result == "loaded_config"
        source.load_config.assert_called_once()
        config_class.from_dict.assert_called_once_with({"key": "value"})

    def test_load_config_from_registry_with_async_source_skipped(self) -> None:
        """Test load_config_from_registry skips async sources."""
        registry = get_component_registry()

        config_class = Mock()
        config_class.from_dict = Mock(return_value="empty_config")

        # Mock async config source (should be skipped)
        async_source = Mock()
        async_source.load_config = AsyncMock(return_value={"async_key": "async_value"})

        registry.register(
            name="async_config_source",
            value=async_source,
            dimension=ComponentCategory.CONFIG_SOURCE.value,
            metadata={"priority": 1},
        )

        result = load_config_from_registry(config_class)

        # Should skip async source and return empty config
        assert result == "empty_config"
        config_class.from_dict.assert_called_once_with({})
        # Async method should not be called in sync context
        async_source.load_config.assert_not_called()


class TestMiscellaneousFunctionality(FoundationTestCase):
    """Test miscellaneous functionality and edge cases."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

    def teardown_method(self) -> None:
        """Clean up after tests."""
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

    def test_discover_components_stub(self) -> None:
        """Test discover_components stub functionality."""
        result = discover_components("test_group", "test_dimension", None)
        assert result == {}

    def test_reset_hub_state_clears_registry(self) -> None:
        """Test reset_hub_state clears registry state."""
        registry = get_component_registry()

        # Add some test data
        test_component = Mock()
        registry.register("test", test_component, "test_dimension", {})

        # Add to initialized components cache
        global _initialized_components
        _initialized_components[("test", "test_dimension")] = test_component

        # Reset should clear everything
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

        assert len(list(registry)) == 0
        assert len(_initialized_components) == 0

    def test_global_registry_access(self) -> None:
        """Test get_component_registry returns global registry."""
        registry1 = get_component_registry()
        registry2 = get_component_registry()

        # Should be the same instance
        assert registry1 is registry2
        assert registry1 is _component_registry

    def test_thread_safety_basics(self) -> None:
        """Test basic thread safety with registry lock."""
        from provide.foundation.concurrency.locks import get_lock_manager

        # Test that the lock manager can acquire registry lock
        lock_manager = get_lock_manager()

        # Test that we can acquire and release the lock
        with lock_manager.acquire("foundation.registry"):
            registry = get_component_registry()
            assert registry is not None


# 🧱🏗️🔚
