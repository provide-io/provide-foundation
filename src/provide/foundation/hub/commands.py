"""
Command registration and management for the hub.

This module provides decorators and utilities for registering CLI commands
and integrating them with Click.
"""

from __future__ import annotations

import inspect
import types
import typing
from dataclasses import dataclass, field
from typing import Any, Callable, TypeVar, overload, get_origin, get_args

import click

from provide.foundation.logger import get_logger
from provide.foundation.registry import Registry

log = get_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])

# Global registry for commands
_command_registry = Registry()


@dataclass(frozen=True, slots=True)
class CommandInfo:
    """Information about a registered command."""
    
    name: str
    func: Callable[..., Any]
    description: str | None = None
    aliases: list[str] = field(default_factory=list)
    hidden: bool = False
    category: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    click_command: click.Command | None = None
    parent: str | None = None  # Parent path extracted from dot notation


@overload
def register_command(
    name: str | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
) -> Callable[[F], F]: ...


@overload
def register_command(
    func: F,
    /,
) -> F: ...


def register_command(
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """
    Register a CLI command in the hub.
    
    Can be used as a decorator with or without arguments:
        
        @register_command
        def my_command():
            pass
        
        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass
        
        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass
        
        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass
        
        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass
    
    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        registry: Custom registry (defaults to global)
    
    Returns:
        Decorator function or decorated function
    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )
    
    # Handle @register_command(...) (with arguments)
    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_or_func,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )
    
    return decorator


def _register_command_func(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or _command_registry
    
    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]
            
            # Auto-create parent groups if they don't exist
            _ensure_parent_groups(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Convert function name to kebab-case
        parent = None
        command_name = func.__name__.replace("_", "-").replace("cmd", "").strip("-")
    
    # Check if it's already a Click command
    click_cmd = None
    if isinstance(func, click.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func
    
    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)
    
    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        click_command=click_cmd,
        parent=parent,
    )
    
    # Build full registry key
    if parent:
        full_name = f"{parent.replace('.', '-')}-{command_name}"
    else:
        full_name = command_name
    
    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "click_command": click_cmd,
    }
    reg_metadata.update(extra_metadata)
    
    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension="command",
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )
    
    # Add metadata to the function
    func.__registry_name__ = command_name
    func.__registry_dimension__ = "command"
    func.__registry_info__ = info
    
    log.info(
        "Registered command",
        name=command_name,
        parent=parent,
        aliases=aliases,
        hidden=hidden,
        category=category,
    )
    
    return func


def _ensure_parent_groups(parent_path: str, registry: Registry) -> None:
    """Ensure all parent groups in the path exist, creating them if needed."""
    parts = parent_path.split(".")
    
    # Build up the path progressively
    for i in range(len(parts)):
        group_path = ".".join(parts[:i+1])
        registry_key = group_path.replace(".", "-")
        
        # Check if this group already exists
        if not registry.get_entry(registry_key, dimension="command"):
            # Create a placeholder group
            def group_func():
                """Auto-generated command group."""
                pass
            
            # Set the function name for better debugging
            group_func.__name__ = f"{parts[i]}_group"
            
            # Register the group
            parent = ".".join(parts[:i]) if i > 0 else None
            
            info = CommandInfo(
                name=parts[i],
                func=group_func,
                description=f"{parts[i].capitalize()} commands",
                metadata={"is_group": True, "auto_created": True},
                parent=parent,
            )
            
            registry.register(
                name=registry_key,
                value=group_func,
                dimension="command",
                metadata={
                    "info": info,
                    "description": info.description,
                    "parent": parent,
                    "is_group": True,
                    "auto_created": True,
                },
            )
            
            log.debug(f"Auto-created group: {group_path}")


def _extract_click_type(annotation: Any) -> type:
    """
    Extract a Click-compatible type from a Python type annotation.
    
    Handles:
    - Union types (str | None, Union[str, None])
    - Optional types (Optional[str])
    - Regular types (str, int, bool)
    
    Args:
        annotation: Type annotation from function signature
        
    Returns:
        A type that Click can understand
    """
    # Handle None type
    if annotation is type(None):
        return str
    
    # Get the origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)
    
    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr(types, 'UnionType') and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, '__args__'):
            args = annotation.__args__
        
        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]
        
        if non_none_types:
            # Return the first non-None type
            # Could be enhanced to handle Union[str, int] etc.
            return non_none_types[0]
        else:
            # If only None, default to str
            return str
    
    # For non-generic types, return as-is
    return annotation


def build_click_command(
    name: str,
    registry: Registry | None = None,
) -> click.Command | None:
    """
    Build a Click command from a registered function.
    
    This function takes a registered command and converts it to a
    Click command with proper options and arguments based on the
    function signature.
    
    Args:
        name: Command name in registry
        registry: Custom registry (defaults to global)
    
    Returns:
        Click Command or None if not found
    
    Example:
        >>> @register_command("greet")
        >>> def greet(name: str = "World"):
        >>>     print(f"Hello, {name}!")
        >>> 
        >>> click_cmd = build_click_command("greet")
        >>> # Now click_cmd can be added to a Click group
    """
    reg = registry or _command_registry
    entry = reg.get_entry(name, dimension="command")
    
    if not entry:
        return None
    
    info = entry.metadata.get("info")
    if not info:
        return None
    
    # If it's already a Click command, return it
    if info.click_command:
        return info.click_command
    
    func = info.func
    if not callable(func):
        return None
    
    # Build Click command from function signature
    sig = inspect.signature(func)
    
    # Process parameters in reverse order for Click decorator stacking
    params = list(sig.parameters.items())
    
    # Start with the base function
    decorated_func = func
    
    for param_name, param in reversed(params):
        if param_name in ("self", "cls", "ctx"):
            continue
        
        # Determine if it's an option or argument
        has_default = param.default != inspect.Parameter.empty
        
        if has_default:
            # Create option
            option_name = f"--{param_name.replace('_', '-')}"
            if param.annotation != inspect.Parameter.empty:
                # Extract the actual type from unions/optionals
                param_type = _extract_click_type(param.annotation)
                
                # Use type annotation
                if param_type == bool:
                    decorated_func = click.option(
                        option_name,
                        is_flag=True,
                        default=param.default,
                        help=f"{param_name} flag",
                    )(decorated_func)
                else:
                    decorated_func = click.option(
                        option_name,
                        type=param_type,
                        default=param.default,
                        help=f"{param_name} option",
                    )(decorated_func)
            else:
                decorated_func = click.option(
                    option_name,
                    default=param.default,
                    help=f"{param_name} option",
                )(decorated_func)
        else:
            # Create argument
            if param.annotation != inspect.Parameter.empty:
                # Extract the actual type from unions/optionals
                param_type = _extract_click_type(param.annotation)
                decorated_func = click.argument(
                    param_name,
                    type=param_type,
                )(decorated_func)
            else:
                decorated_func = click.argument(param_name)(decorated_func)
    
    # Create the Click command with the decorated function
    cmd = click.Command(
        name=info.name,
        callback=decorated_func,
        help=info.description,
        hidden=info.hidden,
    )
    
    # Copy over the params from the decorated function (Click stores them there)
    if hasattr(decorated_func, '__click_params__'):
        cmd.params = decorated_func.__click_params__
    
    return cmd


def create_command_group(
    name: str = "cli",
    commands: list[str] | None = None,
    registry: Registry | None = None,
    **kwargs: Any,
) -> click.Group:
    """
    Create a Click group with registered commands.
    
    Args:
        name: Name for the CLI group
        commands: List of command names to include (None = all)
        registry: Custom registry (defaults to global)
        **kwargs: Additional Click Group options
    
    Returns:
        Click Group with registered commands
    
    Example:
        >>> # Register some commands
        >>> @register_command("init")
        >>> def init_cmd():
        >>>     pass
        >>> 
        >>> # Create CLI group
        >>> cli = create_command_group("myapp")
        >>> 
        >>> # Run the CLI
        >>> if __name__ == "__main__":
        >>>     cli()
    """
    reg = registry or _command_registry
    group = click.Group(name=name, **kwargs)
    
    # Build nested command structure
    groups: dict[str, click.Group] = {}
    
    # Get commands to include
    if commands is None:
        commands = reg.list_dimension("command")
    
    # Sort commands to ensure parents are created before children
    sorted_commands = sorted(commands, key=lambda x: x.count("-"))
    
    # First pass: create all groups
    for cmd_name in sorted_commands:
        entry = reg.get_entry(cmd_name, dimension="command")
        if not entry:
            continue
        
        info = entry.metadata.get("info")
        if not info:
            continue
        
        # Check if this is a group
        if entry.metadata.get("is_group"):
            parent = entry.metadata.get("parent")
            # Extract the actual group name (without parent prefix)
            actual_name = cmd_name.split("-")[-1] if parent else cmd_name
            
            subgroup = click.Group(
                name=actual_name,
                help=info.description,
                hidden=info.hidden,
            )
            groups[cmd_name] = subgroup
            
            # Add to parent or root
            if parent:
                # Handle multi-level parents with dot notation
                parent_key = parent.replace(".", "-")
                if parent_key in groups:
                    groups[parent_key].add_command(subgroup)
                else:
                    # Parent should have been created, add to root as fallback
                    group.add_command(subgroup)
            else:
                group.add_command(subgroup)
    
    # Second pass: add commands to groups
    for cmd_name in sorted_commands:
        entry = reg.get_entry(cmd_name, dimension="command")
        if not entry:
            continue
        
        info = entry.metadata.get("info")
        if not info or info.hidden or entry.metadata.get("is_group"):
            continue
        
        # Build Click command
        click_cmd = build_click_command(cmd_name, registry=reg)
        if click_cmd:
            parent = entry.metadata.get("parent")
            
            # Update command name if it has a parent
            if parent:
                # Extract the actual command name (without parent prefix)
                parts = cmd_name.split("-")
                parent_parts = parent.replace(".", "-").split("-")
                # Remove parent parts from command name
                cmd_parts = parts[len(parent_parts):]
                click_cmd.name = "-".join(cmd_parts) if cmd_parts else parts[-1]
            
            # Add to parent group or root
            if parent:
                parent_key = parent.replace(".", "-")
                if parent_key in groups:
                    groups[parent_key].add_command(click_cmd)
                else:
                    # Parent not found, add to root
                    group.add_command(click_cmd)
            else:
                group.add_command(click_cmd)
    
    return group


def get_command_registry() -> Registry:
    """Get the global command registry."""
    return _command_registry