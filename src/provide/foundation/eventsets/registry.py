"""
Event set registry and discovery for the Foundation event enrichment system.
"""

import importlib
import pkgutil
import threading
from pathlib import Path

from provide.foundation.errors.resources import AlreadyExistsError, NotFoundError

from provide.foundation.eventsets.types import EventSetConfig


class EventSetRegistry:
    """
    Registry for event set configurations.
    
    Thread-safe registry for managing event set configurations.
    """
    
    def __init__(self) -> None:
        """Initialize the registry."""
        self._lock = threading.RLock()
        self._configs: dict[str, EventSetConfig] = {}
    
    def register_event_set(self, config: EventSetConfig) -> None:
        """
        Register an event set configuration.
        
        Args:
            config: The EventSetConfig to register
            
        Raises:
            AlreadyExistsError: If an event set with this name already exists
        """
        with self._lock:
            if config.name in self._configs:
                raise AlreadyExistsError(f"Event set '{config.name}' already registered")
            self._configs[config.name] = config
    
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
        with self._lock:
            if name not in self._configs:
                raise NotFoundError(f"Event set '{name}' not found")
            return self._configs[name]
    
    def list_event_sets(self) -> list[EventSetConfig]:
        """
        List all registered event sets sorted by priority.
        
        Returns:
            List of EventSetConfig objects sorted by descending priority
        """
        with self._lock:
            configs = list(self._configs.values())
            configs.sort(key=lambda c: c.priority, reverse=True)
            return configs
    
    def discover_sets(self) -> None:
        """
        Auto-discover and register event sets from the sets/ directory.
        
        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
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
                        except AlreadyExistsError:
                            pass  # Already registered
                    else:
                        pass  # Not an EventSetConfig
                        
            except (ImportError, Exception):
                pass  # Skip modules that fail to import


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