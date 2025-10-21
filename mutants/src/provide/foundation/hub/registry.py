# provide/foundation/hub/registry.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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

    def xǁRegistryǁ__init____mutmut_orig(self) -> None:
        """Initialize an empty registry."""
        # Use managed lock for deadlock prevention
        # Lock is registered during Foundation initialization via register_foundation_locks()
        from provide.foundation.concurrency.locks import get_lock_manager

        self._lock = get_lock_manager().get_lock("foundation.registry")
        self._registry: dict[str, dict[str, RegistryEntry]] = defaultdict(dict)
        self._aliases: dict[str, tuple[str, str]] = {}
        # Type-based registry for dependency injection
        self._type_registry: dict[type[Any], Any] = {}

    def xǁRegistryǁ__init____mutmut_1(self) -> None:
        """Initialize an empty registry."""
        # Use managed lock for deadlock prevention
        # Lock is registered during Foundation initialization via register_foundation_locks()
        from provide.foundation.concurrency.locks import get_lock_manager

        self._lock = None
        self._registry: dict[str, dict[str, RegistryEntry]] = defaultdict(dict)
        self._aliases: dict[str, tuple[str, str]] = {}
        # Type-based registry for dependency injection
        self._type_registry: dict[type[Any], Any] = {}

    def xǁRegistryǁ__init____mutmut_2(self) -> None:
        """Initialize an empty registry."""
        # Use managed lock for deadlock prevention
        # Lock is registered during Foundation initialization via register_foundation_locks()
        from provide.foundation.concurrency.locks import get_lock_manager

        self._lock = get_lock_manager().get_lock(None)
        self._registry: dict[str, dict[str, RegistryEntry]] = defaultdict(dict)
        self._aliases: dict[str, tuple[str, str]] = {}
        # Type-based registry for dependency injection
        self._type_registry: dict[type[Any], Any] = {}

    def xǁRegistryǁ__init____mutmut_3(self) -> None:
        """Initialize an empty registry."""
        # Use managed lock for deadlock prevention
        # Lock is registered during Foundation initialization via register_foundation_locks()
        from provide.foundation.concurrency.locks import get_lock_manager

        self._lock = get_lock_manager().get_lock("XXfoundation.registryXX")
        self._registry: dict[str, dict[str, RegistryEntry]] = defaultdict(dict)
        self._aliases: dict[str, tuple[str, str]] = {}
        # Type-based registry for dependency injection
        self._type_registry: dict[type[Any], Any] = {}

    def xǁRegistryǁ__init____mutmut_4(self) -> None:
        """Initialize an empty registry."""
        # Use managed lock for deadlock prevention
        # Lock is registered during Foundation initialization via register_foundation_locks()
        from provide.foundation.concurrency.locks import get_lock_manager

        self._lock = get_lock_manager().get_lock("FOUNDATION.REGISTRY")
        self._registry: dict[str, dict[str, RegistryEntry]] = defaultdict(dict)
        self._aliases: dict[str, tuple[str, str]] = {}
        # Type-based registry for dependency injection
        self._type_registry: dict[type[Any], Any] = {}

    def xǁRegistryǁ__init____mutmut_5(self) -> None:
        """Initialize an empty registry."""
        # Use managed lock for deadlock prevention
        # Lock is registered during Foundation initialization via register_foundation_locks()
        from provide.foundation.concurrency.locks import get_lock_manager

        self._lock = get_lock_manager().get_lock("foundation.registry")
        self._registry: dict[str, dict[str, RegistryEntry]] = None
        self._aliases: dict[str, tuple[str, str]] = {}
        # Type-based registry for dependency injection
        self._type_registry: dict[type[Any], Any] = {}

    def xǁRegistryǁ__init____mutmut_6(self) -> None:
        """Initialize an empty registry."""
        # Use managed lock for deadlock prevention
        # Lock is registered during Foundation initialization via register_foundation_locks()
        from provide.foundation.concurrency.locks import get_lock_manager

        self._lock = get_lock_manager().get_lock("foundation.registry")
        self._registry: dict[str, dict[str, RegistryEntry]] = defaultdict(None)
        self._aliases: dict[str, tuple[str, str]] = {}
        # Type-based registry for dependency injection
        self._type_registry: dict[type[Any], Any] = {}

    def xǁRegistryǁ__init____mutmut_7(self) -> None:
        """Initialize an empty registry."""
        # Use managed lock for deadlock prevention
        # Lock is registered during Foundation initialization via register_foundation_locks()
        from provide.foundation.concurrency.locks import get_lock_manager

        self._lock = get_lock_manager().get_lock("foundation.registry")
        self._registry: dict[str, dict[str, RegistryEntry]] = defaultdict(dict)
        self._aliases: dict[str, tuple[str, str]] = None
        # Type-based registry for dependency injection
        self._type_registry: dict[type[Any], Any] = {}

    def xǁRegistryǁ__init____mutmut_8(self) -> None:
        """Initialize an empty registry."""
        # Use managed lock for deadlock prevention
        # Lock is registered during Foundation initialization via register_foundation_locks()
        from provide.foundation.concurrency.locks import get_lock_manager

        self._lock = get_lock_manager().get_lock("foundation.registry")
        self._registry: dict[str, dict[str, RegistryEntry]] = defaultdict(dict)
        self._aliases: dict[str, tuple[str, str]] = {}
        # Type-based registry for dependency injection
        self._type_registry: dict[type[Any], Any] = None
    
    xǁRegistryǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRegistryǁ__init____mutmut_1': xǁRegistryǁ__init____mutmut_1, 
        'xǁRegistryǁ__init____mutmut_2': xǁRegistryǁ__init____mutmut_2, 
        'xǁRegistryǁ__init____mutmut_3': xǁRegistryǁ__init____mutmut_3, 
        'xǁRegistryǁ__init____mutmut_4': xǁRegistryǁ__init____mutmut_4, 
        'xǁRegistryǁ__init____mutmut_5': xǁRegistryǁ__init____mutmut_5, 
        'xǁRegistryǁ__init____mutmut_6': xǁRegistryǁ__init____mutmut_6, 
        'xǁRegistryǁ__init____mutmut_7': xǁRegistryǁ__init____mutmut_7, 
        'xǁRegistryǁ__init____mutmut_8': xǁRegistryǁ__init____mutmut_8
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRegistryǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁRegistryǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁRegistryǁ__init____mutmut_orig)
    xǁRegistryǁ__init____mutmut_orig.__name__ = 'xǁRegistryǁ__init__'

    def xǁRegistryǁregister__mutmut_orig(
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

    def xǁRegistryǁregister__mutmut_1(
        self,
        name: str,
        value: Any,
        dimension: str = "XXdefaultXX",
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

    def xǁRegistryǁregister__mutmut_2(
        self,
        name: str,
        value: Any,
        dimension: str = "DEFAULT",
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

    def xǁRegistryǁregister__mutmut_3(
        self,
        name: str,
        value: Any,
        dimension: str = "default",
        metadata: dict[str, Any] | None = None,
        aliases: list[str] | None = None,
        replace: bool = True,
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

    def xǁRegistryǁregister__mutmut_4(
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
            if not replace or name in self._registry[dimension]:
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

    def xǁRegistryǁregister__mutmut_5(
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
            if replace and name in self._registry[dimension]:
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

    def xǁRegistryǁregister__mutmut_6(
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
            if not replace and name not in self._registry[dimension]:
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

    def xǁRegistryǁregister__mutmut_7(
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
                    None,
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

    def xǁRegistryǁregister__mutmut_8(
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
                    code=None,
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

    def xǁRegistryǁregister__mutmut_9(
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
                    item_name=None,
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

    def xǁRegistryǁregister__mutmut_10(
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
                    dimension=None,
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

    def xǁRegistryǁregister__mutmut_11(
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

    def xǁRegistryǁregister__mutmut_12(
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

    def xǁRegistryǁregister__mutmut_13(
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

    def xǁRegistryǁregister__mutmut_14(
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

    def xǁRegistryǁregister__mutmut_15(
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
                    "XXUse replace=True to override.XX",
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

    def xǁRegistryǁregister__mutmut_16(
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
                    "use replace=true to override.",
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

    def xǁRegistryǁregister__mutmut_17(
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
                    "USE REPLACE=TRUE TO OVERRIDE.",
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

    def xǁRegistryǁregister__mutmut_18(
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
                    code="XXREGISTRY_ITEM_EXISTSXX",
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

    def xǁRegistryǁregister__mutmut_19(
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
                    code="registry_item_exists",
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

    def xǁRegistryǁregister__mutmut_20(
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

            entry = None

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

    def xǁRegistryǁregister__mutmut_21(
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
                name=None,
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

    def xǁRegistryǁregister__mutmut_22(
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
                dimension=None,
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

    def xǁRegistryǁregister__mutmut_23(
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
                value=None,
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

    def xǁRegistryǁregister__mutmut_24(
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
                metadata=None,
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

    def xǁRegistryǁregister__mutmut_25(
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

    def xǁRegistryǁregister__mutmut_26(
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

    def xǁRegistryǁregister__mutmut_27(
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

    def xǁRegistryǁregister__mutmut_28(
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

    def xǁRegistryǁregister__mutmut_29(
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
                metadata=metadata and {},
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

    def xǁRegistryǁregister__mutmut_30(
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

            self._registry[dimension][name] = None

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

    def xǁRegistryǁregister__mutmut_31(
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
                    self._aliases[alias] = None

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

    def xǁRegistryǁregister__mutmut_32(
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
                operation=None,
                item_name=name,
                dimension=dimension,
                has_metadata=bool(metadata),
                aliases=aliases,
            )

            return entry

    def xǁRegistryǁregister__mutmut_33(
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
                item_name=None,
                dimension=dimension,
                has_metadata=bool(metadata),
                aliases=aliases,
            )

            return entry

    def xǁRegistryǁregister__mutmut_34(
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
                dimension=None,
                has_metadata=bool(metadata),
                aliases=aliases,
            )

            return entry

    def xǁRegistryǁregister__mutmut_35(
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
                has_metadata=None,
                aliases=aliases,
            )

            return entry

    def xǁRegistryǁregister__mutmut_36(
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
                aliases=None,
            )

            return entry

    def xǁRegistryǁregister__mutmut_37(
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
                item_name=name,
                dimension=dimension,
                has_metadata=bool(metadata),
                aliases=aliases,
            )

            return entry

    def xǁRegistryǁregister__mutmut_38(
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
                dimension=dimension,
                has_metadata=bool(metadata),
                aliases=aliases,
            )

            return entry

    def xǁRegistryǁregister__mutmut_39(
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
                has_metadata=bool(metadata),
                aliases=aliases,
            )

            return entry

    def xǁRegistryǁregister__mutmut_40(
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
                aliases=aliases,
            )

            return entry

    def xǁRegistryǁregister__mutmut_41(
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
                )

            return entry

    def xǁRegistryǁregister__mutmut_42(
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
                operation="XXregisterXX",
                item_name=name,
                dimension=dimension,
                has_metadata=bool(metadata),
                aliases=aliases,
            )

            return entry

    def xǁRegistryǁregister__mutmut_43(
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
                operation="REGISTER",
                item_name=name,
                dimension=dimension,
                has_metadata=bool(metadata),
                aliases=aliases,
            )

            return entry

    def xǁRegistryǁregister__mutmut_44(
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
                has_metadata=bool(None),
                aliases=aliases,
            )

            return entry
    
    xǁRegistryǁregister__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRegistryǁregister__mutmut_1': xǁRegistryǁregister__mutmut_1, 
        'xǁRegistryǁregister__mutmut_2': xǁRegistryǁregister__mutmut_2, 
        'xǁRegistryǁregister__mutmut_3': xǁRegistryǁregister__mutmut_3, 
        'xǁRegistryǁregister__mutmut_4': xǁRegistryǁregister__mutmut_4, 
        'xǁRegistryǁregister__mutmut_5': xǁRegistryǁregister__mutmut_5, 
        'xǁRegistryǁregister__mutmut_6': xǁRegistryǁregister__mutmut_6, 
        'xǁRegistryǁregister__mutmut_7': xǁRegistryǁregister__mutmut_7, 
        'xǁRegistryǁregister__mutmut_8': xǁRegistryǁregister__mutmut_8, 
        'xǁRegistryǁregister__mutmut_9': xǁRegistryǁregister__mutmut_9, 
        'xǁRegistryǁregister__mutmut_10': xǁRegistryǁregister__mutmut_10, 
        'xǁRegistryǁregister__mutmut_11': xǁRegistryǁregister__mutmut_11, 
        'xǁRegistryǁregister__mutmut_12': xǁRegistryǁregister__mutmut_12, 
        'xǁRegistryǁregister__mutmut_13': xǁRegistryǁregister__mutmut_13, 
        'xǁRegistryǁregister__mutmut_14': xǁRegistryǁregister__mutmut_14, 
        'xǁRegistryǁregister__mutmut_15': xǁRegistryǁregister__mutmut_15, 
        'xǁRegistryǁregister__mutmut_16': xǁRegistryǁregister__mutmut_16, 
        'xǁRegistryǁregister__mutmut_17': xǁRegistryǁregister__mutmut_17, 
        'xǁRegistryǁregister__mutmut_18': xǁRegistryǁregister__mutmut_18, 
        'xǁRegistryǁregister__mutmut_19': xǁRegistryǁregister__mutmut_19, 
        'xǁRegistryǁregister__mutmut_20': xǁRegistryǁregister__mutmut_20, 
        'xǁRegistryǁregister__mutmut_21': xǁRegistryǁregister__mutmut_21, 
        'xǁRegistryǁregister__mutmut_22': xǁRegistryǁregister__mutmut_22, 
        'xǁRegistryǁregister__mutmut_23': xǁRegistryǁregister__mutmut_23, 
        'xǁRegistryǁregister__mutmut_24': xǁRegistryǁregister__mutmut_24, 
        'xǁRegistryǁregister__mutmut_25': xǁRegistryǁregister__mutmut_25, 
        'xǁRegistryǁregister__mutmut_26': xǁRegistryǁregister__mutmut_26, 
        'xǁRegistryǁregister__mutmut_27': xǁRegistryǁregister__mutmut_27, 
        'xǁRegistryǁregister__mutmut_28': xǁRegistryǁregister__mutmut_28, 
        'xǁRegistryǁregister__mutmut_29': xǁRegistryǁregister__mutmut_29, 
        'xǁRegistryǁregister__mutmut_30': xǁRegistryǁregister__mutmut_30, 
        'xǁRegistryǁregister__mutmut_31': xǁRegistryǁregister__mutmut_31, 
        'xǁRegistryǁregister__mutmut_32': xǁRegistryǁregister__mutmut_32, 
        'xǁRegistryǁregister__mutmut_33': xǁRegistryǁregister__mutmut_33, 
        'xǁRegistryǁregister__mutmut_34': xǁRegistryǁregister__mutmut_34, 
        'xǁRegistryǁregister__mutmut_35': xǁRegistryǁregister__mutmut_35, 
        'xǁRegistryǁregister__mutmut_36': xǁRegistryǁregister__mutmut_36, 
        'xǁRegistryǁregister__mutmut_37': xǁRegistryǁregister__mutmut_37, 
        'xǁRegistryǁregister__mutmut_38': xǁRegistryǁregister__mutmut_38, 
        'xǁRegistryǁregister__mutmut_39': xǁRegistryǁregister__mutmut_39, 
        'xǁRegistryǁregister__mutmut_40': xǁRegistryǁregister__mutmut_40, 
        'xǁRegistryǁregister__mutmut_41': xǁRegistryǁregister__mutmut_41, 
        'xǁRegistryǁregister__mutmut_42': xǁRegistryǁregister__mutmut_42, 
        'xǁRegistryǁregister__mutmut_43': xǁRegistryǁregister__mutmut_43, 
        'xǁRegistryǁregister__mutmut_44': xǁRegistryǁregister__mutmut_44
    }
    
    def register(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRegistryǁregister__mutmut_orig"), object.__getattribute__(self, "xǁRegistryǁregister__mutmut_mutants"), args, kwargs, self)
        return result 
    
    register.__signature__ = _mutmut_signature(xǁRegistryǁregister__mutmut_orig)
    xǁRegistryǁregister__mutmut_orig.__name__ = 'xǁRegistryǁregister'

    def xǁRegistryǁget__mutmut_orig(
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

    def xǁRegistryǁget__mutmut_1(
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
            if dimension is None:
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

    def xǁRegistryǁget__mutmut_2(
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
                entry = None
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

    def xǁRegistryǁget__mutmut_3(
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
                entry = self._registry[dimension].get(None)
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

    def xǁRegistryǁget__mutmut_4(
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

            if name not in self._aliases:
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

    def xǁRegistryǁget__mutmut_5(
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
                dim_key, real_name = None
                if dimension is None or dim_key == dimension:
                    entry = self._registry[dim_key].get(real_name)
                    if entry:
                        return entry.value

            if dimension is None:
                for dim_registry in self._registry.values():
                    if name in dim_registry:
                        return dim_registry[name].value

            return None

    def xǁRegistryǁget__mutmut_6(
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
                if dimension is None and dim_key == dimension:
                    entry = self._registry[dim_key].get(real_name)
                    if entry:
                        return entry.value

            if dimension is None:
                for dim_registry in self._registry.values():
                    if name in dim_registry:
                        return dim_registry[name].value

            return None

    def xǁRegistryǁget__mutmut_7(
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
                if dimension is not None or dim_key == dimension:
                    entry = self._registry[dim_key].get(real_name)
                    if entry:
                        return entry.value

            if dimension is None:
                for dim_registry in self._registry.values():
                    if name in dim_registry:
                        return dim_registry[name].value

            return None

    def xǁRegistryǁget__mutmut_8(
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
                if dimension is None or dim_key != dimension:
                    entry = self._registry[dim_key].get(real_name)
                    if entry:
                        return entry.value

            if dimension is None:
                for dim_registry in self._registry.values():
                    if name in dim_registry:
                        return dim_registry[name].value

            return None

    def xǁRegistryǁget__mutmut_9(
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
                    entry = None
                    if entry:
                        return entry.value

            if dimension is None:
                for dim_registry in self._registry.values():
                    if name in dim_registry:
                        return dim_registry[name].value

            return None

    def xǁRegistryǁget__mutmut_10(
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
                    entry = self._registry[dim_key].get(None)
                    if entry:
                        return entry.value

            if dimension is None:
                for dim_registry in self._registry.values():
                    if name in dim_registry:
                        return dim_registry[name].value

            return None

    def xǁRegistryǁget__mutmut_11(
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

            if dimension is not None:
                for dim_registry in self._registry.values():
                    if name in dim_registry:
                        return dim_registry[name].value

            return None

    def xǁRegistryǁget__mutmut_12(
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
                    if name not in dim_registry:
                        return dim_registry[name].value

            return None
    
    xǁRegistryǁget__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRegistryǁget__mutmut_1': xǁRegistryǁget__mutmut_1, 
        'xǁRegistryǁget__mutmut_2': xǁRegistryǁget__mutmut_2, 
        'xǁRegistryǁget__mutmut_3': xǁRegistryǁget__mutmut_3, 
        'xǁRegistryǁget__mutmut_4': xǁRegistryǁget__mutmut_4, 
        'xǁRegistryǁget__mutmut_5': xǁRegistryǁget__mutmut_5, 
        'xǁRegistryǁget__mutmut_6': xǁRegistryǁget__mutmut_6, 
        'xǁRegistryǁget__mutmut_7': xǁRegistryǁget__mutmut_7, 
        'xǁRegistryǁget__mutmut_8': xǁRegistryǁget__mutmut_8, 
        'xǁRegistryǁget__mutmut_9': xǁRegistryǁget__mutmut_9, 
        'xǁRegistryǁget__mutmut_10': xǁRegistryǁget__mutmut_10, 
        'xǁRegistryǁget__mutmut_11': xǁRegistryǁget__mutmut_11, 
        'xǁRegistryǁget__mutmut_12': xǁRegistryǁget__mutmut_12
    }
    
    def get(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRegistryǁget__mutmut_orig"), object.__getattribute__(self, "xǁRegistryǁget__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get.__signature__ = _mutmut_signature(xǁRegistryǁget__mutmut_orig)
    xǁRegistryǁget__mutmut_orig.__name__ = 'xǁRegistryǁget'

    def xǁRegistryǁget_entry__mutmut_orig(
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

    def xǁRegistryǁget_entry__mutmut_1(
        self,
        name: str,
        dimension: str | None = None,
    ) -> RegistryEntry | None:
        """Get the full registry entry."""
        with self._lock:
            if dimension is None:
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

    def xǁRegistryǁget_entry__mutmut_2(
        self,
        name: str,
        dimension: str | None = None,
    ) -> RegistryEntry | None:
        """Get the full registry entry."""
        with self._lock:
            if dimension is not None:
                return self._registry[dimension].get(None)

            if name in self._aliases:
                dim_key, real_name = self._aliases[name]
                if dimension is None or dim_key == dimension:
                    return self._registry[dim_key].get(real_name)

            if dimension is None:
                for dim_registry in self._registry.values():
                    if name in dim_registry:
                        return dim_registry[name]

            return None

    def xǁRegistryǁget_entry__mutmut_3(
        self,
        name: str,
        dimension: str | None = None,
    ) -> RegistryEntry | None:
        """Get the full registry entry."""
        with self._lock:
            if dimension is not None:
                return self._registry[dimension].get(name)

            if name not in self._aliases:
                dim_key, real_name = self._aliases[name]
                if dimension is None or dim_key == dimension:
                    return self._registry[dim_key].get(real_name)

            if dimension is None:
                for dim_registry in self._registry.values():
                    if name in dim_registry:
                        return dim_registry[name]

            return None

    def xǁRegistryǁget_entry__mutmut_4(
        self,
        name: str,
        dimension: str | None = None,
    ) -> RegistryEntry | None:
        """Get the full registry entry."""
        with self._lock:
            if dimension is not None:
                return self._registry[dimension].get(name)

            if name in self._aliases:
                dim_key, real_name = None
                if dimension is None or dim_key == dimension:
                    return self._registry[dim_key].get(real_name)

            if dimension is None:
                for dim_registry in self._registry.values():
                    if name in dim_registry:
                        return dim_registry[name]

            return None

    def xǁRegistryǁget_entry__mutmut_5(
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
                if dimension is None and dim_key == dimension:
                    return self._registry[dim_key].get(real_name)

            if dimension is None:
                for dim_registry in self._registry.values():
                    if name in dim_registry:
                        return dim_registry[name]

            return None

    def xǁRegistryǁget_entry__mutmut_6(
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
                if dimension is not None or dim_key == dimension:
                    return self._registry[dim_key].get(real_name)

            if dimension is None:
                for dim_registry in self._registry.values():
                    if name in dim_registry:
                        return dim_registry[name]

            return None

    def xǁRegistryǁget_entry__mutmut_7(
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
                if dimension is None or dim_key != dimension:
                    return self._registry[dim_key].get(real_name)

            if dimension is None:
                for dim_registry in self._registry.values():
                    if name in dim_registry:
                        return dim_registry[name]

            return None

    def xǁRegistryǁget_entry__mutmut_8(
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
                    return self._registry[dim_key].get(None)

            if dimension is None:
                for dim_registry in self._registry.values():
                    if name in dim_registry:
                        return dim_registry[name]

            return None

    def xǁRegistryǁget_entry__mutmut_9(
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

            if dimension is not None:
                for dim_registry in self._registry.values():
                    if name in dim_registry:
                        return dim_registry[name]

            return None

    def xǁRegistryǁget_entry__mutmut_10(
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
                    if name not in dim_registry:
                        return dim_registry[name]

            return None
    
    xǁRegistryǁget_entry__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRegistryǁget_entry__mutmut_1': xǁRegistryǁget_entry__mutmut_1, 
        'xǁRegistryǁget_entry__mutmut_2': xǁRegistryǁget_entry__mutmut_2, 
        'xǁRegistryǁget_entry__mutmut_3': xǁRegistryǁget_entry__mutmut_3, 
        'xǁRegistryǁget_entry__mutmut_4': xǁRegistryǁget_entry__mutmut_4, 
        'xǁRegistryǁget_entry__mutmut_5': xǁRegistryǁget_entry__mutmut_5, 
        'xǁRegistryǁget_entry__mutmut_6': xǁRegistryǁget_entry__mutmut_6, 
        'xǁRegistryǁget_entry__mutmut_7': xǁRegistryǁget_entry__mutmut_7, 
        'xǁRegistryǁget_entry__mutmut_8': xǁRegistryǁget_entry__mutmut_8, 
        'xǁRegistryǁget_entry__mutmut_9': xǁRegistryǁget_entry__mutmut_9, 
        'xǁRegistryǁget_entry__mutmut_10': xǁRegistryǁget_entry__mutmut_10
    }
    
    def get_entry(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRegistryǁget_entry__mutmut_orig"), object.__getattribute__(self, "xǁRegistryǁget_entry__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_entry.__signature__ = _mutmut_signature(xǁRegistryǁget_entry__mutmut_orig)
    xǁRegistryǁget_entry__mutmut_orig.__name__ = 'xǁRegistryǁget_entry'

    def xǁRegistryǁlist_dimension__mutmut_orig(
        self,
        dimension: str,
    ) -> list[str]:
        """List all names in a dimension."""
        with self._lock:
            return list(self._registry[dimension].keys())

    def xǁRegistryǁlist_dimension__mutmut_1(
        self,
        dimension: str,
    ) -> list[str]:
        """List all names in a dimension."""
        with self._lock:
            return list(None)
    
    xǁRegistryǁlist_dimension__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRegistryǁlist_dimension__mutmut_1': xǁRegistryǁlist_dimension__mutmut_1
    }
    
    def list_dimension(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRegistryǁlist_dimension__mutmut_orig"), object.__getattribute__(self, "xǁRegistryǁlist_dimension__mutmut_mutants"), args, kwargs, self)
        return result 
    
    list_dimension.__signature__ = _mutmut_signature(xǁRegistryǁlist_dimension__mutmut_orig)
    xǁRegistryǁlist_dimension__mutmut_orig.__name__ = 'xǁRegistryǁlist_dimension'

    def xǁRegistryǁlist_all__mutmut_orig(self) -> dict[str, list[str]]:
        """List all dimensions and their items."""
        with self._lock:
            return {dimension: list(items.keys()) for dimension, items in self._registry.items()}

    def xǁRegistryǁlist_all__mutmut_1(self) -> dict[str, list[str]]:
        """List all dimensions and their items."""
        with self._lock:
            return {dimension: list(None) for dimension, items in self._registry.items()}
    
    xǁRegistryǁlist_all__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRegistryǁlist_all__mutmut_1': xǁRegistryǁlist_all__mutmut_1
    }
    
    def list_all(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRegistryǁlist_all__mutmut_orig"), object.__getattribute__(self, "xǁRegistryǁlist_all__mutmut_mutants"), args, kwargs, self)
        return result 
    
    list_all.__signature__ = _mutmut_signature(xǁRegistryǁlist_all__mutmut_orig)
    xǁRegistryǁlist_all__mutmut_orig.__name__ = 'xǁRegistryǁlist_all'

    def xǁRegistryǁremove__mutmut_orig(
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

    def xǁRegistryǁremove__mutmut_1(
        self,
        name: str,
        dimension: str | None = None,
    ) -> bool:
        """Remove an item from the registry.

        Returns:
            True if item was removed, False if not found

        """
        with self._lock:
            if dimension is None:
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

    def xǁRegistryǁremove__mutmut_2(
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
                if name not in self._registry[dimension]:
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

    def xǁRegistryǁremove__mutmut_3(
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

                    aliases_to_remove = None
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

    def xǁRegistryǁremove__mutmut_4(
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
                        alias for alias, (dim, n) in self._aliases.items() if dim == dimension or n == name
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

    def xǁRegistryǁremove__mutmut_5(
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
                        alias for alias, (dim, n) in self._aliases.items() if dim != dimension and n == name
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

    def xǁRegistryǁremove__mutmut_6(
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
                        alias for alias, (dim, n) in self._aliases.items() if dim == dimension and n != name
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

    def xǁRegistryǁremove__mutmut_7(
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
                        operation=None,
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

    def xǁRegistryǁremove__mutmut_8(
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
                        item_name=None,
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

    def xǁRegistryǁremove__mutmut_9(
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
                        dimension=None,
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

    def xǁRegistryǁremove__mutmut_10(
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

    def xǁRegistryǁremove__mutmut_11(
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

    def xǁRegistryǁremove__mutmut_12(
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

    def xǁRegistryǁremove__mutmut_13(
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
                        operation="XXremoveXX",
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

    def xǁRegistryǁremove__mutmut_14(
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
                        operation="REMOVE",
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

    def xǁRegistryǁremove__mutmut_15(
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
                    return False
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

    def xǁRegistryǁremove__mutmut_16(
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
                    if name not in dim_registry:
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

    def xǁRegistryǁremove__mutmut_17(
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

                        aliases_to_remove = None
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

    def xǁRegistryǁremove__mutmut_18(
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
                            alias for alias, (d, n) in self._aliases.items() if d == dim_key or n == name
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

    def xǁRegistryǁremove__mutmut_19(
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
                            alias for alias, (d, n) in self._aliases.items() if d != dim_key and n == name
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

    def xǁRegistryǁremove__mutmut_20(
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
                            alias for alias, (d, n) in self._aliases.items() if d == dim_key and n != name
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

    def xǁRegistryǁremove__mutmut_21(
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
                            operation=None,
                            item_name=name,
                            dimension=dim_key,
                        )
                        return True

            return False

    def xǁRegistryǁremove__mutmut_22(
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
                            item_name=None,
                            dimension=dim_key,
                        )
                        return True

            return False

    def xǁRegistryǁremove__mutmut_23(
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
                            dimension=None,
                        )
                        return True

            return False

    def xǁRegistryǁremove__mutmut_24(
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
                            item_name=name,
                            dimension=dim_key,
                        )
                        return True

            return False

    def xǁRegistryǁremove__mutmut_25(
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
                            dimension=dim_key,
                        )
                        return True

            return False

    def xǁRegistryǁremove__mutmut_26(
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
                            )
                        return True

            return False

    def xǁRegistryǁremove__mutmut_27(
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
                            operation="XXremoveXX",
                            item_name=name,
                            dimension=dim_key,
                        )
                        return True

            return False

    def xǁRegistryǁremove__mutmut_28(
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
                            operation="REMOVE",
                            item_name=name,
                            dimension=dim_key,
                        )
                        return True

            return False

    def xǁRegistryǁremove__mutmut_29(
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
                        return False

            return False

    def xǁRegistryǁremove__mutmut_30(
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

            return True
    
    xǁRegistryǁremove__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRegistryǁremove__mutmut_1': xǁRegistryǁremove__mutmut_1, 
        'xǁRegistryǁremove__mutmut_2': xǁRegistryǁremove__mutmut_2, 
        'xǁRegistryǁremove__mutmut_3': xǁRegistryǁremove__mutmut_3, 
        'xǁRegistryǁremove__mutmut_4': xǁRegistryǁremove__mutmut_4, 
        'xǁRegistryǁremove__mutmut_5': xǁRegistryǁremove__mutmut_5, 
        'xǁRegistryǁremove__mutmut_6': xǁRegistryǁremove__mutmut_6, 
        'xǁRegistryǁremove__mutmut_7': xǁRegistryǁremove__mutmut_7, 
        'xǁRegistryǁremove__mutmut_8': xǁRegistryǁremove__mutmut_8, 
        'xǁRegistryǁremove__mutmut_9': xǁRegistryǁremove__mutmut_9, 
        'xǁRegistryǁremove__mutmut_10': xǁRegistryǁremove__mutmut_10, 
        'xǁRegistryǁremove__mutmut_11': xǁRegistryǁremove__mutmut_11, 
        'xǁRegistryǁremove__mutmut_12': xǁRegistryǁremove__mutmut_12, 
        'xǁRegistryǁremove__mutmut_13': xǁRegistryǁremove__mutmut_13, 
        'xǁRegistryǁremove__mutmut_14': xǁRegistryǁremove__mutmut_14, 
        'xǁRegistryǁremove__mutmut_15': xǁRegistryǁremove__mutmut_15, 
        'xǁRegistryǁremove__mutmut_16': xǁRegistryǁremove__mutmut_16, 
        'xǁRegistryǁremove__mutmut_17': xǁRegistryǁremove__mutmut_17, 
        'xǁRegistryǁremove__mutmut_18': xǁRegistryǁremove__mutmut_18, 
        'xǁRegistryǁremove__mutmut_19': xǁRegistryǁremove__mutmut_19, 
        'xǁRegistryǁremove__mutmut_20': xǁRegistryǁremove__mutmut_20, 
        'xǁRegistryǁremove__mutmut_21': xǁRegistryǁremove__mutmut_21, 
        'xǁRegistryǁremove__mutmut_22': xǁRegistryǁremove__mutmut_22, 
        'xǁRegistryǁremove__mutmut_23': xǁRegistryǁremove__mutmut_23, 
        'xǁRegistryǁremove__mutmut_24': xǁRegistryǁremove__mutmut_24, 
        'xǁRegistryǁremove__mutmut_25': xǁRegistryǁremove__mutmut_25, 
        'xǁRegistryǁremove__mutmut_26': xǁRegistryǁremove__mutmut_26, 
        'xǁRegistryǁremove__mutmut_27': xǁRegistryǁremove__mutmut_27, 
        'xǁRegistryǁremove__mutmut_28': xǁRegistryǁremove__mutmut_28, 
        'xǁRegistryǁremove__mutmut_29': xǁRegistryǁremove__mutmut_29, 
        'xǁRegistryǁremove__mutmut_30': xǁRegistryǁremove__mutmut_30
    }
    
    def remove(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRegistryǁremove__mutmut_orig"), object.__getattribute__(self, "xǁRegistryǁremove__mutmut_mutants"), args, kwargs, self)
        return result 
    
    remove.__signature__ = _mutmut_signature(xǁRegistryǁremove__mutmut_orig)
    xǁRegistryǁremove__mutmut_orig.__name__ = 'xǁRegistryǁremove'

    def xǁRegistryǁclear__mutmut_orig(self, dimension: str | None = None) -> None:
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

    def xǁRegistryǁclear__mutmut_1(self, dimension: str | None = None) -> None:
        """Clear the registry or a specific dimension."""
        with self._lock:
            if dimension is None:
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

    def xǁRegistryǁclear__mutmut_2(self, dimension: str | None = None) -> None:
        """Clear the registry or a specific dimension."""
        with self._lock:
            if dimension is not None:
                # Dispose of resources before clearing
                self._dispose_resources(None)
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

    def xǁRegistryǁclear__mutmut_3(self, dimension: str | None = None) -> None:
        """Clear the registry or a specific dimension."""
        with self._lock:
            if dimension is not None:
                # Dispose of resources before clearing
                self._dispose_resources(dimension)
                self._registry[dimension].clear()

                aliases_to_remove = None
                for alias in aliases_to_remove:
                    del self._aliases[alias]
            else:
                # Dispose of all resources before clearing
                self._dispose_all_resources()
                self._registry.clear()
                self._aliases.clear()
                self._type_registry.clear()

    def xǁRegistryǁclear__mutmut_4(self, dimension: str | None = None) -> None:
        """Clear the registry or a specific dimension."""
        with self._lock:
            if dimension is not None:
                # Dispose of resources before clearing
                self._dispose_resources(dimension)
                self._registry[dimension].clear()

                aliases_to_remove = [alias for alias, (dim, _) in self._aliases.items() if dim != dimension]
                for alias in aliases_to_remove:
                    del self._aliases[alias]
            else:
                # Dispose of all resources before clearing
                self._dispose_all_resources()
                self._registry.clear()
                self._aliases.clear()
                self._type_registry.clear()
    
    xǁRegistryǁclear__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRegistryǁclear__mutmut_1': xǁRegistryǁclear__mutmut_1, 
        'xǁRegistryǁclear__mutmut_2': xǁRegistryǁclear__mutmut_2, 
        'xǁRegistryǁclear__mutmut_3': xǁRegistryǁclear__mutmut_3, 
        'xǁRegistryǁclear__mutmut_4': xǁRegistryǁclear__mutmut_4
    }
    
    def clear(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRegistryǁclear__mutmut_orig"), object.__getattribute__(self, "xǁRegistryǁclear__mutmut_mutants"), args, kwargs, self)
        return result 
    
    clear.__signature__ = _mutmut_signature(xǁRegistryǁclear__mutmut_orig)
    xǁRegistryǁclear__mutmut_orig.__name__ = 'xǁRegistryǁclear'

    # Type-based registration for dependency injection

    def xǁRegistryǁregister_type__mutmut_orig(
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

    # Type-based registration for dependency injection

    def xǁRegistryǁregister_type__mutmut_1(
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
            self._type_registry[type_hint] = None

            # Also register in standard registry for backward compatibility
            if name is not None:
                self.register(
                    name=name,
                    value=instance,
                    dimension="types",
                    metadata={"type": type_hint},
                    replace=True,
                )

    # Type-based registration for dependency injection

    def xǁRegistryǁregister_type__mutmut_2(
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
            if name is None:
                self.register(
                    name=name,
                    value=instance,
                    dimension="types",
                    metadata={"type": type_hint},
                    replace=True,
                )

    # Type-based registration for dependency injection

    def xǁRegistryǁregister_type__mutmut_3(
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
                    name=None,
                    value=instance,
                    dimension="types",
                    metadata={"type": type_hint},
                    replace=True,
                )

    # Type-based registration for dependency injection

    def xǁRegistryǁregister_type__mutmut_4(
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
                    value=None,
                    dimension="types",
                    metadata={"type": type_hint},
                    replace=True,
                )

    # Type-based registration for dependency injection

    def xǁRegistryǁregister_type__mutmut_5(
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
                    dimension=None,
                    metadata={"type": type_hint},
                    replace=True,
                )

    # Type-based registration for dependency injection

    def xǁRegistryǁregister_type__mutmut_6(
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
                    metadata=None,
                    replace=True,
                )

    # Type-based registration for dependency injection

    def xǁRegistryǁregister_type__mutmut_7(
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
                    replace=None,
                )

    # Type-based registration for dependency injection

    def xǁRegistryǁregister_type__mutmut_8(
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
                    value=instance,
                    dimension="types",
                    metadata={"type": type_hint},
                    replace=True,
                )

    # Type-based registration for dependency injection

    def xǁRegistryǁregister_type__mutmut_9(
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
                    dimension="types",
                    metadata={"type": type_hint},
                    replace=True,
                )

    # Type-based registration for dependency injection

    def xǁRegistryǁregister_type__mutmut_10(
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
                    metadata={"type": type_hint},
                    replace=True,
                )

    # Type-based registration for dependency injection

    def xǁRegistryǁregister_type__mutmut_11(
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
                    replace=True,
                )

    # Type-based registration for dependency injection

    def xǁRegistryǁregister_type__mutmut_12(
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
                    )

    # Type-based registration for dependency injection

    def xǁRegistryǁregister_type__mutmut_13(
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
                    dimension="XXtypesXX",
                    metadata={"type": type_hint},
                    replace=True,
                )

    # Type-based registration for dependency injection

    def xǁRegistryǁregister_type__mutmut_14(
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
                    dimension="TYPES",
                    metadata={"type": type_hint},
                    replace=True,
                )

    # Type-based registration for dependency injection

    def xǁRegistryǁregister_type__mutmut_15(
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
                    metadata={"XXtypeXX": type_hint},
                    replace=True,
                )

    # Type-based registration for dependency injection

    def xǁRegistryǁregister_type__mutmut_16(
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
                    metadata={"TYPE": type_hint},
                    replace=True,
                )

    # Type-based registration for dependency injection

    def xǁRegistryǁregister_type__mutmut_17(
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
                    replace=False,
                )
    
    xǁRegistryǁregister_type__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRegistryǁregister_type__mutmut_1': xǁRegistryǁregister_type__mutmut_1, 
        'xǁRegistryǁregister_type__mutmut_2': xǁRegistryǁregister_type__mutmut_2, 
        'xǁRegistryǁregister_type__mutmut_3': xǁRegistryǁregister_type__mutmut_3, 
        'xǁRegistryǁregister_type__mutmut_4': xǁRegistryǁregister_type__mutmut_4, 
        'xǁRegistryǁregister_type__mutmut_5': xǁRegistryǁregister_type__mutmut_5, 
        'xǁRegistryǁregister_type__mutmut_6': xǁRegistryǁregister_type__mutmut_6, 
        'xǁRegistryǁregister_type__mutmut_7': xǁRegistryǁregister_type__mutmut_7, 
        'xǁRegistryǁregister_type__mutmut_8': xǁRegistryǁregister_type__mutmut_8, 
        'xǁRegistryǁregister_type__mutmut_9': xǁRegistryǁregister_type__mutmut_9, 
        'xǁRegistryǁregister_type__mutmut_10': xǁRegistryǁregister_type__mutmut_10, 
        'xǁRegistryǁregister_type__mutmut_11': xǁRegistryǁregister_type__mutmut_11, 
        'xǁRegistryǁregister_type__mutmut_12': xǁRegistryǁregister_type__mutmut_12, 
        'xǁRegistryǁregister_type__mutmut_13': xǁRegistryǁregister_type__mutmut_13, 
        'xǁRegistryǁregister_type__mutmut_14': xǁRegistryǁregister_type__mutmut_14, 
        'xǁRegistryǁregister_type__mutmut_15': xǁRegistryǁregister_type__mutmut_15, 
        'xǁRegistryǁregister_type__mutmut_16': xǁRegistryǁregister_type__mutmut_16, 
        'xǁRegistryǁregister_type__mutmut_17': xǁRegistryǁregister_type__mutmut_17
    }
    
    def register_type(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRegistryǁregister_type__mutmut_orig"), object.__getattribute__(self, "xǁRegistryǁregister_type__mutmut_mutants"), args, kwargs, self)
        return result 
    
    register_type.__signature__ = _mutmut_signature(xǁRegistryǁregister_type__mutmut_orig)
    xǁRegistryǁregister_type__mutmut_orig.__name__ = 'xǁRegistryǁregister_type'

    def xǁRegistryǁget_by_type__mutmut_orig(self, type_hint: type[Any]) -> Any | None:
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

    def xǁRegistryǁget_by_type__mutmut_1(self, type_hint: type[Any]) -> Any | None:
        """Get a registered instance by its type.

        Args:
            type_hint: Type to look up

        Returns:
            Registered instance or None if not found

        Example:
            >>> db = registry.get_by_type(DatabaseClient)
        """
        with self._lock:
            return self._type_registry.get(None)
    
    xǁRegistryǁget_by_type__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRegistryǁget_by_type__mutmut_1': xǁRegistryǁget_by_type__mutmut_1
    }
    
    def get_by_type(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRegistryǁget_by_type__mutmut_orig"), object.__getattribute__(self, "xǁRegistryǁget_by_type__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_by_type.__signature__ = _mutmut_signature(xǁRegistryǁget_by_type__mutmut_orig)
    xǁRegistryǁget_by_type__mutmut_orig.__name__ = 'xǁRegistryǁget_by_type'

    def xǁRegistryǁlist_types__mutmut_orig(self) -> list[type[Any]]:
        """List all registered types.

        Returns:
            List of registered types
        """
        with self._lock:
            return list(self._type_registry.keys())

    def xǁRegistryǁlist_types__mutmut_1(self) -> list[type[Any]]:
        """List all registered types.

        Returns:
            List of registered types
        """
        with self._lock:
            return list(None)
    
    xǁRegistryǁlist_types__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRegistryǁlist_types__mutmut_1': xǁRegistryǁlist_types__mutmut_1
    }
    
    def list_types(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRegistryǁlist_types__mutmut_orig"), object.__getattribute__(self, "xǁRegistryǁlist_types__mutmut_mutants"), args, kwargs, self)
        return result 
    
    list_types.__signature__ = _mutmut_signature(xǁRegistryǁlist_types__mutmut_orig)
    xǁRegistryǁlist_types__mutmut_orig.__name__ = 'xǁRegistryǁlist_types'

    def dispose_all(self) -> None:
        """Dispose of all registered resources properly."""
        with self._lock:
            self._dispose_all_resources()

    def xǁRegistryǁ_dispose_all_resources__mutmut_orig(self) -> None:
        """Dispose of all resources across all dimensions."""
        for dimension in self._registry:
            self._dispose_resources(dimension)

    def xǁRegistryǁ_dispose_all_resources__mutmut_1(self) -> None:
        """Dispose of all resources across all dimensions."""
        for dimension in self._registry:
            self._dispose_resources(None)
    
    xǁRegistryǁ_dispose_all_resources__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRegistryǁ_dispose_all_resources__mutmut_1': xǁRegistryǁ_dispose_all_resources__mutmut_1
    }
    
    def _dispose_all_resources(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRegistryǁ_dispose_all_resources__mutmut_orig"), object.__getattribute__(self, "xǁRegistryǁ_dispose_all_resources__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _dispose_all_resources.__signature__ = _mutmut_signature(xǁRegistryǁ_dispose_all_resources__mutmut_orig)
    xǁRegistryǁ_dispose_all_resources__mutmut_orig.__name__ = 'xǁRegistryǁ_dispose_all_resources'

    def xǁRegistryǁ_dispose_resources__mutmut_orig(self, dimension: str) -> None:
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

    def xǁRegistryǁ_dispose_resources__mutmut_1(self, dimension: str) -> None:
        """Dispose of resources in a specific dimension."""
        from provide.foundation.hub.protocols import AsyncDisposable, Disposable

        for entry in self._registry[dimension].values():
            value = None
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

    def xǁRegistryǁ_dispose_resources__mutmut_2(self, dimension: str) -> None:
        """Dispose of resources in a specific dimension."""
        from provide.foundation.hub.protocols import AsyncDisposable, Disposable

        for entry in self._registry[dimension].values():
            value = entry.value
            if isinstance(value, Disposable):
                import contextlib

                with contextlib.suppress(None):
                    # Continue disposing other resources even if one fails
                    value.dispose()
            elif isinstance(value, AsyncDisposable):
                # For async disposables in sync context, we can't await
                # They should be disposed in async context managers
                # Log a warning that proper async disposal is needed
                pass
    
    xǁRegistryǁ_dispose_resources__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRegistryǁ_dispose_resources__mutmut_1': xǁRegistryǁ_dispose_resources__mutmut_1, 
        'xǁRegistryǁ_dispose_resources__mutmut_2': xǁRegistryǁ_dispose_resources__mutmut_2
    }
    
    def _dispose_resources(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRegistryǁ_dispose_resources__mutmut_orig"), object.__getattribute__(self, "xǁRegistryǁ_dispose_resources__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _dispose_resources.__signature__ = _mutmut_signature(xǁRegistryǁ_dispose_resources__mutmut_orig)
    xǁRegistryǁ_dispose_resources__mutmut_orig.__name__ = 'xǁRegistryǁ_dispose_resources'

    def xǁRegistryǁ__contains____mutmut_orig(self, key: str | tuple[str, str]) -> bool:
        """Check if an item exists in the registry."""
        with self._lock:
            if isinstance(key, tuple):
                dimension, name = key
                return name in self._registry[dimension]
            return any(key in dim_reg for dim_reg in self._registry.values())

    def xǁRegistryǁ__contains____mutmut_1(self, key: str | tuple[str, str]) -> bool:
        """Check if an item exists in the registry."""
        with self._lock:
            if isinstance(key, tuple):
                dimension, name = None
                return name in self._registry[dimension]
            return any(key in dim_reg for dim_reg in self._registry.values())

    def xǁRegistryǁ__contains____mutmut_2(self, key: str | tuple[str, str]) -> bool:
        """Check if an item exists in the registry."""
        with self._lock:
            if isinstance(key, tuple):
                dimension, name = key
                return name not in self._registry[dimension]
            return any(key in dim_reg for dim_reg in self._registry.values())

    def xǁRegistryǁ__contains____mutmut_3(self, key: str | tuple[str, str]) -> bool:
        """Check if an item exists in the registry."""
        with self._lock:
            if isinstance(key, tuple):
                dimension, name = key
                return name in self._registry[dimension]
            return any(None)

    def xǁRegistryǁ__contains____mutmut_4(self, key: str | tuple[str, str]) -> bool:
        """Check if an item exists in the registry."""
        with self._lock:
            if isinstance(key, tuple):
                dimension, name = key
                return name in self._registry[dimension]
            return any(key not in dim_reg for dim_reg in self._registry.values())
    
    xǁRegistryǁ__contains____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRegistryǁ__contains____mutmut_1': xǁRegistryǁ__contains____mutmut_1, 
        'xǁRegistryǁ__contains____mutmut_2': xǁRegistryǁ__contains____mutmut_2, 
        'xǁRegistryǁ__contains____mutmut_3': xǁRegistryǁ__contains____mutmut_3, 
        'xǁRegistryǁ__contains____mutmut_4': xǁRegistryǁ__contains____mutmut_4
    }
    
    def __contains__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRegistryǁ__contains____mutmut_orig"), object.__getattribute__(self, "xǁRegistryǁ__contains____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __contains__.__signature__ = _mutmut_signature(xǁRegistryǁ__contains____mutmut_orig)
    xǁRegistryǁ__contains____mutmut_orig.__name__ = 'xǁRegistryǁ__contains__'

    def xǁRegistryǁ__iter____mutmut_orig(self) -> Iterator[RegistryEntry]:
        """Iterate over all registry entries."""
        with self._lock:
            # Create a snapshot to avoid holding lock during iteration
            entries: list[RegistryEntry] = []
            for dim_registry in self._registry.values():
                entries.extend(dim_registry.values())
        # Yield outside the lock
        yield from entries

    def xǁRegistryǁ__iter____mutmut_1(self) -> Iterator[RegistryEntry]:
        """Iterate over all registry entries."""
        with self._lock:
            # Create a snapshot to avoid holding lock during iteration
            entries: list[RegistryEntry] = None
            for dim_registry in self._registry.values():
                entries.extend(dim_registry.values())
        # Yield outside the lock
        yield from entries

    def xǁRegistryǁ__iter____mutmut_2(self) -> Iterator[RegistryEntry]:
        """Iterate over all registry entries."""
        with self._lock:
            # Create a snapshot to avoid holding lock during iteration
            entries: list[RegistryEntry] = []
            for dim_registry in self._registry.values():
                entries.extend(None)
        # Yield outside the lock
        yield from entries
    
    xǁRegistryǁ__iter____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRegistryǁ__iter____mutmut_1': xǁRegistryǁ__iter____mutmut_1, 
        'xǁRegistryǁ__iter____mutmut_2': xǁRegistryǁ__iter____mutmut_2
    }
    
    def __iter__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRegistryǁ__iter____mutmut_orig"), object.__getattribute__(self, "xǁRegistryǁ__iter____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __iter__.__signature__ = _mutmut_signature(xǁRegistryǁ__iter____mutmut_orig)
    xǁRegistryǁ__iter____mutmut_orig.__name__ = 'xǁRegistryǁ__iter__'

    def xǁRegistryǁ__len____mutmut_orig(self) -> int:
        """Get total number of registered items."""
        with self._lock:
            return sum(len(dim_reg) for dim_reg in self._registry.values())

    def xǁRegistryǁ__len____mutmut_1(self) -> int:
        """Get total number of registered items."""
        with self._lock:
            return sum(None)
    
    xǁRegistryǁ__len____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRegistryǁ__len____mutmut_1': xǁRegistryǁ__len____mutmut_1
    }
    
    def __len__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRegistryǁ__len____mutmut_orig"), object.__getattribute__(self, "xǁRegistryǁ__len____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __len__.__signature__ = _mutmut_signature(xǁRegistryǁ__len____mutmut_orig)
    xǁRegistryǁ__len____mutmut_orig.__name__ = 'xǁRegistryǁ__len__'


# Global registry for commands
_command_registry = Registry()


def get_command_registry() -> Registry:
    """Get the global command registry."""
    return _command_registry


__all__ = ["Registry", "RegistryEntry", "get_command_registry"]


# <3 🧱🤝🌐🪄
