# provide/foundation/hub/lifecycle.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
import inspect
from typing import Any

from provide.foundation.hub.foundation import get_foundation_logger

"""Hub component lifecycle management utilities.

Provides functions for initializing, managing, and cleaning up components
registered in the Hub registry system.
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

# No global async lock - registry handles its own thread safety
# and _initialized_components dict access is simplified


def _get_registry_and_globals() -> Any:
    """Get registry and initialized components from components module."""
    from provide.foundation.hub.components import (
        _initialized_components,
        get_component_registry,
    )

    return get_component_registry(), _initialized_components


def x_get_or_initialize_component__mutmut_orig(name: str, dimension: str) -> Any:
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


def x_get_or_initialize_component__mutmut_1(name: str, dimension: str) -> Any:
    """Get component, initializing lazily if needed."""
    registry, initialized_components = None
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


def x_get_or_initialize_component__mutmut_2(name: str, dimension: str) -> Any:
    """Get component, initializing lazily if needed."""
    registry, initialized_components = _get_registry_and_globals()
    key = None

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


def x_get_or_initialize_component__mutmut_3(name: str, dimension: str) -> Any:
    """Get component, initializing lazily if needed."""
    registry, initialized_components = _get_registry_and_globals()
    key = (name, dimension)

    # Return already initialized component
    if key not in initialized_components:
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


def x_get_or_initialize_component__mutmut_4(name: str, dimension: str) -> Any:
    """Get component, initializing lazily if needed."""
    registry, initialized_components = _get_registry_and_globals()
    key = (name, dimension)

    # Return already initialized component
    if key in initialized_components:
        return initialized_components[key]

    entry = None

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


def x_get_or_initialize_component__mutmut_5(name: str, dimension: str) -> Any:
    """Get component, initializing lazily if needed."""
    registry, initialized_components = _get_registry_and_globals()
    key = (name, dimension)

    # Return already initialized component
    if key in initialized_components:
        return initialized_components[key]

    entry = registry.get_entry(None, dimension)

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


def x_get_or_initialize_component__mutmut_6(name: str, dimension: str) -> Any:
    """Get component, initializing lazily if needed."""
    registry, initialized_components = _get_registry_and_globals()
    key = (name, dimension)

    # Return already initialized component
    if key in initialized_components:
        return initialized_components[key]

    entry = registry.get_entry(name, None)

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


def x_get_or_initialize_component__mutmut_7(name: str, dimension: str) -> Any:
    """Get component, initializing lazily if needed."""
    registry, initialized_components = _get_registry_and_globals()
    key = (name, dimension)

    # Return already initialized component
    if key in initialized_components:
        return initialized_components[key]

    entry = registry.get_entry(dimension)

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


def x_get_or_initialize_component__mutmut_8(name: str, dimension: str) -> Any:
    """Get component, initializing lazily if needed."""
    registry, initialized_components = _get_registry_and_globals()
    key = (name, dimension)

    # Return already initialized component
    if key in initialized_components:
        return initialized_components[key]

    entry = registry.get_entry(name, )

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


def x_get_or_initialize_component__mutmut_9(name: str, dimension: str) -> Any:
    """Get component, initializing lazily if needed."""
    registry, initialized_components = _get_registry_and_globals()
    key = (name, dimension)

    # Return already initialized component
    if key in initialized_components:
        return initialized_components[key]

    entry = registry.get_entry(name, dimension)

    if entry:
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


def x_get_or_initialize_component__mutmut_10(name: str, dimension: str) -> Any:
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
    if entry.value is None:
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


def x_get_or_initialize_component__mutmut_11(name: str, dimension: str) -> Any:
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
        initialized_components[key] = None
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


def x_get_or_initialize_component__mutmut_12(name: str, dimension: str) -> Any:
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
    if entry.metadata.get(None, False):
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


def x_get_or_initialize_component__mutmut_13(name: str, dimension: str) -> Any:
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
    if entry.metadata.get("lazy", None):
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


def x_get_or_initialize_component__mutmut_14(name: str, dimension: str) -> Any:
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
    if entry.metadata.get(False):
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


def x_get_or_initialize_component__mutmut_15(name: str, dimension: str) -> Any:
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
    if entry.metadata.get("lazy", ):
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


def x_get_or_initialize_component__mutmut_16(name: str, dimension: str) -> Any:
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
    if entry.metadata.get("XXlazyXX", False):
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


def x_get_or_initialize_component__mutmut_17(name: str, dimension: str) -> Any:
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
    if entry.metadata.get("LAZY", False):
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


def x_get_or_initialize_component__mutmut_18(name: str, dimension: str) -> Any:
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
    if entry.metadata.get("lazy", True):
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


def x_get_or_initialize_component__mutmut_19(name: str, dimension: str) -> Any:
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
        factory = None
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


def x_get_or_initialize_component__mutmut_20(name: str, dimension: str) -> Any:
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
        factory = entry.metadata.get(None)
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


def x_get_or_initialize_component__mutmut_21(name: str, dimension: str) -> Any:
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
        factory = entry.metadata.get("XXfactoryXX")
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


def x_get_or_initialize_component__mutmut_22(name: str, dimension: str) -> Any:
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
        factory = entry.metadata.get("FACTORY")
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


def x_get_or_initialize_component__mutmut_23(name: str, dimension: str) -> Any:
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
                component = None
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


def x_get_or_initialize_component__mutmut_24(name: str, dimension: str) -> Any:
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
                    name=None,
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


def x_get_or_initialize_component__mutmut_25(name: str, dimension: str) -> Any:
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
                    value=None,
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


def x_get_or_initialize_component__mutmut_26(name: str, dimension: str) -> Any:
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
                    dimension=None,
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


def x_get_or_initialize_component__mutmut_27(name: str, dimension: str) -> Any:
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
                    metadata=None,
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


def x_get_or_initialize_component__mutmut_28(name: str, dimension: str) -> Any:
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
                    replace=None,
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


def x_get_or_initialize_component__mutmut_29(name: str, dimension: str) -> Any:
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


def x_get_or_initialize_component__mutmut_30(name: str, dimension: str) -> Any:
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


def x_get_or_initialize_component__mutmut_31(name: str, dimension: str) -> Any:
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


def x_get_or_initialize_component__mutmut_32(name: str, dimension: str) -> Any:
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


def x_get_or_initialize_component__mutmut_33(name: str, dimension: str) -> Any:
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


def x_get_or_initialize_component__mutmut_34(name: str, dimension: str) -> Any:
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
                    replace=False,
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


def x_get_or_initialize_component__mutmut_35(name: str, dimension: str) -> Any:
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
                initialized_components[key] = None
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


def x_get_or_initialize_component__mutmut_36(name: str, dimension: str) -> Any:
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
                    None,
                    component=name,
                    dimension=dimension,
                    error=str(e),
                )
                # Return None on failure for resilient behavior
                return None

    return entry.value


def x_get_or_initialize_component__mutmut_37(name: str, dimension: str) -> Any:
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
                    component=None,
                    dimension=dimension,
                    error=str(e),
                )
                # Return None on failure for resilient behavior
                return None

    return entry.value


def x_get_or_initialize_component__mutmut_38(name: str, dimension: str) -> Any:
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
                    dimension=None,
                    error=str(e),
                )
                # Return None on failure for resilient behavior
                return None

    return entry.value


def x_get_or_initialize_component__mutmut_39(name: str, dimension: str) -> Any:
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
                    error=None,
                )
                # Return None on failure for resilient behavior
                return None

    return entry.value


def x_get_or_initialize_component__mutmut_40(name: str, dimension: str) -> Any:
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
                    component=name,
                    dimension=dimension,
                    error=str(e),
                )
                # Return None on failure for resilient behavior
                return None

    return entry.value


def x_get_or_initialize_component__mutmut_41(name: str, dimension: str) -> Any:
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
                    dimension=dimension,
                    error=str(e),
                )
                # Return None on failure for resilient behavior
                return None

    return entry.value


def x_get_or_initialize_component__mutmut_42(name: str, dimension: str) -> Any:
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
                    error=str(e),
                )
                # Return None on failure for resilient behavior
                return None

    return entry.value


def x_get_or_initialize_component__mutmut_43(name: str, dimension: str) -> Any:
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
                    )
                # Return None on failure for resilient behavior
                return None

    return entry.value


def x_get_or_initialize_component__mutmut_44(name: str, dimension: str) -> Any:
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
                    "XXComponent initialization failedXX",
                    component=name,
                    dimension=dimension,
                    error=str(e),
                )
                # Return None on failure for resilient behavior
                return None

    return entry.value


def x_get_or_initialize_component__mutmut_45(name: str, dimension: str) -> Any:
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
                    "component initialization failed",
                    component=name,
                    dimension=dimension,
                    error=str(e),
                )
                # Return None on failure for resilient behavior
                return None

    return entry.value


def x_get_or_initialize_component__mutmut_46(name: str, dimension: str) -> Any:
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
                    "COMPONENT INITIALIZATION FAILED",
                    component=name,
                    dimension=dimension,
                    error=str(e),
                )
                # Return None on failure for resilient behavior
                return None

    return entry.value


def x_get_or_initialize_component__mutmut_47(name: str, dimension: str) -> Any:
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
                    error=str(None),
                )
                # Return None on failure for resilient behavior
                return None

    return entry.value

x_get_or_initialize_component__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_or_initialize_component__mutmut_1': x_get_or_initialize_component__mutmut_1, 
    'x_get_or_initialize_component__mutmut_2': x_get_or_initialize_component__mutmut_2, 
    'x_get_or_initialize_component__mutmut_3': x_get_or_initialize_component__mutmut_3, 
    'x_get_or_initialize_component__mutmut_4': x_get_or_initialize_component__mutmut_4, 
    'x_get_or_initialize_component__mutmut_5': x_get_or_initialize_component__mutmut_5, 
    'x_get_or_initialize_component__mutmut_6': x_get_or_initialize_component__mutmut_6, 
    'x_get_or_initialize_component__mutmut_7': x_get_or_initialize_component__mutmut_7, 
    'x_get_or_initialize_component__mutmut_8': x_get_or_initialize_component__mutmut_8, 
    'x_get_or_initialize_component__mutmut_9': x_get_or_initialize_component__mutmut_9, 
    'x_get_or_initialize_component__mutmut_10': x_get_or_initialize_component__mutmut_10, 
    'x_get_or_initialize_component__mutmut_11': x_get_or_initialize_component__mutmut_11, 
    'x_get_or_initialize_component__mutmut_12': x_get_or_initialize_component__mutmut_12, 
    'x_get_or_initialize_component__mutmut_13': x_get_or_initialize_component__mutmut_13, 
    'x_get_or_initialize_component__mutmut_14': x_get_or_initialize_component__mutmut_14, 
    'x_get_or_initialize_component__mutmut_15': x_get_or_initialize_component__mutmut_15, 
    'x_get_or_initialize_component__mutmut_16': x_get_or_initialize_component__mutmut_16, 
    'x_get_or_initialize_component__mutmut_17': x_get_or_initialize_component__mutmut_17, 
    'x_get_or_initialize_component__mutmut_18': x_get_or_initialize_component__mutmut_18, 
    'x_get_or_initialize_component__mutmut_19': x_get_or_initialize_component__mutmut_19, 
    'x_get_or_initialize_component__mutmut_20': x_get_or_initialize_component__mutmut_20, 
    'x_get_or_initialize_component__mutmut_21': x_get_or_initialize_component__mutmut_21, 
    'x_get_or_initialize_component__mutmut_22': x_get_or_initialize_component__mutmut_22, 
    'x_get_or_initialize_component__mutmut_23': x_get_or_initialize_component__mutmut_23, 
    'x_get_or_initialize_component__mutmut_24': x_get_or_initialize_component__mutmut_24, 
    'x_get_or_initialize_component__mutmut_25': x_get_or_initialize_component__mutmut_25, 
    'x_get_or_initialize_component__mutmut_26': x_get_or_initialize_component__mutmut_26, 
    'x_get_or_initialize_component__mutmut_27': x_get_or_initialize_component__mutmut_27, 
    'x_get_or_initialize_component__mutmut_28': x_get_or_initialize_component__mutmut_28, 
    'x_get_or_initialize_component__mutmut_29': x_get_or_initialize_component__mutmut_29, 
    'x_get_or_initialize_component__mutmut_30': x_get_or_initialize_component__mutmut_30, 
    'x_get_or_initialize_component__mutmut_31': x_get_or_initialize_component__mutmut_31, 
    'x_get_or_initialize_component__mutmut_32': x_get_or_initialize_component__mutmut_32, 
    'x_get_or_initialize_component__mutmut_33': x_get_or_initialize_component__mutmut_33, 
    'x_get_or_initialize_component__mutmut_34': x_get_or_initialize_component__mutmut_34, 
    'x_get_or_initialize_component__mutmut_35': x_get_or_initialize_component__mutmut_35, 
    'x_get_or_initialize_component__mutmut_36': x_get_or_initialize_component__mutmut_36, 
    'x_get_or_initialize_component__mutmut_37': x_get_or_initialize_component__mutmut_37, 
    'x_get_or_initialize_component__mutmut_38': x_get_or_initialize_component__mutmut_38, 
    'x_get_or_initialize_component__mutmut_39': x_get_or_initialize_component__mutmut_39, 
    'x_get_or_initialize_component__mutmut_40': x_get_or_initialize_component__mutmut_40, 
    'x_get_or_initialize_component__mutmut_41': x_get_or_initialize_component__mutmut_41, 
    'x_get_or_initialize_component__mutmut_42': x_get_or_initialize_component__mutmut_42, 
    'x_get_or_initialize_component__mutmut_43': x_get_or_initialize_component__mutmut_43, 
    'x_get_or_initialize_component__mutmut_44': x_get_or_initialize_component__mutmut_44, 
    'x_get_or_initialize_component__mutmut_45': x_get_or_initialize_component__mutmut_45, 
    'x_get_or_initialize_component__mutmut_46': x_get_or_initialize_component__mutmut_46, 
    'x_get_or_initialize_component__mutmut_47': x_get_or_initialize_component__mutmut_47
}

def get_or_initialize_component(*args, **kwargs):
    result = _mutmut_trampoline(x_get_or_initialize_component__mutmut_orig, x_get_or_initialize_component__mutmut_mutants, args, kwargs)
    return result 

get_or_initialize_component.__signature__ = _mutmut_signature(x_get_or_initialize_component__mutmut_orig)
x_get_or_initialize_component__mutmut_orig.__name__ = 'x_get_or_initialize_component'


async def x_initialize_async_component__mutmut_orig(name: str, dimension: str) -> Any:
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


async def x_initialize_async_component__mutmut_1(name: str, dimension: str) -> Any:
    """Initialize component asynchronously."""
    registry, initialized_components = None
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


async def x_initialize_async_component__mutmut_2(name: str, dimension: str) -> Any:
    """Initialize component asynchronously."""
    registry, initialized_components = _get_registry_and_globals()
    key = None

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


async def x_initialize_async_component__mutmut_3(name: str, dimension: str) -> Any:
    """Initialize component asynchronously."""
    registry, initialized_components = _get_registry_and_globals()
    key = (name, dimension)

    # First, check if already initialized
    if key not in initialized_components:
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


async def x_initialize_async_component__mutmut_4(name: str, dimension: str) -> Any:
    """Initialize component asynchronously."""
    registry, initialized_components = _get_registry_and_globals()
    key = (name, dimension)

    # First, check if already initialized
    if key in initialized_components:
        return initialized_components[key]

    # Registry operations are thread-safe internally, no external lock needed
    entry = None

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


async def x_initialize_async_component__mutmut_5(name: str, dimension: str) -> Any:
    """Initialize component asynchronously."""
    registry, initialized_components = _get_registry_and_globals()
    key = (name, dimension)

    # First, check if already initialized
    if key in initialized_components:
        return initialized_components[key]

    # Registry operations are thread-safe internally, no external lock needed
    entry = registry.get_entry(None, dimension)

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


async def x_initialize_async_component__mutmut_6(name: str, dimension: str) -> Any:
    """Initialize component asynchronously."""
    registry, initialized_components = _get_registry_and_globals()
    key = (name, dimension)

    # First, check if already initialized
    if key in initialized_components:
        return initialized_components[key]

    # Registry operations are thread-safe internally, no external lock needed
    entry = registry.get_entry(name, None)

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


async def x_initialize_async_component__mutmut_7(name: str, dimension: str) -> Any:
    """Initialize component asynchronously."""
    registry, initialized_components = _get_registry_and_globals()
    key = (name, dimension)

    # First, check if already initialized
    if key in initialized_components:
        return initialized_components[key]

    # Registry operations are thread-safe internally, no external lock needed
    entry = registry.get_entry(dimension)

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


async def x_initialize_async_component__mutmut_8(name: str, dimension: str) -> Any:
    """Initialize component asynchronously."""
    registry, initialized_components = _get_registry_and_globals()
    key = (name, dimension)

    # First, check if already initialized
    if key in initialized_components:
        return initialized_components[key]

    # Registry operations are thread-safe internally, no external lock needed
    entry = registry.get_entry(name, )

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


async def x_initialize_async_component__mutmut_9(name: str, dimension: str) -> Any:
    """Initialize component asynchronously."""
    registry, initialized_components = _get_registry_and_globals()
    key = (name, dimension)

    # First, check if already initialized
    if key in initialized_components:
        return initialized_components[key]

    # Registry operations are thread-safe internally, no external lock needed
    entry = registry.get_entry(name, dimension)

    if entry:
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


async def x_initialize_async_component__mutmut_10(name: str, dimension: str) -> Any:
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
    if entry.metadata.get("async", False):
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


async def x_initialize_async_component__mutmut_11(name: str, dimension: str) -> Any:
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
    if not entry.metadata.get(None, False):
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


async def x_initialize_async_component__mutmut_12(name: str, dimension: str) -> Any:
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
    if not entry.metadata.get("async", None):
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


async def x_initialize_async_component__mutmut_13(name: str, dimension: str) -> Any:
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
    if not entry.metadata.get(False):
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


async def x_initialize_async_component__mutmut_14(name: str, dimension: str) -> Any:
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
    if not entry.metadata.get("async", ):
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


async def x_initialize_async_component__mutmut_15(name: str, dimension: str) -> Any:
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
    if not entry.metadata.get("XXasyncXX", False):
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


async def x_initialize_async_component__mutmut_16(name: str, dimension: str) -> Any:
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
    if not entry.metadata.get("ASYNC", False):
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


async def x_initialize_async_component__mutmut_17(name: str, dimension: str) -> Any:
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
    if not entry.metadata.get("async", True):
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


async def x_initialize_async_component__mutmut_18(name: str, dimension: str) -> Any:
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

    factory = None
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


async def x_initialize_async_component__mutmut_19(name: str, dimension: str) -> Any:
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

    factory = entry.metadata.get(None)
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


async def x_initialize_async_component__mutmut_20(name: str, dimension: str) -> Any:
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

    factory = entry.metadata.get("XXfactoryXX")
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


async def x_initialize_async_component__mutmut_21(name: str, dimension: str) -> Any:
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

    factory = entry.metadata.get("FACTORY")
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


async def x_initialize_async_component__mutmut_22(name: str, dimension: str) -> Any:
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
    if factory:
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


async def x_initialize_async_component__mutmut_23(name: str, dimension: str) -> Any:
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
    if key not in initialized_components:
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


async def x_initialize_async_component__mutmut_24(name: str, dimension: str) -> Any:
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
        if inspect.iscoroutinefunction(None):
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


async def x_initialize_async_component__mutmut_25(name: str, dimension: str) -> Any:
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
            component = None
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


async def x_initialize_async_component__mutmut_26(name: str, dimension: str) -> Any:
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
            component = None

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


async def x_initialize_async_component__mutmut_27(name: str, dimension: str) -> Any:
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
            name=None,
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


async def x_initialize_async_component__mutmut_28(name: str, dimension: str) -> Any:
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
            value=None,
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


async def x_initialize_async_component__mutmut_29(name: str, dimension: str) -> Any:
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
            dimension=None,
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


async def x_initialize_async_component__mutmut_30(name: str, dimension: str) -> Any:
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
            metadata=None,
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


async def x_initialize_async_component__mutmut_31(name: str, dimension: str) -> Any:
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
            replace=None,
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


async def x_initialize_async_component__mutmut_32(name: str, dimension: str) -> Any:
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


async def x_initialize_async_component__mutmut_33(name: str, dimension: str) -> Any:
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


async def x_initialize_async_component__mutmut_34(name: str, dimension: str) -> Any:
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


async def x_initialize_async_component__mutmut_35(name: str, dimension: str) -> Any:
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


async def x_initialize_async_component__mutmut_36(name: str, dimension: str) -> Any:
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


async def x_initialize_async_component__mutmut_37(name: str, dimension: str) -> Any:
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
            replace=False,
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


async def x_initialize_async_component__mutmut_38(name: str, dimension: str) -> Any:
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
        if key in initialized_components:
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


async def x_initialize_async_component__mutmut_39(name: str, dimension: str) -> Any:
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
            initialized_components[key] = None
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


async def x_initialize_async_component__mutmut_40(name: str, dimension: str) -> Any:
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
            None,
            component=name,
            dimension=dimension,
            error=str(e),
        )
        # Return None on failure for resilient behavior
        return None


async def x_initialize_async_component__mutmut_41(name: str, dimension: str) -> Any:
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
            component=None,
            dimension=dimension,
            error=str(e),
        )
        # Return None on failure for resilient behavior
        return None


async def x_initialize_async_component__mutmut_42(name: str, dimension: str) -> Any:
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
            dimension=None,
            error=str(e),
        )
        # Return None on failure for resilient behavior
        return None


async def x_initialize_async_component__mutmut_43(name: str, dimension: str) -> Any:
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
            error=None,
        )
        # Return None on failure for resilient behavior
        return None


async def x_initialize_async_component__mutmut_44(name: str, dimension: str) -> Any:
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
            component=name,
            dimension=dimension,
            error=str(e),
        )
        # Return None on failure for resilient behavior
        return None


async def x_initialize_async_component__mutmut_45(name: str, dimension: str) -> Any:
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
            dimension=dimension,
            error=str(e),
        )
        # Return None on failure for resilient behavior
        return None


async def x_initialize_async_component__mutmut_46(name: str, dimension: str) -> Any:
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
            error=str(e),
        )
        # Return None on failure for resilient behavior
        return None


async def x_initialize_async_component__mutmut_47(name: str, dimension: str) -> Any:
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
            )
        # Return None on failure for resilient behavior
        return None


async def x_initialize_async_component__mutmut_48(name: str, dimension: str) -> Any:
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
            "XXAsync component initialization failedXX",
            component=name,
            dimension=dimension,
            error=str(e),
        )
        # Return None on failure for resilient behavior
        return None


async def x_initialize_async_component__mutmut_49(name: str, dimension: str) -> Any:
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
            "async component initialization failed",
            component=name,
            dimension=dimension,
            error=str(e),
        )
        # Return None on failure for resilient behavior
        return None


async def x_initialize_async_component__mutmut_50(name: str, dimension: str) -> Any:
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
            "ASYNC COMPONENT INITIALIZATION FAILED",
            component=name,
            dimension=dimension,
            error=str(e),
        )
        # Return None on failure for resilient behavior
        return None


async def x_initialize_async_component__mutmut_51(name: str, dimension: str) -> Any:
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
            error=str(None),
        )
        # Return None on failure for resilient behavior
        return None

x_initialize_async_component__mutmut_mutants : ClassVar[MutantDict] = {
'x_initialize_async_component__mutmut_1': x_initialize_async_component__mutmut_1, 
    'x_initialize_async_component__mutmut_2': x_initialize_async_component__mutmut_2, 
    'x_initialize_async_component__mutmut_3': x_initialize_async_component__mutmut_3, 
    'x_initialize_async_component__mutmut_4': x_initialize_async_component__mutmut_4, 
    'x_initialize_async_component__mutmut_5': x_initialize_async_component__mutmut_5, 
    'x_initialize_async_component__mutmut_6': x_initialize_async_component__mutmut_6, 
    'x_initialize_async_component__mutmut_7': x_initialize_async_component__mutmut_7, 
    'x_initialize_async_component__mutmut_8': x_initialize_async_component__mutmut_8, 
    'x_initialize_async_component__mutmut_9': x_initialize_async_component__mutmut_9, 
    'x_initialize_async_component__mutmut_10': x_initialize_async_component__mutmut_10, 
    'x_initialize_async_component__mutmut_11': x_initialize_async_component__mutmut_11, 
    'x_initialize_async_component__mutmut_12': x_initialize_async_component__mutmut_12, 
    'x_initialize_async_component__mutmut_13': x_initialize_async_component__mutmut_13, 
    'x_initialize_async_component__mutmut_14': x_initialize_async_component__mutmut_14, 
    'x_initialize_async_component__mutmut_15': x_initialize_async_component__mutmut_15, 
    'x_initialize_async_component__mutmut_16': x_initialize_async_component__mutmut_16, 
    'x_initialize_async_component__mutmut_17': x_initialize_async_component__mutmut_17, 
    'x_initialize_async_component__mutmut_18': x_initialize_async_component__mutmut_18, 
    'x_initialize_async_component__mutmut_19': x_initialize_async_component__mutmut_19, 
    'x_initialize_async_component__mutmut_20': x_initialize_async_component__mutmut_20, 
    'x_initialize_async_component__mutmut_21': x_initialize_async_component__mutmut_21, 
    'x_initialize_async_component__mutmut_22': x_initialize_async_component__mutmut_22, 
    'x_initialize_async_component__mutmut_23': x_initialize_async_component__mutmut_23, 
    'x_initialize_async_component__mutmut_24': x_initialize_async_component__mutmut_24, 
    'x_initialize_async_component__mutmut_25': x_initialize_async_component__mutmut_25, 
    'x_initialize_async_component__mutmut_26': x_initialize_async_component__mutmut_26, 
    'x_initialize_async_component__mutmut_27': x_initialize_async_component__mutmut_27, 
    'x_initialize_async_component__mutmut_28': x_initialize_async_component__mutmut_28, 
    'x_initialize_async_component__mutmut_29': x_initialize_async_component__mutmut_29, 
    'x_initialize_async_component__mutmut_30': x_initialize_async_component__mutmut_30, 
    'x_initialize_async_component__mutmut_31': x_initialize_async_component__mutmut_31, 
    'x_initialize_async_component__mutmut_32': x_initialize_async_component__mutmut_32, 
    'x_initialize_async_component__mutmut_33': x_initialize_async_component__mutmut_33, 
    'x_initialize_async_component__mutmut_34': x_initialize_async_component__mutmut_34, 
    'x_initialize_async_component__mutmut_35': x_initialize_async_component__mutmut_35, 
    'x_initialize_async_component__mutmut_36': x_initialize_async_component__mutmut_36, 
    'x_initialize_async_component__mutmut_37': x_initialize_async_component__mutmut_37, 
    'x_initialize_async_component__mutmut_38': x_initialize_async_component__mutmut_38, 
    'x_initialize_async_component__mutmut_39': x_initialize_async_component__mutmut_39, 
    'x_initialize_async_component__mutmut_40': x_initialize_async_component__mutmut_40, 
    'x_initialize_async_component__mutmut_41': x_initialize_async_component__mutmut_41, 
    'x_initialize_async_component__mutmut_42': x_initialize_async_component__mutmut_42, 
    'x_initialize_async_component__mutmut_43': x_initialize_async_component__mutmut_43, 
    'x_initialize_async_component__mutmut_44': x_initialize_async_component__mutmut_44, 
    'x_initialize_async_component__mutmut_45': x_initialize_async_component__mutmut_45, 
    'x_initialize_async_component__mutmut_46': x_initialize_async_component__mutmut_46, 
    'x_initialize_async_component__mutmut_47': x_initialize_async_component__mutmut_47, 
    'x_initialize_async_component__mutmut_48': x_initialize_async_component__mutmut_48, 
    'x_initialize_async_component__mutmut_49': x_initialize_async_component__mutmut_49, 
    'x_initialize_async_component__mutmut_50': x_initialize_async_component__mutmut_50, 
    'x_initialize_async_component__mutmut_51': x_initialize_async_component__mutmut_51
}

def initialize_async_component(*args, **kwargs):
    result = _mutmut_trampoline(x_initialize_async_component__mutmut_orig, x_initialize_async_component__mutmut_mutants, args, kwargs)
    return result 

initialize_async_component.__signature__ = _mutmut_signature(x_initialize_async_component__mutmut_orig)
x_initialize_async_component__mutmut_orig.__name__ = 'x_initialize_async_component'


def x_cleanup_all_components__mutmut_orig(dimension: str | None = None) -> None:
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


def x_cleanup_all_components__mutmut_1(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = None

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


def x_cleanup_all_components__mutmut_2(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = _get_registry_and_globals()

    entries = None

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


def x_cleanup_all_components__mutmut_3(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = _get_registry_and_globals()

    entries = [entry for entry in registry if entry.dimension != dimension] if dimension else list(registry)

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


def x_cleanup_all_components__mutmut_4(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = _get_registry_and_globals()

    entries = [entry for entry in registry if entry.dimension == dimension] if dimension else list(None)

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


def x_cleanup_all_components__mutmut_5(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = _get_registry_and_globals()

    entries = [entry for entry in registry if entry.dimension == dimension] if dimension else list(registry)

    for entry in entries:
        if entry.metadata.get(None, False):
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


def x_cleanup_all_components__mutmut_6(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = _get_registry_and_globals()

    entries = [entry for entry in registry if entry.dimension == dimension] if dimension else list(registry)

    for entry in entries:
        if entry.metadata.get("supports_cleanup", None):
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


def x_cleanup_all_components__mutmut_7(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = _get_registry_and_globals()

    entries = [entry for entry in registry if entry.dimension == dimension] if dimension else list(registry)

    for entry in entries:
        if entry.metadata.get(False):
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


def x_cleanup_all_components__mutmut_8(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = _get_registry_and_globals()

    entries = [entry for entry in registry if entry.dimension == dimension] if dimension else list(registry)

    for entry in entries:
        if entry.metadata.get("supports_cleanup", ):
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


def x_cleanup_all_components__mutmut_9(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = _get_registry_and_globals()

    entries = [entry for entry in registry if entry.dimension == dimension] if dimension else list(registry)

    for entry in entries:
        if entry.metadata.get("XXsupports_cleanupXX", False):
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


def x_cleanup_all_components__mutmut_10(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = _get_registry_and_globals()

    entries = [entry for entry in registry if entry.dimension == dimension] if dimension else list(registry)

    for entry in entries:
        if entry.metadata.get("SUPPORTS_CLEANUP", False):
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


def x_cleanup_all_components__mutmut_11(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = _get_registry_and_globals()

    entries = [entry for entry in registry if entry.dimension == dimension] if dimension else list(registry)

    for entry in entries:
        if entry.metadata.get("supports_cleanup", True):
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


def x_cleanup_all_components__mutmut_12(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = _get_registry_and_globals()

    entries = [entry for entry in registry if entry.dimension == dimension] if dimension else list(registry)

    for entry in entries:
        if entry.metadata.get("supports_cleanup", False):
            component = None
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


def x_cleanup_all_components__mutmut_13(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = _get_registry_and_globals()

    entries = [entry for entry in registry if entry.dimension == dimension] if dimension else list(registry)

    for entry in entries:
        if entry.metadata.get("supports_cleanup", False):
            component = entry.value
            if hasattr(None, "cleanup"):
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


def x_cleanup_all_components__mutmut_14(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = _get_registry_and_globals()

    entries = [entry for entry in registry if entry.dimension == dimension] if dimension else list(registry)

    for entry in entries:
        if entry.metadata.get("supports_cleanup", False):
            component = entry.value
            if hasattr(component, None):
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


def x_cleanup_all_components__mutmut_15(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = _get_registry_and_globals()

    entries = [entry for entry in registry if entry.dimension == dimension] if dimension else list(registry)

    for entry in entries:
        if entry.metadata.get("supports_cleanup", False):
            component = entry.value
            if hasattr("cleanup"):
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


def x_cleanup_all_components__mutmut_16(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = _get_registry_and_globals()

    entries = [entry for entry in registry if entry.dimension == dimension] if dimension else list(registry)

    for entry in entries:
        if entry.metadata.get("supports_cleanup", False):
            component = entry.value
            if hasattr(component, ):
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


def x_cleanup_all_components__mutmut_17(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = _get_registry_and_globals()

    entries = [entry for entry in registry if entry.dimension == dimension] if dimension else list(registry)

    for entry in entries:
        if entry.metadata.get("supports_cleanup", False):
            component = entry.value
            if hasattr(component, "XXcleanupXX"):
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


def x_cleanup_all_components__mutmut_18(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = _get_registry_and_globals()

    entries = [entry for entry in registry if entry.dimension == dimension] if dimension else list(registry)

    for entry in entries:
        if entry.metadata.get("supports_cleanup", False):
            component = entry.value
            if hasattr(component, "CLEANUP"):
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


def x_cleanup_all_components__mutmut_19(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = _get_registry_and_globals()

    entries = [entry for entry in registry if entry.dimension == dimension] if dimension else list(registry)

    for entry in entries:
        if entry.metadata.get("supports_cleanup", False):
            component = entry.value
            if hasattr(component, "cleanup"):
                try:
                    cleanup_func = None
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


def x_cleanup_all_components__mutmut_20(dimension: str | None = None) -> None:
    """Clean up all components in dimension."""
    registry, _ = _get_registry_and_globals()

    entries = [entry for entry in registry if entry.dimension == dimension] if dimension else list(registry)

    for entry in entries:
        if entry.metadata.get("supports_cleanup", False):
            component = entry.value
            if hasattr(component, "cleanup"):
                try:
                    cleanup_func = component.cleanup
                    if inspect.iscoroutinefunction(None):
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


def x_cleanup_all_components__mutmut_21(dimension: str | None = None) -> None:
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
                        loop = ""
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


def x_cleanup_all_components__mutmut_22(dimension: str | None = None) -> None:
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
                            loop = None
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


def x_cleanup_all_components__mutmut_23(dimension: str | None = None) -> None:
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
                                task = None
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


def x_cleanup_all_components__mutmut_24(dimension: str | None = None) -> None:
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
                                task = loop.create_task(None)
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


def x_cleanup_all_components__mutmut_25(dimension: str | None = None) -> None:
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
                                task.add_done_callback(None)
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


def x_cleanup_all_components__mutmut_26(dimension: str | None = None) -> None:
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
                                task.add_done_callback(lambda t: 0)
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


def x_cleanup_all_components__mutmut_27(dimension: str | None = None) -> None:
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
                                loop.run_until_complete(None)
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


def x_cleanup_all_components__mutmut_28(dimension: str | None = None) -> None:
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
                            loop = None
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


def x_cleanup_all_components__mutmut_29(dimension: str | None = None) -> None:
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
                            loop.run_until_complete(None)
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


def x_cleanup_all_components__mutmut_30(dimension: str | None = None) -> None:
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
                        None,
                        component=entry.name,
                        dimension=entry.dimension,
                        error=str(e),
                    )
                    # Log but don't re-raise during cleanup to allow other components to clean up


def x_cleanup_all_components__mutmut_31(dimension: str | None = None) -> None:
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
                        component=None,
                        dimension=entry.dimension,
                        error=str(e),
                    )
                    # Log but don't re-raise during cleanup to allow other components to clean up


def x_cleanup_all_components__mutmut_32(dimension: str | None = None) -> None:
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
                        dimension=None,
                        error=str(e),
                    )
                    # Log but don't re-raise during cleanup to allow other components to clean up


def x_cleanup_all_components__mutmut_33(dimension: str | None = None) -> None:
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
                        error=None,
                    )
                    # Log but don't re-raise during cleanup to allow other components to clean up


def x_cleanup_all_components__mutmut_34(dimension: str | None = None) -> None:
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
                        component=entry.name,
                        dimension=entry.dimension,
                        error=str(e),
                    )
                    # Log but don't re-raise during cleanup to allow other components to clean up


def x_cleanup_all_components__mutmut_35(dimension: str | None = None) -> None:
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
                        dimension=entry.dimension,
                        error=str(e),
                    )
                    # Log but don't re-raise during cleanup to allow other components to clean up


def x_cleanup_all_components__mutmut_36(dimension: str | None = None) -> None:
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
                        error=str(e),
                    )
                    # Log but don't re-raise during cleanup to allow other components to clean up


def x_cleanup_all_components__mutmut_37(dimension: str | None = None) -> None:
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
                        )
                    # Log but don't re-raise during cleanup to allow other components to clean up


def x_cleanup_all_components__mutmut_38(dimension: str | None = None) -> None:
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
                        "XXComponent cleanup failedXX",
                        component=entry.name,
                        dimension=entry.dimension,
                        error=str(e),
                    )
                    # Log but don't re-raise during cleanup to allow other components to clean up


def x_cleanup_all_components__mutmut_39(dimension: str | None = None) -> None:
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
                        "component cleanup failed",
                        component=entry.name,
                        dimension=entry.dimension,
                        error=str(e),
                    )
                    # Log but don't re-raise during cleanup to allow other components to clean up


def x_cleanup_all_components__mutmut_40(dimension: str | None = None) -> None:
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
                        "COMPONENT CLEANUP FAILED",
                        component=entry.name,
                        dimension=entry.dimension,
                        error=str(e),
                    )
                    # Log but don't re-raise during cleanup to allow other components to clean up


def x_cleanup_all_components__mutmut_41(dimension: str | None = None) -> None:
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
                        error=str(None),
                    )
                    # Log but don't re-raise during cleanup to allow other components to clean up

x_cleanup_all_components__mutmut_mutants : ClassVar[MutantDict] = {
'x_cleanup_all_components__mutmut_1': x_cleanup_all_components__mutmut_1, 
    'x_cleanup_all_components__mutmut_2': x_cleanup_all_components__mutmut_2, 
    'x_cleanup_all_components__mutmut_3': x_cleanup_all_components__mutmut_3, 
    'x_cleanup_all_components__mutmut_4': x_cleanup_all_components__mutmut_4, 
    'x_cleanup_all_components__mutmut_5': x_cleanup_all_components__mutmut_5, 
    'x_cleanup_all_components__mutmut_6': x_cleanup_all_components__mutmut_6, 
    'x_cleanup_all_components__mutmut_7': x_cleanup_all_components__mutmut_7, 
    'x_cleanup_all_components__mutmut_8': x_cleanup_all_components__mutmut_8, 
    'x_cleanup_all_components__mutmut_9': x_cleanup_all_components__mutmut_9, 
    'x_cleanup_all_components__mutmut_10': x_cleanup_all_components__mutmut_10, 
    'x_cleanup_all_components__mutmut_11': x_cleanup_all_components__mutmut_11, 
    'x_cleanup_all_components__mutmut_12': x_cleanup_all_components__mutmut_12, 
    'x_cleanup_all_components__mutmut_13': x_cleanup_all_components__mutmut_13, 
    'x_cleanup_all_components__mutmut_14': x_cleanup_all_components__mutmut_14, 
    'x_cleanup_all_components__mutmut_15': x_cleanup_all_components__mutmut_15, 
    'x_cleanup_all_components__mutmut_16': x_cleanup_all_components__mutmut_16, 
    'x_cleanup_all_components__mutmut_17': x_cleanup_all_components__mutmut_17, 
    'x_cleanup_all_components__mutmut_18': x_cleanup_all_components__mutmut_18, 
    'x_cleanup_all_components__mutmut_19': x_cleanup_all_components__mutmut_19, 
    'x_cleanup_all_components__mutmut_20': x_cleanup_all_components__mutmut_20, 
    'x_cleanup_all_components__mutmut_21': x_cleanup_all_components__mutmut_21, 
    'x_cleanup_all_components__mutmut_22': x_cleanup_all_components__mutmut_22, 
    'x_cleanup_all_components__mutmut_23': x_cleanup_all_components__mutmut_23, 
    'x_cleanup_all_components__mutmut_24': x_cleanup_all_components__mutmut_24, 
    'x_cleanup_all_components__mutmut_25': x_cleanup_all_components__mutmut_25, 
    'x_cleanup_all_components__mutmut_26': x_cleanup_all_components__mutmut_26, 
    'x_cleanup_all_components__mutmut_27': x_cleanup_all_components__mutmut_27, 
    'x_cleanup_all_components__mutmut_28': x_cleanup_all_components__mutmut_28, 
    'x_cleanup_all_components__mutmut_29': x_cleanup_all_components__mutmut_29, 
    'x_cleanup_all_components__mutmut_30': x_cleanup_all_components__mutmut_30, 
    'x_cleanup_all_components__mutmut_31': x_cleanup_all_components__mutmut_31, 
    'x_cleanup_all_components__mutmut_32': x_cleanup_all_components__mutmut_32, 
    'x_cleanup_all_components__mutmut_33': x_cleanup_all_components__mutmut_33, 
    'x_cleanup_all_components__mutmut_34': x_cleanup_all_components__mutmut_34, 
    'x_cleanup_all_components__mutmut_35': x_cleanup_all_components__mutmut_35, 
    'x_cleanup_all_components__mutmut_36': x_cleanup_all_components__mutmut_36, 
    'x_cleanup_all_components__mutmut_37': x_cleanup_all_components__mutmut_37, 
    'x_cleanup_all_components__mutmut_38': x_cleanup_all_components__mutmut_38, 
    'x_cleanup_all_components__mutmut_39': x_cleanup_all_components__mutmut_39, 
    'x_cleanup_all_components__mutmut_40': x_cleanup_all_components__mutmut_40, 
    'x_cleanup_all_components__mutmut_41': x_cleanup_all_components__mutmut_41
}

def cleanup_all_components(*args, **kwargs):
    result = _mutmut_trampoline(x_cleanup_all_components__mutmut_orig, x_cleanup_all_components__mutmut_mutants, args, kwargs)
    return result 

cleanup_all_components.__signature__ = _mutmut_signature(x_cleanup_all_components__mutmut_orig)
x_cleanup_all_components__mutmut_orig.__name__ = 'x_cleanup_all_components'


async def x_initialize_all_async_components__mutmut_orig() -> None:
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


async def x_initialize_all_async_components__mutmut_1() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = None

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


async def x_initialize_all_async_components__mutmut_2() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = None

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


async def x_initialize_all_async_components__mutmut_3() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get(None, False)]

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


async def x_initialize_all_async_components__mutmut_4() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", None)]

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


async def x_initialize_all_async_components__mutmut_5() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get(False)]

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


async def x_initialize_all_async_components__mutmut_6() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", )]

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


async def x_initialize_all_async_components__mutmut_7() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("XXasyncXX", False)]

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


async def x_initialize_all_async_components__mutmut_8() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("ASYNC", False)]

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


async def x_initialize_all_async_components__mutmut_9() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", True)]

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


async def x_initialize_all_async_components__mutmut_10() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", False)]

    # Sort by priority for initialization order
    async_components.sort(key=None, reverse=True)

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


async def x_initialize_all_async_components__mutmut_11() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", False)]

    # Sort by priority for initialization order
    async_components.sort(key=lambda e: e.metadata.get("priority", 0), reverse=None)

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


async def x_initialize_all_async_components__mutmut_12() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", False)]

    # Sort by priority for initialization order
    async_components.sort(reverse=True)

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


async def x_initialize_all_async_components__mutmut_13() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", False)]

    # Sort by priority for initialization order
    async_components.sort(key=lambda e: e.metadata.get("priority", 0), )

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


async def x_initialize_all_async_components__mutmut_14() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", False)]

    # Sort by priority for initialization order
    async_components.sort(key=lambda e: None, reverse=True)

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


async def x_initialize_all_async_components__mutmut_15() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", False)]

    # Sort by priority for initialization order
    async_components.sort(key=lambda e: e.metadata.get(None, 0), reverse=True)

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


async def x_initialize_all_async_components__mutmut_16() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", False)]

    # Sort by priority for initialization order
    async_components.sort(key=lambda e: e.metadata.get("priority", None), reverse=True)

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


async def x_initialize_all_async_components__mutmut_17() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", False)]

    # Sort by priority for initialization order
    async_components.sort(key=lambda e: e.metadata.get(0), reverse=True)

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


async def x_initialize_all_async_components__mutmut_18() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", False)]

    # Sort by priority for initialization order
    async_components.sort(key=lambda e: e.metadata.get("priority", ), reverse=True)

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


async def x_initialize_all_async_components__mutmut_19() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", False)]

    # Sort by priority for initialization order
    async_components.sort(key=lambda e: e.metadata.get("XXpriorityXX", 0), reverse=True)

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


async def x_initialize_all_async_components__mutmut_20() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", False)]

    # Sort by priority for initialization order
    async_components.sort(key=lambda e: e.metadata.get("PRIORITY", 0), reverse=True)

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


async def x_initialize_all_async_components__mutmut_21() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", False)]

    # Sort by priority for initialization order
    async_components.sort(key=lambda e: e.metadata.get("priority", 1), reverse=True)

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


async def x_initialize_all_async_components__mutmut_22() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", False)]

    # Sort by priority for initialization order
    async_components.sort(key=lambda e: e.metadata.get("priority", 0), reverse=False)

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


async def x_initialize_all_async_components__mutmut_23() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", False)]

    # Sort by priority for initialization order
    async_components.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)

    # Initialize each component
    for entry in async_components:
        try:
            await initialize_async_component(None, entry.dimension)
        except Exception as e:
            get_foundation_logger().error(
                "Failed to initialize async component",
                component=entry.name,
                dimension=entry.dimension,
                error=str(e),
            )
            # Log but don't re-raise to allow other components to initialize


async def x_initialize_all_async_components__mutmut_24() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", False)]

    # Sort by priority for initialization order
    async_components.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)

    # Initialize each component
    for entry in async_components:
        try:
            await initialize_async_component(entry.name, None)
        except Exception as e:
            get_foundation_logger().error(
                "Failed to initialize async component",
                component=entry.name,
                dimension=entry.dimension,
                error=str(e),
            )
            # Log but don't re-raise to allow other components to initialize


async def x_initialize_all_async_components__mutmut_25() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", False)]

    # Sort by priority for initialization order
    async_components.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)

    # Initialize each component
    for entry in async_components:
        try:
            await initialize_async_component(entry.dimension)
        except Exception as e:
            get_foundation_logger().error(
                "Failed to initialize async component",
                component=entry.name,
                dimension=entry.dimension,
                error=str(e),
            )
            # Log but don't re-raise to allow other components to initialize


async def x_initialize_all_async_components__mutmut_26() -> None:
    """Initialize all async components in dependency order."""
    registry, _ = _get_registry_and_globals()

    # Get all async components
    async_components = [entry for entry in registry if entry.metadata.get("async", False)]

    # Sort by priority for initialization order
    async_components.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)

    # Initialize each component
    for entry in async_components:
        try:
            await initialize_async_component(entry.name, )
        except Exception as e:
            get_foundation_logger().error(
                "Failed to initialize async component",
                component=entry.name,
                dimension=entry.dimension,
                error=str(e),
            )
            # Log but don't re-raise to allow other components to initialize


async def x_initialize_all_async_components__mutmut_27() -> None:
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
                None,
                component=entry.name,
                dimension=entry.dimension,
                error=str(e),
            )
            # Log but don't re-raise to allow other components to initialize


async def x_initialize_all_async_components__mutmut_28() -> None:
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
                component=None,
                dimension=entry.dimension,
                error=str(e),
            )
            # Log but don't re-raise to allow other components to initialize


async def x_initialize_all_async_components__mutmut_29() -> None:
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
                dimension=None,
                error=str(e),
            )
            # Log but don't re-raise to allow other components to initialize


async def x_initialize_all_async_components__mutmut_30() -> None:
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
                error=None,
            )
            # Log but don't re-raise to allow other components to initialize


async def x_initialize_all_async_components__mutmut_31() -> None:
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
                component=entry.name,
                dimension=entry.dimension,
                error=str(e),
            )
            # Log but don't re-raise to allow other components to initialize


async def x_initialize_all_async_components__mutmut_32() -> None:
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
                dimension=entry.dimension,
                error=str(e),
            )
            # Log but don't re-raise to allow other components to initialize


async def x_initialize_all_async_components__mutmut_33() -> None:
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
                error=str(e),
            )
            # Log but don't re-raise to allow other components to initialize


async def x_initialize_all_async_components__mutmut_34() -> None:
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
                )
            # Log but don't re-raise to allow other components to initialize


async def x_initialize_all_async_components__mutmut_35() -> None:
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
                "XXFailed to initialize async componentXX",
                component=entry.name,
                dimension=entry.dimension,
                error=str(e),
            )
            # Log but don't re-raise to allow other components to initialize


async def x_initialize_all_async_components__mutmut_36() -> None:
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
                "failed to initialize async component",
                component=entry.name,
                dimension=entry.dimension,
                error=str(e),
            )
            # Log but don't re-raise to allow other components to initialize


async def x_initialize_all_async_components__mutmut_37() -> None:
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
                "FAILED TO INITIALIZE ASYNC COMPONENT",
                component=entry.name,
                dimension=entry.dimension,
                error=str(e),
            )
            # Log but don't re-raise to allow other components to initialize


async def x_initialize_all_async_components__mutmut_38() -> None:
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
                error=str(None),
            )
            # Log but don't re-raise to allow other components to initialize

x_initialize_all_async_components__mutmut_mutants : ClassVar[MutantDict] = {
'x_initialize_all_async_components__mutmut_1': x_initialize_all_async_components__mutmut_1, 
    'x_initialize_all_async_components__mutmut_2': x_initialize_all_async_components__mutmut_2, 
    'x_initialize_all_async_components__mutmut_3': x_initialize_all_async_components__mutmut_3, 
    'x_initialize_all_async_components__mutmut_4': x_initialize_all_async_components__mutmut_4, 
    'x_initialize_all_async_components__mutmut_5': x_initialize_all_async_components__mutmut_5, 
    'x_initialize_all_async_components__mutmut_6': x_initialize_all_async_components__mutmut_6, 
    'x_initialize_all_async_components__mutmut_7': x_initialize_all_async_components__mutmut_7, 
    'x_initialize_all_async_components__mutmut_8': x_initialize_all_async_components__mutmut_8, 
    'x_initialize_all_async_components__mutmut_9': x_initialize_all_async_components__mutmut_9, 
    'x_initialize_all_async_components__mutmut_10': x_initialize_all_async_components__mutmut_10, 
    'x_initialize_all_async_components__mutmut_11': x_initialize_all_async_components__mutmut_11, 
    'x_initialize_all_async_components__mutmut_12': x_initialize_all_async_components__mutmut_12, 
    'x_initialize_all_async_components__mutmut_13': x_initialize_all_async_components__mutmut_13, 
    'x_initialize_all_async_components__mutmut_14': x_initialize_all_async_components__mutmut_14, 
    'x_initialize_all_async_components__mutmut_15': x_initialize_all_async_components__mutmut_15, 
    'x_initialize_all_async_components__mutmut_16': x_initialize_all_async_components__mutmut_16, 
    'x_initialize_all_async_components__mutmut_17': x_initialize_all_async_components__mutmut_17, 
    'x_initialize_all_async_components__mutmut_18': x_initialize_all_async_components__mutmut_18, 
    'x_initialize_all_async_components__mutmut_19': x_initialize_all_async_components__mutmut_19, 
    'x_initialize_all_async_components__mutmut_20': x_initialize_all_async_components__mutmut_20, 
    'x_initialize_all_async_components__mutmut_21': x_initialize_all_async_components__mutmut_21, 
    'x_initialize_all_async_components__mutmut_22': x_initialize_all_async_components__mutmut_22, 
    'x_initialize_all_async_components__mutmut_23': x_initialize_all_async_components__mutmut_23, 
    'x_initialize_all_async_components__mutmut_24': x_initialize_all_async_components__mutmut_24, 
    'x_initialize_all_async_components__mutmut_25': x_initialize_all_async_components__mutmut_25, 
    'x_initialize_all_async_components__mutmut_26': x_initialize_all_async_components__mutmut_26, 
    'x_initialize_all_async_components__mutmut_27': x_initialize_all_async_components__mutmut_27, 
    'x_initialize_all_async_components__mutmut_28': x_initialize_all_async_components__mutmut_28, 
    'x_initialize_all_async_components__mutmut_29': x_initialize_all_async_components__mutmut_29, 
    'x_initialize_all_async_components__mutmut_30': x_initialize_all_async_components__mutmut_30, 
    'x_initialize_all_async_components__mutmut_31': x_initialize_all_async_components__mutmut_31, 
    'x_initialize_all_async_components__mutmut_32': x_initialize_all_async_components__mutmut_32, 
    'x_initialize_all_async_components__mutmut_33': x_initialize_all_async_components__mutmut_33, 
    'x_initialize_all_async_components__mutmut_34': x_initialize_all_async_components__mutmut_34, 
    'x_initialize_all_async_components__mutmut_35': x_initialize_all_async_components__mutmut_35, 
    'x_initialize_all_async_components__mutmut_36': x_initialize_all_async_components__mutmut_36, 
    'x_initialize_all_async_components__mutmut_37': x_initialize_all_async_components__mutmut_37, 
    'x_initialize_all_async_components__mutmut_38': x_initialize_all_async_components__mutmut_38
}

def initialize_all_async_components(*args, **kwargs):
    result = _mutmut_trampoline(x_initialize_all_async_components__mutmut_orig, x_initialize_all_async_components__mutmut_mutants, args, kwargs)
    return result 

initialize_all_async_components.__signature__ = _mutmut_signature(x_initialize_all_async_components__mutmut_orig)
x_initialize_all_async_components__mutmut_orig.__name__ = 'x_initialize_all_async_components'


__all__ = [
    "cleanup_all_components",
    "get_or_initialize_component",
    "initialize_all_async_components",
    "initialize_async_component",
]


# <3 🧱🤝🌐🪄
