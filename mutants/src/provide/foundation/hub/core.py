# provide/foundation/hub/core.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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


def x__get_click__mutmut_orig() -> tuple[Any, bool]:
    """Get click module and availability flag."""
    global _click_module, _HAS_CLICK
    if _HAS_CLICK is None:
        from provide.foundation.cli.deps import _HAS_CLICK as has_click, click

        _click_module = click
        _HAS_CLICK = has_click
    return _click_module, _HAS_CLICK


def x__get_click__mutmut_1() -> tuple[Any, bool]:
    """Get click module and availability flag."""
    global _click_module, _HAS_CLICK
    if _HAS_CLICK is not None:
        from provide.foundation.cli.deps import _HAS_CLICK as has_click, click

        _click_module = click
        _HAS_CLICK = has_click
    return _click_module, _HAS_CLICK


def x__get_click__mutmut_2() -> tuple[Any, bool]:
    """Get click module and availability flag."""
    global _click_module, _HAS_CLICK
    if _HAS_CLICK is None:
        from provide.foundation.cli.deps import _HAS_CLICK as has_click, click

        _click_module = None
        _HAS_CLICK = has_click
    return _click_module, _HAS_CLICK


def x__get_click__mutmut_3() -> tuple[Any, bool]:
    """Get click module and availability flag."""
    global _click_module, _HAS_CLICK
    if _HAS_CLICK is None:
        from provide.foundation.cli.deps import _HAS_CLICK as has_click, click

        _click_module = click
        _HAS_CLICK = None
    return _click_module, _HAS_CLICK

x__get_click__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_click__mutmut_1': x__get_click__mutmut_1, 
    'x__get_click__mutmut_2': x__get_click__mutmut_2, 
    'x__get_click__mutmut_3': x__get_click__mutmut_3
}

def _get_click(*args, **kwargs):
    result = _mutmut_trampoline(x__get_click__mutmut_orig, x__get_click__mutmut_mutants, args, kwargs)
    return result 

_get_click.__signature__ = _mutmut_signature(x__get_click__mutmut_orig)
x__get_click__mutmut_orig.__name__ = 'x__get_click'


class CoreHub:
    """Core hub for managing components and commands.

    The CoreHub provides basic functionality for:
    - Registering components and commands
    - Managing component lifecycle
    - Creating Click CLI applications

    Does not include Foundation-specific initialization.
    """

    def xǁCoreHubǁ__init____mutmut_orig(
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

    def xǁCoreHubǁ__init____mutmut_1(
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
        self.context = None
        self._component_registry = component_registry or Registry()
        self._command_registry = command_registry or get_command_registry()
        self._cli_group: click.Group | None = None

    def xǁCoreHubǁ__init____mutmut_2(
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
        self.context = context and CLIContext()
        self._component_registry = component_registry or Registry()
        self._command_registry = command_registry or get_command_registry()
        self._cli_group: click.Group | None = None

    def xǁCoreHubǁ__init____mutmut_3(
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
        self._component_registry = None
        self._command_registry = command_registry or get_command_registry()
        self._cli_group: click.Group | None = None

    def xǁCoreHubǁ__init____mutmut_4(
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
        self._component_registry = component_registry and Registry()
        self._command_registry = command_registry or get_command_registry()
        self._cli_group: click.Group | None = None

    def xǁCoreHubǁ__init____mutmut_5(
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
        self._command_registry = None
        self._cli_group: click.Group | None = None

    def xǁCoreHubǁ__init____mutmut_6(
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
        self._command_registry = command_registry and get_command_registry()
        self._cli_group: click.Group | None = None

    def xǁCoreHubǁ__init____mutmut_7(
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
        self._cli_group: click.Group | None = ""
    
    xǁCoreHubǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCoreHubǁ__init____mutmut_1': xǁCoreHubǁ__init____mutmut_1, 
        'xǁCoreHubǁ__init____mutmut_2': xǁCoreHubǁ__init____mutmut_2, 
        'xǁCoreHubǁ__init____mutmut_3': xǁCoreHubǁ__init____mutmut_3, 
        'xǁCoreHubǁ__init____mutmut_4': xǁCoreHubǁ__init____mutmut_4, 
        'xǁCoreHubǁ__init____mutmut_5': xǁCoreHubǁ__init____mutmut_5, 
        'xǁCoreHubǁ__init____mutmut_6': xǁCoreHubǁ__init____mutmut_6, 
        'xǁCoreHubǁ__init____mutmut_7': xǁCoreHubǁ__init____mutmut_7
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCoreHubǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁCoreHubǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁCoreHubǁ__init____mutmut_orig)
    xǁCoreHubǁ__init____mutmut_orig.__name__ = 'xǁCoreHubǁ__init__'

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

    def xǁCoreHubǁget_component__mutmut_orig(
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

    def xǁCoreHubǁget_component__mutmut_1(
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
        return self._component_registry.get(None, dimension)

    def xǁCoreHubǁget_component__mutmut_2(
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
        return self._component_registry.get(name, None)

    def xǁCoreHubǁget_component__mutmut_3(
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
        return self._component_registry.get(dimension)

    def xǁCoreHubǁget_component__mutmut_4(
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
        return self._component_registry.get(name, )
    
    xǁCoreHubǁget_component__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCoreHubǁget_component__mutmut_1': xǁCoreHubǁget_component__mutmut_1, 
        'xǁCoreHubǁget_component__mutmut_2': xǁCoreHubǁget_component__mutmut_2, 
        'xǁCoreHubǁget_component__mutmut_3': xǁCoreHubǁget_component__mutmut_3, 
        'xǁCoreHubǁget_component__mutmut_4': xǁCoreHubǁget_component__mutmut_4
    }
    
    def get_component(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCoreHubǁget_component__mutmut_orig"), object.__getattribute__(self, "xǁCoreHubǁget_component__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_component.__signature__ = _mutmut_signature(xǁCoreHubǁget_component__mutmut_orig)
    xǁCoreHubǁget_component__mutmut_orig.__name__ = 'xǁCoreHubǁget_component'

    def xǁCoreHubǁlist_components__mutmut_orig(
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

    def xǁCoreHubǁlist_components__mutmut_1(
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
            return self._component_registry.list_dimension(None)

        # List all non-command dimensions
        all_items = self._component_registry.list_all()
        components = []
        for dim, names in all_items.items():
            if dim != ComponentCategory.COMMAND.value:
                components.extend(names)
        return components

    def xǁCoreHubǁlist_components__mutmut_2(
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
        all_items = None
        components = []
        for dim, names in all_items.items():
            if dim != ComponentCategory.COMMAND.value:
                components.extend(names)
        return components

    def xǁCoreHubǁlist_components__mutmut_3(
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
        components = None
        for dim, names in all_items.items():
            if dim != ComponentCategory.COMMAND.value:
                components.extend(names)
        return components

    def xǁCoreHubǁlist_components__mutmut_4(
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
            if dim == ComponentCategory.COMMAND.value:
                components.extend(names)
        return components

    def xǁCoreHubǁlist_components__mutmut_5(
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
                components.extend(None)
        return components
    
    xǁCoreHubǁlist_components__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCoreHubǁlist_components__mutmut_1': xǁCoreHubǁlist_components__mutmut_1, 
        'xǁCoreHubǁlist_components__mutmut_2': xǁCoreHubǁlist_components__mutmut_2, 
        'xǁCoreHubǁlist_components__mutmut_3': xǁCoreHubǁlist_components__mutmut_3, 
        'xǁCoreHubǁlist_components__mutmut_4': xǁCoreHubǁlist_components__mutmut_4, 
        'xǁCoreHubǁlist_components__mutmut_5': xǁCoreHubǁlist_components__mutmut_5
    }
    
    def list_components(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCoreHubǁlist_components__mutmut_orig"), object.__getattribute__(self, "xǁCoreHubǁlist_components__mutmut_mutants"), args, kwargs, self)
        return result 
    
    list_components.__signature__ = _mutmut_signature(xǁCoreHubǁlist_components__mutmut_orig)
    xǁCoreHubǁlist_components__mutmut_orig.__name__ = 'xǁCoreHubǁlist_components'

    def xǁCoreHubǁdiscover_components__mutmut_orig(
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

    def xǁCoreHubǁdiscover_components__mutmut_1(
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

        return _discover_components(None, dimension, self._component_registry)

    def xǁCoreHubǁdiscover_components__mutmut_2(
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

        return _discover_components(group, None, self._component_registry)

    def xǁCoreHubǁdiscover_components__mutmut_3(
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

        return _discover_components(group, dimension, None)

    def xǁCoreHubǁdiscover_components__mutmut_4(
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

        return _discover_components(dimension, self._component_registry)

    def xǁCoreHubǁdiscover_components__mutmut_5(
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

        return _discover_components(group, self._component_registry)

    def xǁCoreHubǁdiscover_components__mutmut_6(
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

        return _discover_components(group, dimension, )
    
    xǁCoreHubǁdiscover_components__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCoreHubǁdiscover_components__mutmut_1': xǁCoreHubǁdiscover_components__mutmut_1, 
        'xǁCoreHubǁdiscover_components__mutmut_2': xǁCoreHubǁdiscover_components__mutmut_2, 
        'xǁCoreHubǁdiscover_components__mutmut_3': xǁCoreHubǁdiscover_components__mutmut_3, 
        'xǁCoreHubǁdiscover_components__mutmut_4': xǁCoreHubǁdiscover_components__mutmut_4, 
        'xǁCoreHubǁdiscover_components__mutmut_5': xǁCoreHubǁdiscover_components__mutmut_5, 
        'xǁCoreHubǁdiscover_components__mutmut_6': xǁCoreHubǁdiscover_components__mutmut_6
    }
    
    def discover_components(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCoreHubǁdiscover_components__mutmut_orig"), object.__getattribute__(self, "xǁCoreHubǁdiscover_components__mutmut_mutants"), args, kwargs, self)
        return result 
    
    discover_components.__signature__ = _mutmut_signature(xǁCoreHubǁdiscover_components__mutmut_orig)
    xǁCoreHubǁdiscover_components__mutmut_orig.__name__ = 'xǁCoreHubǁdiscover_components'

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_orig(
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_1(
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
        click_module, has_click = None
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_2(
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
        if has_click or isinstance(func, click_module.Command):
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_3(
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
            command_name = None
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_4(
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
            command_name = name and func.name
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_5(
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
            command_func = None
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_6(
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
            click_command = None
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_7(
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
            if hasattr(None, "__name__"):
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_8(
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
            if hasattr(func, None):
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_9(
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
            if hasattr("__name__"):
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_10(
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
            if hasattr(func, ):
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_11(
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
            if hasattr(func, "XX__name__XX"):
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_12(
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
            if hasattr(func, "__NAME__"):
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_13(
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
                func_name = None
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_14(
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
                func_name = getattr(None, "__name__", "")
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_15(
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
                func_name = getattr(func, None, "")
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_16(
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
                func_name = getattr(func, "__name__", None)
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_17(
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
                func_name = getattr("__name__", "")
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_18(
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
                func_name = getattr(func, "")
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_19(
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
                func_name = getattr(func, "__name__", )
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_20(
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
                func_name = getattr(func, "XX__name__XX", "")
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_21(
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
                func_name = getattr(func, "__NAME__", "")
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_22(
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
                func_name = getattr(func, "__name__", "XXXX")
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_23(
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
                command_name = None
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_24(
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
                command_name = name and (
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_25(
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
                    func_name.replace(None, "-") if isinstance(func_name, str) else "unknown_command"
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_26(
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
                    func_name.replace("_", None) if isinstance(func_name, str) else "unknown_command"
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_27(
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
                    func_name.replace("-") if isinstance(func_name, str) else "unknown_command"
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_28(
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
                    func_name.replace("_", ) if isinstance(func_name, str) else "unknown_command"
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_29(
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
                    func_name.replace("XX_XX", "-") if isinstance(func_name, str) else "unknown_command"
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_30(
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
                    func_name.replace("_", "XX-XX") if isinstance(func_name, str) else "unknown_command"
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_31(
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
                    func_name.replace("_", "-") if isinstance(func_name, str) else "XXunknown_commandXX"
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_32(
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
                    func_name.replace("_", "-") if isinstance(func_name, str) else "UNKNOWN_COMMAND"
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_33(
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
                command_name = None
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_34(
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
                command_name = name if name is None else "unknown_command"
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_35(
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
                command_name = name if name is not None else "XXunknown_commandXX"
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_36(
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
                command_name = name if name is not None else "UNKNOWN_COMMAND"
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_37(
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
            command_func = None
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_38(
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
            click_command = ""

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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_39(
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

        info = None

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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_40(
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
            name=None,
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_41(
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
            func=None,
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_42(
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
            description=None,
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_43(
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
            aliases=None,
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_44(
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
            hidden=None,
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_45(
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
            category=None,
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_46(
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
            metadata=None,
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_47(
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_48(
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_49(
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_50(
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_51(
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_52(
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_53(
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_54(
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
            description=kwargs.get(None, getattr(func, "__doc__", None)),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_55(
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
            description=kwargs.get("description", None),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_56(
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
            description=kwargs.get(getattr(func, "__doc__", None)),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_57(
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
            description=kwargs.get("description", ),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_58(
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
            description=kwargs.get("XXdescriptionXX", getattr(func, "__doc__", None)),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_59(
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
            description=kwargs.get("DESCRIPTION", getattr(func, "__doc__", None)),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_60(
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
            description=kwargs.get("description", getattr(None, "__doc__", None)),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_61(
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
            description=kwargs.get("description", getattr(func, None, None)),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_62(
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
            description=kwargs.get("description", getattr("__doc__", None)),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_63(
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
            description=kwargs.get("description", getattr(func, None)),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_64(
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
            description=kwargs.get("description", getattr(func, "__doc__", )),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_65(
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
            description=kwargs.get("description", getattr(func, "XX__doc__XX", None)),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_66(
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
            description=kwargs.get("description", getattr(func, "__DOC__", None)),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_67(
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
            aliases=kwargs.get(None, []),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_68(
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
            aliases=kwargs.get("aliases", None),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_69(
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
            aliases=kwargs.get([]),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_70(
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
            aliases=kwargs.get("aliases", ),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_71(
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
            aliases=kwargs.get("XXaliasesXX", []),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_72(
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
            aliases=kwargs.get("ALIASES", []),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_73(
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
            hidden=kwargs.get(None, False),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_74(
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
            hidden=kwargs.get("hidden", None),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_75(
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
            hidden=kwargs.get(False),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_76(
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
            hidden=kwargs.get("hidden", ),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_77(
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
            hidden=kwargs.get("XXhiddenXX", False),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_78(
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
            hidden=kwargs.get("HIDDEN", False),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_79(
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
            hidden=kwargs.get("hidden", True),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_80(
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
            category=kwargs.get(None),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_81(
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
            category=kwargs.get("XXcategoryXX"),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_82(
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
            category=kwargs.get("CATEGORY"),
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_83(
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
            name=None,
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_84(
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
            value=None,
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_85(
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
            dimension=None,
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_86(
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
            metadata=None,
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_87(
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
            aliases=None,
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_88(
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_89(
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_90(
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_91(
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_92(
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_93(
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
                "XXinfoXX": info,
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_94(
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
                "INFO": info,
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_95(
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
                "XXclick_commandXX": click_command,
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_96(
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
                "CLICK_COMMAND": click_command,
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

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_97(
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
        if self._cli_group or click_command:
            self._cli_group.add_command(click_command)

        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().info(
            "Added command to hub",
            name=command_name,
            aliases=info.aliases,
        )

        return info

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_98(
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
            self._cli_group.add_command(None)

        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().info(
            "Added command to hub",
            name=command_name,
            aliases=info.aliases,
        )

        return info

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_99(
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
            None,
            name=command_name,
            aliases=info.aliases,
        )

        return info

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_100(
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
            name=None,
            aliases=info.aliases,
        )

        return info

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_101(
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
            aliases=None,
        )

        return info

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_102(
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
            name=command_name,
            aliases=info.aliases,
        )

        return info

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_103(
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
            aliases=info.aliases,
        )

        return info

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_104(
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
            )

        return info

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_105(
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
            "XXAdded command to hubXX",
            name=command_name,
            aliases=info.aliases,
        )

        return info

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_106(
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
            "added command to hub",
            name=command_name,
            aliases=info.aliases,
        )

        return info

    # Command Management

    def xǁCoreHubǁadd_command__mutmut_107(
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
            "ADDED COMMAND TO HUB",
            name=command_name,
            aliases=info.aliases,
        )

        return info
    
    xǁCoreHubǁadd_command__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCoreHubǁadd_command__mutmut_1': xǁCoreHubǁadd_command__mutmut_1, 
        'xǁCoreHubǁadd_command__mutmut_2': xǁCoreHubǁadd_command__mutmut_2, 
        'xǁCoreHubǁadd_command__mutmut_3': xǁCoreHubǁadd_command__mutmut_3, 
        'xǁCoreHubǁadd_command__mutmut_4': xǁCoreHubǁadd_command__mutmut_4, 
        'xǁCoreHubǁadd_command__mutmut_5': xǁCoreHubǁadd_command__mutmut_5, 
        'xǁCoreHubǁadd_command__mutmut_6': xǁCoreHubǁadd_command__mutmut_6, 
        'xǁCoreHubǁadd_command__mutmut_7': xǁCoreHubǁadd_command__mutmut_7, 
        'xǁCoreHubǁadd_command__mutmut_8': xǁCoreHubǁadd_command__mutmut_8, 
        'xǁCoreHubǁadd_command__mutmut_9': xǁCoreHubǁadd_command__mutmut_9, 
        'xǁCoreHubǁadd_command__mutmut_10': xǁCoreHubǁadd_command__mutmut_10, 
        'xǁCoreHubǁadd_command__mutmut_11': xǁCoreHubǁadd_command__mutmut_11, 
        'xǁCoreHubǁadd_command__mutmut_12': xǁCoreHubǁadd_command__mutmut_12, 
        'xǁCoreHubǁadd_command__mutmut_13': xǁCoreHubǁadd_command__mutmut_13, 
        'xǁCoreHubǁadd_command__mutmut_14': xǁCoreHubǁadd_command__mutmut_14, 
        'xǁCoreHubǁadd_command__mutmut_15': xǁCoreHubǁadd_command__mutmut_15, 
        'xǁCoreHubǁadd_command__mutmut_16': xǁCoreHubǁadd_command__mutmut_16, 
        'xǁCoreHubǁadd_command__mutmut_17': xǁCoreHubǁadd_command__mutmut_17, 
        'xǁCoreHubǁadd_command__mutmut_18': xǁCoreHubǁadd_command__mutmut_18, 
        'xǁCoreHubǁadd_command__mutmut_19': xǁCoreHubǁadd_command__mutmut_19, 
        'xǁCoreHubǁadd_command__mutmut_20': xǁCoreHubǁadd_command__mutmut_20, 
        'xǁCoreHubǁadd_command__mutmut_21': xǁCoreHubǁadd_command__mutmut_21, 
        'xǁCoreHubǁadd_command__mutmut_22': xǁCoreHubǁadd_command__mutmut_22, 
        'xǁCoreHubǁadd_command__mutmut_23': xǁCoreHubǁadd_command__mutmut_23, 
        'xǁCoreHubǁadd_command__mutmut_24': xǁCoreHubǁadd_command__mutmut_24, 
        'xǁCoreHubǁadd_command__mutmut_25': xǁCoreHubǁadd_command__mutmut_25, 
        'xǁCoreHubǁadd_command__mutmut_26': xǁCoreHubǁadd_command__mutmut_26, 
        'xǁCoreHubǁadd_command__mutmut_27': xǁCoreHubǁadd_command__mutmut_27, 
        'xǁCoreHubǁadd_command__mutmut_28': xǁCoreHubǁadd_command__mutmut_28, 
        'xǁCoreHubǁadd_command__mutmut_29': xǁCoreHubǁadd_command__mutmut_29, 
        'xǁCoreHubǁadd_command__mutmut_30': xǁCoreHubǁadd_command__mutmut_30, 
        'xǁCoreHubǁadd_command__mutmut_31': xǁCoreHubǁadd_command__mutmut_31, 
        'xǁCoreHubǁadd_command__mutmut_32': xǁCoreHubǁadd_command__mutmut_32, 
        'xǁCoreHubǁadd_command__mutmut_33': xǁCoreHubǁadd_command__mutmut_33, 
        'xǁCoreHubǁadd_command__mutmut_34': xǁCoreHubǁadd_command__mutmut_34, 
        'xǁCoreHubǁadd_command__mutmut_35': xǁCoreHubǁadd_command__mutmut_35, 
        'xǁCoreHubǁadd_command__mutmut_36': xǁCoreHubǁadd_command__mutmut_36, 
        'xǁCoreHubǁadd_command__mutmut_37': xǁCoreHubǁadd_command__mutmut_37, 
        'xǁCoreHubǁadd_command__mutmut_38': xǁCoreHubǁadd_command__mutmut_38, 
        'xǁCoreHubǁadd_command__mutmut_39': xǁCoreHubǁadd_command__mutmut_39, 
        'xǁCoreHubǁadd_command__mutmut_40': xǁCoreHubǁadd_command__mutmut_40, 
        'xǁCoreHubǁadd_command__mutmut_41': xǁCoreHubǁadd_command__mutmut_41, 
        'xǁCoreHubǁadd_command__mutmut_42': xǁCoreHubǁadd_command__mutmut_42, 
        'xǁCoreHubǁadd_command__mutmut_43': xǁCoreHubǁadd_command__mutmut_43, 
        'xǁCoreHubǁadd_command__mutmut_44': xǁCoreHubǁadd_command__mutmut_44, 
        'xǁCoreHubǁadd_command__mutmut_45': xǁCoreHubǁadd_command__mutmut_45, 
        'xǁCoreHubǁadd_command__mutmut_46': xǁCoreHubǁadd_command__mutmut_46, 
        'xǁCoreHubǁadd_command__mutmut_47': xǁCoreHubǁadd_command__mutmut_47, 
        'xǁCoreHubǁadd_command__mutmut_48': xǁCoreHubǁadd_command__mutmut_48, 
        'xǁCoreHubǁadd_command__mutmut_49': xǁCoreHubǁadd_command__mutmut_49, 
        'xǁCoreHubǁadd_command__mutmut_50': xǁCoreHubǁadd_command__mutmut_50, 
        'xǁCoreHubǁadd_command__mutmut_51': xǁCoreHubǁadd_command__mutmut_51, 
        'xǁCoreHubǁadd_command__mutmut_52': xǁCoreHubǁadd_command__mutmut_52, 
        'xǁCoreHubǁadd_command__mutmut_53': xǁCoreHubǁadd_command__mutmut_53, 
        'xǁCoreHubǁadd_command__mutmut_54': xǁCoreHubǁadd_command__mutmut_54, 
        'xǁCoreHubǁadd_command__mutmut_55': xǁCoreHubǁadd_command__mutmut_55, 
        'xǁCoreHubǁadd_command__mutmut_56': xǁCoreHubǁadd_command__mutmut_56, 
        'xǁCoreHubǁadd_command__mutmut_57': xǁCoreHubǁadd_command__mutmut_57, 
        'xǁCoreHubǁadd_command__mutmut_58': xǁCoreHubǁadd_command__mutmut_58, 
        'xǁCoreHubǁadd_command__mutmut_59': xǁCoreHubǁadd_command__mutmut_59, 
        'xǁCoreHubǁadd_command__mutmut_60': xǁCoreHubǁadd_command__mutmut_60, 
        'xǁCoreHubǁadd_command__mutmut_61': xǁCoreHubǁadd_command__mutmut_61, 
        'xǁCoreHubǁadd_command__mutmut_62': xǁCoreHubǁadd_command__mutmut_62, 
        'xǁCoreHubǁadd_command__mutmut_63': xǁCoreHubǁadd_command__mutmut_63, 
        'xǁCoreHubǁadd_command__mutmut_64': xǁCoreHubǁadd_command__mutmut_64, 
        'xǁCoreHubǁadd_command__mutmut_65': xǁCoreHubǁadd_command__mutmut_65, 
        'xǁCoreHubǁadd_command__mutmut_66': xǁCoreHubǁadd_command__mutmut_66, 
        'xǁCoreHubǁadd_command__mutmut_67': xǁCoreHubǁadd_command__mutmut_67, 
        'xǁCoreHubǁadd_command__mutmut_68': xǁCoreHubǁadd_command__mutmut_68, 
        'xǁCoreHubǁadd_command__mutmut_69': xǁCoreHubǁadd_command__mutmut_69, 
        'xǁCoreHubǁadd_command__mutmut_70': xǁCoreHubǁadd_command__mutmut_70, 
        'xǁCoreHubǁadd_command__mutmut_71': xǁCoreHubǁadd_command__mutmut_71, 
        'xǁCoreHubǁadd_command__mutmut_72': xǁCoreHubǁadd_command__mutmut_72, 
        'xǁCoreHubǁadd_command__mutmut_73': xǁCoreHubǁadd_command__mutmut_73, 
        'xǁCoreHubǁadd_command__mutmut_74': xǁCoreHubǁadd_command__mutmut_74, 
        'xǁCoreHubǁadd_command__mutmut_75': xǁCoreHubǁadd_command__mutmut_75, 
        'xǁCoreHubǁadd_command__mutmut_76': xǁCoreHubǁadd_command__mutmut_76, 
        'xǁCoreHubǁadd_command__mutmut_77': xǁCoreHubǁadd_command__mutmut_77, 
        'xǁCoreHubǁadd_command__mutmut_78': xǁCoreHubǁadd_command__mutmut_78, 
        'xǁCoreHubǁadd_command__mutmut_79': xǁCoreHubǁadd_command__mutmut_79, 
        'xǁCoreHubǁadd_command__mutmut_80': xǁCoreHubǁadd_command__mutmut_80, 
        'xǁCoreHubǁadd_command__mutmut_81': xǁCoreHubǁadd_command__mutmut_81, 
        'xǁCoreHubǁadd_command__mutmut_82': xǁCoreHubǁadd_command__mutmut_82, 
        'xǁCoreHubǁadd_command__mutmut_83': xǁCoreHubǁadd_command__mutmut_83, 
        'xǁCoreHubǁadd_command__mutmut_84': xǁCoreHubǁadd_command__mutmut_84, 
        'xǁCoreHubǁadd_command__mutmut_85': xǁCoreHubǁadd_command__mutmut_85, 
        'xǁCoreHubǁadd_command__mutmut_86': xǁCoreHubǁadd_command__mutmut_86, 
        'xǁCoreHubǁadd_command__mutmut_87': xǁCoreHubǁadd_command__mutmut_87, 
        'xǁCoreHubǁadd_command__mutmut_88': xǁCoreHubǁadd_command__mutmut_88, 
        'xǁCoreHubǁadd_command__mutmut_89': xǁCoreHubǁadd_command__mutmut_89, 
        'xǁCoreHubǁadd_command__mutmut_90': xǁCoreHubǁadd_command__mutmut_90, 
        'xǁCoreHubǁadd_command__mutmut_91': xǁCoreHubǁadd_command__mutmut_91, 
        'xǁCoreHubǁadd_command__mutmut_92': xǁCoreHubǁadd_command__mutmut_92, 
        'xǁCoreHubǁadd_command__mutmut_93': xǁCoreHubǁadd_command__mutmut_93, 
        'xǁCoreHubǁadd_command__mutmut_94': xǁCoreHubǁadd_command__mutmut_94, 
        'xǁCoreHubǁadd_command__mutmut_95': xǁCoreHubǁadd_command__mutmut_95, 
        'xǁCoreHubǁadd_command__mutmut_96': xǁCoreHubǁadd_command__mutmut_96, 
        'xǁCoreHubǁadd_command__mutmut_97': xǁCoreHubǁadd_command__mutmut_97, 
        'xǁCoreHubǁadd_command__mutmut_98': xǁCoreHubǁadd_command__mutmut_98, 
        'xǁCoreHubǁadd_command__mutmut_99': xǁCoreHubǁadd_command__mutmut_99, 
        'xǁCoreHubǁadd_command__mutmut_100': xǁCoreHubǁadd_command__mutmut_100, 
        'xǁCoreHubǁadd_command__mutmut_101': xǁCoreHubǁadd_command__mutmut_101, 
        'xǁCoreHubǁadd_command__mutmut_102': xǁCoreHubǁadd_command__mutmut_102, 
        'xǁCoreHubǁadd_command__mutmut_103': xǁCoreHubǁadd_command__mutmut_103, 
        'xǁCoreHubǁadd_command__mutmut_104': xǁCoreHubǁadd_command__mutmut_104, 
        'xǁCoreHubǁadd_command__mutmut_105': xǁCoreHubǁadd_command__mutmut_105, 
        'xǁCoreHubǁadd_command__mutmut_106': xǁCoreHubǁadd_command__mutmut_106, 
        'xǁCoreHubǁadd_command__mutmut_107': xǁCoreHubǁadd_command__mutmut_107
    }
    
    def add_command(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCoreHubǁadd_command__mutmut_orig"), object.__getattribute__(self, "xǁCoreHubǁadd_command__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_command.__signature__ = _mutmut_signature(xǁCoreHubǁadd_command__mutmut_orig)
    xǁCoreHubǁadd_command__mutmut_orig.__name__ = 'xǁCoreHubǁadd_command'

    def xǁCoreHubǁget_command__mutmut_orig(self, name: str) -> Callable[..., Any] | None:
        """Get a command by name.

        Args:
            name: Command name or alias

        Returns:
            Command function or None

        """
        return self._command_registry.get(name, dimension=ComponentCategory.COMMAND.value)

    def xǁCoreHubǁget_command__mutmut_1(self, name: str) -> Callable[..., Any] | None:
        """Get a command by name.

        Args:
            name: Command name or alias

        Returns:
            Command function or None

        """
        return self._command_registry.get(None, dimension=ComponentCategory.COMMAND.value)

    def xǁCoreHubǁget_command__mutmut_2(self, name: str) -> Callable[..., Any] | None:
        """Get a command by name.

        Args:
            name: Command name or alias

        Returns:
            Command function or None

        """
        return self._command_registry.get(name, dimension=None)

    def xǁCoreHubǁget_command__mutmut_3(self, name: str) -> Callable[..., Any] | None:
        """Get a command by name.

        Args:
            name: Command name or alias

        Returns:
            Command function or None

        """
        return self._command_registry.get(dimension=ComponentCategory.COMMAND.value)

    def xǁCoreHubǁget_command__mutmut_4(self, name: str) -> Callable[..., Any] | None:
        """Get a command by name.

        Args:
            name: Command name or alias

        Returns:
            Command function or None

        """
        return self._command_registry.get(name, )
    
    xǁCoreHubǁget_command__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCoreHubǁget_command__mutmut_1': xǁCoreHubǁget_command__mutmut_1, 
        'xǁCoreHubǁget_command__mutmut_2': xǁCoreHubǁget_command__mutmut_2, 
        'xǁCoreHubǁget_command__mutmut_3': xǁCoreHubǁget_command__mutmut_3, 
        'xǁCoreHubǁget_command__mutmut_4': xǁCoreHubǁget_command__mutmut_4
    }
    
    def get_command(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCoreHubǁget_command__mutmut_orig"), object.__getattribute__(self, "xǁCoreHubǁget_command__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_command.__signature__ = _mutmut_signature(xǁCoreHubǁget_command__mutmut_orig)
    xǁCoreHubǁget_command__mutmut_orig.__name__ = 'xǁCoreHubǁget_command'

    def xǁCoreHubǁlist_commands__mutmut_orig(self) -> list[str]:
        """List all command names.

        Returns:
            List of command names

        """
        return self._command_registry.list_dimension(ComponentCategory.COMMAND.value)

    def xǁCoreHubǁlist_commands__mutmut_1(self) -> list[str]:
        """List all command names.

        Returns:
            List of command names

        """
        return self._command_registry.list_dimension(None)
    
    xǁCoreHubǁlist_commands__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCoreHubǁlist_commands__mutmut_1': xǁCoreHubǁlist_commands__mutmut_1
    }
    
    def list_commands(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCoreHubǁlist_commands__mutmut_orig"), object.__getattribute__(self, "xǁCoreHubǁlist_commands__mutmut_mutants"), args, kwargs, self)
        return result 
    
    list_commands.__signature__ = _mutmut_signature(xǁCoreHubǁlist_commands__mutmut_orig)
    xǁCoreHubǁlist_commands__mutmut_orig.__name__ = 'xǁCoreHubǁlist_commands'

    # CLI Integration

    def xǁCoreHubǁcreate_cli__mutmut_orig(
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

    # CLI Integration

    def xǁCoreHubǁcreate_cli__mutmut_1(
        self,
        name: str = "XXcliXX",
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

    # CLI Integration

    def xǁCoreHubǁcreate_cli__mutmut_2(
        self,
        name: str = "CLI",
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

    # CLI Integration

    def xǁCoreHubǁcreate_cli__mutmut_3(
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
        click_module, has_click = None
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

    # CLI Integration

    def xǁCoreHubǁcreate_cli__mutmut_4(
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
        if has_click:
            raise ImportError("CLI creation requires: pip install 'provide-foundation[cli]'")

        from provide.foundation.hub.commands import create_command_group

        # Use create_command_group which handles nested groups
        cli = create_command_group(name=name, registry=self._command_registry, **kwargs)

        # Add version option if provided
        if version:
            cli = click_module.version_option(version=version)(cli)

        self._cli_group = cli
        return cli

    # CLI Integration

    def xǁCoreHubǁcreate_cli__mutmut_5(
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
            raise ImportError(None)

        from provide.foundation.hub.commands import create_command_group

        # Use create_command_group which handles nested groups
        cli = create_command_group(name=name, registry=self._command_registry, **kwargs)

        # Add version option if provided
        if version:
            cli = click_module.version_option(version=version)(cli)

        self._cli_group = cli
        return cli

    # CLI Integration

    def xǁCoreHubǁcreate_cli__mutmut_6(
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
            raise ImportError("XXCLI creation requires: pip install 'provide-foundation[cli]'XX")

        from provide.foundation.hub.commands import create_command_group

        # Use create_command_group which handles nested groups
        cli = create_command_group(name=name, registry=self._command_registry, **kwargs)

        # Add version option if provided
        if version:
            cli = click_module.version_option(version=version)(cli)

        self._cli_group = cli
        return cli

    # CLI Integration

    def xǁCoreHubǁcreate_cli__mutmut_7(
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
            raise ImportError("cli creation requires: pip install 'provide-foundation[cli]'")

        from provide.foundation.hub.commands import create_command_group

        # Use create_command_group which handles nested groups
        cli = create_command_group(name=name, registry=self._command_registry, **kwargs)

        # Add version option if provided
        if version:
            cli = click_module.version_option(version=version)(cli)

        self._cli_group = cli
        return cli

    # CLI Integration

    def xǁCoreHubǁcreate_cli__mutmut_8(
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
            raise ImportError("CLI CREATION REQUIRES: PIP INSTALL 'PROVIDE-FOUNDATION[CLI]'")

        from provide.foundation.hub.commands import create_command_group

        # Use create_command_group which handles nested groups
        cli = create_command_group(name=name, registry=self._command_registry, **kwargs)

        # Add version option if provided
        if version:
            cli = click_module.version_option(version=version)(cli)

        self._cli_group = cli
        return cli

    # CLI Integration

    def xǁCoreHubǁcreate_cli__mutmut_9(
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
        cli = None

        # Add version option if provided
        if version:
            cli = click_module.version_option(version=version)(cli)

        self._cli_group = cli
        return cli

    # CLI Integration

    def xǁCoreHubǁcreate_cli__mutmut_10(
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
        cli = create_command_group(name=None, registry=self._command_registry, **kwargs)

        # Add version option if provided
        if version:
            cli = click_module.version_option(version=version)(cli)

        self._cli_group = cli
        return cli

    # CLI Integration

    def xǁCoreHubǁcreate_cli__mutmut_11(
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
        cli = create_command_group(name=name, registry=None, **kwargs)

        # Add version option if provided
        if version:
            cli = click_module.version_option(version=version)(cli)

        self._cli_group = cli
        return cli

    # CLI Integration

    def xǁCoreHubǁcreate_cli__mutmut_12(
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
        cli = create_command_group(registry=self._command_registry, **kwargs)

        # Add version option if provided
        if version:
            cli = click_module.version_option(version=version)(cli)

        self._cli_group = cli
        return cli

    # CLI Integration

    def xǁCoreHubǁcreate_cli__mutmut_13(
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
        cli = create_command_group(name=name, **kwargs)

        # Add version option if provided
        if version:
            cli = click_module.version_option(version=version)(cli)

        self._cli_group = cli
        return cli

    # CLI Integration

    def xǁCoreHubǁcreate_cli__mutmut_14(
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
        cli = create_command_group(name=name, registry=self._command_registry, )

        # Add version option if provided
        if version:
            cli = click_module.version_option(version=version)(cli)

        self._cli_group = cli
        return cli

    # CLI Integration

    def xǁCoreHubǁcreate_cli__mutmut_15(
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
            cli = None

        self._cli_group = cli
        return cli

    # CLI Integration

    def xǁCoreHubǁcreate_cli__mutmut_16(
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
            cli = click_module.version_option(version=version)(None)

        self._cli_group = cli
        return cli

    # CLI Integration

    def xǁCoreHubǁcreate_cli__mutmut_17(
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
            cli = click_module.version_option(version=None)(cli)

        self._cli_group = cli
        return cli

    # CLI Integration

    def xǁCoreHubǁcreate_cli__mutmut_18(
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

        self._cli_group = None
        return cli
    
    xǁCoreHubǁcreate_cli__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCoreHubǁcreate_cli__mutmut_1': xǁCoreHubǁcreate_cli__mutmut_1, 
        'xǁCoreHubǁcreate_cli__mutmut_2': xǁCoreHubǁcreate_cli__mutmut_2, 
        'xǁCoreHubǁcreate_cli__mutmut_3': xǁCoreHubǁcreate_cli__mutmut_3, 
        'xǁCoreHubǁcreate_cli__mutmut_4': xǁCoreHubǁcreate_cli__mutmut_4, 
        'xǁCoreHubǁcreate_cli__mutmut_5': xǁCoreHubǁcreate_cli__mutmut_5, 
        'xǁCoreHubǁcreate_cli__mutmut_6': xǁCoreHubǁcreate_cli__mutmut_6, 
        'xǁCoreHubǁcreate_cli__mutmut_7': xǁCoreHubǁcreate_cli__mutmut_7, 
        'xǁCoreHubǁcreate_cli__mutmut_8': xǁCoreHubǁcreate_cli__mutmut_8, 
        'xǁCoreHubǁcreate_cli__mutmut_9': xǁCoreHubǁcreate_cli__mutmut_9, 
        'xǁCoreHubǁcreate_cli__mutmut_10': xǁCoreHubǁcreate_cli__mutmut_10, 
        'xǁCoreHubǁcreate_cli__mutmut_11': xǁCoreHubǁcreate_cli__mutmut_11, 
        'xǁCoreHubǁcreate_cli__mutmut_12': xǁCoreHubǁcreate_cli__mutmut_12, 
        'xǁCoreHubǁcreate_cli__mutmut_13': xǁCoreHubǁcreate_cli__mutmut_13, 
        'xǁCoreHubǁcreate_cli__mutmut_14': xǁCoreHubǁcreate_cli__mutmut_14, 
        'xǁCoreHubǁcreate_cli__mutmut_15': xǁCoreHubǁcreate_cli__mutmut_15, 
        'xǁCoreHubǁcreate_cli__mutmut_16': xǁCoreHubǁcreate_cli__mutmut_16, 
        'xǁCoreHubǁcreate_cli__mutmut_17': xǁCoreHubǁcreate_cli__mutmut_17, 
        'xǁCoreHubǁcreate_cli__mutmut_18': xǁCoreHubǁcreate_cli__mutmut_18
    }
    
    def create_cli(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCoreHubǁcreate_cli__mutmut_orig"), object.__getattribute__(self, "xǁCoreHubǁcreate_cli__mutmut_mutants"), args, kwargs, self)
        return result 
    
    create_cli.__signature__ = _mutmut_signature(xǁCoreHubǁcreate_cli__mutmut_orig)
    xǁCoreHubǁcreate_cli__mutmut_orig.__name__ = 'xǁCoreHubǁcreate_cli'

    def xǁCoreHubǁadd_cli_group__mutmut_orig(self, group: click.Group) -> None:
        """Add an existing Click group to the hub.

        This registers all commands from the group.

        Args:
            group: Click Group to add

        """
        for name, cmd in group.commands.items():
            self.add_command(cmd, name)

    def xǁCoreHubǁadd_cli_group__mutmut_1(self, group: click.Group) -> None:
        """Add an existing Click group to the hub.

        This registers all commands from the group.

        Args:
            group: Click Group to add

        """
        for name, cmd in group.commands.items():
            self.add_command(None, name)

    def xǁCoreHubǁadd_cli_group__mutmut_2(self, group: click.Group) -> None:
        """Add an existing Click group to the hub.

        This registers all commands from the group.

        Args:
            group: Click Group to add

        """
        for name, cmd in group.commands.items():
            self.add_command(cmd, None)

    def xǁCoreHubǁadd_cli_group__mutmut_3(self, group: click.Group) -> None:
        """Add an existing Click group to the hub.

        This registers all commands from the group.

        Args:
            group: Click Group to add

        """
        for name, cmd in group.commands.items():
            self.add_command(name)

    def xǁCoreHubǁadd_cli_group__mutmut_4(self, group: click.Group) -> None:
        """Add an existing Click group to the hub.

        This registers all commands from the group.

        Args:
            group: Click Group to add

        """
        for name, cmd in group.commands.items():
            self.add_command(cmd, )
    
    xǁCoreHubǁadd_cli_group__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCoreHubǁadd_cli_group__mutmut_1': xǁCoreHubǁadd_cli_group__mutmut_1, 
        'xǁCoreHubǁadd_cli_group__mutmut_2': xǁCoreHubǁadd_cli_group__mutmut_2, 
        'xǁCoreHubǁadd_cli_group__mutmut_3': xǁCoreHubǁadd_cli_group__mutmut_3, 
        'xǁCoreHubǁadd_cli_group__mutmut_4': xǁCoreHubǁadd_cli_group__mutmut_4
    }
    
    def add_cli_group(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCoreHubǁadd_cli_group__mutmut_orig"), object.__getattribute__(self, "xǁCoreHubǁadd_cli_group__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_cli_group.__signature__ = _mutmut_signature(xǁCoreHubǁadd_cli_group__mutmut_orig)
    xǁCoreHubǁadd_cli_group__mutmut_orig.__name__ = 'xǁCoreHubǁadd_cli_group'

    # Lifecycle Management

    def xǁCoreHubǁinitialize__mutmut_orig(self) -> None:
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

    # Lifecycle Management

    def xǁCoreHubǁinitialize__mutmut_1(self) -> None:
        """Initialize all components that support initialization."""
        for entry in self._component_registry:
            if entry.dimension != ComponentCategory.COMMAND.value:
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

    # Lifecycle Management

    def xǁCoreHubǁinitialize__mutmut_2(self) -> None:
        """Initialize all components that support initialization."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                break

            component_class = entry.value
            if hasattr(component_class, "initialize"):
                try:
                    component_class.initialize()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(f"Initialized component: {entry.name}")
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to initialize {entry.name}: {e}")

    # Lifecycle Management

    def xǁCoreHubǁinitialize__mutmut_3(self) -> None:
        """Initialize all components that support initialization."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                continue

            component_class = None
            if hasattr(component_class, "initialize"):
                try:
                    component_class.initialize()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(f"Initialized component: {entry.name}")
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to initialize {entry.name}: {e}")

    # Lifecycle Management

    def xǁCoreHubǁinitialize__mutmut_4(self) -> None:
        """Initialize all components that support initialization."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                continue

            component_class = entry.value
            if hasattr(None, "initialize"):
                try:
                    component_class.initialize()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(f"Initialized component: {entry.name}")
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to initialize {entry.name}: {e}")

    # Lifecycle Management

    def xǁCoreHubǁinitialize__mutmut_5(self) -> None:
        """Initialize all components that support initialization."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                continue

            component_class = entry.value
            if hasattr(component_class, None):
                try:
                    component_class.initialize()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(f"Initialized component: {entry.name}")
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to initialize {entry.name}: {e}")

    # Lifecycle Management

    def xǁCoreHubǁinitialize__mutmut_6(self) -> None:
        """Initialize all components that support initialization."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                continue

            component_class = entry.value
            if hasattr("initialize"):
                try:
                    component_class.initialize()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(f"Initialized component: {entry.name}")
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to initialize {entry.name}: {e}")

    # Lifecycle Management

    def xǁCoreHubǁinitialize__mutmut_7(self) -> None:
        """Initialize all components that support initialization."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                continue

            component_class = entry.value
            if hasattr(component_class, ):
                try:
                    component_class.initialize()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(f"Initialized component: {entry.name}")
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to initialize {entry.name}: {e}")

    # Lifecycle Management

    def xǁCoreHubǁinitialize__mutmut_8(self) -> None:
        """Initialize all components that support initialization."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                continue

            component_class = entry.value
            if hasattr(component_class, "XXinitializeXX"):
                try:
                    component_class.initialize()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(f"Initialized component: {entry.name}")
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to initialize {entry.name}: {e}")

    # Lifecycle Management

    def xǁCoreHubǁinitialize__mutmut_9(self) -> None:
        """Initialize all components that support initialization."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                continue

            component_class = entry.value
            if hasattr(component_class, "INITIALIZE"):
                try:
                    component_class.initialize()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(f"Initialized component: {entry.name}")
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to initialize {entry.name}: {e}")

    # Lifecycle Management

    def xǁCoreHubǁinitialize__mutmut_10(self) -> None:
        """Initialize all components that support initialization."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                continue

            component_class = entry.value
            if hasattr(component_class, "initialize"):
                try:
                    component_class.initialize()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(None)
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to initialize {entry.name}: {e}")

    # Lifecycle Management

    def xǁCoreHubǁinitialize__mutmut_11(self) -> None:
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

                    get_foundation_logger().error(None)
    
    xǁCoreHubǁinitialize__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCoreHubǁinitialize__mutmut_1': xǁCoreHubǁinitialize__mutmut_1, 
        'xǁCoreHubǁinitialize__mutmut_2': xǁCoreHubǁinitialize__mutmut_2, 
        'xǁCoreHubǁinitialize__mutmut_3': xǁCoreHubǁinitialize__mutmut_3, 
        'xǁCoreHubǁinitialize__mutmut_4': xǁCoreHubǁinitialize__mutmut_4, 
        'xǁCoreHubǁinitialize__mutmut_5': xǁCoreHubǁinitialize__mutmut_5, 
        'xǁCoreHubǁinitialize__mutmut_6': xǁCoreHubǁinitialize__mutmut_6, 
        'xǁCoreHubǁinitialize__mutmut_7': xǁCoreHubǁinitialize__mutmut_7, 
        'xǁCoreHubǁinitialize__mutmut_8': xǁCoreHubǁinitialize__mutmut_8, 
        'xǁCoreHubǁinitialize__mutmut_9': xǁCoreHubǁinitialize__mutmut_9, 
        'xǁCoreHubǁinitialize__mutmut_10': xǁCoreHubǁinitialize__mutmut_10, 
        'xǁCoreHubǁinitialize__mutmut_11': xǁCoreHubǁinitialize__mutmut_11
    }
    
    def initialize(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCoreHubǁinitialize__mutmut_orig"), object.__getattribute__(self, "xǁCoreHubǁinitialize__mutmut_mutants"), args, kwargs, self)
        return result 
    
    initialize.__signature__ = _mutmut_signature(xǁCoreHubǁinitialize__mutmut_orig)
    xǁCoreHubǁinitialize__mutmut_orig.__name__ = 'xǁCoreHubǁinitialize'

    def xǁCoreHubǁcleanup__mutmut_orig(self) -> None:
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

    def xǁCoreHubǁcleanup__mutmut_1(self) -> None:
        """Cleanup all components that support cleanup."""
        for entry in self._component_registry:
            if entry.dimension != ComponentCategory.COMMAND.value:
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

    def xǁCoreHubǁcleanup__mutmut_2(self) -> None:
        """Cleanup all components that support cleanup."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                break

            component_class = entry.value
            if hasattr(component_class, "cleanup"):
                try:
                    component_class.cleanup()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(f"Cleaned up component: {entry.name}")
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to cleanup {entry.name}: {e}")

    def xǁCoreHubǁcleanup__mutmut_3(self) -> None:
        """Cleanup all components that support cleanup."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                continue

            component_class = None
            if hasattr(component_class, "cleanup"):
                try:
                    component_class.cleanup()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(f"Cleaned up component: {entry.name}")
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to cleanup {entry.name}: {e}")

    def xǁCoreHubǁcleanup__mutmut_4(self) -> None:
        """Cleanup all components that support cleanup."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                continue

            component_class = entry.value
            if hasattr(None, "cleanup"):
                try:
                    component_class.cleanup()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(f"Cleaned up component: {entry.name}")
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to cleanup {entry.name}: {e}")

    def xǁCoreHubǁcleanup__mutmut_5(self) -> None:
        """Cleanup all components that support cleanup."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                continue

            component_class = entry.value
            if hasattr(component_class, None):
                try:
                    component_class.cleanup()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(f"Cleaned up component: {entry.name}")
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to cleanup {entry.name}: {e}")

    def xǁCoreHubǁcleanup__mutmut_6(self) -> None:
        """Cleanup all components that support cleanup."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                continue

            component_class = entry.value
            if hasattr("cleanup"):
                try:
                    component_class.cleanup()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(f"Cleaned up component: {entry.name}")
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to cleanup {entry.name}: {e}")

    def xǁCoreHubǁcleanup__mutmut_7(self) -> None:
        """Cleanup all components that support cleanup."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                continue

            component_class = entry.value
            if hasattr(component_class, ):
                try:
                    component_class.cleanup()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(f"Cleaned up component: {entry.name}")
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to cleanup {entry.name}: {e}")

    def xǁCoreHubǁcleanup__mutmut_8(self) -> None:
        """Cleanup all components that support cleanup."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                continue

            component_class = entry.value
            if hasattr(component_class, "XXcleanupXX"):
                try:
                    component_class.cleanup()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(f"Cleaned up component: {entry.name}")
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to cleanup {entry.name}: {e}")

    def xǁCoreHubǁcleanup__mutmut_9(self) -> None:
        """Cleanup all components that support cleanup."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                continue

            component_class = entry.value
            if hasattr(component_class, "CLEANUP"):
                try:
                    component_class.cleanup()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(f"Cleaned up component: {entry.name}")
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to cleanup {entry.name}: {e}")

    def xǁCoreHubǁcleanup__mutmut_10(self) -> None:
        """Cleanup all components that support cleanup."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                continue

            component_class = entry.value
            if hasattr(component_class, "cleanup"):
                try:
                    component_class.cleanup()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(None)
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to cleanup {entry.name}: {e}")

    def xǁCoreHubǁcleanup__mutmut_11(self) -> None:
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

                    get_foundation_logger().error(None)
    
    xǁCoreHubǁcleanup__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCoreHubǁcleanup__mutmut_1': xǁCoreHubǁcleanup__mutmut_1, 
        'xǁCoreHubǁcleanup__mutmut_2': xǁCoreHubǁcleanup__mutmut_2, 
        'xǁCoreHubǁcleanup__mutmut_3': xǁCoreHubǁcleanup__mutmut_3, 
        'xǁCoreHubǁcleanup__mutmut_4': xǁCoreHubǁcleanup__mutmut_4, 
        'xǁCoreHubǁcleanup__mutmut_5': xǁCoreHubǁcleanup__mutmut_5, 
        'xǁCoreHubǁcleanup__mutmut_6': xǁCoreHubǁcleanup__mutmut_6, 
        'xǁCoreHubǁcleanup__mutmut_7': xǁCoreHubǁcleanup__mutmut_7, 
        'xǁCoreHubǁcleanup__mutmut_8': xǁCoreHubǁcleanup__mutmut_8, 
        'xǁCoreHubǁcleanup__mutmut_9': xǁCoreHubǁcleanup__mutmut_9, 
        'xǁCoreHubǁcleanup__mutmut_10': xǁCoreHubǁcleanup__mutmut_10, 
        'xǁCoreHubǁcleanup__mutmut_11': xǁCoreHubǁcleanup__mutmut_11
    }
    
    def cleanup(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCoreHubǁcleanup__mutmut_orig"), object.__getattribute__(self, "xǁCoreHubǁcleanup__mutmut_mutants"), args, kwargs, self)
        return result 
    
    cleanup.__signature__ = _mutmut_signature(xǁCoreHubǁcleanup__mutmut_orig)
    xǁCoreHubǁcleanup__mutmut_orig.__name__ = 'xǁCoreHubǁcleanup'

    def xǁCoreHubǁclear__mutmut_orig(self, dimension: str | None = None) -> None:
        """Clear registrations.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        if dimension == ComponentCategory.COMMAND.value or dimension is None:
            self._command_registry.clear(dimension=ComponentCategory.COMMAND.value if dimension else None)
            self._cli_group = None

        if dimension != ComponentCategory.COMMAND.value or dimension is None:
            self._component_registry.clear(dimension=dimension)

    def xǁCoreHubǁclear__mutmut_1(self, dimension: str | None = None) -> None:
        """Clear registrations.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        if dimension == ComponentCategory.COMMAND.value and dimension is None:
            self._command_registry.clear(dimension=ComponentCategory.COMMAND.value if dimension else None)
            self._cli_group = None

        if dimension != ComponentCategory.COMMAND.value or dimension is None:
            self._component_registry.clear(dimension=dimension)

    def xǁCoreHubǁclear__mutmut_2(self, dimension: str | None = None) -> None:
        """Clear registrations.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        if dimension != ComponentCategory.COMMAND.value or dimension is None:
            self._command_registry.clear(dimension=ComponentCategory.COMMAND.value if dimension else None)
            self._cli_group = None

        if dimension != ComponentCategory.COMMAND.value or dimension is None:
            self._component_registry.clear(dimension=dimension)

    def xǁCoreHubǁclear__mutmut_3(self, dimension: str | None = None) -> None:
        """Clear registrations.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        if dimension == ComponentCategory.COMMAND.value or dimension is not None:
            self._command_registry.clear(dimension=ComponentCategory.COMMAND.value if dimension else None)
            self._cli_group = None

        if dimension != ComponentCategory.COMMAND.value or dimension is None:
            self._component_registry.clear(dimension=dimension)

    def xǁCoreHubǁclear__mutmut_4(self, dimension: str | None = None) -> None:
        """Clear registrations.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        if dimension == ComponentCategory.COMMAND.value or dimension is None:
            self._command_registry.clear(dimension=None)
            self._cli_group = None

        if dimension != ComponentCategory.COMMAND.value or dimension is None:
            self._component_registry.clear(dimension=dimension)

    def xǁCoreHubǁclear__mutmut_5(self, dimension: str | None = None) -> None:
        """Clear registrations.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        if dimension == ComponentCategory.COMMAND.value or dimension is None:
            self._command_registry.clear(dimension=ComponentCategory.COMMAND.value if dimension else None)
            self._cli_group = ""

        if dimension != ComponentCategory.COMMAND.value or dimension is None:
            self._component_registry.clear(dimension=dimension)

    def xǁCoreHubǁclear__mutmut_6(self, dimension: str | None = None) -> None:
        """Clear registrations.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        if dimension == ComponentCategory.COMMAND.value or dimension is None:
            self._command_registry.clear(dimension=ComponentCategory.COMMAND.value if dimension else None)
            self._cli_group = None

        if dimension != ComponentCategory.COMMAND.value and dimension is None:
            self._component_registry.clear(dimension=dimension)

    def xǁCoreHubǁclear__mutmut_7(self, dimension: str | None = None) -> None:
        """Clear registrations.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        if dimension == ComponentCategory.COMMAND.value or dimension is None:
            self._command_registry.clear(dimension=ComponentCategory.COMMAND.value if dimension else None)
            self._cli_group = None

        if dimension == ComponentCategory.COMMAND.value or dimension is None:
            self._component_registry.clear(dimension=dimension)

    def xǁCoreHubǁclear__mutmut_8(self, dimension: str | None = None) -> None:
        """Clear registrations.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        if dimension == ComponentCategory.COMMAND.value or dimension is None:
            self._command_registry.clear(dimension=ComponentCategory.COMMAND.value if dimension else None)
            self._cli_group = None

        if dimension != ComponentCategory.COMMAND.value or dimension is not None:
            self._component_registry.clear(dimension=dimension)

    def xǁCoreHubǁclear__mutmut_9(self, dimension: str | None = None) -> None:
        """Clear registrations.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        if dimension == ComponentCategory.COMMAND.value or dimension is None:
            self._command_registry.clear(dimension=ComponentCategory.COMMAND.value if dimension else None)
            self._cli_group = None

        if dimension != ComponentCategory.COMMAND.value or dimension is None:
            self._component_registry.clear(dimension=None)
    
    xǁCoreHubǁclear__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCoreHubǁclear__mutmut_1': xǁCoreHubǁclear__mutmut_1, 
        'xǁCoreHubǁclear__mutmut_2': xǁCoreHubǁclear__mutmut_2, 
        'xǁCoreHubǁclear__mutmut_3': xǁCoreHubǁclear__mutmut_3, 
        'xǁCoreHubǁclear__mutmut_4': xǁCoreHubǁclear__mutmut_4, 
        'xǁCoreHubǁclear__mutmut_5': xǁCoreHubǁclear__mutmut_5, 
        'xǁCoreHubǁclear__mutmut_6': xǁCoreHubǁclear__mutmut_6, 
        'xǁCoreHubǁclear__mutmut_7': xǁCoreHubǁclear__mutmut_7, 
        'xǁCoreHubǁclear__mutmut_8': xǁCoreHubǁclear__mutmut_8, 
        'xǁCoreHubǁclear__mutmut_9': xǁCoreHubǁclear__mutmut_9
    }
    
    def clear(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCoreHubǁclear__mutmut_orig"), object.__getattribute__(self, "xǁCoreHubǁclear__mutmut_mutants"), args, kwargs, self)
        return result 
    
    clear.__signature__ = _mutmut_signature(xǁCoreHubǁclear__mutmut_orig)
    xǁCoreHubǁclear__mutmut_orig.__name__ = 'xǁCoreHubǁclear'

    # Dependency Injection

    def xǁCoreHubǁregister__mutmut_orig(
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

    # Dependency Injection

    def xǁCoreHubǁregister__mutmut_1(
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
        self._component_registry.register_type(None, instance, name)

    # Dependency Injection

    def xǁCoreHubǁregister__mutmut_2(
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
        self._component_registry.register_type(type_hint, None, name)

    # Dependency Injection

    def xǁCoreHubǁregister__mutmut_3(
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
        self._component_registry.register_type(type_hint, instance, None)

    # Dependency Injection

    def xǁCoreHubǁregister__mutmut_4(
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
        self._component_registry.register_type(instance, name)

    # Dependency Injection

    def xǁCoreHubǁregister__mutmut_5(
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
        self._component_registry.register_type(type_hint, name)

    # Dependency Injection

    def xǁCoreHubǁregister__mutmut_6(
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
        self._component_registry.register_type(type_hint, instance, )
    
    xǁCoreHubǁregister__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCoreHubǁregister__mutmut_1': xǁCoreHubǁregister__mutmut_1, 
        'xǁCoreHubǁregister__mutmut_2': xǁCoreHubǁregister__mutmut_2, 
        'xǁCoreHubǁregister__mutmut_3': xǁCoreHubǁregister__mutmut_3, 
        'xǁCoreHubǁregister__mutmut_4': xǁCoreHubǁregister__mutmut_4, 
        'xǁCoreHubǁregister__mutmut_5': xǁCoreHubǁregister__mutmut_5, 
        'xǁCoreHubǁregister__mutmut_6': xǁCoreHubǁregister__mutmut_6
    }
    
    def register(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCoreHubǁregister__mutmut_orig"), object.__getattribute__(self, "xǁCoreHubǁregister__mutmut_mutants"), args, kwargs, self)
        return result 
    
    register.__signature__ = _mutmut_signature(xǁCoreHubǁregister__mutmut_orig)
    xǁCoreHubǁregister__mutmut_orig.__name__ = 'xǁCoreHubǁregister'

    def xǁCoreHubǁresolve__mutmut_orig(
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

    def xǁCoreHubǁresolve__mutmut_1(
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

        return create_instance(None, self._component_registry, **overrides)

    def xǁCoreHubǁresolve__mutmut_2(
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

        return create_instance(cls, None, **overrides)

    def xǁCoreHubǁresolve__mutmut_3(
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

        return create_instance(self._component_registry, **overrides)

    def xǁCoreHubǁresolve__mutmut_4(
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

        return create_instance(cls, **overrides)

    def xǁCoreHubǁresolve__mutmut_5(
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

        return create_instance(cls, self._component_registry, )
    
    xǁCoreHubǁresolve__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCoreHubǁresolve__mutmut_1': xǁCoreHubǁresolve__mutmut_1, 
        'xǁCoreHubǁresolve__mutmut_2': xǁCoreHubǁresolve__mutmut_2, 
        'xǁCoreHubǁresolve__mutmut_3': xǁCoreHubǁresolve__mutmut_3, 
        'xǁCoreHubǁresolve__mutmut_4': xǁCoreHubǁresolve__mutmut_4, 
        'xǁCoreHubǁresolve__mutmut_5': xǁCoreHubǁresolve__mutmut_5
    }
    
    def resolve(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCoreHubǁresolve__mutmut_orig"), object.__getattribute__(self, "xǁCoreHubǁresolve__mutmut_mutants"), args, kwargs, self)
        return result 
    
    resolve.__signature__ = _mutmut_signature(xǁCoreHubǁresolve__mutmut_orig)
    xǁCoreHubǁresolve__mutmut_orig.__name__ = 'xǁCoreHubǁresolve'

    def __enter__(self) -> CoreHub:
        """Context manager entry."""
        self.initialize()
        return self

    def __exit__(self, *args: object) -> None:
        """Context manager exit."""
        self.cleanup()


# <3 🧱🤝🌐🪄
