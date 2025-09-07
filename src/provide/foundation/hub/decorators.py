"""Command registration decorators."""

from collections.abc import Callable
from typing import Any, TypeVar, overload

try:
    import click

    _HAS_CLICK = True
except ImportError:
    click = None
    _HAS_CLICK = False


# Defer click_builder import to avoid circular dependency
def _get_ensure_parent_groups():
    if not _HAS_CLICK:
        return None
    from provide.foundation.hub.click_builder import ensure_parent_groups

    return ensure_parent_groups


from provide.foundation.hub.info import CommandInfo
from provide.foundation.hub.registry import Registry, get_command_registry
from provide.foundation.logger import get_logger

log = get_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


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
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            if _HAS_CLICK:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = func.__name__

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
    full_name = f"{parent}.{command_name}" if parent else command_name

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


__all__ = ["register_command"]
