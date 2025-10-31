#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Click command group builder and orchestration.

Main orchestrator for building Click CLI groups from registered commands.
Coordinates parameter processing, command building, and group hierarchy."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from provide.foundation.cli.click.commands import add_command_to_group
from provide.foundation.cli.click.hierarchy import (
    create_subgroup,
    should_skip_command,
    should_skip_entry,
)
from provide.foundation.cli.deps import click
from provide.foundation.cli.errors import CLIBuildError
from provide.foundation.hub.categories import ComponentCategory

if TYPE_CHECKING:
    from click import Group

    from provide.foundation.hub.registry import Registry

__all__ = [
    "create_command_group",
]


def create_command_group(  # noqa: C901
    name: str = "cli",
    commands: list[str] | None = None,
    registry: Registry | None = None,
    **kwargs: Any,
) -> Group:
    """Create a Click group with registered commands.

    Args:
        name: Name for the CLI group
        commands: List of command names to include (None = all)
        registry: Custom registry (defaults to global)
        **kwargs: Additional Click Group options

    Returns:
        Click Group with registered commands

    Raises:
        CLIBuildError: If group creation fails

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
    from provide.foundation.hub.registry import get_command_registry

    reg = registry or get_command_registry()

    try:
        group = click.Group(name=name, **kwargs)
        groups: dict[str, Group] = {}

        # Get commands to include
        if commands is None:
            commands = reg.list_dimension(ComponentCategory.COMMAND.value)

        # Sort commands to ensure parents are created before children
        sorted_commands = sorted(commands, key=lambda x: x.count("."))

        # First pass: create all groups
        for cmd_name in sorted_commands:
            entry = reg.get_entry(cmd_name, dimension=ComponentCategory.COMMAND.value)
            if should_skip_entry(entry):
                continue

            # Check if this is a group
            if entry and entry.metadata.get("is_group"):
                create_subgroup(cmd_name, entry, groups, group)

        # Second pass: add commands to groups
        for cmd_name in sorted_commands:
            entry = reg.get_entry(cmd_name, dimension=ComponentCategory.COMMAND.value)
            if should_skip_entry(entry) or should_skip_command(entry):
                continue

            if entry is not None:
                info = entry.metadata.get("info")
                if info:
                    add_command_to_group(info, groups, group, reg)

        return group

    except Exception as e:
        if isinstance(e, CLIBuildError):
            raise
        raise CLIBuildError(
            f"Failed to create Click command group '{name}': {e}",
            group_name=name,
            cause=e,
        ) from e


# 🧱🏗️🔚
