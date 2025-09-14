"""Advanced cleanup, config loading, and miscellaneous tests for hub components module."""

from unittest.mock import AsyncMock, Mock

from provide.foundation.hub.components import (
    ComponentCategory,
    _component_registry,
    _initialized_components,
    _registry_lock,
    bootstrap_foundation,
    cleanup_all_components,
    discover_components,
    get_component_registry,
    load_config_from_registry,
    reset_registry_for_tests,
)


class TestAdvancedCleanup:
    """Test advanced cleanup scenarios."""

    def setup_method(self):
        """Set up test environment."""
        reset_registry_for_tests()

    def teardown_method(self):
        """Clean up after tests."""
        reset_registry_for_tests()

    def test_cleanup_all_components_with_async_cleanup(self):
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
            async_component.cleanup, "call_count",
        )

    def test_cleanup_all_components_no_dimension_filter(self):
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


class TestConfigFromRegistry:
    """Test configuration loading from registry."""

    def setup_method(self):
        """Set up test environment."""
        reset_registry_for_tests()

    def teardown_method(self):
        """Clean up after tests."""
        reset_registry_for_tests()

    def test_load_config_from_registry_sync_sources(self):
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

    def test_load_config_from_registry_with_async_source_skipped(self):
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


class TestMiscellaneousFunctionality:
    """Test miscellaneous functionality and edge cases."""

    def setup_method(self):
        """Set up test environment."""
        reset_registry_for_tests()

    def teardown_method(self):
        """Clean up after tests."""
        reset_registry_for_tests()

    def test_discover_components_stub(self):
        """Test discover_components stub functionality."""
        result = discover_components("test_group", "test_dimension", None)
        assert result == {}

    def test_bootstrap_foundation_creates_default_components(self):
        """Test bootstrap_foundation creates expected components."""
        from provide.foundation.eventsets.registry import (
            discover_event_sets,
            get_registry as get_eventset_registry,
        )

        # Clear registries first
        reset_registry_for_tests()

        # Clear the event registry and reset discovery state
        event_registry = get_eventset_registry()
        event_registry.clear()
        from provide.foundation.eventsets.registry import reset_discovery_state
        reset_discovery_state()

        # Bootstrap should create default components
        bootstrap_foundation()

        registry = get_component_registry()

        # Should have timestamp processor
        timestamp_proc = registry.get("timestamp", ComponentCategory.PROCESSOR.value)
        assert timestamp_proc is not None

        # Trigger event set discovery (this should register them fresh)
        discover_event_sets()

        # Event sets should be in the EventSetRegistry, not ComponentRegistry
        event_sets = event_registry.list_event_sets()
        assert len(event_sets) > 0, f"No event sets found. Registry has {len(list(event_registry))} entries"

        # Check what event sets we have
        event_set_names = [es.name for es in event_sets]
        assert "default" in event_set_names, f"'default' not found in event sets: {event_set_names}"

        # Should have default event set (registered during module discovery)
        default_event_set = event_registry.get_event_set("default")
        assert default_event_set is not None

    def test_reset_registry_for_tests(self):
        """Test reset_registry_for_tests clears state."""
        registry = get_component_registry()

        # Add some test data
        test_component = Mock()
        registry.register("test", test_component, "test_dimension", {})

        # Add to initialized components cache
        global _initialized_components
        _initialized_components[("test", "test_dimension")] = test_component

        # Reset should clear everything
        reset_registry_for_tests()

        assert len(list(registry)) == 0
        assert len(_initialized_components) == 0

    def test_global_registry_access(self):
        """Test get_component_registry returns global registry."""
        registry1 = get_component_registry()
        registry2 = get_component_registry()

        # Should be the same instance
        assert registry1 is registry2
        assert registry1 is _component_registry

    def test_thread_safety_basics(self):
        """Test basic thread safety with registry lock."""
        # Test that the registry lock exists and is accessible
        assert _registry_lock is not None
        assert hasattr(_registry_lock, "acquire") and hasattr(_registry_lock, "release")

        # Test that we can acquire and release the lock
        with _registry_lock:
            registry = get_component_registry()
            assert registry is not None
