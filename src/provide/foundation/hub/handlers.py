#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

from provide.foundation.errors.decorators import resilient
from provide.foundation.hub.foundation import get_foundation_logger
from provide.foundation.hub.registry import RegistryEntry

"""Hub error handler management utilities.

Provides functions for discovering and executing error handlers from the registry.
"""


def _get_registry_and_lock() -> tuple[Any, Any]:
    """Get registry and ComponentCategory from components module."""
    from provide.foundation.hub.components import (
        ComponentCategory,
        get_component_registry,
    )

    return get_component_registry(), ComponentCategory


def get_handlers_for_exception(exception: Exception) -> list[RegistryEntry]:
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

# 🧱🏗️🔚
