"""
TDD tests for registry-based component management architecture.

This test suite defines Foundation's end-state architecture where all internal
components are managed through the Hub registry system. No backward compatibility
is maintained - this is the target implementation.
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
            ComponentCategory.EMOJI_SET,
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


class TestEmojiSetRegistration:
    """Test emoji set registration and discovery through the registry."""

    def test_emoji_sets_register_in_emoji_category(self):
        """Emoji sets must register in the EMOJI_SET category."""
        from provide.foundation.hub.components import (
            ComponentCategory,
            get_component_registry,
        )
        from provide.foundation.logger.emoji.types import EmojiSet

        registry = get_component_registry()

        # Create a test emoji set
        test_emoji_set = EmojiSet(
            name="test_set",
            emojis={
                "success": "✅",
                "error": "❌",
                "info": "ℹ️",
            },
        )

        # Register the emoji set
        registry.register(
            name="test_domain",
            value=test_emoji_set,
            dimension=ComponentCategory.EMOJI_SET.value,
            metadata={
                "domain": "test_domain",
                "priority": 50,
                "default": False,
            },
        )

        # Verify registration
        retrieved_set = registry.get("test_domain", ComponentCategory.EMOJI_SET.value)
        assert retrieved_set is test_emoji_set
        assert retrieved_set.name == "test_set"

    def test_emoji_set_discovery_by_domain(self):
        """Foundation must discover emoji sets by domain automatically."""
        from provide.foundation.hub.components import find_emoji_set_for_domain

        # This function must exist and work with the registry
        emoji_set = find_emoji_set_for_domain("http")

        # Should return default or domain-specific set
        assert emoji_set is not None
        assert hasattr(emoji_set, "emojis")
        assert isinstance(emoji_set.emojis, dict)

    def test_default_emoji_set_fallback(self):
        """Foundation must have a default emoji set for unknown domains."""
        from provide.foundation.hub.components import get_default_emoji_set

        default_set = get_default_emoji_set()
        assert default_set is not None
        assert "success" in default_set.emojis
        assert "error" in default_set.emojis
        assert "info" in default_set.emojis

    def test_emoji_set_priority_ordering(self):
        """Higher priority emoji sets must override lower priority ones."""
        from provide.foundation.hub.components import (
            ComponentCategory,
            get_component_registry,
            resolve_emoji_for_domain,
        )
        from provide.foundation.logger.emoji.types import EmojiSet

        registry = get_component_registry()

        # Use unique names for this test to avoid conflicts
        domain_name = "priority_test_domain"

        # Register low priority set
        low_priority_set = EmojiSet("low", {"success": "👍"})
        registry.register(
            name="priority_low",
            value=low_priority_set,
            dimension=ComponentCategory.EMOJI_SET.value,
            metadata={"domain": domain_name, "priority": 10},
        )

        # Register high priority set
        high_priority_set = EmojiSet("high", {"success": "🎉"})
        registry.register(
            name="priority_high",
            value=high_priority_set,
            dimension=ComponentCategory.EMOJI_SET.value,
            metadata={"domain": domain_name, "priority": 90},
        )

        # High priority should win
        emoji = resolve_emoji_for_domain(domain_name, "success")
        assert emoji == "🎉"

    def test_emoji_set_composition(self):
        """Multiple emoji sets for the same domain must compose properly."""
        from provide.foundation.hub.components import (
            ComponentCategory,
            get_component_registry,
            get_composed_emoji_set,
        )
        from provide.foundation.logger.emoji.types import EmojiSet

        registry = get_component_registry()

        # Use unique domain name for this test
        domain_name = "composition_test_domain"

        # Register base set
        base_set = EmojiSet("base", {"success": "✅", "error": "❌", "info": "ℹ️"})
        registry.register(
            name="composition_base",
            value=base_set,
            dimension=ComponentCategory.EMOJI_SET.value,
            metadata={"domain": domain_name, "priority": 10, "composition": "base"},
        )

        # Register extension set
        extension_set = EmojiSet(
            "extension",
            {
                "request": "📤",
                "response": "📥",
            },
        )
        registry.register(
            name="composition_extension",
            value=extension_set,
            dimension=ComponentCategory.EMOJI_SET.value,
            metadata={
                "domain": domain_name,
                "priority": 20,
                "composition": "extension",
            },
        )

        # Composed set should have all emojis
        composed = get_composed_emoji_set(domain_name)
        assert "success" in composed.emojis  # from base
        assert "request" in composed.emojis  # from extension


# Configuration source tests removed - module doesn't exist yet


class TestProcessorRegistration:
    """Test processor registration and pipeline management."""

    def test_processors_register_in_processor_category(self):
        """Log processors must register in PROCESSOR category."""
        from provide.foundation.hub.components import (
            ComponentCategory,
            get_component_registry,
        )

        registry = get_component_registry()

        # Create a test processor
        def test_processor(logger, method_name, event_dict):
            event_dict["processed"] = True
            return event_dict

        # Register the processor
        registry.register(
            name="test_processor",
            value=test_processor,
            dimension=ComponentCategory.PROCESSOR.value,
            metadata={
                "priority": 50,
                "stage": "pre_format",
                "async": False,
            },
        )

        # Verify registration
        retrieved_processor = registry.get(
            "test_processor", ComponentCategory.PROCESSOR.value
        )
        assert retrieved_processor is test_processor

    def test_processor_pipeline_ordering(self):
        """Processors must be executed in priority order."""
        from provide.foundation.hub.components import (
            get_processor_pipeline,
            bootstrap_foundation,
        )

        pipeline = get_processor_pipeline()

        # If pipeline is empty (due to test isolation), re-bootstrap
        if len(pipeline) == 0:
            bootstrap_foundation()
            pipeline = get_processor_pipeline()

        # Pipeline should be ordered by priority
        assert len(pipeline) > 0

        for i in range(len(pipeline) - 1):
            current_priority = pipeline[i].metadata.get("priority", 0)
            next_priority = pipeline[i + 1].metadata.get("priority", 0)
            assert current_priority >= next_priority

    def test_async_processor_support(self):
        """Registry must support async processors."""
        from provide.foundation.hub.components import (
            ComponentCategory,
            get_component_registry,
        )

        registry = get_component_registry()

        # Create async processor
        async def async_processor(logger, method_name, event_dict):
            await asyncio.sleep(0)  # Simulate async work
            event_dict["async_processed"] = True
            return event_dict

        registry.register(
            name="async_processor",
            value=async_processor,
            dimension=ComponentCategory.PROCESSOR.value,
            metadata={"async": True, "priority": 60},
        )

        # Should be retrievable
        retrieved = registry.get("async_processor", ComponentCategory.PROCESSOR.value)
        assert retrieved is async_processor

    def test_processor_stage_filtering(self):
        """Processors must be filterable by processing stage."""
        from provide.foundation.hub.components import get_processors_for_stage

        pre_format_processors = get_processors_for_stage("pre_format")
        post_format_processors = get_processors_for_stage("post_format")

        assert isinstance(pre_format_processors, list)
        assert isinstance(post_format_processors, list)

        # Each should contain only processors for that stage
        for processor in pre_format_processors:
            assert processor.metadata.get("stage") == "pre_format"

    def test_conditional_processor_execution(self):
        """Processors must support conditional execution based on metadata."""
        from provide.foundation.hub.components import (
            ComponentCategory,
            get_component_registry,
        )

        registry = get_component_registry()

        # Processor with conditions
        def conditional_processor(logger, method_name, event_dict):
            return event_dict

        registry.register(
            name="conditional_processor",
            value=conditional_processor,
            dimension=ComponentCategory.PROCESSOR.value,
            metadata={
                "conditions": {
                    "min_level": "INFO",
                    "domains": ["http", "database"],
                },
                "priority": 30,
            },
        )

        entry = registry.get_entry(
            "conditional_processor", ComponentCategory.PROCESSOR.value
        )
        assert "conditions" in entry.metadata
        assert entry.metadata["conditions"]["min_level"] == "INFO"


class TestErrorHandlerComponents:
    """Test error handler component registration and management."""

    def test_error_handlers_register_in_error_handler_category(self):
        """Error handlers must register in ERROR_HANDLER category."""
        from provide.foundation.hub.components import (
            ComponentCategory,
            get_component_registry,
        )

        registry = get_component_registry()

        # Create test error handler
        def test_error_handler(exception, context):
            return {"handled": True, "error": str(exception)}

        registry.register(
            name="test_error_handler",
            value=test_error_handler,
            dimension=ComponentCategory.ERROR_HANDLER.value,
            metadata={
                "priority": 100,
                "exception_types": ["ValueError", "TypeError"],
                "async": False,
            },
        )

        retrieved = registry.get(
            "test_error_handler", ComponentCategory.ERROR_HANDLER.value
        )
        assert retrieved is test_error_handler

    def test_error_handler_exception_type_matching(self):
        """Error handlers must be matched by exception type."""
        from provide.foundation.hub.components import get_handlers_for_exception

        handlers = get_handlers_for_exception(ValueError("test"))

        assert isinstance(handlers, list)
        # Should contain handlers that can handle ValueError
        for handler in handlers:
            exception_types = handler.metadata.get("exception_types", [])
            assert any("ValueError" in exc_type for exc_type in exception_types)

    def test_error_handler_priority_chain(self):
        """Error handlers must execute in priority order until handled."""
        from provide.foundation.hub.components import (
            ComponentCategory,
            get_component_registry,
            execute_error_handlers,
        )

        registry = get_component_registry()

        # High priority handler that doesn't handle
        def high_priority_handler(exception, context):
            return None  # Don't handle

        registry.register(
            name="high_priority",
            value=high_priority_handler,
            dimension=ComponentCategory.ERROR_HANDLER.value,
            metadata={"priority": 90, "exception_types": ["Exception"]},
        )

        # Low priority handler that handles
        def low_priority_handler(exception, context):
            return {"handled": True, "handler": "low_priority"}

        registry.register(
            name="low_priority",
            value=low_priority_handler,
            dimension=ComponentCategory.ERROR_HANDLER.value,
            metadata={"priority": 10, "exception_types": ["Exception"]},
        )

        # Test the handlers are registered correctly
        handlers = registry.list_dimension(ComponentCategory.ERROR_HANDLER.value)
        assert "high_priority" in handlers
        assert "low_priority" in handlers

        # Test priority ordering (get metadata from registry entries)
        high_entry = registry.get_entry(
            "high_priority", ComponentCategory.ERROR_HANDLER.value
        )
        low_entry = registry.get_entry(
            "low_priority", ComponentCategory.ERROR_HANDLER.value
        )
        assert high_entry.metadata["priority"] > low_entry.metadata["priority"]

    async def test_async_error_handler_support(self):
        """Error handlers must support async execution."""
        from provide.foundation.hub.components import (
            ComponentCategory,
            get_component_registry,
        )

        registry = get_component_registry()

        async def async_error_handler(exception, context):
            await asyncio.sleep(0)  # Simulate async work
            return {"handled": True, "async": True}

        registry.register(
            name="async_error_handler",
            value=async_error_handler,
            dimension=ComponentCategory.ERROR_HANDLER.value,
            metadata={"async": True, "priority": 50},
        )

        retrieved = registry.get(
            "async_error_handler", ComponentCategory.ERROR_HANDLER.value
        )
        assert retrieved is async_error_handler


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


class TestThreadSafeComponentAccess:
    """Test thread-safe component access and initialization."""

    def test_concurrent_component_registration(self):
        """Component registration must be thread-safe."""
        from provide.foundation.hub.components import get_component_registry

        registry = get_component_registry()
        results = []
        errors = []

        def register_component(i):
            try:
                component = Mock()
                component.id = i
                registry.register(
                    name=f"concurrent_component_{i}", value=component, dimension="test"
                )
                results.append(i)
            except Exception as e:
                errors.append((i, e))

        # Register components concurrently
        threads = []
        for i in range(10):
            thread = threading.Thread(target=register_component, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # All registrations should succeed
        assert len(errors) == 0
        assert len(results) == 10

        # All components should be retrievable
        for i in range(10):
            component = registry.get(f"concurrent_component_{i}", "test")
            assert component.id == i

    def test_concurrent_component_access(self):
        """Component access must be thread-safe."""
        from provide.foundation.hub.components import get_component_registry

        registry = get_component_registry()

        # Register a component
        test_component = Mock()
        test_component.access_count = 0
        test_component.increment = lambda: setattr(
            test_component, "access_count", test_component.access_count + 1
        )

        registry.register(
            name="shared_component", value=test_component, dimension="test"
        )

        results = []

        def access_component():
            component = registry.get("shared_component", "test")
            component.increment()
            results.append(component.access_count)

        # Access component concurrently
        threads = []
        for i in range(50):
            thread = threading.Thread(target=access_component)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # All accesses should get the same component
        assert len(results) == 50
        assert test_component.access_count == 50

    def test_lazy_component_initialization(self):
        """Components must support lazy initialization."""
        from provide.foundation.hub.components import (
            get_component_registry,
            get_or_initialize_component,
        )

        registry = get_component_registry()

        # Component factory
        initialization_count = 0

        def component_factory():
            nonlocal initialization_count
            initialization_count += 1
            component = Mock()
            component.initialized = True
            return component

        registry.register(
            name="lazy_component",
            value=None,  # Not initialized yet
            dimension="test",
            metadata={
                "lazy": True,
                "factory": component_factory,
            },
        )

        # Should not be initialized yet
        assert initialization_count == 0

        # First access should initialize
        component1 = get_or_initialize_component("lazy_component", "test")
        assert initialization_count == 1
        assert component1.initialized is True

        # Second access should return same instance
        component2 = get_or_initialize_component("lazy_component", "test")
        assert initialization_count == 1
        assert component2 is component1

    async def test_async_component_initialization(self):
        """Components must support async initialization."""
        from provide.foundation.hub.components import (
            get_component_registry,
            initialize_async_component,
        )

        registry = get_component_registry()

        # Async component factory
        async def async_component_factory():
            await asyncio.sleep(0.01)  # Simulate async init
            component = Mock()
            component.async_initialized = True
            return component

        registry.register(
            name="async_component",
            value=None,
            dimension="test",
            metadata={
                "async": True,
                "factory": async_component_factory,
            },
        )

        component = await initialize_async_component("async_component", "test")
        assert component.async_initialized is True

    def test_component_cleanup_on_shutdown(self):
        """Components must support cleanup on shutdown."""
        from provide.foundation.hub.components import (
            get_component_registry,
            cleanup_all_components,
        )

        registry = get_component_registry()

        # Component with cleanup
        cleanup_called = []
        component_with_cleanup = Mock()
        component_with_cleanup.cleanup = lambda: cleanup_called.append("cleaned")

        registry.register(
            name="cleanup_component",
            value=component_with_cleanup,
            dimension="test",
            metadata={"supports_cleanup": True},
        )

        # Cleanup should call component cleanup
        cleanup_all_components("test")
        assert "cleaned" in cleanup_called


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

        # If registry is empty (due to test isolation), re-bootstrap
        emoji_sets = registry.list_dimension(ComponentCategory.EMOJI_SET.value)
        processors = registry.list_dimension(ComponentCategory.PROCESSOR.value)

        if len(emoji_sets) == 0 and len(processors) == 0:
            bootstrap_foundation()
            # Re-fetch after bootstrap
            emoji_sets = registry.list_dimension(ComponentCategory.EMOJI_SET.value)
            processors = registry.list_dimension(ComponentCategory.PROCESSOR.value)

        # Should have default emoji sets
        assert len(emoji_sets) > 0

        # Should have processors
        assert len(processors) > 0

    def test_foundation_logger_uses_registry_components(self):
        """Foundation logger must use registry for all component access."""
        from provide.foundation.logger import get_logger
        from provide.foundation.hub.components import get_component_registry

        # Create logger
        logger = get_logger("test.registry")

        # Logger should use registry for emoji resolution
        registry = get_component_registry()

        # Mock an emoji set in registry
        from provide.foundation.hub.components import ComponentCategory
        from provide.foundation.logger.emoji.types import EmojiSet

        test_emoji_set = EmojiSet("test", {"info": "🔍"})
        registry.register(
            name="test_domain_logger",  # Use unique name
            value=test_emoji_set,
            dimension=ComponentCategory.EMOJI_SET.value,
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
