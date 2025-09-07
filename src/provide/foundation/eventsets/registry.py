"""
Event set registry and discovery for the Foundation event enrichment system.
"""

import importlib
import pkgutil
from pathlib import Path
from typing import Any

from provide.foundation.errors.resources import AlreadyExistsError, NotFoundError
from provide.foundation.hub.registry import Registry
from provide.foundation.logger import get_logger

from provide.foundation.eventsets.types import EventSetConfig

logger = get_logger(__name__)


class EventSetRegistry(Registry):
    """
    Registry for event set configurations.
    
    Extends the foundation Registry to provide specialized
    methods for event set registration and discovery.
    """
    
    def register_event_set(self, config: EventSetConfig) -> None:
        """
        Register an event set configuration.
        
        Args:
            config: The EventSetConfig to register
            
        Raises:
            AlreadyExistsError: If an event set with this name already exists
        """
        try:
            self.register("eventset", config.name, config, metadata={"priority": config.priority})
            logger.debug(
                "Registered event set",
                name=config.name,
                priority=config.priority,
                field_count=len(config.field_mappings),
                set_count=len(config.event_sets)
            )
        except AlreadyExistsError:
            logger.warning(
                "Event set already registered",
                name=config.name
            )
            raise
    
    def get_event_set(self, name: str) -> EventSetConfig:
        """
        Retrieve an event set configuration by name.
        
        Args:
            name: The name of the event set
            
        Returns:
            The EventSetConfig
            
        Raises:
            NotFoundError: If no event set with this name exists
        """
        entry = self.get("eventset", name)
        if entry is None:
            raise NotFoundError(f"Event set '{name}' not found")
        return entry.value
    
    def list_event_sets(self) -> list[EventSetConfig]:
        """
        List all registered event sets sorted by priority.
        
        Returns:
            List of EventSetConfig objects sorted by descending priority
        """
        entries = list(self.list_dimension("eventset"))
        entries.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
        return [entry.value for entry in entries]
    
    def discover_sets(self) -> None:
        """
        Auto-discover and register event sets from the sets/ directory.
        
        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return
        
        # Import all modules in the sets directory
        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue
                
            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)
                
                # Look for EVENT_SET constant
                if hasattr(module, "EVENT_SET"):
                    event_set = getattr(module, "EVENT_SET")
                    if isinstance(event_set, EventSetConfig):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name
                            )
                        except AlreadyExistsError:
                            logger.debug(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSetConfig",
                            module=module_name,
                            type=type(event_set).__name__
                        )
                        
            except ImportError as e:
                logger.warning(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e)
                )
            except Exception as e:
                logger.error(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__
                )


# Global registry instance
_registry = EventSetRegistry()


def get_registry() -> EventSetRegistry:
    """Get the global event set registry instance."""
    return _registry


def register_event_set(config: EventSetConfig) -> None:
    """
    Register an event set configuration in the global registry.
    
    Args:
        config: The EventSetConfig to register
    """
    _registry.register_event_set(config)


def discover_event_sets() -> None:
    """Auto-discover and register all event sets."""
    _registry.discover_sets()