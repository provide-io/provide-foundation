from __future__ import annotations

from typing import Any

from provide.foundation.hub.registry import Registry

"""Hub component discovery and dependency resolution utilities.

Provides functions for discovering components and resolving their dependencies
in the Hub registry system.
"""


def _get_registry_and_lock() -> tuple[Any, Any]:
    """Get registry and lock from components module."""
    from provide.foundation.hub.components import _registry_lock, get_component_registry

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
    """Discover and register components from entry points.

    Args:
        group: Entry point group name (e.g., 'provide.components')
        dimension: Registry dimension for components
        registry: Optional registry to use (defaults to global registry)

    Returns:
        Dictionary mapping component names to their classes

    """
    try:
        from importlib import metadata
    except ImportError:
        # Python < 3.8 fallback
        import importlib_metadata as metadata  # type: ignore

    discovered = {}

    # If no registry provided, get the global component registry
    if registry is None:
        registry, _ = _get_registry_and_lock()

    # Discover all entry points in the specified group
    try:
        entry_points = metadata.entry_points()
        if hasattr(entry_points, "select"):
            # Python 3.10+ API
            group_entries = entry_points.select(group=group)
        else:
            # Python 3.8-3.9 API
            group_entries = entry_points.get(group, [])

        for entry_point in group_entries:
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

                discovered[entry_point.name] = component_class

            except Exception as e:
                # Log error but continue discovering other components
                import sys

                print(f"Failed to load entry point {entry_point.name}: {e}", file=sys.stderr)
                continue

    except Exception as e:
        # If entry points can't be read, return empty dict
        import sys

        print(f"Failed to discover entry points for group {group}: {e}", file=sys.stderr)

    return discovered


__all__ = [
    "discover_components",
    "resolve_component_dependencies",
]
