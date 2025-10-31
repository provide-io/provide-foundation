#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator
from typing import Any

from attrs import define, field

from provide.foundation.errors.resources import AlreadyExistsError

"""Registry management for the foundation.

Provides both generic multi-dimensional registry functionality and
specialized command registry management.
"""


@define(frozen=True, slots=True)
class RegistryEntry:
    """A single entry in the registry."""

    name: str
    dimension: str
    value: Any
    metadata: dict[str, Any] = field(factory=dict)

    @property
    def key(self) -> tuple[str, str]:
        """Get the registry key for this entry."""
        return (self.dimension, self.name)


class Registry:
    """Multi-dimensional registry for storing and retrieving objects.

    Supports hierarchical organization by dimension (component, command, etc.)
    and name within each dimension. This is a generic registry that can be
    used for any type of object storage and retrieval.

    Thread-safe: All operations are protected by an RLock for safe concurrent access.

    Note: Uses threading.RLock (not asyncio.Lock) for thread safety. For async-only
    applications with high-frequency registry access in request hot-paths (>10k req/sec
    with runtime registration), consider using an async-native registry implementation
    with asyncio.Lock. For typical use cases (initialization-time registration, CLI apps,
    read-heavy workloads), the threading lock has negligible impact.

    See: docs/architecture/design-decisions.md#threading-model
    """

    def __init__(self) -> None:
        """Initialize an empty registry."""
        # Use managed lock for deadlock prevention
        # Lock is registered during Foundation initialization via register_foundation_locks()
        from provide.foundation.concurrency.locks import get_lock_manager

        self._lock = get_lock_manager().get_lock("foundation.registry")
        self._registry: dict[str, dict[str, RegistryEntry]] = defaultdict(dict)
        self._aliases: dict[str, tuple[str, str]] = {}
        # Type-based registry for dependency injection
        self._type_registry: dict[type[Any], Any] = {}

    def register(
        self,
        name: str,
        value: Any,
        dimension: str = "default",
        metadata: dict[str, Any] | None = None,
        aliases: list[str] | None = None,
        replace: bool = False,
    ) -> RegistryEntry:
        """Register an item in the registry.

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

            # Emit event instead of direct logging to break circular dependency
            from provide.foundation.hub.events import emit_registry_event

            emit_registry_event(
                operation="register",
                item_name=name,
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
        """Get an item from the registry.

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
            return {dimension: list(items.keys()) for dimension, items in self._registry.items()}

    def remove(
        self,
        name: str,
        dimension: str | None = None,
    ) -> bool:
        """Remove an item from the registry.

        Returns:
            True if item was removed, False if not found

        """
        with self._lock:
            if dimension is not None:
                if name in self._registry[dimension]:
                    del self._registry[dimension][name]

                    aliases_to_remove = [
                        alias for alias, (dim, n) in self._aliases.items() if dim == dimension and n == name
                    ]
                    for alias in aliases_to_remove:
                        del self._aliases[alias]

                    # Emit event instead of direct logging to break circular dependency
                    from provide.foundation.hub.events import emit_registry_event

                    emit_registry_event(
                        operation="remove",
                        item_name=name,
                        dimension=dimension,
                    )
                    return True
            else:
                for dim_key, dim_registry in self._registry.items():
                    if name in dim_registry:
                        del dim_registry[name]

                        aliases_to_remove = [
                            alias for alias, (d, n) in self._aliases.items() if d == dim_key and n == name
                        ]
                        for alias in aliases_to_remove:
                            del self._aliases[alias]

                        # Emit event instead of direct logging to break circular dependency
                        from provide.foundation.hub.events import emit_registry_event

                        emit_registry_event(
                            operation="remove",
                            item_name=name,
                            dimension=dim_key,
                        )
                        return True

            return False

    def clear(self, dimension: str | None = None) -> None:
        """Clear the registry or a specific dimension."""
        with self._lock:
            if dimension is not None:
                # Dispose of resources before clearing
                self._dispose_resources(dimension)
                self._registry[dimension].clear()

                aliases_to_remove = [alias for alias, (dim, _) in self._aliases.items() if dim == dimension]
                for alias in aliases_to_remove:
                    del self._aliases[alias]
            else:
                # Dispose of all resources before clearing
                self._dispose_all_resources()
                self._registry.clear()
                self._aliases.clear()
                self._type_registry.clear()

    # Type-based registration for dependency injection

    def register_type(
        self,
        type_hint: type[Any],
        instance: Any,
        name: str | None = None,
    ) -> None:
        """Register an instance by its type for dependency injection.

        This enables type-based lookup which is essential for DI patterns.

        Args:
            type_hint: Type to register under
            instance: Instance to register
            name: Optional name for standard registry (defaults to type name)

        Example:
            >>> registry.register_type(DatabaseClient, db_instance)
            >>> db = registry.get_by_type(DatabaseClient)
        """
        with self._lock:
            self._type_registry[type_hint] = instance

            # Also register in standard registry for backward compatibility
            if name is not None:
                self.register(
                    name=name,
                    value=instance,
                    dimension="types",
                    metadata={"type": type_hint},
                    replace=True,
                )

    def get_by_type(self, type_hint: type[Any]) -> Any | None:
        """Get a registered instance by its type.

        Args:
            type_hint: Type to look up

        Returns:
            Registered instance or None if not found

        Example:
            >>> db = registry.get_by_type(DatabaseClient)
        """
        with self._lock:
            return self._type_registry.get(type_hint)

    def list_types(self) -> list[type[Any]]:
        """List all registered types.

        Returns:
            List of registered types
        """
        with self._lock:
            return list(self._type_registry.keys())

    def dispose_all(self) -> None:
        """Dispose of all registered resources properly."""
        with self._lock:
            self._dispose_all_resources()

    def _dispose_all_resources(self) -> None:
        """Dispose of all resources across all dimensions."""
        for dimension in self._registry:
            self._dispose_resources(dimension)

    def _dispose_resources(self, dimension: str) -> None:
        """Dispose of resources in a specific dimension."""
        from provide.foundation.hub.protocols import AsyncDisposable, Disposable

        for entry in self._registry[dimension].values():
            value = entry.value
            if isinstance(value, Disposable):
                import contextlib

                with contextlib.suppress(Exception):
                    # Continue disposing other resources even if one fails
                    value.dispose()
            elif isinstance(value, AsyncDisposable):
                # For async disposables in sync context, we can't await
                # They should be disposed in async context managers
                # Log a warning that proper async disposal is needed
                pass

    def __contains__(self, key: str | tuple[str, str]) -> bool:
        """Check if an item exists in the registry."""
        with self._lock:
            if isinstance(key, tuple):
                dimension, name = key
                return name in self._registry[dimension]
            return any(key in dim_reg for dim_reg in self._registry.values())

    def __iter__(self) -> Iterator[RegistryEntry]:
        """Iterate over all registry entries."""
        with self._lock:
            # Create a snapshot to avoid holding lock during iteration
            entries: list[RegistryEntry] = []
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

# 🧱🏗️🔚
