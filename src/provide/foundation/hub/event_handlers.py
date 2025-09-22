from __future__ import annotations

from provide.foundation.hub.events import Event, RegistryEvent, get_event_bus

"""Event handlers to connect events back to logging.

This module provides the bridge between the event system and logging,
breaking the circular dependency while maintaining logging functionality.
"""


def _get_logger_safely():
    """Get logger without creating circular dependency.

    Returns None if logger is not yet available to avoid initialization issues.
    """
    try:
        # Only import after we know the system is initialized
        from provide.foundation.hub.foundation import get_foundation_logger
        return get_foundation_logger()
    except Exception:
        # If logger isn't ready yet, gracefully ignore
        return None


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
                name=event.item_name,
                dimension=event.dimension,
                **event.data
            )
        elif event.operation == "remove":
            logger.debug(
                "Removed item",
                name=event.item_name,
                dimension=event.dimension,
                **event.data
            )
    elif event.name.startswith("registry."):
        logger.debug(f"Registry event: {event.name}", **event.data)


def handle_circuit_breaker_event(event: Event) -> None:
    """Handle circuit breaker events by logging them.

    Args:
        event: Circuit breaker event to handle
    """
    logger = _get_logger_safely()
    if not logger:
        return

    if event.name == "circuit_breaker.recovered":
        logger.info("Circuit breaker recovered - closing circuit", **event.data)
    elif event.name == "circuit_breaker.opened":
        logger.error("Circuit breaker opened due to failures", **event.data)
    elif event.name == "circuit_breaker.recovery_failed":
        logger.warning("Circuit breaker recovery failed - opening circuit", **event.data)
    elif event.name == "circuit_breaker.attempting_recovery":
        logger.info("Circuit breaker attempting recovery", **event.data)
    elif event.name == "circuit_breaker.manual_reset":
        logger.info("Circuit breaker manually reset", **event.data)


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


__all__ = [
    "handle_registry_event",
    "handle_circuit_breaker_event",
    "setup_event_logging"
]