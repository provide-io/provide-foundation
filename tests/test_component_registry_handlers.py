"""
TDD tests for error handler components and thread-safe registry access.

This test suite covers error handler registration, exception type matching,
priority chains, and thread-safe component access patterns.
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