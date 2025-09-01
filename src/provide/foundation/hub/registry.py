"""Core registry implementation."""

from collections import defaultdict
from typing import Any, Iterator

import structlog

from .types import RegistryDimension, RegistryEntry, RegistryKey

log = structlog.get_logger(__name__)


class Registry:
    """
    Multi-dimensional registry for components and commands.
    
    Supports hierarchical organization by dimension (component, command, etc.)
    and name within each dimension.
    """
    
    def __init__(self) -> None:
        """Initialize an empty registry."""
        self._registry: dict[str, dict[str, RegistryEntry]] = defaultdict(dict)
        self._aliases: dict[str, RegistryKey] = {}
    
    def register(
        self,
        name: str,
        value: Any,
        dimension: RegistryDimension | str = RegistryDimension.COMPONENT,
        metadata: dict[str, Any] | None = None,
        aliases: list[str] | None = None,
        replace: bool = False,
    ) -> RegistryEntry:
        """
        Register an item in the registry.
        
        Args:
            name: Unique name within the dimension
            value: The item to register  
            dimension: Registry dimension (component, command, etc.)
            metadata: Optional metadata about the item
            aliases: Optional list of aliases for this item
            replace: Whether to replace existing entries
            
        Returns:
            The created registry entry
            
        Raises:
            ValueError: If name already exists and replace=False
        """
        dimension_key = str(dimension)
        
        if not replace and name in self._registry[dimension_key]:
            raise ValueError(
                f"Item '{name}' already registered in dimension '{dimension_key}'. "
                "Use replace=True to override."
            )
        
        entry = RegistryEntry(
            name=name,
            dimension=dimension,
            value=value,
            metadata=metadata or {},
        )
        
        self._registry[dimension_key][name] = entry
        
        if aliases:
            for alias in aliases:
                self._aliases[alias] = (dimension_key, name)
        
        log.debug(
            "Registered item",
            name=name,
            dimension=dimension_key,
            has_metadata=bool(metadata),
            aliases=aliases,
        )
        
        return entry
    
    def get(
        self,
        name: str,
        dimension: RegistryDimension | str | None = None,
    ) -> Any | None:
        """
        Get an item from the registry.
        
        Args:
            name: Name or alias of the item
            dimension: Optional dimension to search in
            
        Returns:
            The registered value or None if not found
        """
        if dimension is not None:
            dimension_key = str(dimension)
            entry = self._registry[dimension_key].get(name)
            if entry:
                return entry.value
        
        if name in self._aliases:
            dim_key, real_name = self._aliases[name]
            if dimension is None or dim_key == str(dimension):
                entry = self._registry[dim_key].get(real_name)
                if entry:
                    return entry.value
        
        if dimension is None:
            for dim_registry in self._registry.values():
                if name in dim_registry:
                    return dim_registry[name].value
        
        return None
    
    def get_entry(
        self,
        name: str,
        dimension: RegistryDimension | str | None = None,
    ) -> RegistryEntry | None:
        """Get the full registry entry."""
        if dimension is not None:
            dimension_key = str(dimension)
            return self._registry[dimension_key].get(name)
        
        if name in self._aliases:
            dim_key, real_name = self._aliases[name]
            if dimension is None or dim_key == str(dimension):
                return self._registry[dim_key].get(real_name)
        
        if dimension is None:
            for dim_registry in self._registry.values():
                if name in dim_registry:
                    return dim_registry[name]
        
        return None
    
    def list_dimension(
        self,
        dimension: RegistryDimension | str,
    ) -> list[str]:
        """List all names in a dimension."""
        return list(self._registry[str(dimension)].keys())
    
    def list_all(self) -> dict[str, list[str]]:
        """List all dimensions and their items."""
        return {
            dimension: list(items.keys())
            for dimension, items in self._registry.items()
        }
    
    def remove(
        self,
        name: str,
        dimension: RegistryDimension | str | None = None,
    ) -> bool:
        """
        Remove an item from the registry.
        
        Returns:
            True if item was removed, False if not found
        """
        if dimension is not None:
            dimension_key = str(dimension)
            if name in self._registry[dimension_key]:
                del self._registry[dimension_key][name]
                
                aliases_to_remove = [
                    alias for alias, (dim, n) in self._aliases.items()
                    if dim == dimension_key and n == name
                ]
                for alias in aliases_to_remove:
                    del self._aliases[alias]
                
                log.debug("Removed item", name=name, dimension=dimension_key)
                return True
        else:
            for dim_key, dim_registry in self._registry.items():
                if name in dim_registry:
                    del dim_registry[name]
                    
                    aliases_to_remove = [
                        alias for alias, (d, n) in self._aliases.items()
                        if d == dim_key and n == name
                    ]
                    for alias in aliases_to_remove:
                        del self._aliases[alias]
                    
                    log.debug("Removed item", name=name, dimension=dim_key)
                    return True
        
        return False
    
    def clear(self, dimension: RegistryDimension | str | None = None) -> None:
        """Clear the registry or a specific dimension."""
        if dimension is not None:
            dimension_key = str(dimension)
            self._registry[dimension_key].clear()
            
            aliases_to_remove = [
                alias for alias, (dim, _) in self._aliases.items()
                if dim == dimension_key
            ]
            for alias in aliases_to_remove:
                del self._aliases[alias]
        else:
            self._registry.clear()
            self._aliases.clear()
    
    def __contains__(self, key: str | tuple[str, str]) -> bool:
        """Check if an item exists in the registry."""
        if isinstance(key, tuple):
            dimension, name = key
            return name in self._registry[dimension]
        else:
            return any(key in dim_reg for dim_reg in self._registry.values())
    
    def __iter__(self) -> Iterator[RegistryEntry]:
        """Iterate over all registry entries."""
        for dim_registry in self._registry.values():
            yield from dim_registry.values()
    
    def __len__(self) -> int:
        """Get total number of registered items."""
        return sum(len(dim_reg) for dim_reg in self._registry.values())