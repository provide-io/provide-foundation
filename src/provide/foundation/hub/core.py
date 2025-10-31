#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    import click

from provide.foundation.context import CLIContext
from provide.foundation.errors.config import ValidationError
from provide.foundation.errors.decorators import resilient
from provide.foundation.errors.resources import AlreadyExistsError
from provide.foundation.hub.categories import ComponentCategory
from provide.foundation.hub.commands import CommandInfo
from provide.foundation.hub.components import ComponentInfo
from provide.foundation.hub.registry import Registry, get_command_registry

T = TypeVar("T")

"""Core Hub class for component and command management.

This module provides the core Hub functionality for registering and
managing components and commands, without Foundation-specific features.
"""

# Lazy import to avoid circular dependency
_click_module: Any = None
_HAS_CLICK: bool | None = None


def _get_click() -> tuple[Any, bool]:
    """Get click module and availability flag."""
    global _click_module, _HAS_CLICK
    if _HAS_CLICK is None:
        from provide.foundation.cli.deps import _HAS_CLICK as has_click, click

        _click_module = click
        _HAS_CLICK = has_click
    return _click_module, _HAS_CLICK


class CoreHub:
    """Core hub for managing components and commands.

    The CoreHub provides basic functionality for:
    - Registering components and commands
    - Managing component lifecycle
    - Creating Click CLI applications

    Does not include Foundation-specific initialization.
    """

    def __init__(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
    ) -> None:
        """Initialize the core hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
        """
        self.context = context or CLIContext()
        self._component_registry = component_registry or Registry()
        self._command_registry = command_registry or get_command_registry()
        self._cli_group: click.Group | None = None

    # Component Management

    @resilient(
        context_provider=lambda: {"hub": "add_component"},
        error_mapper=lambda e: ValidationError(
            f"Failed to add component: {e}",
            code="HUB_COMPONENT_ADD_ERROR",
            cause=e,
        )
        if not isinstance(e, AlreadyExistsError | ValidationError)
        else e,
    )
    def add_component(
        self,
        component_class: type[Any],
        name: str | None = None,
        dimension: str = ComponentCategory.COMPONENT.value,
        **metadata: Any,
    ) -> ComponentInfo:
        """Add a component to the hub.

        Args:
            component_class: Component class to register
            name: Optional name (defaults to class name)
            dimension: Registry dimension
            **metadata: Additional metadata

        Returns:
            ComponentInfo for the registered component

        Raises:
            AlreadyExistsError: If component is already registered
            ValidationError: If component class is invalid

        """
        if not isinstance(component_class, type):
            raise ValidationError(
                f"Component must be a class, got {type(component_class).__name__}",
                code="HUB_INVALID_COMPONENT",
                component_type=type(component_class).__name__,
            )

        component_name = name or component_class.__name__

        # Check if already exists
        if self._component_registry.get_entry(component_name, dimension=dimension):
            raise AlreadyExistsError(
                f"Component '{component_name}' already registered in dimension '{dimension}'",
                code="HUB_COMPONENT_EXISTS",
                component_name=component_name,
                dimension=dimension,
            )

        info = ComponentInfo(
            name=component_name,
            component_class=component_class,
            dimension=dimension,
            version=metadata.get("version"),
            description=metadata.get("description", component_class.__doc__),
            author=metadata.get("author"),
            tags=metadata.get("tags", []),
            metadata=metadata,
        )

        self._component_registry.register(
            name=component_name,
            value=component_class,
            dimension=dimension,
            metadata={"info": info, **metadata},
            replace=False,  # Don't allow replacement by default
        )

        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().info(
            "Added component to hub",
            name=component_name,
            dimension=dimension,
        )

        return info

    def get_component(
        self,
        name: str,
        dimension: str | None = None,
    ) -> type[Any] | None:
        """Get a component by name.

        Args:
            name: Component name
            dimension: Optional dimension filter

        Returns:
            Component class or None

        """
        return self._component_registry.get(name, dimension)

    def list_components(
        self,
        dimension: str | None = None,
    ) -> list[str]:
        """List component names.

        Args:
            dimension: Optional dimension filter

        Returns:
            List of component names

        """
        if dimension:
            return self._component_registry.list_dimension(dimension)

        # List all non-command dimensions
        all_items = self._component_registry.list_all()
        components = []
        for dim, names in all_items.items():
            if dim != ComponentCategory.COMMAND.value:
                components.extend(names)
        return components

    def discover_components(
        self,
        group: str,
        dimension: str = ComponentCategory.COMPONENT.value,
    ) -> dict[str, type[Any]]:
        """Discover and register components from entry points.

        Args:
            group: Entry point group name
            dimension: Dimension to register under

        Returns:
            Dictionary of discovered components

        """
        from provide.foundation.hub.components import discover_components as _discover_components

        return _discover_components(group, dimension, self._component_registry)

    # Command Management

    def add_command(
        self,
        func: Callable[..., Any] | click.Command,
        name: str | None = None,
        **kwargs: Any,
    ) -> CommandInfo:
        """Add a CLI command to the hub.

        Args:
            func: Command function or Click command
            name: Optional name (defaults to function name)
            **kwargs: Additional command options

        Returns:
            CommandInfo for the registered command

        """
        click_module, has_click = _get_click()
        if has_click and isinstance(func, click_module.Command):
            command_name = name or func.name
            command_func = func.callback
            click_command = func
        else:
            # func should be a callable with __name__
            if hasattr(func, "__name__"):
                func_name = getattr(func, "__name__", "")
                command_name = name or (
                    func_name.replace("_", "-") if isinstance(func_name, str) else "unknown_command"
                )
            else:
                command_name = name if name is not None else "unknown_command"
            command_func = func
            click_command = None

        info = CommandInfo(
            name=command_name,
            func=command_func,
            description=kwargs.get("description", getattr(func, "__doc__", None)),
            aliases=kwargs.get("aliases", []),
            hidden=kwargs.get("hidden", False),
            category=kwargs.get("category"),
            metadata=kwargs,
        )

        self._command_registry.register(
            name=command_name,
            value=func,
            dimension=ComponentCategory.COMMAND.value,
            metadata={
                "info": info,
                "click_command": click_command,
                **kwargs,
            },
            aliases=info.aliases,
        )

        # Add to CLI group if it exists
        if self._cli_group and click_command:
            self._cli_group.add_command(click_command)

        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().info(
            "Added command to hub",
            name=command_name,
            aliases=info.aliases,
        )

        return info

    def get_command(self, name: str) -> Callable[..., Any] | None:
        """Get a command by name.

        Args:
            name: Command name or alias

        Returns:
            Command function or None

        """
        return self._command_registry.get(name, dimension=ComponentCategory.COMMAND.value)

    def list_commands(self) -> list[str]:
        """List all command names.

        Returns:
            List of command names

        """
        return self._command_registry.list_dimension(ComponentCategory.COMMAND.value)

    # CLI Integration

    def create_cli(
        self,
        name: str = "cli",
        version: str | None = None,
        **kwargs: Any,
    ) -> click.Group:
        """Create a Click CLI with all registered commands.

        Requires click to be installed.

        Args:
            name: CLI name
            version: CLI version
            **kwargs: Additional Click Group options

        Returns:
            Click Group with registered commands

        """
        click_module, has_click = _get_click()
        if not has_click:
            raise ImportError("CLI creation requires: pip install 'provide-foundation[cli]'")

        from provide.foundation.hub.commands import create_command_group

        # Use create_command_group which handles nested groups
        cli = create_command_group(name=name, registry=self._command_registry, **kwargs)

        # Add version option if provided
        if version:
            cli = click_module.version_option(version=version)(cli)

        self._cli_group = cli
        return cli

    def add_cli_group(self, group: click.Group) -> None:
        """Add an existing Click group to the hub.

        This registers all commands from the group.

        Args:
            group: Click Group to add

        """
        for name, cmd in group.commands.items():
            self.add_command(cmd, name)

    # Lifecycle Management

    def initialize(self) -> None:
        """Initialize all components that support initialization."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                continue

            component_class = entry.value
            if hasattr(component_class, "initialize"):
                try:
                    component_class.initialize()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(f"Initialized component: {entry.name}")
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to initialize {entry.name}: {e}")

    def cleanup(self) -> None:
        """Cleanup all components that support cleanup."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                continue

            component_class = entry.value
            if hasattr(component_class, "cleanup"):
                try:
                    component_class.cleanup()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(f"Cleaned up component: {entry.name}")
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to cleanup {entry.name}: {e}")

    def clear(self, dimension: str | None = None) -> None:
        """Clear registrations.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        if dimension == ComponentCategory.COMMAND.value or dimension is None:
            self._command_registry.clear(dimension=ComponentCategory.COMMAND.value if dimension else None)
            self._cli_group = None

        if dimension != ComponentCategory.COMMAND.value or dimension is None:
            self._component_registry.clear(dimension=dimension)

    # Dependency Injection

    def register(
        self,
        type_hint: type[T],
        instance: T,
        name: str | None = None,
    ) -> None:
        """Register a dependency by type for dependency injection.

        This enables type-based registration which is the foundation
        of the dependency injection pattern. Use this in your application's
        composition root (e.g., main.py) to wire up dependencies.

        Args:
            type_hint: Type to register under
            instance: Instance to register
            name: Optional name for named registration

        Example:
            >>> hub = Hub()
            >>> hub.register(DatabaseClient, db_instance)
            >>> hub.register(HTTPClient, http_instance)
            >>> service = hub.resolve(MyService)  # Auto-injects

        See Also:
            - resolve(): Create instances with auto-injected dependencies
            - @injectable: Decorator to mark DI-ready classes
        """
        self._component_registry.register_type(type_hint, instance, name)

    def resolve(
        self,
        cls: type[T],
        **overrides: Any,
    ) -> T:
        """Create an instance with dependency injection.

        Inspects the class constructor, resolves dependencies from the
        registry, and instantiates the class. This is the core of the
        dependency injection pattern.

        Args:
            cls: Class to instantiate
            **overrides: Explicitly provided dependencies (override registry)

        Returns:
            New instance with dependencies injected

        Raises:
            NotFoundError: If required dependency not registered
            ValidationError: If instantiation fails

        Example:
            >>> @injectable
            >>> class UserService:
            ...     def __init__(self, db: Database, logger: Logger):
            ...         self.db = db
            ...         self.logger = logger
            >>>
            >>> hub = Hub()
            >>> hub.register(Database, db_instance)
            >>> hub.register(Logger, logger_instance)
            >>> service = hub.resolve(UserService)  # Auto-injects db & logger

        Pattern:
            This implements the Dependency Injection pattern with an explicit
            Composition Root. The Hub acts as a DI Container that:
            1. Stores registered dependencies by type
            2. Inspects constructor signatures
            3. Automatically wires dependencies together

        See Also:
            - register(): Register dependencies by type
            - @injectable: Decorator to mark DI-ready classes
        """
        from provide.foundation.hub.injection import create_instance

        return create_instance(cls, self._component_registry, **overrides)

    def __enter__(self) -> CoreHub:
        """Context manager entry."""
        self.initialize()
        return self

    def __exit__(self, *args: object) -> None:
        """Context manager exit."""
        self.cleanup()


# 🧱🏗️🔚
