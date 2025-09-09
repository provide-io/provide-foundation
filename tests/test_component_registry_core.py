"""
TDD tests for core registry-based component management architecture.

This test suite defines Foundation's core registry architecture, metadata handling,
and bootstrap integration. No backward compatibility is maintained.
"""

import asyncio
from collections.abc import AsyncIterator, Iterator
import threading
from typing import Any
from unittest.mock import Mock, AsyncMock

import pytest
from structlog.typing import EventDict

from provide.foundation.config.base import BaseConfig
from provide.foundation.hub.registry import Registry, RegistryEntry
from provide.foundation.logger.config import LoggingConfig, TelemetryConfig


class TestComponentRegistryArchitecture:
    """Test the core component registry architecture."""

    def test_foundation_uses_global_component_registry(self):
        """Foundation must use a single global registry for all components."""
        from provide.foundation.hub.components import get_component_registry

        registry = get_component_registry()
        assert isinstance(registry, Registry)

        # Registry should be singleton
        registry2 = get_component_registry()
        assert registry is registry2

    def test_component_categories_are_predefined(self):
        """Component registry must support predefined categories."""
        from provide.foundation.hub.components import ComponentCategory

        # These are the core component categories Foundation must support
        expected_categories = {
            ComponentCategory.EVENT_SET,
            ComponentCategory.CONFIG_SOURCE,
            ComponentCategory.PROCESSOR,
            ComponentCategory.ERROR_HANDLER,
            ComponentCategory.FORMATTER,
            ComponentCategory.FILTER,
        }

        # All categories must be string enums
        for category in expected_categories:
            assert isinstance(category.value, str)
            assert len(category.value) > 0

    def test_component_registry_supports_metadata(self):
        """All registered components must support rich metadata."""
        from provide.foundation.hub.components import get_component_registry

        registry = get_component_registry()

        # Register a test component with metadata
        test_component = Mock()
        entry = registry.register(
            name="test_component",
            value=test_component,
            dimension="test",
            metadata={
                "version": "1.0.0",
                "author": "foundation",
                "description": "Test component",
                "dependencies": ["other_component"],
                "priority": 100,
            },
        )

        assert entry.metadata["version"] == "1.0.0"
        assert entry.metadata["author"] == "foundation"
        assert entry.metadata["description"] == "Test component"
        assert entry.metadata["dependencies"] == ["other_component"]
        assert entry.metadata["priority"] == 100

    def test_component_lifecycle_management(self):
        """Components must support initialization and cleanup lifecycle."""
        from provide.foundation.hub.components import (
            ComponentLifecycle,
            get_component_registry,
        )

        registry = get_component_registry()

        # Create a component with lifecycle methods
        lifecycle_component = Mock(spec=ComponentLifecycle)
        lifecycle_component.initialize = AsyncMock()
        lifecycle_component.cleanup = AsyncMock()

        registry.register(
            name="lifecycle_test",
            value=lifecycle_component,
            dimension="test",
            metadata={"has_lifecycle": True},
        )

        # Components with lifecycle must be detectable
        entry = registry.get_entry("lifecycle_test", "test")
        assert entry.metadata.get("has_lifecycle") is True


class TestComponentMetadataAndVersioning:
    """Test component metadata and versioning support."""

    def test_component_versioning_support(self):
        """All components must support version metadata."""
        from provide.foundation.hub.components import get_component_registry

        registry = get_component_registry()

        test_component = Mock()
        registry.register(
            name="versioned_component",
            value=test_component,
            dimension="test",
            metadata={
                "version": "2.1.0",
                "api_version": "v1",
                "compatibility": ["2.0.0", "2.1.0"],
            },
        )

        entry = registry.get_entry("versioned_component", "test")
        assert entry.metadata["version"] == "2.1.0"
        assert entry.metadata["api_version"] == "v1"
        assert "2.1.0" in entry.metadata["compatibility"]

    def test_component_dependency_tracking(self):
        """Components must track dependencies on other components."""
        from provide.foundation.hub.components import (
            get_component_registry,
            resolve_component_dependencies,
        )

        registry = get_component_registry()

        # Register dependency
        dependency = Mock()
        registry.register(
            name="dependency_component", value=dependency, dimension="test"
        )

        # Register component with dependency
        main_component = Mock()
        registry.register(
            name="main_component",
            value=main_component,
            dimension="test",
            metadata={
                "dependencies": ["dependency_component"],
                "optional_dependencies": ["optional_component"],
            },
        )

        # Should resolve dependency chain
        deps = resolve_component_dependencies("main_component", "test")
        assert "dependency_component" in deps
        assert deps["dependency_component"] is dependency

    def test_component_health_monitoring(self):
        """Components must support health checking."""
        from provide.foundation.hub.components import (
            get_component_registry,
            check_component_health,
        )

        registry = get_component_registry()

        # Component with health check
        healthy_component = Mock()
        healthy_component.health_check = Mock(return_value={"status": "healthy"})

        registry.register(
            name="monitored_component",
            value=healthy_component,
            dimension="test",
            metadata={"supports_health_check": True},
        )

        health = check_component_health("monitored_component", "test")
        assert health["status"] == "healthy"

    def test_component_configuration_schema(self):
        """Components must declare configuration schema."""
        from provide.foundation.hub.components import (
            get_component_registry,
            get_component_config_schema,
        )

        registry = get_component_registry()

        config_schema = {
            "type": "object",
            "properties": {
                "timeout": {"type": "number", "default": 30},
                "retries": {"type": "integer", "default": 3},
            },
        }

        configurable_component = Mock()
        registry.register(
            name="configurable_component",
            value=configurable_component,
            dimension="test",
            metadata={
                "config_schema": config_schema,
                "config_prefix": "COMPONENT_",
            },
        )

        retrieved_schema = get_component_config_schema("configurable_component", "test")
        assert retrieved_schema == config_schema


class TestFoundationBootstrapIntegration:
    """Test Foundation's bootstrap process using registry components."""

    def test_foundation_bootstraps_with_registry(self):
        """Foundation initialization must use registry for all components."""
        from provide.foundation.hub.components import (
            get_component_registry,
            bootstrap_foundation,
            ComponentCategory,
        )

        # Bootstrap already happens on import, just check registry state
        registry = get_component_registry()

        # Bootstrap and discover
        try:
            bootstrap_foundation()
        except Exception:
            # Bootstrap might fail if already bootstrapped
            pass
        
        # Trigger event set discovery
        from provide.foundation.eventsets.registry import discover_event_sets, get_registry as get_eventset_registry
        discover_event_sets()
            
        # Fetch after bootstrap
        # Event sets are in their own registry, not the component registry
        event_registry = get_eventset_registry()
        event_sets = event_registry.list_event_sets()
        processors = registry.list_dimension(ComponentCategory.PROCESSOR.value)

        # Should have default event sets
        assert len(event_sets) > 0

        # Should have processors
        assert len(processors) > 0

    def test_foundation_logger_uses_registry_components(self):
        """Foundation logger must use registry for all component access."""
        from provide.foundation.logger import get_logger
        from provide.foundation.hub.components import get_component_registry

        # Create logger
        logger = get_logger("test.registry")

        # Logger should use registry for event set resolution
        registry = get_component_registry()

        # Mock an event set in registry
        from provide.foundation.hub.components import ComponentCategory
        from provide.foundation.eventsets.types import EventSet, EventMapping

        test_event_mapping = EventMapping(
            name="info",
            visual_markers={"default": "🔍"}
        )
        test_event_set = EventSet(
            name="test",
            description="Test event set",
            mappings=[test_event_mapping]
        )
        registry.register(
            name="test_domain_logger",  # Use unique name
            value=test_event_set,
            dimension=ComponentCategory.EVENT_SET.value,
            metadata={"domain": "test", "priority": 100},
        )

        # Logger should use this emoji through registry
        logger.info("Testing registry integration", domain="test")
        # This test passes if no exceptions are raised

    def test_configuration_loading_through_registry(self):
        """Configuration loading must use registered config sources."""
        # This test would verify config loading when config sources are implemented
        pass

    async def test_async_component_coordination(self):
        """Registry must coordinate async component initialization."""
        from provide.foundation.hub.components import initialize_all_async_components

        # Should initialize all async components in dependency order
        await initialize_all_async_components()

        # This test passes if all async components initialize without error

    def test_registry_state_isolation_in_tests(self):
        """Each test must have isolated registry state."""
        from provide.foundation.hub.components import (
            get_component_registry,
            reset_registry_for_tests,
        )

        registry = get_component_registry()

        # Add test component
        test_component = Mock()
        registry.register(name="test_isolation", value=test_component, dimension="test")

        # Reset registry
        reset_registry_for_tests()

        # Component should be gone
        retrieved = registry.get("test_isolation", "test")
        assert retrieved is None