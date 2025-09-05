"""Registry management for the foundation.

Provides both generic multi-dimensional registry functionality and
specialized command registry management.
"""

from collections import defaultdict
from collections.abc import Iterator
import threading
from typing import Any

from attrs import define, field

from provide.foundation.errors.resources import AlreadyExistsError
from provide.foundation.logger import get_logger

log = get_logger(__name__)


@define(frozen=True, slots=True)
class RegistryEntry:
    """A single entry in the registry."""

    name: str
    dimension: str
    value: Any
    metadata: dict[str, Any] = field(factory=lambda: {})

    @property
    def key(self) -> tuple[str, str]:
        """Get the registry key for this entry."""
        return (self.dimension, self.name)


class Registry:
    """
    Multi-dimensional registry for storing and retrieving objects.

    Supports hierarchical organization by dimension (component, command, etc.)
    and name within each dimension. This is a generic registry that can be
    used for any type of object storage and retrieval.

    Thread-safe: All operations are protected by an RLock for safe concurrent access.
    """

    def __init__(self) -> None:
        """Initialize an empty registry."""
        self._lock = threading.RLock()  # Reentrant lock for thread safety
        self._registry: dict[str, dict[str, RegistryEntry]] = defaultdict(dict)
        self._aliases: dict[str, tuple[str, str]] = {}

    def register(
        self,
        name: str,
        value: Any,
        dimension: str = "default",
        metadata: dict[str, Any] | None = None,
        aliases: list[str] | None = None,
        replace: bool = False,
    ) -> RegistryEntry:
        """
        Register an item in the registry.

        Args:
            name: Unique name within the dimension
            value: The item to register
            dimension: Registry dimension for categorization
            metadata: Optional metadata about the item
            aliases: Optional list of aliases for this item
            replace: Whether to replace existing entries

        Returns:
            The created registry entry

        Raises:
            ValueError: If name already exists and replace=False
        """
        with self._lock:
            if not replace and name in self._registry[dimension]:
                raise AlreadyExistsError(
                    f"Item '{name}' already registered in dimension '{dimension}'. "
                    "Use replace=True to override.",
                    code="REGISTRY_ITEM_EXISTS",
                    item_name=name,
                    dimension=dimension,
                )

            entry = RegistryEntry(
                name=name,
                dimension=dimension,
                value=value,
                metadata=metadata or {},
            )

            self._registry[dimension][name] = entry

            if aliases:
                for alias in aliases:
                    self._aliases[alias] = (dimension, name)

            log.debug(
                "Registered item",
                name=name,
                dimension=dimension,
                has_metadata=bool(metadata),
                aliases=aliases,
            )

            return entry

    def get(
        self,
        name: str,
        dimension: str | None = None,
    ) -> Any | None:
        """
        Get an item from the registry.

        Args:
            name: Name or alias of the item
            dimension: Optional dimension to search in

        Returns:
            The registered value or None if not found
        """
        with self._lock:
            if dimension is not None:
                entry = self._registry[dimension].get(name)
                if entry:
                    return entry.value

            if name in self._aliases:
                dim_key, real_name = self._aliases[name]
                if dimension is None or dim_key == dimension:
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
        dimension: str | None = None,
    ) -> RegistryEntry | None:
        """Get the full registry entry."""
        with self._lock:
            if dimension is not None:
                return self._registry[dimension].get(name)

            if name in self._aliases:
                dim_key, real_name = self._aliases[name]
                if dimension is None or dim_key == dimension:
                    return self._registry[dim_key].get(real_name)

            if dimension is None:
                for dim_registry in self._registry.values():
                    if name in dim_registry:
                        return dim_registry[name]

            return None

    def list_dimension(
        self,
        dimension: str,
    ) -> list[str]:
        """List all names in a dimension."""
        with self._lock:
            return list(self._registry[dimension].keys())

    def list_all(self) -> dict[str, list[str]]:
        """List all dimensions and their items."""
        with self._lock:
            return {
                dimension: list(items.keys())
                for dimension, items in self._registry.items()
            }

    def remove(
        self,
        name: str,
        dimension: str | None = None,
    ) -> bool:
        """
        Remove an item from the registry.

        Returns:
            True if item was removed, False if not found
        """
        with self._lock:
            if dimension is not None:
                if name in self._registry[dimension]:
                    del self._registry[dimension][name]

                    aliases_to_remove = [
                        alias
                        for alias, (dim, n) in self._aliases.items()
                        if dim == dimension and n == name
                    ]
                    for alias in aliases_to_remove:
                        del self._aliases[alias]

                    log.debug("Removed item", name=name, dimension=dimension)
                    return True
            else:
                for dim_key, dim_registry in self._registry.items():
                    if name in dim_registry:
                        del dim_registry[name]

                        aliases_to_remove = [
                            alias
                            for alias, (d, n) in self._aliases.items()
                            if d == dim_key and n == name
                        ]
                        for alias in aliases_to_remove:
                            del self._aliases[alias]

                        log.debug("Removed item", name=name, dimension=dim_key)
                        return True

            return False

    def clear(self, dimension: str | None = None) -> None:
        """Clear the registry or a specific dimension."""
        with self._lock:
            if dimension is not None:
                self._registry[dimension].clear()

                aliases_to_remove = [
                    alias
                    for alias, (dim, _) in self._aliases.items()
                    if dim == dimension
                ]
                for alias in aliases_to_remove:
                    del self._aliases[alias]
            else:
                self._registry.clear()
                self._aliases.clear()

    def __contains__(self, key: str | tuple[str, str]) -> bool:
        """Check if an item exists in the registry."""
        with self._lock:
            if isinstance(key, tuple):
                dimension, name = key
                return name in self._registry[dimension]
            else:
                return any(key in dim_reg for dim_reg in self._registry.values())

    def __iter__(self) -> Iterator[RegistryEntry]:
        """Iterate over all registry entries."""
        with self._lock:
            # Create a snapshot to avoid holding lock during iteration
            entries = []
            for dim_registry in self._registry.values():
                entries.extend(dim_registry.values())
        # Yield outside the lock
        yield from entries

    def __len__(self) -> int:
        """Get total number of registered items."""
        with self._lock:
            return sum(len(dim_reg) for dim_reg in self._registry.values())


# Global registry for commands
_command_registry = Registry()


def get_command_registry() -> Registry:
    """Get the global command registry."""
    return _command_registry


__all__ = ["Registry", "RegistryEntry", "get_command_registry"]
