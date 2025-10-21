# provide/foundation/hub/container.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any, TypeVar

from provide.foundation.hub.manager import Hub
from provide.foundation.hub.registry import Registry

"""DI Container - A focused wrapper for dependency injection patterns.

This module provides a Container class that wraps the Hub with a cleaner
API specifically designed for dependency injection workflows. This is ideal
for users who prefer pure DI patterns over Service Locator.

Example:
    >>> from provide.foundation.hub import Container, injectable
    >>>
    >>> @injectable
    >>> class MyService:
    ...     def __init__(self, db: Database, logger: Logger):
    ...         self.db = db
    ...         self.logger = logger
    >>>
    >>> # Composition Root (main.py)
    >>> container = Container()
    >>> container.register(Database, db_instance)
    >>> container.register(Logger, logger_instance)
    >>> service = container.resolve(MyService)
"""

T = TypeVar("T")
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


class Container:
    """Dependency Injection Container.

    A focused API for dependency injection patterns, wrapping the Hub
    with a simpler interface for type-based registration and resolution.

    This container follows the Composition Root pattern where all
    dependencies are registered at application startup and then resolved
    as needed.

    Example:
        >>> container = Container()
        >>> container.register(DatabaseClient, db_instance)
        >>> container.register(HTTPClient, http_instance)
        >>>
        >>> # Resolve with automatic dependency injection
        >>> service = container.resolve(MyService)
        >>> # MyService.__init__(db, http) called automatically

    Pattern:
        The Container is designed for the Composition Root pattern:
        1. Create container at app startup (main.py)
        2. Register all core dependencies
        3. Resolve application entry points
        4. Pass dependencies explicitly (no global access)

    This matches the idiomatic patterns in Go and Rust, making it
    easier to adopt for developers from those ecosystems.
    """

    def xǁContainerǁ__init____mutmut_orig(self, hub: Hub | None = None, registry: Registry | None = None) -> None:
        """Initialize the DI container.

        Args:
            hub: Optional Hub instance (creates new if not provided)
            registry: Optional Registry instance (creates new if not provided)
        """
        if hub is not None:
            self._hub = hub
        elif registry is not None:
            # Create a Hub with the provided registry
            from provide.foundation.context import CLIContext

            self._hub = Hub(context=CLIContext(), component_registry=registry)
        else:
            # Create a new isolated Hub
            from provide.foundation.context import CLIContext

            self._hub = Hub(context=CLIContext())

    def xǁContainerǁ__init____mutmut_1(self, hub: Hub | None = None, registry: Registry | None = None) -> None:
        """Initialize the DI container.

        Args:
            hub: Optional Hub instance (creates new if not provided)
            registry: Optional Registry instance (creates new if not provided)
        """
        if hub is None:
            self._hub = hub
        elif registry is not None:
            # Create a Hub with the provided registry
            from provide.foundation.context import CLIContext

            self._hub = Hub(context=CLIContext(), component_registry=registry)
        else:
            # Create a new isolated Hub
            from provide.foundation.context import CLIContext

            self._hub = Hub(context=CLIContext())

    def xǁContainerǁ__init____mutmut_2(self, hub: Hub | None = None, registry: Registry | None = None) -> None:
        """Initialize the DI container.

        Args:
            hub: Optional Hub instance (creates new if not provided)
            registry: Optional Registry instance (creates new if not provided)
        """
        if hub is not None:
            self._hub = None
        elif registry is not None:
            # Create a Hub with the provided registry
            from provide.foundation.context import CLIContext

            self._hub = Hub(context=CLIContext(), component_registry=registry)
        else:
            # Create a new isolated Hub
            from provide.foundation.context import CLIContext

            self._hub = Hub(context=CLIContext())

    def xǁContainerǁ__init____mutmut_3(self, hub: Hub | None = None, registry: Registry | None = None) -> None:
        """Initialize the DI container.

        Args:
            hub: Optional Hub instance (creates new if not provided)
            registry: Optional Registry instance (creates new if not provided)
        """
        if hub is not None:
            self._hub = hub
        elif registry is None:
            # Create a Hub with the provided registry
            from provide.foundation.context import CLIContext

            self._hub = Hub(context=CLIContext(), component_registry=registry)
        else:
            # Create a new isolated Hub
            from provide.foundation.context import CLIContext

            self._hub = Hub(context=CLIContext())

    def xǁContainerǁ__init____mutmut_4(self, hub: Hub | None = None, registry: Registry | None = None) -> None:
        """Initialize the DI container.

        Args:
            hub: Optional Hub instance (creates new if not provided)
            registry: Optional Registry instance (creates new if not provided)
        """
        if hub is not None:
            self._hub = hub
        elif registry is not None:
            # Create a Hub with the provided registry
            from provide.foundation.context import CLIContext

            self._hub = None
        else:
            # Create a new isolated Hub
            from provide.foundation.context import CLIContext

            self._hub = Hub(context=CLIContext())

    def xǁContainerǁ__init____mutmut_5(self, hub: Hub | None = None, registry: Registry | None = None) -> None:
        """Initialize the DI container.

        Args:
            hub: Optional Hub instance (creates new if not provided)
            registry: Optional Registry instance (creates new if not provided)
        """
        if hub is not None:
            self._hub = hub
        elif registry is not None:
            # Create a Hub with the provided registry
            from provide.foundation.context import CLIContext

            self._hub = Hub(context=None, component_registry=registry)
        else:
            # Create a new isolated Hub
            from provide.foundation.context import CLIContext

            self._hub = Hub(context=CLIContext())

    def xǁContainerǁ__init____mutmut_6(self, hub: Hub | None = None, registry: Registry | None = None) -> None:
        """Initialize the DI container.

        Args:
            hub: Optional Hub instance (creates new if not provided)
            registry: Optional Registry instance (creates new if not provided)
        """
        if hub is not None:
            self._hub = hub
        elif registry is not None:
            # Create a Hub with the provided registry
            from provide.foundation.context import CLIContext

            self._hub = Hub(context=CLIContext(), component_registry=None)
        else:
            # Create a new isolated Hub
            from provide.foundation.context import CLIContext

            self._hub = Hub(context=CLIContext())

    def xǁContainerǁ__init____mutmut_7(self, hub: Hub | None = None, registry: Registry | None = None) -> None:
        """Initialize the DI container.

        Args:
            hub: Optional Hub instance (creates new if not provided)
            registry: Optional Registry instance (creates new if not provided)
        """
        if hub is not None:
            self._hub = hub
        elif registry is not None:
            # Create a Hub with the provided registry
            from provide.foundation.context import CLIContext

            self._hub = Hub(component_registry=registry)
        else:
            # Create a new isolated Hub
            from provide.foundation.context import CLIContext

            self._hub = Hub(context=CLIContext())

    def xǁContainerǁ__init____mutmut_8(self, hub: Hub | None = None, registry: Registry | None = None) -> None:
        """Initialize the DI container.

        Args:
            hub: Optional Hub instance (creates new if not provided)
            registry: Optional Registry instance (creates new if not provided)
        """
        if hub is not None:
            self._hub = hub
        elif registry is not None:
            # Create a Hub with the provided registry
            from provide.foundation.context import CLIContext

            self._hub = Hub(context=CLIContext(), )
        else:
            # Create a new isolated Hub
            from provide.foundation.context import CLIContext

            self._hub = Hub(context=CLIContext())

    def xǁContainerǁ__init____mutmut_9(self, hub: Hub | None = None, registry: Registry | None = None) -> None:
        """Initialize the DI container.

        Args:
            hub: Optional Hub instance (creates new if not provided)
            registry: Optional Registry instance (creates new if not provided)
        """
        if hub is not None:
            self._hub = hub
        elif registry is not None:
            # Create a Hub with the provided registry
            from provide.foundation.context import CLIContext

            self._hub = Hub(context=CLIContext(), component_registry=registry)
        else:
            # Create a new isolated Hub
            from provide.foundation.context import CLIContext

            self._hub = None

    def xǁContainerǁ__init____mutmut_10(self, hub: Hub | None = None, registry: Registry | None = None) -> None:
        """Initialize the DI container.

        Args:
            hub: Optional Hub instance (creates new if not provided)
            registry: Optional Registry instance (creates new if not provided)
        """
        if hub is not None:
            self._hub = hub
        elif registry is not None:
            # Create a Hub with the provided registry
            from provide.foundation.context import CLIContext

            self._hub = Hub(context=CLIContext(), component_registry=registry)
        else:
            # Create a new isolated Hub
            from provide.foundation.context import CLIContext

            self._hub = Hub(context=None)
    
    xǁContainerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContainerǁ__init____mutmut_1': xǁContainerǁ__init____mutmut_1, 
        'xǁContainerǁ__init____mutmut_2': xǁContainerǁ__init____mutmut_2, 
        'xǁContainerǁ__init____mutmut_3': xǁContainerǁ__init____mutmut_3, 
        'xǁContainerǁ__init____mutmut_4': xǁContainerǁ__init____mutmut_4, 
        'xǁContainerǁ__init____mutmut_5': xǁContainerǁ__init____mutmut_5, 
        'xǁContainerǁ__init____mutmut_6': xǁContainerǁ__init____mutmut_6, 
        'xǁContainerǁ__init____mutmut_7': xǁContainerǁ__init____mutmut_7, 
        'xǁContainerǁ__init____mutmut_8': xǁContainerǁ__init____mutmut_8, 
        'xǁContainerǁ__init____mutmut_9': xǁContainerǁ__init____mutmut_9, 
        'xǁContainerǁ__init____mutmut_10': xǁContainerǁ__init____mutmut_10
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContainerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁContainerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁContainerǁ__init____mutmut_orig)
    xǁContainerǁ__init____mutmut_orig.__name__ = 'xǁContainerǁ__init__'

    def xǁContainerǁregister__mutmut_orig(
        self,
        type_hint: type[T],
        instance: T,
        name: str | None = None,
    ) -> Container:
        """Register a dependency by type.

        Args:
            type_hint: Type to register under
            instance: Instance to register
            name: Optional name for named registration

        Returns:
            Self for method chaining

        Example:
            >>> container.register(Database, db).register(Cache, cache)
        """
        self._hub.register(type_hint, instance, name)
        return self

    def xǁContainerǁregister__mutmut_1(
        self,
        type_hint: type[T],
        instance: T,
        name: str | None = None,
    ) -> Container:
        """Register a dependency by type.

        Args:
            type_hint: Type to register under
            instance: Instance to register
            name: Optional name for named registration

        Returns:
            Self for method chaining

        Example:
            >>> container.register(Database, db).register(Cache, cache)
        """
        self._hub.register(None, instance, name)
        return self

    def xǁContainerǁregister__mutmut_2(
        self,
        type_hint: type[T],
        instance: T,
        name: str | None = None,
    ) -> Container:
        """Register a dependency by type.

        Args:
            type_hint: Type to register under
            instance: Instance to register
            name: Optional name for named registration

        Returns:
            Self for method chaining

        Example:
            >>> container.register(Database, db).register(Cache, cache)
        """
        self._hub.register(type_hint, None, name)
        return self

    def xǁContainerǁregister__mutmut_3(
        self,
        type_hint: type[T],
        instance: T,
        name: str | None = None,
    ) -> Container:
        """Register a dependency by type.

        Args:
            type_hint: Type to register under
            instance: Instance to register
            name: Optional name for named registration

        Returns:
            Self for method chaining

        Example:
            >>> container.register(Database, db).register(Cache, cache)
        """
        self._hub.register(type_hint, instance, None)
        return self

    def xǁContainerǁregister__mutmut_4(
        self,
        type_hint: type[T],
        instance: T,
        name: str | None = None,
    ) -> Container:
        """Register a dependency by type.

        Args:
            type_hint: Type to register under
            instance: Instance to register
            name: Optional name for named registration

        Returns:
            Self for method chaining

        Example:
            >>> container.register(Database, db).register(Cache, cache)
        """
        self._hub.register(instance, name)
        return self

    def xǁContainerǁregister__mutmut_5(
        self,
        type_hint: type[T],
        instance: T,
        name: str | None = None,
    ) -> Container:
        """Register a dependency by type.

        Args:
            type_hint: Type to register under
            instance: Instance to register
            name: Optional name for named registration

        Returns:
            Self for method chaining

        Example:
            >>> container.register(Database, db).register(Cache, cache)
        """
        self._hub.register(type_hint, name)
        return self

    def xǁContainerǁregister__mutmut_6(
        self,
        type_hint: type[T],
        instance: T,
        name: str | None = None,
    ) -> Container:
        """Register a dependency by type.

        Args:
            type_hint: Type to register under
            instance: Instance to register
            name: Optional name for named registration

        Returns:
            Self for method chaining

        Example:
            >>> container.register(Database, db).register(Cache, cache)
        """
        self._hub.register(type_hint, instance, )
        return self
    
    xǁContainerǁregister__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContainerǁregister__mutmut_1': xǁContainerǁregister__mutmut_1, 
        'xǁContainerǁregister__mutmut_2': xǁContainerǁregister__mutmut_2, 
        'xǁContainerǁregister__mutmut_3': xǁContainerǁregister__mutmut_3, 
        'xǁContainerǁregister__mutmut_4': xǁContainerǁregister__mutmut_4, 
        'xǁContainerǁregister__mutmut_5': xǁContainerǁregister__mutmut_5, 
        'xǁContainerǁregister__mutmut_6': xǁContainerǁregister__mutmut_6
    }
    
    def register(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContainerǁregister__mutmut_orig"), object.__getattribute__(self, "xǁContainerǁregister__mutmut_mutants"), args, kwargs, self)
        return result 
    
    register.__signature__ = _mutmut_signature(xǁContainerǁregister__mutmut_orig)
    xǁContainerǁregister__mutmut_orig.__name__ = 'xǁContainerǁregister'

    def xǁContainerǁresolve__mutmut_orig(
        self,
        cls: type[T],
        **overrides: Any,
    ) -> T:
        """Resolve a class with dependency injection.

        Args:
            cls: Class to instantiate
            **overrides: Explicitly provided dependencies

        Returns:
            New instance with dependencies injected

        Example:
            >>> service = container.resolve(MyService)
            >>> # Or with overrides:
            >>> service = container.resolve(MyService, logger=custom_logger)
        """
        return self._hub.resolve(cls, **overrides)

    def xǁContainerǁresolve__mutmut_1(
        self,
        cls: type[T],
        **overrides: Any,
    ) -> T:
        """Resolve a class with dependency injection.

        Args:
            cls: Class to instantiate
            **overrides: Explicitly provided dependencies

        Returns:
            New instance with dependencies injected

        Example:
            >>> service = container.resolve(MyService)
            >>> # Or with overrides:
            >>> service = container.resolve(MyService, logger=custom_logger)
        """
        return self._hub.resolve(None, **overrides)

    def xǁContainerǁresolve__mutmut_2(
        self,
        cls: type[T],
        **overrides: Any,
    ) -> T:
        """Resolve a class with dependency injection.

        Args:
            cls: Class to instantiate
            **overrides: Explicitly provided dependencies

        Returns:
            New instance with dependencies injected

        Example:
            >>> service = container.resolve(MyService)
            >>> # Or with overrides:
            >>> service = container.resolve(MyService, logger=custom_logger)
        """
        return self._hub.resolve(**overrides)

    def xǁContainerǁresolve__mutmut_3(
        self,
        cls: type[T],
        **overrides: Any,
    ) -> T:
        """Resolve a class with dependency injection.

        Args:
            cls: Class to instantiate
            **overrides: Explicitly provided dependencies

        Returns:
            New instance with dependencies injected

        Example:
            >>> service = container.resolve(MyService)
            >>> # Or with overrides:
            >>> service = container.resolve(MyService, logger=custom_logger)
        """
        return self._hub.resolve(cls, )
    
    xǁContainerǁresolve__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContainerǁresolve__mutmut_1': xǁContainerǁresolve__mutmut_1, 
        'xǁContainerǁresolve__mutmut_2': xǁContainerǁresolve__mutmut_2, 
        'xǁContainerǁresolve__mutmut_3': xǁContainerǁresolve__mutmut_3
    }
    
    def resolve(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContainerǁresolve__mutmut_orig"), object.__getattribute__(self, "xǁContainerǁresolve__mutmut_mutants"), args, kwargs, self)
        return result 
    
    resolve.__signature__ = _mutmut_signature(xǁContainerǁresolve__mutmut_orig)
    xǁContainerǁresolve__mutmut_orig.__name__ = 'xǁContainerǁresolve'

    def xǁContainerǁget__mutmut_orig(self, type_hint: type[T]) -> T | None:
        """Get a registered instance by type.

        Args:
            type_hint: Type to retrieve

        Returns:
            Registered instance or None if not found

        Example:
            >>> db = container.get(Database)
        """
        # Access the component registry directly
        return self._hub._component_registry.get_by_type(type_hint)

    def xǁContainerǁget__mutmut_1(self, type_hint: type[T]) -> T | None:
        """Get a registered instance by type.

        Args:
            type_hint: Type to retrieve

        Returns:
            Registered instance or None if not found

        Example:
            >>> db = container.get(Database)
        """
        # Access the component registry directly
        return self._hub._component_registry.get_by_type(None)
    
    xǁContainerǁget__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContainerǁget__mutmut_1': xǁContainerǁget__mutmut_1
    }
    
    def get(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContainerǁget__mutmut_orig"), object.__getattribute__(self, "xǁContainerǁget__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get.__signature__ = _mutmut_signature(xǁContainerǁget__mutmut_orig)
    xǁContainerǁget__mutmut_orig.__name__ = 'xǁContainerǁget'

    def xǁContainerǁhas__mutmut_orig(self, type_hint: type[Any]) -> bool:
        """Check if a type is registered.

        Args:
            type_hint: Type to check

        Returns:
            True if type is registered

        Example:
            >>> if container.has(Database):
            ...     db = container.get(Database)
        """
        return self.get(type_hint) is not None

    def xǁContainerǁhas__mutmut_1(self, type_hint: type[Any]) -> bool:
        """Check if a type is registered.

        Args:
            type_hint: Type to check

        Returns:
            True if type is registered

        Example:
            >>> if container.has(Database):
            ...     db = container.get(Database)
        """
        return self.get(None) is not None

    def xǁContainerǁhas__mutmut_2(self, type_hint: type[Any]) -> bool:
        """Check if a type is registered.

        Args:
            type_hint: Type to check

        Returns:
            True if type is registered

        Example:
            >>> if container.has(Database):
            ...     db = container.get(Database)
        """
        return self.get(type_hint) is None
    
    xǁContainerǁhas__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContainerǁhas__mutmut_1': xǁContainerǁhas__mutmut_1, 
        'xǁContainerǁhas__mutmut_2': xǁContainerǁhas__mutmut_2
    }
    
    def has(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContainerǁhas__mutmut_orig"), object.__getattribute__(self, "xǁContainerǁhas__mutmut_mutants"), args, kwargs, self)
        return result 
    
    has.__signature__ = _mutmut_signature(xǁContainerǁhas__mutmut_orig)
    xǁContainerǁhas__mutmut_orig.__name__ = 'xǁContainerǁhas'

    def clear(self) -> None:
        """Clear all registered dependencies.

        Warning:
            This clears the underlying Hub registry. Use with caution.
        """
        self._hub.clear()

    def __enter__(self) -> Container:
        """Context manager entry.

        Example:
            >>> with Container() as container:
            ...     container.register(Database, db)
            ...     service = container.resolve(MyService)
        """
        return self

    def __exit__(self, *args: object) -> None:
        """Context manager exit."""
        # Cleanup is handled by the Hub
        pass


def create_container() -> Container:
    """Create a new DI container.

    Convenience function for creating containers.

    Returns:
        New Container instance

    Example:
        >>> container = create_container()
        >>> container.register(Database, db_instance)
    """
    return Container()


__all__ = [
    "Container",
    "create_container",
]


# <3 🧱🤝🌐🪄
