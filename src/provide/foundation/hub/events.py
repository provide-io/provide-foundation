from __future__ import annotations

from collections.abc import Callable
import contextlib
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
                    with contextlib.suppress(Exception):
                        # Silently ignore handler errors to prevent cascading failures
                        handler(event)

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count += 1
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 0

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
