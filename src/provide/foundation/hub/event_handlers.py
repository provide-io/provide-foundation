#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

from provide.foundation.hub.events import Event, RegistryEvent, get_event_bus

"""Event handlers to connect events back to logging.

This module provides the bridge between the event system and logging,
breaking the circular dependency while maintaining logging functionality.
"""

# Global flags to prevent event logging during Foundation initialization/reset
# This prevents infinite loops when modules auto-register during import/reset
_foundation_initializing = False
_reset_in_progress = False


def _get_logger_safely() -> Any:
    """Get logger without creating circular dependency.

    Returns None if logger is not yet available to avoid initialization issues.
    Uses vanilla Python logger to completely avoid Foundation initialization.
    """
    global _foundation_initializing, _reset_in_progress

    # Never try to get logger if Foundation is currently initializing or resetting
    # This prevents cascade imports during module initialization and infinite loops during reset
    if _foundation_initializing or _reset_in_progress:
        return None

    try:
        # Use vanilla Python logger which doesn't trigger any Foundation initialization
        # Per coordinator.py docs: "Components should use get_system_logger() instead"
        from provide.foundation.logger.setup.coordinator import get_system_logger

        return get_system_logger("provide.foundation.hub.events")
    except Exception:
        # If logger isn't ready yet, gracefully ignore
        return None


def set_reset_in_progress(in_progress: bool) -> None:
    """Set whether a reset is currently in progress.

    This prevents event handlers from triggering logger operations during resets,
    which would cause infinite loops.

    Args:
        in_progress: True if reset is starting, False if reset is complete
    """
    global _reset_in_progress
    _reset_in_progress = in_progress


def handle_registry_event(event: Event | RegistryEvent) -> None:
    """Handle registry events by logging them.

    Args:
        event: Registry event to handle
    """
    logger = _get_logger_safely()
    if not logger:
        return

    if isinstance(event, RegistryEvent):
        if event.operation == "register":
            logger.debug(
                "Registered item",
                item_name=event.item_name,
                dimension=event.dimension,
                data=event.data,
            )
        elif event.operation == "remove":
            logger.debug(
                "Removed item",
                item_name=event.item_name,
                dimension=event.dimension,
                data=event.data,
            )
    elif event.name.startswith("registry."):
        logger.debug("Registry event", event_name=event.name, data=event.data)


def handle_circuit_breaker_event(event: Event) -> None:
    """Handle circuit breaker events by logging them.

    Args:
        event: Circuit breaker event to handle
    """
    logger = _get_logger_safely()
    if not logger:
        return

    if event.name == "circuit_breaker.recovered":
        logger.info("Circuit breaker recovered - closing circuit", data=event.data)
    elif event.name == "circuit_breaker.opened":
        logger.error("Circuit breaker opened due to failures", data=event.data)
    elif event.name == "circuit_breaker.recovery_failed":
        logger.warning("Circuit breaker recovery failed - opening circuit", data=event.data)
    elif event.name == "circuit_breaker.attempting_recovery":
        logger.info("Circuit breaker attempting recovery", data=event.data)
    elif event.name == "circuit_breaker.manual_reset":
        logger.info("Circuit breaker manually reset", data=event.data)


def setup_event_logging() -> None:
    """Set up event handlers to connect events back to logging.

    This should be called after the logger is initialized to avoid
    circular dependencies.
    """
    event_bus = get_event_bus()

    # Subscribe to registry events
    event_bus.subscribe("registry.register", handle_registry_event)
    event_bus.subscribe("registry.remove", handle_registry_event)

    # Subscribe to circuit breaker events
    event_bus.subscribe("circuit_breaker.recovered", handle_circuit_breaker_event)
    event_bus.subscribe("circuit_breaker.opened", handle_circuit_breaker_event)
    event_bus.subscribe("circuit_breaker.recovery_failed", handle_circuit_breaker_event)
    event_bus.subscribe("circuit_breaker.attempting_recovery", handle_circuit_breaker_event)
    event_bus.subscribe("circuit_breaker.manual_reset", handle_circuit_breaker_event)


__all__ = ["handle_circuit_breaker_event", "handle_registry_event", "setup_event_logging"]

# 🧱🏗️🔚
