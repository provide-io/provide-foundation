#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Click CLI adapter implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from provide.foundation.cli.click.builder import create_command_group
from provide.foundation.cli.click.commands import build_click_command_from_info
from provide.foundation.cli.click.hierarchy import ensure_parent_groups

if TYPE_CHECKING:
    import click as click_types

    from provide.foundation.hub.info import CommandInfo
    from provide.foundation.hub.registry import Registry

__all__ = ["ClickAdapter"]


class ClickAdapter:
    """Click framework adapter.

    Implements the CLIAdapter protocol for the Click framework,
    converting framework-agnostic CommandInfo objects to Click
    commands and groups.

    Examples:
        >>> adapter = ClickAdapter()
        >>> command = adapter.build_command(command_info)
        >>> isinstance(command, click.Command)
        True

    """

    def build_command(self, info: CommandInfo) -> click_types.Command:
        """Build Click command from CommandInfo.

        Args:
            info: Framework-agnostic command information

        Returns:
            Click Command object

        Raises:
            CLIBuildError: If command building fails

        """
        return build_click_command_from_info(info)

    def build_group(
        self,
        name: str,
        commands: list[CommandInfo] | None = None,
        registry: Registry | None = None,
        **kwargs: Any,
    ) -> click_types.Group:
        """Build Click group with commands.

        Args:
            name: Group name
            commands: List of CommandInfo objects (or None to use registry)
            registry: Command registry
            **kwargs: Additional Click Group options

        Returns:
            Click Group object

        Raises:
            CLIBuildError: If group building fails

        """
        # If commands is a list of CommandInfo, extract names
        command_names = None
        if commands:
            command_names = [cmd.name for cmd in commands]

        return create_command_group(
            name=name,
            commands=command_names,
            registry=registry,
            **kwargs,
        )

    def ensure_parent_groups(self, parent_path: str, registry: Registry) -> None:
        """Ensure all parent groups in path exist.

        Args:
            parent_path: Dot-notation path (e.g., "db.migrate")
            registry: Command registry to update

        """
        ensure_parent_groups(parent_path, registry)


# 🧱🏗️🔚
