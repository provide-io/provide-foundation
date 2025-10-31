#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import importlib
from pathlib import Path
import pkgutil

from provide.foundation.errors.resources import AlreadyExistsError, NotFoundError
from provide.foundation.eventsets.types import EventSet
from provide.foundation.hub.registry import Registry
from provide.foundation.logger.setup.coordinator import (
    create_foundation_internal_logger,
)

"""Event set registry and discovery."""

# Bootstrap logger that doesn't trigger full logger setup
logger = create_foundation_internal_logger()


class EventSetRegistry(Registry):
    """Registry for event set definitions using foundation Registry.

    Extends the foundation Registry to provide specialized
    methods for event set registration and discovery.
    """

    def register_event_set(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def get_event_set(self, name: str) -> EventSet:
        """Retrieve an event set by name.

        Args:
            name: The name of the event set

        Returns:
            The EventSet

        Raises:
            NotFoundError: If no event set with this name exists

        """
        event_set = self.get(name, "eventset")
        if event_set is None:
            raise NotFoundError(f"Event set '{name}' not found")
        return event_set

    def list_event_sets(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
        return [entry.value for entry in valid_entries]

    def discover_sets(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )


# Global registry instance
_registry = EventSetRegistry()
_discovery_completed = False


def get_registry() -> EventSetRegistry:
    """Get the global event set registry instance."""
    return _registry


def register_event_set(event_set: EventSet) -> None:
    """Register an event set in the global registry.

    Args:
        event_set: The EventSet to register

    """
    _registry.register_event_set(event_set)


def discover_event_sets() -> None:
    """Auto-discover and register all event sets."""
    global _discovery_completed
    if _discovery_completed:
        logger.trace("Event set discovery already completed, skipping")
        return

    logger.debug("Starting event set discovery")
    _registry.discover_sets()
    _discovery_completed = True
    logger.debug("Event set discovery completed")


def reset_discovery_state() -> None:
    """Reset discovery state for testing."""
    global _discovery_completed
    _discovery_completed = False
    logger.trace("Event set discovery state reset")


def clear_registry() -> None:
    """Clear the registry for testing."""
    global _registry, _discovery_completed
    _registry = EventSetRegistry()
    _discovery_completed = False
    logger.trace("Event set registry cleared")


# 🧱🏗️🔚
