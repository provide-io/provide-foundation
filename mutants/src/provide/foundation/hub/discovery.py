# provide/foundation/hub/discovery.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

from provide.foundation.errors.decorators import resilient
from provide.foundation.hub.categories import ComponentCategory
from provide.foundation.hub.registry import Registry

"""Hub component discovery and dependency resolution utilities.

Provides functions for discovering components and resolving their dependencies
in the Hub registry system.
"""
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def _get_registry_and_lock() -> Any:
    """Get registry from components module."""
    from provide.foundation.hub.components import get_component_registry

    return get_component_registry()


def x_resolve_component_dependencies__mutmut_orig(name: str, dimension: str) -> dict[str, Any]:
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


def x_resolve_component_dependencies__mutmut_1(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = None

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


def x_resolve_component_dependencies__mutmut_2(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = _get_registry_and_lock()

    entry = None

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


def x_resolve_component_dependencies__mutmut_3(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = _get_registry_and_lock()

    entry = registry.get_entry(None, dimension)

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


def x_resolve_component_dependencies__mutmut_4(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = _get_registry_and_lock()

    entry = registry.get_entry(name, None)

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


def x_resolve_component_dependencies__mutmut_5(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = _get_registry_and_lock()

    entry = registry.get_entry(dimension)

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


def x_resolve_component_dependencies__mutmut_6(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = _get_registry_and_lock()

    entry = registry.get_entry(name, )

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


def x_resolve_component_dependencies__mutmut_7(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = _get_registry_and_lock()

    entry = registry.get_entry(name, dimension)

    if entry:
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


def x_resolve_component_dependencies__mutmut_8(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = _get_registry_and_lock()

    entry = registry.get_entry(name, dimension)

    if not entry:
        return {}

    dependencies = None
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


def x_resolve_component_dependencies__mutmut_9(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = _get_registry_and_lock()

    entry = registry.get_entry(name, dimension)

    if not entry:
        return {}

    dependencies = {}
    dep_names = None

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


def x_resolve_component_dependencies__mutmut_10(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = _get_registry_and_lock()

    entry = registry.get_entry(name, dimension)

    if not entry:
        return {}

    dependencies = {}
    dep_names = entry.metadata.get(None, [])

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


def x_resolve_component_dependencies__mutmut_11(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = _get_registry_and_lock()

    entry = registry.get_entry(name, dimension)

    if not entry:
        return {}

    dependencies = {}
    dep_names = entry.metadata.get("dependencies", None)

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


def x_resolve_component_dependencies__mutmut_12(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = _get_registry_and_lock()

    entry = registry.get_entry(name, dimension)

    if not entry:
        return {}

    dependencies = {}
    dep_names = entry.metadata.get([])

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


def x_resolve_component_dependencies__mutmut_13(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = _get_registry_and_lock()

    entry = registry.get_entry(name, dimension)

    if not entry:
        return {}

    dependencies = {}
    dep_names = entry.metadata.get("dependencies", )

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


def x_resolve_component_dependencies__mutmut_14(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = _get_registry_and_lock()

    entry = registry.get_entry(name, dimension)

    if not entry:
        return {}

    dependencies = {}
    dep_names = entry.metadata.get("XXdependenciesXX", [])

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


def x_resolve_component_dependencies__mutmut_15(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = _get_registry_and_lock()

    entry = registry.get_entry(name, dimension)

    if not entry:
        return {}

    dependencies = {}
    dep_names = entry.metadata.get("DEPENDENCIES", [])

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


def x_resolve_component_dependencies__mutmut_16(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = _get_registry_and_lock()

    entry = registry.get_entry(name, dimension)

    if not entry:
        return {}

    dependencies = {}
    dep_names = entry.metadata.get("dependencies", [])

    for dep_name in dep_names:
        # Try same dimension first
        dep_component = None
        if dep_component is not None:
            dependencies[dep_name] = dep_component
        else:
            # Search across dimensions
            dep_component = registry.get(dep_name)
            if dep_component is not None:
                dependencies[dep_name] = dep_component

    return dependencies


def x_resolve_component_dependencies__mutmut_17(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = _get_registry_and_lock()

    entry = registry.get_entry(name, dimension)

    if not entry:
        return {}

    dependencies = {}
    dep_names = entry.metadata.get("dependencies", [])

    for dep_name in dep_names:
        # Try same dimension first
        dep_component = registry.get(None, dimension)
        if dep_component is not None:
            dependencies[dep_name] = dep_component
        else:
            # Search across dimensions
            dep_component = registry.get(dep_name)
            if dep_component is not None:
                dependencies[dep_name] = dep_component

    return dependencies


def x_resolve_component_dependencies__mutmut_18(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = _get_registry_and_lock()

    entry = registry.get_entry(name, dimension)

    if not entry:
        return {}

    dependencies = {}
    dep_names = entry.metadata.get("dependencies", [])

    for dep_name in dep_names:
        # Try same dimension first
        dep_component = registry.get(dep_name, None)
        if dep_component is not None:
            dependencies[dep_name] = dep_component
        else:
            # Search across dimensions
            dep_component = registry.get(dep_name)
            if dep_component is not None:
                dependencies[dep_name] = dep_component

    return dependencies


def x_resolve_component_dependencies__mutmut_19(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = _get_registry_and_lock()

    entry = registry.get_entry(name, dimension)

    if not entry:
        return {}

    dependencies = {}
    dep_names = entry.metadata.get("dependencies", [])

    for dep_name in dep_names:
        # Try same dimension first
        dep_component = registry.get(dimension)
        if dep_component is not None:
            dependencies[dep_name] = dep_component
        else:
            # Search across dimensions
            dep_component = registry.get(dep_name)
            if dep_component is not None:
                dependencies[dep_name] = dep_component

    return dependencies


def x_resolve_component_dependencies__mutmut_20(name: str, dimension: str) -> dict[str, Any]:
    """Resolve component dependencies recursively."""
    registry = _get_registry_and_lock()

    entry = registry.get_entry(name, dimension)

    if not entry:
        return {}

    dependencies = {}
    dep_names = entry.metadata.get("dependencies", [])

    for dep_name in dep_names:
        # Try same dimension first
        dep_component = registry.get(dep_name, )
        if dep_component is not None:
            dependencies[dep_name] = dep_component
        else:
            # Search across dimensions
            dep_component = registry.get(dep_name)
            if dep_component is not None:
                dependencies[dep_name] = dep_component

    return dependencies


def x_resolve_component_dependencies__mutmut_21(name: str, dimension: str) -> dict[str, Any]:
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
        if dep_component is None:
            dependencies[dep_name] = dep_component
        else:
            # Search across dimensions
            dep_component = registry.get(dep_name)
            if dep_component is not None:
                dependencies[dep_name] = dep_component

    return dependencies


def x_resolve_component_dependencies__mutmut_22(name: str, dimension: str) -> dict[str, Any]:
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
            dependencies[dep_name] = None
        else:
            # Search across dimensions
            dep_component = registry.get(dep_name)
            if dep_component is not None:
                dependencies[dep_name] = dep_component

    return dependencies


def x_resolve_component_dependencies__mutmut_23(name: str, dimension: str) -> dict[str, Any]:
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
            dep_component = None
            if dep_component is not None:
                dependencies[dep_name] = dep_component

    return dependencies


def x_resolve_component_dependencies__mutmut_24(name: str, dimension: str) -> dict[str, Any]:
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
            dep_component = registry.get(None)
            if dep_component is not None:
                dependencies[dep_name] = dep_component

    return dependencies


def x_resolve_component_dependencies__mutmut_25(name: str, dimension: str) -> dict[str, Any]:
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
            if dep_component is None:
                dependencies[dep_name] = dep_component

    return dependencies


def x_resolve_component_dependencies__mutmut_26(name: str, dimension: str) -> dict[str, Any]:
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
                dependencies[dep_name] = None

    return dependencies

x_resolve_component_dependencies__mutmut_mutants : ClassVar[MutantDict] = {
'x_resolve_component_dependencies__mutmut_1': x_resolve_component_dependencies__mutmut_1, 
    'x_resolve_component_dependencies__mutmut_2': x_resolve_component_dependencies__mutmut_2, 
    'x_resolve_component_dependencies__mutmut_3': x_resolve_component_dependencies__mutmut_3, 
    'x_resolve_component_dependencies__mutmut_4': x_resolve_component_dependencies__mutmut_4, 
    'x_resolve_component_dependencies__mutmut_5': x_resolve_component_dependencies__mutmut_5, 
    'x_resolve_component_dependencies__mutmut_6': x_resolve_component_dependencies__mutmut_6, 
    'x_resolve_component_dependencies__mutmut_7': x_resolve_component_dependencies__mutmut_7, 
    'x_resolve_component_dependencies__mutmut_8': x_resolve_component_dependencies__mutmut_8, 
    'x_resolve_component_dependencies__mutmut_9': x_resolve_component_dependencies__mutmut_9, 
    'x_resolve_component_dependencies__mutmut_10': x_resolve_component_dependencies__mutmut_10, 
    'x_resolve_component_dependencies__mutmut_11': x_resolve_component_dependencies__mutmut_11, 
    'x_resolve_component_dependencies__mutmut_12': x_resolve_component_dependencies__mutmut_12, 
    'x_resolve_component_dependencies__mutmut_13': x_resolve_component_dependencies__mutmut_13, 
    'x_resolve_component_dependencies__mutmut_14': x_resolve_component_dependencies__mutmut_14, 
    'x_resolve_component_dependencies__mutmut_15': x_resolve_component_dependencies__mutmut_15, 
    'x_resolve_component_dependencies__mutmut_16': x_resolve_component_dependencies__mutmut_16, 
    'x_resolve_component_dependencies__mutmut_17': x_resolve_component_dependencies__mutmut_17, 
    'x_resolve_component_dependencies__mutmut_18': x_resolve_component_dependencies__mutmut_18, 
    'x_resolve_component_dependencies__mutmut_19': x_resolve_component_dependencies__mutmut_19, 
    'x_resolve_component_dependencies__mutmut_20': x_resolve_component_dependencies__mutmut_20, 
    'x_resolve_component_dependencies__mutmut_21': x_resolve_component_dependencies__mutmut_21, 
    'x_resolve_component_dependencies__mutmut_22': x_resolve_component_dependencies__mutmut_22, 
    'x_resolve_component_dependencies__mutmut_23': x_resolve_component_dependencies__mutmut_23, 
    'x_resolve_component_dependencies__mutmut_24': x_resolve_component_dependencies__mutmut_24, 
    'x_resolve_component_dependencies__mutmut_25': x_resolve_component_dependencies__mutmut_25, 
    'x_resolve_component_dependencies__mutmut_26': x_resolve_component_dependencies__mutmut_26
}

def resolve_component_dependencies(*args, **kwargs):
    result = _mutmut_trampoline(x_resolve_component_dependencies__mutmut_orig, x_resolve_component_dependencies__mutmut_mutants, args, kwargs)
    return result 

resolve_component_dependencies.__signature__ = _mutmut_signature(x_resolve_component_dependencies__mutmut_orig)
x_resolve_component_dependencies__mutmut_orig.__name__ = 'x_resolve_component_dependencies'


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


def x_discover_components__mutmut_orig(
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


def x_discover_components__mutmut_1(
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
    if dimension is not None:
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


def x_discover_components__mutmut_2(
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
        dimension = None

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


def x_discover_components__mutmut_3(
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

    discovered = None

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


def x_discover_components__mutmut_4(
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
    if registry is not None:
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


def x_discover_components__mutmut_5(
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
        registry = None

    # Get entry points for the group (with resilient error handling)
    group_entries = _get_entry_points(group)

    # Load each entry point (with resilient error handling per entry point)
    for entry_point in group_entries:
        result = _load_entry_point(entry_point, registry, dimension)
        if result is not None:
            name, component_class = result
            discovered[name] = component_class

    return discovered


def x_discover_components__mutmut_6(
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
    group_entries = None

    # Load each entry point (with resilient error handling per entry point)
    for entry_point in group_entries:
        result = _load_entry_point(entry_point, registry, dimension)
        if result is not None:
            name, component_class = result
            discovered[name] = component_class

    return discovered


def x_discover_components__mutmut_7(
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
    group_entries = _get_entry_points(None)

    # Load each entry point (with resilient error handling per entry point)
    for entry_point in group_entries:
        result = _load_entry_point(entry_point, registry, dimension)
        if result is not None:
            name, component_class = result
            discovered[name] = component_class

    return discovered


def x_discover_components__mutmut_8(
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
        result = None
        if result is not None:
            name, component_class = result
            discovered[name] = component_class

    return discovered


def x_discover_components__mutmut_9(
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
        result = _load_entry_point(None, registry, dimension)
        if result is not None:
            name, component_class = result
            discovered[name] = component_class

    return discovered


def x_discover_components__mutmut_10(
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
        result = _load_entry_point(entry_point, None, dimension)
        if result is not None:
            name, component_class = result
            discovered[name] = component_class

    return discovered


def x_discover_components__mutmut_11(
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
        result = _load_entry_point(entry_point, registry, None)
        if result is not None:
            name, component_class = result
            discovered[name] = component_class

    return discovered


def x_discover_components__mutmut_12(
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
        result = _load_entry_point(registry, dimension)
        if result is not None:
            name, component_class = result
            discovered[name] = component_class

    return discovered


def x_discover_components__mutmut_13(
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
        result = _load_entry_point(entry_point, dimension)
        if result is not None:
            name, component_class = result
            discovered[name] = component_class

    return discovered


def x_discover_components__mutmut_14(
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
        result = _load_entry_point(entry_point, registry, )
        if result is not None:
            name, component_class = result
            discovered[name] = component_class

    return discovered


def x_discover_components__mutmut_15(
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
        if result is None:
            name, component_class = result
            discovered[name] = component_class

    return discovered


def x_discover_components__mutmut_16(
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
            name, component_class = None
            discovered[name] = component_class

    return discovered


def x_discover_components__mutmut_17(
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
            discovered[name] = None

    return discovered

x_discover_components__mutmut_mutants : ClassVar[MutantDict] = {
'x_discover_components__mutmut_1': x_discover_components__mutmut_1, 
    'x_discover_components__mutmut_2': x_discover_components__mutmut_2, 
    'x_discover_components__mutmut_3': x_discover_components__mutmut_3, 
    'x_discover_components__mutmut_4': x_discover_components__mutmut_4, 
    'x_discover_components__mutmut_5': x_discover_components__mutmut_5, 
    'x_discover_components__mutmut_6': x_discover_components__mutmut_6, 
    'x_discover_components__mutmut_7': x_discover_components__mutmut_7, 
    'x_discover_components__mutmut_8': x_discover_components__mutmut_8, 
    'x_discover_components__mutmut_9': x_discover_components__mutmut_9, 
    'x_discover_components__mutmut_10': x_discover_components__mutmut_10, 
    'x_discover_components__mutmut_11': x_discover_components__mutmut_11, 
    'x_discover_components__mutmut_12': x_discover_components__mutmut_12, 
    'x_discover_components__mutmut_13': x_discover_components__mutmut_13, 
    'x_discover_components__mutmut_14': x_discover_components__mutmut_14, 
    'x_discover_components__mutmut_15': x_discover_components__mutmut_15, 
    'x_discover_components__mutmut_16': x_discover_components__mutmut_16, 
    'x_discover_components__mutmut_17': x_discover_components__mutmut_17
}

def discover_components(*args, **kwargs):
    result = _mutmut_trampoline(x_discover_components__mutmut_orig, x_discover_components__mutmut_mutants, args, kwargs)
    return result 

discover_components.__signature__ = _mutmut_signature(x_discover_components__mutmut_orig)
x_discover_components__mutmut_orig.__name__ = 'x_discover_components'


__all__ = [
    "discover_components",
    "resolve_component_dependencies",
]


# <3 🧱🤝🌐🪄
