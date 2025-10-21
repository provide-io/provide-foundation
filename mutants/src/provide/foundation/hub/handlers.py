# provide/foundation/hub/handlers.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

from provide.foundation.errors.decorators import resilient
from provide.foundation.hub.foundation import get_foundation_logger
from provide.foundation.hub.registry import RegistryEntry

"""Hub error handler management utilities.

Provides functions for discovering and executing error handlers from the registry.
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


def _get_registry_and_lock() -> tuple[Any, Any]:
    """Get registry and ComponentCategory from components module."""
    from provide.foundation.hub.components import (
        ComponentCategory,
        get_component_registry,
    )

    return get_component_registry(), ComponentCategory


def x_get_handlers_for_exception__mutmut_orig(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_1(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = None

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_2(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = None
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_3(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(None)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_4(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = None

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_5(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension != ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_6(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = None
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_7(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(None).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_8(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = None

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_9(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = None
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_10(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get(None, [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_11(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", None)
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_12(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get([])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_13(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", )
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_14(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("XXexception_typesXX", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_15(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("EXCEPTION_TYPES", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_16(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            None
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_17(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name and exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_18(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type not in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_19(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name not in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_20(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(None)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_21(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=None, reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_22(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=None)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_23(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_24(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), )
    return matching_handlers


def x_get_handlers_for_exception__mutmut_25(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: None, reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_26(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get(None, 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_27(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", None), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_28(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get(0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_29(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", ), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_30(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("XXpriorityXX", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_31(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("PRIORITY", 0), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_32(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 1), reverse=True)
    return matching_handlers


def x_get_handlers_for_exception__mutmut_33(exception: Exception) -> list[RegistryEntry]:
    """Get error handlers that can handle the given exception type."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all error handlers
    all_entries = list(registry)
    handlers = [entry for entry in all_entries if entry.dimension == ComponentCategory.ERROR_HANDLER.value]

    # Filter by exception type
    exception_type_name = type(exception).__name__
    matching_handlers = []

    for entry in handlers:
        exception_types = entry.metadata.get("exception_types", [])
        if any(
            exc_type in exception_type_name or exception_type_name in exc_type for exc_type in exception_types
        ):
            matching_handlers.append(entry)

    # Sort by priority (highest first)
    matching_handlers.sort(key=lambda e: e.metadata.get("priority", 0), reverse=False)
    return matching_handlers

x_get_handlers_for_exception__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_handlers_for_exception__mutmut_1': x_get_handlers_for_exception__mutmut_1, 
    'x_get_handlers_for_exception__mutmut_2': x_get_handlers_for_exception__mutmut_2, 
    'x_get_handlers_for_exception__mutmut_3': x_get_handlers_for_exception__mutmut_3, 
    'x_get_handlers_for_exception__mutmut_4': x_get_handlers_for_exception__mutmut_4, 
    'x_get_handlers_for_exception__mutmut_5': x_get_handlers_for_exception__mutmut_5, 
    'x_get_handlers_for_exception__mutmut_6': x_get_handlers_for_exception__mutmut_6, 
    'x_get_handlers_for_exception__mutmut_7': x_get_handlers_for_exception__mutmut_7, 
    'x_get_handlers_for_exception__mutmut_8': x_get_handlers_for_exception__mutmut_8, 
    'x_get_handlers_for_exception__mutmut_9': x_get_handlers_for_exception__mutmut_9, 
    'x_get_handlers_for_exception__mutmut_10': x_get_handlers_for_exception__mutmut_10, 
    'x_get_handlers_for_exception__mutmut_11': x_get_handlers_for_exception__mutmut_11, 
    'x_get_handlers_for_exception__mutmut_12': x_get_handlers_for_exception__mutmut_12, 
    'x_get_handlers_for_exception__mutmut_13': x_get_handlers_for_exception__mutmut_13, 
    'x_get_handlers_for_exception__mutmut_14': x_get_handlers_for_exception__mutmut_14, 
    'x_get_handlers_for_exception__mutmut_15': x_get_handlers_for_exception__mutmut_15, 
    'x_get_handlers_for_exception__mutmut_16': x_get_handlers_for_exception__mutmut_16, 
    'x_get_handlers_for_exception__mutmut_17': x_get_handlers_for_exception__mutmut_17, 
    'x_get_handlers_for_exception__mutmut_18': x_get_handlers_for_exception__mutmut_18, 
    'x_get_handlers_for_exception__mutmut_19': x_get_handlers_for_exception__mutmut_19, 
    'x_get_handlers_for_exception__mutmut_20': x_get_handlers_for_exception__mutmut_20, 
    'x_get_handlers_for_exception__mutmut_21': x_get_handlers_for_exception__mutmut_21, 
    'x_get_handlers_for_exception__mutmut_22': x_get_handlers_for_exception__mutmut_22, 
    'x_get_handlers_for_exception__mutmut_23': x_get_handlers_for_exception__mutmut_23, 
    'x_get_handlers_for_exception__mutmut_24': x_get_handlers_for_exception__mutmut_24, 
    'x_get_handlers_for_exception__mutmut_25': x_get_handlers_for_exception__mutmut_25, 
    'x_get_handlers_for_exception__mutmut_26': x_get_handlers_for_exception__mutmut_26, 
    'x_get_handlers_for_exception__mutmut_27': x_get_handlers_for_exception__mutmut_27, 
    'x_get_handlers_for_exception__mutmut_28': x_get_handlers_for_exception__mutmut_28, 
    'x_get_handlers_for_exception__mutmut_29': x_get_handlers_for_exception__mutmut_29, 
    'x_get_handlers_for_exception__mutmut_30': x_get_handlers_for_exception__mutmut_30, 
    'x_get_handlers_for_exception__mutmut_31': x_get_handlers_for_exception__mutmut_31, 
    'x_get_handlers_for_exception__mutmut_32': x_get_handlers_for_exception__mutmut_32, 
    'x_get_handlers_for_exception__mutmut_33': x_get_handlers_for_exception__mutmut_33
}

def get_handlers_for_exception(*args, **kwargs):
    result = _mutmut_trampoline(x_get_handlers_for_exception__mutmut_orig, x_get_handlers_for_exception__mutmut_mutants, args, kwargs)
    return result 

get_handlers_for_exception.__signature__ = _mutmut_signature(x_get_handlers_for_exception__mutmut_orig)
x_get_handlers_for_exception__mutmut_orig.__name__ = 'x_get_handlers_for_exception'


@resilient(
    fallback=None,
    context_provider=lambda: {
        "function": "execute_error_handlers",
        "module": "hub.handlers",
    },
)
def execute_error_handlers(exception: Exception, context: dict[str, Any]) -> dict[str, Any] | None:
    """Execute error handlers until one handles the exception."""
    handlers = get_handlers_for_exception(exception)

    for entry in handlers:
        handler = entry.value
        try:
            result = handler(exception, context)
            if result is not None:
                return result
        except Exception as handler_error:
            get_foundation_logger().error("Error handler failed", handler=entry.name, error=str(handler_error))

    return None


__all__ = [
    "execute_error_handlers",
    "get_handlers_for_exception",
]


# <3 🧱🤝🌐🪄
