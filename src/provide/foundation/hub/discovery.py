#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

from provide.foundation.errors.decorators import resilient
from provide.foundation.hub.categories import ComponentCategory
from provide.foundation.hub.registry import Registry

"""Hub component discovery and dependency resolution utilities.

Provides functions for discovering components and resolving their dependencies
in the Hub registry system.
"""


def _get_registry_and_lock() -> Any:
    """Get registry from components module."""
    from provide.foundation.hub.components import get_component_registry

    return get_component_registry()


def resolve_component_dependencies(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = _get_registry_and_lock()

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


@resilient(
    fallback=None,
    suppress=(Exception,),
    log_errors=False,  # Avoid circular dependency with logger during hub initialization
    reraise=False,
)
def _load_entry_point(
    entry_point: Any,
    registry: Registry,
    dimension: str,
) -> tuple[str, type[Any]] | None:
    """Load and register a single entry point.

    Args:
        entry_point: Entry point to load
        registry: Registry to register component in
        dimension: Registry dimension for the component

    Returns:
        Tuple of (name, component_class) if successful, None otherwise

    """
    import sys

    try:
        # Load the component class
        component_class = entry_point.load()

        # Register in the provided registry
        registry.register(
            name=entry_point.name,
            value=component_class,
            dimension=dimension,
            metadata={
                "entry_point": entry_point.name,
                "module": entry_point.module,
                "discovered": True,
            },
        )

        return entry_point.name, component_class

    except Exception as e:
        # Print error to stderr (avoid circular dependency with logger)
        print(f"Failed to load entry point {entry_point.name}: {e}", file=sys.stderr)
        return None


@resilient(
    fallback={},
    suppress=(Exception,),
    log_errors=False,  # Avoid circular dependency with logger during hub initialization
    reraise=False,
)
def _get_entry_points(group: str) -> Any:
    """Get entry points for a group.

    Args:
        group: Entry point group name

    Returns:
        Entry points for the group

    """
    import sys

    try:
        from importlib import metadata
    except ImportError:
        # Python < 3.8 fallback
        import importlib_metadata as metadata  # type: ignore

    try:
        entry_points = metadata.entry_points()
        # Python 3.11+ API
        return entry_points.select(group=group)
    except Exception as e:
        print(f"Failed to discover entry points for group {group}: {e}", file=sys.stderr)
        return []


def discover_components(
    group: str,
    dimension: str | None = None,
    registry: Registry | None = None,
) -> dict[str, type[Any]]:
    """Discover and register components from entry points.

    Uses the @resilient decorator for standardized error handling.

    Args:
        group: Entry point group name (e.g., 'provide.components')
        dimension: Registry dimension for components (defaults to "component")
        registry: Optional registry to use (defaults to global registry)

    Returns:
        Dictionary mapping component names to their classes

    """
    # Use ComponentCategory default if not specified
    if dimension is None:
        dimension = ComponentCategory.COMPONENT.value

    discovered = {}

    # If no registry provided, get the global component registry
    if registry is None:
        registry = _get_registry_and_lock()

    # Get entry points for the group (with resilient error handling)
    group_entries = _get_entry_points(group)

    # Load each entry point (with resilient error handling per entry point)
    for entry_point in group_entries:
        result = _load_entry_point(entry_point, registry, dimension)
        if result is not None:
            name, component_class = result
            discovered[name] = component_class

    return discovered


__all__ = [
    "discover_components",
    "resolve_component_dependencies",
]

# 🧱🏗️🔚
