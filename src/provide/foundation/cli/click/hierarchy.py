#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Click group hierarchy management and validation.

Handles creation of Click command groups, parent group hierarchies,
and validation of command registry entries."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from provide.foundation import logger
from provide.foundation.cli.deps import click
from provide.foundation.hub.categories import ComponentCategory

if TYPE_CHECKING:
    from click import Group

    from provide.foundation.hub.info import CommandInfo
    from provide.foundation.hub.registry import Registry

__all__ = [
    "create_subgroup",
    "ensure_parent_groups",
    "should_skip_command",
    "should_skip_entry",
    "validate_command_entry",
]


def ensure_parent_groups(parent_path: str, registry: Registry) -> None:
    """Ensure all parent groups in the path exist, creating them if needed.

    Args:
        parent_path: Dot-notation path (e.g., "db.migrate")
        registry: Command registry to update

    """
    parts = parent_path.split(".")

    # Build up the path progressively
    for i in range(len(parts)):
        group_path = ".".join(parts[: i + 1])
        registry_key = group_path

        # Check if this group already exists
        if not registry.get_entry(registry_key, dimension=ComponentCategory.COMMAND.value):
            # Create a placeholder group
            def group_func() -> None:
                """Auto-generated command group."""

            # Set the function name for better debugging
            group_func.__name__ = f"{parts[i]}_group"

            # Register the group
            parent = ".".join(parts[:i]) if i > 0 else None

            from provide.foundation.hub.info import CommandInfo

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
                dimension=ComponentCategory.COMMAND.value,
                metadata={
                    "info": info,
                    "description": info.description,
                    "parent": parent,
                    "is_group": True,
                    "auto_created": True,
                },
            )

            logger.debug(f"Auto-created group: {group_path}")  # type: ignore[attr-defined]


def create_subgroup(cmd_name: str, entry: Any, groups: dict[str, Group], root_group: Group) -> None:
    """Create a Click subgroup and add it to the appropriate parent.

    Args:
        cmd_name: Command name
        entry: Registry entry
        groups: Dictionary of existing groups
        root_group: Root group

    """
    info = entry.metadata.get("info")
    parent = entry.metadata.get("parent")

    # Extract the actual group name (without parent prefix)
    actual_name = cmd_name.split(".")[-1] if parent else cmd_name

    subgroup = click.Group(
        name=actual_name,
        help=info.description,
        hidden=info.hidden,
    )
    groups[cmd_name] = subgroup

    # Add to parent or root
    if parent and parent in groups:
        groups[parent].add_command(subgroup)
    else:
        # Parent not found or no parent, add to root
        root_group.add_command(subgroup)


def validate_command_entry(entry: Any) -> CommandInfo | None:
    """Validate and extract command info from registry entry.

    Args:
        entry: Registry entry

    Returns:
        CommandInfo if valid, None otherwise

    """
    if not entry:
        return None

    info = entry.metadata.get("info")
    if not info:
        return None

    if not callable(info.func):
        return None

    return info


def should_skip_entry(entry: Any) -> bool:
    """Check if an entry should be skipped during processing.

    Args:
        entry: Registry entry

    Returns:
        True if entry should be skipped

    """
    if not entry:
        return True

    info = entry.metadata.get("info")
    return not info


def should_skip_command(entry: Any) -> bool:
    """Check if a command entry should be skipped (hidden or is a group).

    Args:
        entry: Registry entry

    Returns:
        True if command should be skipped

    """
    info = entry.metadata.get("info")
    return not info or info.hidden or entry.metadata.get("is_group")


# 🧱🏗️🔚
