#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Abstract CLI adapter protocol.

Defines the interface for CLI framework adapters, enabling support
for multiple CLI frameworks (Click, Typer, argparse, etc.) through
a common abstraction."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from provide.foundation.hub.info import CommandInfo
    from provide.foundation.hub.registry import Registry

__all__ = ["CLIAdapter"]


@runtime_checkable
class CLIAdapter(Protocol):
    """Protocol for CLI framework adapters.

    Adapters convert framework-agnostic CommandInfo objects into
    framework-specific CLI commands and groups. This allows the hub
    to work with any CLI framework without tight coupling.

    Currently provides ClickAdapter. Custom adapters for other frameworks (Typer, argparse)
    can be implemented by following the CLIAdapter protocol.

    See: docs/guide/advanced/integration-patterns.md#custom-cli-adapters

    Examples:
        >>> from provide.foundation.cli import get_cli_adapter
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """

    def build_command(self, info: CommandInfo) -> Any:
        """Build framework-specific command from CommandInfo.

        Args:
            info: Framework-agnostic command information

        Returns:
            Framework-specific command object (e.g., click.Command)

        Raises:
            CLIBuildError: If command building fails

        """
        ...

    def build_group(
        self,
        name: str,
        commands: list[CommandInfo] | None = None,
        registry: Registry | None = None,
        **kwargs: Any,
    ) -> Any:
        """Build framework-specific command group.

        Args:
            name: Group name
            commands: List of command names to include (None = all from registry)
            registry: Command registry (defaults to global)
            **kwargs: Framework-specific options

        Returns:
            Framework-specific group object (e.g., click.Group)

        Raises:
            CLIBuildError: If group building fails

        """
        ...

    def ensure_parent_groups(self, parent_path: str, registry: Registry) -> None:
        """Ensure all parent groups in path exist.

        Creates missing parent groups in the registry. For example, if
        parent_path is "db.migrate", ensures both "db" and "db.migrate"
        groups exist.

        Args:
            parent_path: Dot-notation path to parent (e.g., "db.migrate")
            registry: Command registry to update

        """
        ...


# 🧱🏗️🔚
