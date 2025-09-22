from __future__ import annotations

from collections.abc import Callable
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
class RegistryEvent(Event):
    """Events emitted by the registry system."""

    operation: str = field()
    item_name: str = field()
    dimension: str = field()

    def __attrs_post_init__(self) -> None:
        """Set event name from operation."""
        object.__setattr__(self, 'name', f'registry.{self.operation}')


class EventBus:
    """Thread-safe event bus for decoupled component communication.

    Uses weak references to prevent memory leaks from event handlers.
    """

    def __init__(self) -> None:
        """Initialize empty event bus."""
        self._handlers: dict[str, list[weakref.ReferenceType]] = {}

    def subscribe(self, event_name: str, handler: Callable[[Event], None]) -> None:
        """Subscribe to events by name.

        Args:
            event_name: Name of event to subscribe to
            handler: Function to call when event occurs
        """
        if event_name not in self._handlers:
            self._handlers[event_name] = []

        # Use weak reference to prevent memory leaks
        weak_handler = weakref.ref(handler)
        self._handlers[event_name].append(weak_handler)

    def emit(self, event: Event) -> None:
        """Emit an event to all subscribers.

        Args:
            event: Event to emit
        """
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
                except Exception:
                    # Silently ignore handler errors to prevent cascading failures
                    pass

        # Update handler list with only live references
        self._handlers[event.name] = live_handlers

    def unsubscribe(self, event_name: str, handler: Callable[[Event], None]) -> None:
        """Unsubscribe from events.

        Args:
            event_name: Name of event to unsubscribe from
            handler: Handler function to remove
        """
        if event_name not in self._handlers:
            return

        # Remove handler by comparing actual functions
        self._handlers[event_name] = [
            weak_ref for weak_ref in self._handlers[event_name]
            if weak_ref() is not handler
        ]


# Global event bus instance
_event_bus = EventBus()


def get_event_bus() -> EventBus:
    """Get the global event bus instance."""
    return _event_bus


def emit_registry_event(
    operation: str,
    item_name: str,
    dimension: str,
    **kwargs: Any
) -> None:
    """Emit a registry operation event.

    Args:
        operation: Type of operation (register, remove, etc.)
        item_name: Name of the registry item
        dimension: Registry dimension
        **kwargs: Additional event data
    """
    event = RegistryEvent(
        operation=operation,
        item_name=item_name,
        dimension=dimension,
        data=kwargs,
        source="registry"
    )
    _event_bus.emit(event)


__all__ = ["Event", "RegistryEvent", "EventBus", "get_event_bus", "emit_registry_event"]