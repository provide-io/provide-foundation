"""
Hub component discovery and dependency resolution utilities.

Provides functions for discovering components and resolving their dependencies
in the Hub registry system.
"""

from typing import Any

from provide.foundation.hub.registry import Registry


def _get_registry_and_lock():
    """Get registry and lock from components module."""
    from provide.foundation.hub.components import get_component_registry, _registry_lock
    return get_component_registry(), _registry_lock


def resolve_component_dependencies(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry, registry_lock = _get_registry_and_lock()
    
    with registry_lock:
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


__all__ = [
    "resolve_component_dependencies",
    "discover_components",
]