"""Click CLI adapter implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from provide.foundation.cli.deps import click
from provide.foundation.cli.click.builder import create_command_group
from provide.foundation.cli.click.commands import build_click_command
from provide.foundation.cli.click.hierarchy import ensure_parent_groups

if TYPE_CHECKING:
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

    def build_command(self, info: CommandInfo) -> click.Command:
        """Build Click command from CommandInfo.

        Args:
            info: Framework-agnostic command information

        Returns:
            Click Command object

        Raises:
            CLIBuildError: If command building fails

        """
        # For now, we need the command to be in the registry
        # In the future, we could build directly from CommandInfo
        # without requiring registry registration
        from provide.foundation.hub.registry import get_command_registry

        registry = get_command_registry()

        # Try to find command in registry
        entry = registry.get_entry(info.name, dimension="command")
        if entry:
            cmd = build_click_command(info.name, registry=registry)
            if cmd:
                return cmd

        # If not in registry, we'd build directly from CommandInfo
        # This would require refactoring build_click_command to accept CommandInfo
        # For now, raise an error
        from provide.foundation.cli.errors import CLIBuildError

        raise CLIBuildError(
            f"Command '{info.name}' not found in registry",
            command_name=info.name,
        )

    def build_group(
        self,
        name: str,
        commands: list[CommandInfo] | None = None,
        registry: Registry | None = None,
        **kwargs: Any,
    ) -> click.Group:
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
