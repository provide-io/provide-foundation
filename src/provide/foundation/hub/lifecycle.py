#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import asyncio
import inspect
from typing import Any

from provide.foundation.hub.foundation import get_foundation_logger

"""Hub component lifecycle management utilities.

Provides functions for initializing, managing, and cleaning up components
registered in the Hub registry system.
"""

# No global async lock - registry handles its own thread safety
# and _initialized_components dict access is simplified


def _get_registry_and_globals() -> Any:
    """Get registry and initialized components from components module."""
    from provide.foundation.hub.components import (
        _initialized_components,
        get_component_registry,
    )

    return get_component_registry(), _initialized_components


def get_or_initialize_component(name: str, dimension: str) -> Any:
    """Get component, initializing lazily if needed."""
    registry, initialized_components = _get_registry_and_globals()
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
                get_foundation_logger().error(
                    "Component initialization failed",
                    component=name,
                    dimension=dimension,
                    error=str(e),
                )
                # Return None on failure for resilient behavior
                return None

    return entry.value


async def initialize_async_component(name: str, dimension: str) -> Any:
    """Initialize component asynchronously."""
    registry, initialized_components = _get_registry_and_globals()
    key = (name, dimension)

    # First, check if already initialized
    if key in initialized_components:
        return initialized_components[key]

    # Registry operations are thread-safe internally, no external lock needed
    entry = registry.get_entry(name, dimension)

    if not entry:
        return None

    # If not async or no factory, return current value
    if not entry.metadata.get("async", False):
        return entry.value

    factory = entry.metadata.get("factory")
    if not factory:
        return entry.value

    # Double-check if already initialized
    if key in initialized_components:
        return initialized_components[key]

    # Initialize component outside any lock
    try:
        if inspect.iscoroutinefunction(factory):
            component = await factory()
        else:
            component = factory()

        # Update both registry and initialized_components
        # Registry handles its own thread-safety
        registry.register(
            name=name,
            value=component,
            dimension=dimension,
            metadata=entry.metadata,
            replace=True,
        )

        # Update initialized_components cache
        # Final check before update (race condition is acceptable here)
        if key not in initialized_components:
            initialized_components[key] = component
        return initialized_components[key]

    except Exception as e:
        get_foundation_logger().error(
            "Async component initialization failed",
            component=name,
            dimension=dimension,
            error=str(e),
        )
        # Return None on failure for resilient behavior
        return None


def cleanup_all_components(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = _get_registry_and_globals()

    entries = [entry for entry in registry if entry.dimension == dimension] if dimension else list(registry)

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
                                task = loop.create_task(cleanup_func())
                                # Store reference to prevent garbage collection
                                task.add_done_callback(lambda t: None)
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
                    get_foundation_logger().error(
                        "Component cleanup failed",
                        component=entry.name,
                        dimension=entry.dimension,
                        error=str(e),
                    )
                    # Log but don't re-raise during cleanup to allow other components to clean up


async def initialize_all_async_components() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", False)]

    # Sort by priority for initialization order
    async_components.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)

    # Initialize each component
    for entry in async_components:
        try:
            await initialize_async_component(entry.name, entry.dimension)
        except Exception as e:
            get_foundation_logger().error(
                "Failed to initialize async component",
                component=entry.name,
                dimension=entry.dimension,
                error=str(e),
            )
            # Log but don't re-raise to allow other components to initialize


__all__ = [
    "cleanup_all_components",
    "get_or_initialize_component",
    "initialize_all_async_components",
    "initialize_async_component",
]

# 🧱🏗️🔚
