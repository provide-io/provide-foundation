#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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

    def __init__(self, hub: Hub | None = None, registry: Registry | None = None) -> None:
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

    def register(
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

    def resolve(
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

    def get(self, type_hint: type[T]) -> T | None:
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

    def has(self, type_hint: type[Any]) -> bool:
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

# 🧱🏗️🔚
