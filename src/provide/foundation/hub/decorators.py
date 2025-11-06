#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, TypeVar, overload

from provide.foundation.hub.categories import ComponentCategory
from provide.foundation.hub.foundation import get_foundation_logger
from provide.foundation.hub.info import CommandInfo
from provide.foundation.hub.registry import Registry, get_command_registry

"""Command registration decorators."""

# Lazy import to avoid circular dependency
if TYPE_CHECKING:
    pass

# Import click lazily to avoid circular imports
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


# Defer click hierarchy import to avoid circular dependency
def _get_ensure_parent_groups() -> Any:
    _, has_click = _get_click()
    if not has_click:
        return None
    from provide.foundation.cli.click.hierarchy import ensure_parent_groups

    return ensure_parent_groups


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
    **metadata: Any,
) -> Callable[[F], F]: ...


@overload
def register_command(
    func: F,
    /,
) -> F: ...


def register_command(  # type: ignore[misc]
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
    """Register a CLI command in the hub.

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
        **metadata: Additional metadata stored in CommandInfo.metadata

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
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
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
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
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
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


# 🧱🏗️🔚
