#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Click command building and integration.

Builds individual Click commands from CommandInfo objects and integrates
them with Click groups."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from provide.foundation.cli.click.parameters import (
    apply_click_argument,
    apply_click_option,
    separate_arguments_and_options,
)
from provide.foundation.cli.deps import click
from provide.foundation.cli.errors import CLIBuildError
from provide.foundation.hub.introspection import introspect_parameters

if TYPE_CHECKING:
    from click import Command, Group

    from provide.foundation.hub.info import CommandInfo
    from provide.foundation.hub.registry import Registry

__all__ = [
    "add_command_to_group",
    "build_click_command_from_info",
]


def build_click_command_from_info(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def add_command_to_group(
    info: CommandInfo,
    groups: dict[str, Group],
    root_group: Group,
    registry: Registry,
) -> None:
    """Build and add a Click command to the appropriate group.

    Args:
        info: CommandInfo object for the command
        groups: Dictionary of existing groups
        root_group: Root group
        registry: Command registry (unused, kept for signature compatibility during refactor)

    """
    click_cmd = build_click_command_from_info(info)
    if not click_cmd:
        return

    # Add to parent group or root
    if info.parent and info.parent in groups:
        groups[info.parent].add_command(click_cmd)
    else:
        # Parent not found or no parent, add to root
        root_group.add_command(click_cmd)


# 🧱🏗️🔚
