#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Callable
import threading
from typing import Any
import weakref

from attrs import define, field

"""Event system for decoupled component communication.

Provides a lightweight event system to break circular dependencies
between components, particularly between registry and logger.
"""


@define(frozen=True, slots=True)
class Event:
    """Base event class for all system events."""

    name: str
    data: dict[str, Any] = field(factory=dict)
    source: str | None = None


@define(frozen=True, slots=True)
class RegistryEvent:
    """Events emitted by the registry system."""

    name: str
    operation: str
    item_name: str
    dimension: str
    data: dict[str, Any] = field(factory=dict)
    source: str | None = None

    def __attrs_post_init__(self) -> None:
        """Set event name from operation."""
        if not self.name:
            object.__setattr__(self, "name", f"registry.{self.operation}")


class EventBus:
    """Thread-safe event bus for decoupled component communication.

    Uses weak references to prevent memory leaks from event handlers.
    """

    def __init__(self) -> None:
        """Initialize empty event bus."""
        self._handlers: dict[str, list[weakref.ReferenceType]] = {}
        self._cleanup_threshold = 10  # Clean up after this many operations
        self._operation_count = 0
        self._lock = threading.RLock()  # RLock for thread safety
        self._failed_handler_count = 0  # Track handler failures for monitoring
        self._last_errors: list[dict[str, Any]] = []  # Recent errors (max 10)

    def subscribe(self, event_name: str, handler: Callable[[Event], None]) -> None:
        """Subscribe to events by name.

        Args:
            event_name: Name of event to subscribe to
            handler: Function to call when event occurs
        """
        with self._lock:
            if event_name not in self._handlers:
                self._handlers[event_name] = []

            # Use weak reference to prevent memory leaks
            weak_handler = weakref.ref(handler)
            self._handlers[event_name].append(weak_handler)

    def emit(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name not in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = []
            for weak_handler in self._handlers[event.name]:
                handler = weak_handler()
                if handler is not None:
                    live_handlers.append(weak_handler)
                    try:
                        handler(event)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(event, handler, e)

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count += 1
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 0

    def _handle_handler_error(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def unsubscribe(self, event_name: str, handler: Callable[[Event], None]) -> None:
        """Unsubscribe from events.

        Args:
            event_name: Name of event to unsubscribe from
            handler: Handler function to remove
        """
        with self._lock:
            if event_name not in self._handlers:
                return

            # Remove handler by comparing actual functions
            self._handlers[event_name] = [
                weak_ref for weak_ref in self._handlers[event_name] if weak_ref() is not handler
            ]

    def _cleanup_dead_references(self) -> None:
        """Clean up all dead weak references across all event types."""
        for event_name in list(self._handlers.keys()):
            live_handlers = []
            for weak_handler in self._handlers[event_name]:
                if weak_handler() is not None:
                    live_handlers.append(weak_handler)

            if live_handlers:
                self._handlers[event_name] = live_handlers
            else:
                # Remove empty event lists
                del self._handlers[event_name]

    def get_memory_stats(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is None:
                        dead_handlers += 1

            return {
                "event_types": len(self._handlers),
                "total_handlers": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "operation_count": self._operation_count,
            }

    def get_error_stats(self) -> dict[str, Any]:
        """Get error statistics for monitoring handler failures.

        Returns:
            Dictionary with error statistics including:
            - failed_handler_count: Total number of handler failures
            - recent_errors: List of recent error details (max 10)
        """
        with self._lock:
            return {
                "failed_handler_count": self._failed_handler_count,
                "recent_errors": self._last_errors.copy(),
            }

    def force_cleanup(self) -> None:
        """Force immediate cleanup of all dead references."""
        with self._lock:
            self._cleanup_dead_references()
            self._operation_count = 0

    def clear(self) -> None:
        """Clear all event subscriptions.

        This is primarily used during test resets to prevent duplicate
        event handlers from accumulating across test runs.
        """
        with self._lock:
            self._handlers.clear()
            self._operation_count = 0
            self._failed_handler_count = 0
            self._last_errors.clear()


# Global event bus instance
_event_bus = EventBus()


def get_event_bus() -> EventBus:
    """Get the global event bus instance."""
    return _event_bus


def emit_registry_event(operation: str, item_name: str, dimension: str, **kwargs: Any) -> None:
    """Emit a registry operation event.

    Args:
        operation: Type of operation (register, remove, etc.)
        item_name: Name of the registry item
        dimension: Registry dimension
        **kwargs: Additional event data
    """
    event = RegistryEvent(
        name="",  # Will be set by __attrs_post_init__
        operation=operation,
        item_name=item_name,
        dimension=dimension,
        data=kwargs,
        source="registry",
    )
    _event_bus.emit(event)


__all__ = ["Event", "EventBus", "RegistryEvent", "emit_registry_event", "get_event_bus"]

# 🧱🏗️🔚
