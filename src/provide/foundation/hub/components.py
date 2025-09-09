"""
Registry-based component management system for Foundation.

This module implements Foundation's end-state architecture where all internal
components are managed through the Hub registry system. Provides centralized
component discovery, lifecycle management, and dependency resolution.
"""

import asyncio
from enum import Enum
import inspect
import threading
from typing import Any, Protocol, TypeVar

from attrs import define, field

from provide.foundation.hub.registry import Registry, RegistryEntry
from provide.foundation.logger import get_logger
from provide.foundation.eventsets.types import EventMapping

log = get_logger(__name__)

T = TypeVar("T")


@define(frozen=True, slots=True)
class ComponentInfo:
    """Information about a registered component."""

    name: str = field()
    component_class: type[Any] = field()
    dimension: str = field(default="component")
    version: str | None = field(default=None)
    description: str | None = field(default=None)
    author: str | None = field(default=None)
    tags: list[str] = field(factory=lambda: [])
    metadata: dict[str, Any] = field(factory=lambda: {})


class ComponentCategory(Enum):
    """Predefined component categories for Foundation."""

    CONFIG_SOURCE = "config_source"
    PROCESSOR = "processor"
    ERROR_HANDLER = "error_handler"
    FORMATTER = "formatter"
    FILTER = "filter"
    TRANSPORT = "transport"
    TRANSPORT_MIDDLEWARE = "transport.middleware"
    TRANSPORT_AUTH = "transport.auth"
    TRANSPORT_CACHE = "transport.cache"
    EVENT_SET = "eventset"


class ComponentLifecycle(Protocol):
    """Protocol for components that support lifecycle management."""

    async def initialize(self) -> None:
        """Initialize the component."""
        ...

    async def cleanup(self) -> None:
        """Clean up the component."""
        ...


# Global component registry
_component_registry = Registry()
_registry_lock = threading.RLock()
_initialized_components: dict[tuple[str, str], Any] = {}


def get_component_registry() -> Registry:
    """Get the global component registry."""
    return _component_registry



def resolve_config_value(key: str) -> Any:
    """Resolve configuration value using priority-ordered sources."""
    with _registry_lock:
        registry = get_component_registry()

        # Get all config sources
        all_entries = list(registry)
        config_sources = [
            entry
            for entry in all_entries
            if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
        ]

        # Sort by priority (highest first)
        config_sources.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)

        # Try each source
        for entry in config_sources:
            source = entry.value
            if hasattr(source, "get_value"):
                try:
                    value = source.get_value(key)
                    if value is not None:
                        return value
                except Exception:
                    continue

        return None


def get_config_chain() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    with _registry_lock:
        registry = get_component_registry()

        # Get all config sources
        all_entries = list(registry)
        config_sources = [
            entry
            for entry in all_entries
            if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
        ]

        # Sort by priority (highest first)
        config_sources.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
        return config_sources


async def load_all_configs() -> dict[str, Any]:
    """Load configurations from all registered sources."""
    configs = {}
    chain = get_config_chain()

    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                if inspect.iscoroutinefunction(source.load_config):
                    source_config = await source.load_config()
                else:
                    source_config = source.load_config()

                if source_config:
                    configs.update(source_config)
            except Exception as e:
                log.warning(
                    "Config source failed to load", source=entry.name, error=str(e)
                )

    return configs


def get_processor_pipeline() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    with _registry_lock:
        registry = get_component_registry()

        # Get all processors
        all_entries = list(registry)
        processors = [
            entry
            for entry in all_entries
            if entry.dimension == ComponentCategory.PROCESSOR.value
        ]

        # Sort by priority (highest first)
        processors.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
        return processors


def get_processors_for_stage(stage: str) -> list[RegistryEntry]:
    """Get processors for a specific processing stage."""
    pipeline = get_processor_pipeline()
    return [entry for entry in pipeline if entry.metadata.get("stage") == stage]


def get_handlers_for_exception(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    with _registry_lock:
        registry = get_component_registry()

        # Get all error handlers
        all_entries = list(registry)
        handlers = [
            entry
            for entry in all_entries
            if entry.dimension == ComponentCategory.ERROR_HANDLER.value
        ]

        # Filter by exception type
        exception_type_name = type(exception).__name__
        matching_handlers = []

        for entry in handlers:
            exception_types = entry.metadata.get("exception_types", [])
            if any(
                exc_type in exception_type_name or exception_type_name in exc_type
                for exc_type in exception_types
            ):
                matching_handlers.append(entry)

        # Sort by priority (highest first)
        matching_handlers.sort(
            key=lambda e: e.metadata.get("priority", 0), reverse=True
        )
        return matching_handlers


def execute_error_handlers(
    exception: Exception, context: dict[str, Any]
) -> dict[str, Any] | None:
    """Execute error handlers until one handles the exception."""
    handlers = get_handlers_for_exception(exception)

    for entry in handlers:
        handler = entry.value
        try:
            result = handler(exception, context)
            if result is not None:
                return result
        except Exception as handler_error:
            log.error(
                "Error handler failed", handler=entry.name, error=str(handler_error)
            )

    return None


def resolve_component_dependencies(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    with _registry_lock:
        registry = get_component_registry()
        entry = registry.get_entry(name, dimension)

        if not entry:
            return {}

        dependencies = {}
        dep_names = entry.metadata.get("dependencies", [])

        for dep_name in dep_names:
            # Try same dimension first
            dep_component = registry.get(dep_name, dimension)
            if dep_component is not None:
                dependencies[dep_name] = dep_component
            else:
                # Search across dimensions
                dep_component = registry.get(dep_name)
                if dep_component is not None:
                    dependencies[dep_name] = dep_component

        return dependencies


def check_component_health(name: str, dimension: str) -> dict[str, Any]:
    """Check component health status."""
    with _registry_lock:
        registry = get_component_registry()
        component = registry.get(name, dimension)

        if not component:
            return {"status": "not_found"}

        entry = registry.get_entry(name, dimension)
        if not entry.metadata.get("supports_health_check", False):
            return {"status": "no_health_check"}

        if hasattr(component, "health_check"):
            try:
                return component.health_check()
            except Exception as e:
                return {"status": "error", "error": str(e)}

        return {"status": "unknown"}


def get_component_config_schema(name: str, dimension: str) -> dict[str, Any] | None:
    """Get component configuration schema."""
    with _registry_lock:
        registry = get_component_registry()
        entry = registry.get_entry(name, dimension)

        if not entry:
            return None

        return entry.metadata.get("config_schema")


def get_or_initialize_component(name: str, dimension: str) -> Any:
    """Get component, initializing lazily if needed."""
    with _registry_lock:
        key = (name, dimension)

        # Return already initialized component
        if key in _initialized_components:
            return _initialized_components[key]

        registry = get_component_registry()
        entry = registry.get_entry(name, dimension)

        if not entry:
            return None

        # If already initialized, return it
        if entry.value is not None:
            _initialized_components[key] = entry.value
            return entry.value

        # Initialize lazily
        if entry.metadata.get("lazy", False):
            factory = entry.metadata.get("factory")
            if factory:
                try:
                    component = factory()
                    # Update registry with initialized component
                    registry.register(
                        name=name,
                        value=component,
                        dimension=dimension,
                        metadata=entry.metadata,
                        replace=True,
                    )
                    _initialized_components[key] = component
                    return component
                except Exception as e:
                    log.error(
                        "Component initialization failed",
                        component=name,
                        dimension=dimension,
                        error=str(e),
                    )

        return entry.value


async def initialize_async_component(name: str, dimension: str) -> Any:
    """Initialize component asynchronously."""
    with _registry_lock:
        key = (name, dimension)

        # Return already initialized component
        if key in _initialized_components:
            return _initialized_components[key]

        registry = get_component_registry()
        entry = registry.get_entry(name, dimension)

        if not entry:
            return None

        # Initialize with async factory
        if entry.metadata.get("async", False):
            factory = entry.metadata.get("factory")
            if factory:
                try:
                    if inspect.iscoroutinefunction(factory):
                        component = await factory()
                    else:
                        component = factory()

                    # Update registry
                    registry.register(
                        name=name,
                        value=component,
                        dimension=dimension,
                        metadata=entry.metadata,
                        replace=True,
                    )
                    _initialized_components[key] = component
                    return component
                except Exception as e:
                    log.error(
                        "Async component initialization failed",
                        component=name,
                        dimension=dimension,
                        error=str(e),
                    )

        return entry.value


def cleanup_all_components(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    with _registry_lock:
        registry = get_component_registry()

        if dimension:
            entries = [entry for entry in registry if entry.dimension == dimension]
        else:
            entries = list(registry)

        for entry in entries:
            if entry.metadata.get("supports_cleanup", False):
                component = entry.value
                if hasattr(component, "cleanup"):
                    try:
                        cleanup_func = component.cleanup
                        if inspect.iscoroutinefunction(cleanup_func):
                            # Run async cleanup
                            loop = None
                            try:
                                loop = asyncio.get_event_loop()
                                if loop.is_running():
                                    # Create task if loop is running
                                    loop.create_task(cleanup_func())
                                else:
                                    loop.run_until_complete(cleanup_func())
                            except RuntimeError:
                                # Create new loop if none exists
                                loop = asyncio.new_event_loop()
                                loop.run_until_complete(cleanup_func())
                                loop.close()
                        else:
                            cleanup_func()
                    except Exception as e:
                        log.error(
                            "Component cleanup failed",
                            component=entry.name,
                            dimension=entry.dimension,
                            error=str(e),
                        )


def bootstrap_foundation() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Event sets are now managed by the eventsets module

    # Config sources would be registered here when implemented

    # Register core processors
    def timestamp_processor(logger, method_name, event_dict):
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
    )

    log.debug("Foundation bootstrap completed with registry components")


def load_config_from_registry(config_class: type[T]) -> T:
    """Load configuration using registered config sources."""
    configs = {}

    # Use sync version for now - async version needs event loop handling
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                if not inspect.iscoroutinefunction(source.load_config):
                    source_config = source.load_config()
                    if source_config:
                        configs.update(source_config)
            except Exception as e:
                log.warning("Config source failed", source=entry.name, error=str(e))

    return config_class.from_dict(configs)


async def initialize_all_async_components() -> None:
    """Initialize all async components in dependency order."""
    registry = get_component_registry()

    # Get all async components
    async_components = [
        entry for entry in registry if entry.metadata.get("async", False)
    ]

    # Sort by priority for initialization order
    async_components.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)

    # Initialize each component
    for entry in async_components:
        try:
            await initialize_async_component(entry.name, entry.dimension)
        except Exception as e:
            log.error(
                "Failed to initialize async component",
                component=entry.name,
                dimension=entry.dimension,
                error=str(e),
            )


def reset_registry_for_tests() -> None:
    """Reset registry state for test isolation."""
    with _registry_lock:
        global _initialized_components
        _component_registry.clear()
        _initialized_components.clear()


def discover_components(
    group: str,
    dimension: str = "component",
    registry: Registry | None = None,
) -> dict[str, type[Any]]:
    """
    Discover and register components from entry points.

    This is a stub for the TDD implementation.
    """
    return {}


# Bootstrap on module import
bootstrap_foundation()
