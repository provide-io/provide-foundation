"""
Hub manager - the main coordinator for components and commands.

This module provides the Hub class that coordinates component and command
registration, discovery, and access.
"""

from __future__ import annotations

import threading
from typing import Any, Callable

import click

from provide.foundation.context import Context
from provide.foundation.logger import get_logger
from provide.foundation.registry import Registry

from provide.foundation.hub.commands import (
    CommandInfo,
    build_click_command,
    get_command_registry,
)
from provide.foundation.hub.components import (
    ComponentInfo,
    discover_components as _discover_components,
    get_component_registry,
)

log = get_logger(__name__)


class Hub:
    """
    Central hub for managing components and commands.
    
    The Hub provides a unified interface for:
    - Registering components and commands
    - Discovering plugins via entry points
    - Creating Click CLI applications
    - Managing component lifecycle
    
    Example:
        >>> hub = Hub()
        >>> hub.add_component(MyResource, "resource")
        >>> hub.add_command(init_cmd, "init")
        >>> 
        >>> # Create CLI with all commands
        >>> cli = hub.create_cli()
        >>> cli()
    """
    
    def __init__(
        self,
        context: Context | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
    ) -> None:
        """
        Initialize the hub.
        
        Args:
            context: Foundation context for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
        """
        self.context = context or Context()
        self._component_registry = component_registry or get_component_registry()
        self._command_registry = command_registry or get_command_registry()
        self._cli_group: click.Group | None = None
    
    # Component Management
    
    def add_component(
        self,
        component_class: type[Any],
        name: str | None = None,
        dimension: str = "component",
        **metadata: Any,
    ) -> ComponentInfo:
        """
        Add a component to the hub.
        
        Args:
            component_class: Component class to register
            name: Optional name (defaults to class name)
            dimension: Registry dimension
            **metadata: Additional metadata
        
        Returns:
            ComponentInfo for the registered component
        """
        component_name = name or component_class.__name__
        
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
        )
        
        log.info(
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
        """
        Get a component by name.
        
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
        """
        List component names.
        
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
            if dim != "command":
                components.extend(names)
        return components
    
    def discover_components(
        self,
        group: str,
        dimension: str = "component",
    ) -> dict[str, type[Any]]:
        """
        Discover and register components from entry points.
        
        Args:
            group: Entry point group name
            dimension: Dimension to register under
        
        Returns:
            Dictionary of discovered components
        """
        return _discover_components(group, dimension, self._component_registry)
    
    # Command Management
    
    def add_command(
        self,
        func: Callable[..., Any] | click.Command,
        name: str | None = None,
        **kwargs: Any,
    ) -> CommandInfo:
        """
        Add a CLI command to the hub.
        
        Args:
            func: Command function or Click command
            name: Optional name (defaults to function name)
            **kwargs: Additional command options
        
        Returns:
            CommandInfo for the registered command
        """
        if isinstance(func, click.Command):
            command_name = name or func.name
            command_func = func.callback
            click_command = func
        else:
            command_name = name or func.__name__.replace("_", "-")
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
            click_command=click_command,
        )
        
        self._command_registry.register(
            name=command_name,
            value=func,
            dimension="command",
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
        
        log.info(
            "Added command to hub",
            name=command_name,
            aliases=info.aliases,
        )
        
        return info
    
    def get_command(self, name: str) -> Callable[..., Any] | None:
        """
        Get a command by name.
        
        Args:
            name: Command name or alias
        
        Returns:
            Command function or None
        """
        return self._command_registry.get(name, dimension="command")
    
    def list_commands(self) -> list[str]:
        """
        List all command names.
        
        Returns:
            List of command names
        """
        return self._command_registry.list_dimension("command")
    
    # CLI Integration
    
    def create_cli(
        self,
        name: str = "cli",
        version: str | None = None,
        **kwargs: Any,
    ) -> click.Group:
        """
        Create a Click CLI with all registered commands.
        
        Args:
            name: CLI name
            version: CLI version
            **kwargs: Additional Click Group options
        
        Returns:
            Click Group with registered commands
        
        Example:
            >>> hub = get_hub()
            >>> cli = hub.create_cli("myapp", version="1.0.0")
            >>> 
            >>> if __name__ == "__main__":
            >>>     cli()
        """
        from provide.foundation.cli.decorators import standard_options, pass_context
        from provide.foundation.hub.commands import create_command_group
        
        # Use create_command_group which now handles nested groups
        cli = create_command_group(name=name, registry=self._command_registry, **kwargs)
        
        # Apply standard decorators
        cli = standard_options(cli)
        cli = pass_context(cli)
        if version:
            cli = click.version_option(version=version)(cli)
        
        self._cli_group = cli
        return cli
    
    def add_cli_group(self, group: click.Group) -> None:
        """
        Add an existing Click group to the hub.
        
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
            if entry.dimension == "command":
                continue
            
            component_class = entry.value
            if hasattr(component_class, "initialize"):
                try:
                    component_class.initialize()
                    log.debug(f"Initialized component: {entry.name}")
                except Exception as e:
                    log.error(f"Failed to initialize {entry.name}: {e}")
    
    def cleanup(self) -> None:
        """Cleanup all components that support cleanup."""
        for entry in self._component_registry:
            if entry.dimension == "command":
                continue
            
            component_class = entry.value
            if hasattr(component_class, "cleanup"):
                try:
                    component_class.cleanup()
                    log.debug(f"Cleaned up component: {entry.name}")
                except Exception as e:
                    log.error(f"Failed to cleanup {entry.name}: {e}")
    
    def clear(self, dimension: str | None = None) -> None:
        """
        Clear registrations.
        
        Args:
            dimension: Optional dimension to clear (None = all)
        """
        if dimension == "command" or dimension is None:
            self._command_registry.clear(dimension="command" if dimension else None)
            self._cli_group = None
        
        if dimension != "command" or dimension is None:
            self._component_registry.clear(dimension=dimension)
    
    def __enter__(self) -> Hub:
        """Context manager entry."""
        self.initialize()
        return self
    
    def __exit__(self, *args: Any) -> None:
        """Context manager exit."""
        self.cleanup()


# Global hub instance and lock for thread-safe initialization
_global_hub: Hub | None = None
_hub_lock = threading.Lock()


def get_hub() -> Hub:
    """
    Get the global hub instance.
    
    Thread-safe: Uses double-checked locking pattern for efficient lazy initialization.
    
    Returns:
        Global Hub instance (created if needed)
    """
    global _global_hub
    
    # Fast path: hub already initialized
    if _global_hub is not None:
        return _global_hub
    
    # Slow path: need to initialize hub
    with _hub_lock:
        # Double-check after acquiring lock
        if _global_hub is None:
            _global_hub = Hub()
    
    return _global_hub


def clear_hub() -> None:
    """Clear the global hub instance."""
    global _global_hub
    with _hub_lock:
        if _global_hub:
            _global_hub.clear()
        _global_hub = None