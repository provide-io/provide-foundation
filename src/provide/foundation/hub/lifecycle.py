"""
Hub component lifecycle management utilities.

Provides functions for initializing, managing, and cleaning up components
registered in the Hub registry system.
"""

import asyncio
import inspect
from typing import Any

from provide.foundation.logger import get_logger

log = get_logger(__name__)


def _get_registry_and_globals():
    """Get registry, lock, and initialized components from components module."""
    from provide.foundation.hub.components import (
        get_component_registry, 
        _registry_lock, 
        _initialized_components
    )
    return get_component_registry(), _registry_lock, _initialized_components


def get_or_initialize_component(name: str, dimension: str) -> Any:
    """Get component, initializing lazily if needed."""
    registry, registry_lock, initialized_components = _get_registry_and_globals()
    
    with registry_lock:
        key = (name, dimension)

        # Return already initialized component
        if key in initialized_components:
            return initialized_components[key]

        entry = registry.get_entry(name, dimension)

        if not entry:
            return None

        # If already initialized, return it
        if entry.value is not None:
            initialized_components[key] = entry.value
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
                    initialized_components[key] = component
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
    registry, registry_lock, initialized_components = _get_registry_and_globals()
    
    with registry_lock:
        key = (name, dimension)

        # Return already initialized component
        if key in initialized_components:
            return initialized_components[key]

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
                    initialized_components[key] = component
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
    registry, registry_lock, _ = _get_registry_and_globals()
    
    with registry_lock:
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


async def initialize_all_async_components() -> None:
    """Initialize all async components in dependency order."""
    registry, _, _ = _get_registry_and_globals()

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


__all__ = [
    "get_or_initialize_component",
    "initialize_async_component", 
    "cleanup_all_components",
    "initialize_all_async_components",
]