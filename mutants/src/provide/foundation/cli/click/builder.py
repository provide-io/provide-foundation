# provide/foundation/cli/click/builder.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Click command group builder and orchestration.

Main orchestrator for building Click CLI groups from registered commands.
Coordinates parameter processing, command building, and group hierarchy.
"""

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_create_command_group__mutmut_orig(  # noqa: C901
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


def x_create_command_group__mutmut_1(  # noqa: C901
    name: str = "XXcliXX",
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


def x_create_command_group__mutmut_2(  # noqa: C901
    name: str = "CLI",
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


def x_create_command_group__mutmut_3(  # noqa: C901
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

    reg = None

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


def x_create_command_group__mutmut_4(  # noqa: C901
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

    reg = registry and get_command_registry()

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


def x_create_command_group__mutmut_5(  # noqa: C901
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
        group = None
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


def x_create_command_group__mutmut_6(  # noqa: C901
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
        group = click.Group(name=None, **kwargs)
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


def x_create_command_group__mutmut_7(  # noqa: C901
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
        group = click.Group(**kwargs)
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


def x_create_command_group__mutmut_8(  # noqa: C901
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
        group = click.Group(name=name, )
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


def x_create_command_group__mutmut_9(  # noqa: C901
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
        groups: dict[str, Group] = None

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


def x_create_command_group__mutmut_10(  # noqa: C901
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
        if commands is not None:
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


def x_create_command_group__mutmut_11(  # noqa: C901
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
            commands = None

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


def x_create_command_group__mutmut_12(  # noqa: C901
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
            commands = reg.list_dimension(None)

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


def x_create_command_group__mutmut_13(  # noqa: C901
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
        sorted_commands = None

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


def x_create_command_group__mutmut_14(  # noqa: C901
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
        sorted_commands = sorted(None, key=lambda x: x.count("."))

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


def x_create_command_group__mutmut_15(  # noqa: C901
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
        sorted_commands = sorted(commands, key=None)

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


def x_create_command_group__mutmut_16(  # noqa: C901
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
        sorted_commands = sorted(key=lambda x: x.count("."))

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


def x_create_command_group__mutmut_17(  # noqa: C901
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
        sorted_commands = sorted(commands, )

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


def x_create_command_group__mutmut_18(  # noqa: C901
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
        sorted_commands = sorted(commands, key=lambda x: None)

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


def x_create_command_group__mutmut_19(  # noqa: C901
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
        sorted_commands = sorted(commands, key=lambda x: x.count(None))

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


def x_create_command_group__mutmut_20(  # noqa: C901
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
        sorted_commands = sorted(commands, key=lambda x: x.count("XX.XX"))

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


def x_create_command_group__mutmut_21(  # noqa: C901
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
            entry = None
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


def x_create_command_group__mutmut_22(  # noqa: C901
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
            entry = reg.get_entry(None, dimension=ComponentCategory.COMMAND.value)
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


def x_create_command_group__mutmut_23(  # noqa: C901
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
            entry = reg.get_entry(cmd_name, dimension=None)
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


def x_create_command_group__mutmut_24(  # noqa: C901
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
            entry = reg.get_entry(dimension=ComponentCategory.COMMAND.value)
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


def x_create_command_group__mutmut_25(  # noqa: C901
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
            entry = reg.get_entry(cmd_name, )
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


def x_create_command_group__mutmut_26(  # noqa: C901
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
            if should_skip_entry(None):
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


def x_create_command_group__mutmut_27(  # noqa: C901
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
                break

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


def x_create_command_group__mutmut_28(  # noqa: C901
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
            if entry or entry.metadata.get("is_group"):
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


def x_create_command_group__mutmut_29(  # noqa: C901
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
            if entry and entry.metadata.get(None):
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


def x_create_command_group__mutmut_30(  # noqa: C901
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
            if entry and entry.metadata.get("XXis_groupXX"):
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


def x_create_command_group__mutmut_31(  # noqa: C901
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
            if entry and entry.metadata.get("IS_GROUP"):
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


def x_create_command_group__mutmut_32(  # noqa: C901
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
                create_subgroup(None, entry, groups, group)

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


def x_create_command_group__mutmut_33(  # noqa: C901
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
                create_subgroup(cmd_name, None, groups, group)

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


def x_create_command_group__mutmut_34(  # noqa: C901
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
                create_subgroup(cmd_name, entry, None, group)

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


def x_create_command_group__mutmut_35(  # noqa: C901
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
                create_subgroup(cmd_name, entry, groups, None)

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


def x_create_command_group__mutmut_36(  # noqa: C901
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
                create_subgroup(entry, groups, group)

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


def x_create_command_group__mutmut_37(  # noqa: C901
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
                create_subgroup(cmd_name, groups, group)

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


def x_create_command_group__mutmut_38(  # noqa: C901
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
                create_subgroup(cmd_name, entry, group)

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


def x_create_command_group__mutmut_39(  # noqa: C901
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
                create_subgroup(cmd_name, entry, groups, )

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


def x_create_command_group__mutmut_40(  # noqa: C901
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
            entry = None
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


def x_create_command_group__mutmut_41(  # noqa: C901
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
            entry = reg.get_entry(None, dimension=ComponentCategory.COMMAND.value)
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


def x_create_command_group__mutmut_42(  # noqa: C901
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
            entry = reg.get_entry(cmd_name, dimension=None)
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


def x_create_command_group__mutmut_43(  # noqa: C901
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
            entry = reg.get_entry(dimension=ComponentCategory.COMMAND.value)
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


def x_create_command_group__mutmut_44(  # noqa: C901
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
            entry = reg.get_entry(cmd_name, )
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


def x_create_command_group__mutmut_45(  # noqa: C901
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
            if should_skip_entry(entry) and should_skip_command(entry):
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


def x_create_command_group__mutmut_46(  # noqa: C901
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
            if should_skip_entry(None) or should_skip_command(entry):
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


def x_create_command_group__mutmut_47(  # noqa: C901
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
            if should_skip_entry(entry) or should_skip_command(None):
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


def x_create_command_group__mutmut_48(  # noqa: C901
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
                break

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


def x_create_command_group__mutmut_49(  # noqa: C901
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

            if entry is None:
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


def x_create_command_group__mutmut_50(  # noqa: C901
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
                info = None
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


def x_create_command_group__mutmut_51(  # noqa: C901
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
                info = entry.metadata.get(None)
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


def x_create_command_group__mutmut_52(  # noqa: C901
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
                info = entry.metadata.get("XXinfoXX")
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


def x_create_command_group__mutmut_53(  # noqa: C901
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
                info = entry.metadata.get("INFO")
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


def x_create_command_group__mutmut_54(  # noqa: C901
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
                    add_command_to_group(None, groups, group, reg)

        return group

    except Exception as e:
        if isinstance(e, CLIBuildError):
            raise
        raise CLIBuildError(
            f"Failed to create Click command group '{name}': {e}",
            group_name=name,
            cause=e,
        ) from e


def x_create_command_group__mutmut_55(  # noqa: C901
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
                    add_command_to_group(info, None, group, reg)

        return group

    except Exception as e:
        if isinstance(e, CLIBuildError):
            raise
        raise CLIBuildError(
            f"Failed to create Click command group '{name}': {e}",
            group_name=name,
            cause=e,
        ) from e


def x_create_command_group__mutmut_56(  # noqa: C901
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
                    add_command_to_group(info, groups, None, reg)

        return group

    except Exception as e:
        if isinstance(e, CLIBuildError):
            raise
        raise CLIBuildError(
            f"Failed to create Click command group '{name}': {e}",
            group_name=name,
            cause=e,
        ) from e


def x_create_command_group__mutmut_57(  # noqa: C901
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
                    add_command_to_group(info, groups, group, None)

        return group

    except Exception as e:
        if isinstance(e, CLIBuildError):
            raise
        raise CLIBuildError(
            f"Failed to create Click command group '{name}': {e}",
            group_name=name,
            cause=e,
        ) from e


def x_create_command_group__mutmut_58(  # noqa: C901
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
                    add_command_to_group(groups, group, reg)

        return group

    except Exception as e:
        if isinstance(e, CLIBuildError):
            raise
        raise CLIBuildError(
            f"Failed to create Click command group '{name}': {e}",
            group_name=name,
            cause=e,
        ) from e


def x_create_command_group__mutmut_59(  # noqa: C901
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
                    add_command_to_group(info, group, reg)

        return group

    except Exception as e:
        if isinstance(e, CLIBuildError):
            raise
        raise CLIBuildError(
            f"Failed to create Click command group '{name}': {e}",
            group_name=name,
            cause=e,
        ) from e


def x_create_command_group__mutmut_60(  # noqa: C901
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
                    add_command_to_group(info, groups, reg)

        return group

    except Exception as e:
        if isinstance(e, CLIBuildError):
            raise
        raise CLIBuildError(
            f"Failed to create Click command group '{name}': {e}",
            group_name=name,
            cause=e,
        ) from e


def x_create_command_group__mutmut_61(  # noqa: C901
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
                    add_command_to_group(info, groups, group, )

        return group

    except Exception as e:
        if isinstance(e, CLIBuildError):
            raise
        raise CLIBuildError(
            f"Failed to create Click command group '{name}': {e}",
            group_name=name,
            cause=e,
        ) from e


def x_create_command_group__mutmut_62(  # noqa: C901
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
            None,
            group_name=name,
            cause=e,
        ) from e


def x_create_command_group__mutmut_63(  # noqa: C901
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
            group_name=None,
            cause=e,
        ) from e


def x_create_command_group__mutmut_64(  # noqa: C901
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
            cause=None,
        ) from e


def x_create_command_group__mutmut_65(  # noqa: C901
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
            group_name=name,
            cause=e,
        ) from e


def x_create_command_group__mutmut_66(  # noqa: C901
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
            cause=e,
        ) from e


def x_create_command_group__mutmut_67(  # noqa: C901
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
            ) from e

x_create_command_group__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_command_group__mutmut_1': x_create_command_group__mutmut_1, 
    'x_create_command_group__mutmut_2': x_create_command_group__mutmut_2, 
    'x_create_command_group__mutmut_3': x_create_command_group__mutmut_3, 
    'x_create_command_group__mutmut_4': x_create_command_group__mutmut_4, 
    'x_create_command_group__mutmut_5': x_create_command_group__mutmut_5, 
    'x_create_command_group__mutmut_6': x_create_command_group__mutmut_6, 
    'x_create_command_group__mutmut_7': x_create_command_group__mutmut_7, 
    'x_create_command_group__mutmut_8': x_create_command_group__mutmut_8, 
    'x_create_command_group__mutmut_9': x_create_command_group__mutmut_9, 
    'x_create_command_group__mutmut_10': x_create_command_group__mutmut_10, 
    'x_create_command_group__mutmut_11': x_create_command_group__mutmut_11, 
    'x_create_command_group__mutmut_12': x_create_command_group__mutmut_12, 
    'x_create_command_group__mutmut_13': x_create_command_group__mutmut_13, 
    'x_create_command_group__mutmut_14': x_create_command_group__mutmut_14, 
    'x_create_command_group__mutmut_15': x_create_command_group__mutmut_15, 
    'x_create_command_group__mutmut_16': x_create_command_group__mutmut_16, 
    'x_create_command_group__mutmut_17': x_create_command_group__mutmut_17, 
    'x_create_command_group__mutmut_18': x_create_command_group__mutmut_18, 
    'x_create_command_group__mutmut_19': x_create_command_group__mutmut_19, 
    'x_create_command_group__mutmut_20': x_create_command_group__mutmut_20, 
    'x_create_command_group__mutmut_21': x_create_command_group__mutmut_21, 
    'x_create_command_group__mutmut_22': x_create_command_group__mutmut_22, 
    'x_create_command_group__mutmut_23': x_create_command_group__mutmut_23, 
    'x_create_command_group__mutmut_24': x_create_command_group__mutmut_24, 
    'x_create_command_group__mutmut_25': x_create_command_group__mutmut_25, 
    'x_create_command_group__mutmut_26': x_create_command_group__mutmut_26, 
    'x_create_command_group__mutmut_27': x_create_command_group__mutmut_27, 
    'x_create_command_group__mutmut_28': x_create_command_group__mutmut_28, 
    'x_create_command_group__mutmut_29': x_create_command_group__mutmut_29, 
    'x_create_command_group__mutmut_30': x_create_command_group__mutmut_30, 
    'x_create_command_group__mutmut_31': x_create_command_group__mutmut_31, 
    'x_create_command_group__mutmut_32': x_create_command_group__mutmut_32, 
    'x_create_command_group__mutmut_33': x_create_command_group__mutmut_33, 
    'x_create_command_group__mutmut_34': x_create_command_group__mutmut_34, 
    'x_create_command_group__mutmut_35': x_create_command_group__mutmut_35, 
    'x_create_command_group__mutmut_36': x_create_command_group__mutmut_36, 
    'x_create_command_group__mutmut_37': x_create_command_group__mutmut_37, 
    'x_create_command_group__mutmut_38': x_create_command_group__mutmut_38, 
    'x_create_command_group__mutmut_39': x_create_command_group__mutmut_39, 
    'x_create_command_group__mutmut_40': x_create_command_group__mutmut_40, 
    'x_create_command_group__mutmut_41': x_create_command_group__mutmut_41, 
    'x_create_command_group__mutmut_42': x_create_command_group__mutmut_42, 
    'x_create_command_group__mutmut_43': x_create_command_group__mutmut_43, 
    'x_create_command_group__mutmut_44': x_create_command_group__mutmut_44, 
    'x_create_command_group__mutmut_45': x_create_command_group__mutmut_45, 
    'x_create_command_group__mutmut_46': x_create_command_group__mutmut_46, 
    'x_create_command_group__mutmut_47': x_create_command_group__mutmut_47, 
    'x_create_command_group__mutmut_48': x_create_command_group__mutmut_48, 
    'x_create_command_group__mutmut_49': x_create_command_group__mutmut_49, 
    'x_create_command_group__mutmut_50': x_create_command_group__mutmut_50, 
    'x_create_command_group__mutmut_51': x_create_command_group__mutmut_51, 
    'x_create_command_group__mutmut_52': x_create_command_group__mutmut_52, 
    'x_create_command_group__mutmut_53': x_create_command_group__mutmut_53, 
    'x_create_command_group__mutmut_54': x_create_command_group__mutmut_54, 
    'x_create_command_group__mutmut_55': x_create_command_group__mutmut_55, 
    'x_create_command_group__mutmut_56': x_create_command_group__mutmut_56, 
    'x_create_command_group__mutmut_57': x_create_command_group__mutmut_57, 
    'x_create_command_group__mutmut_58': x_create_command_group__mutmut_58, 
    'x_create_command_group__mutmut_59': x_create_command_group__mutmut_59, 
    'x_create_command_group__mutmut_60': x_create_command_group__mutmut_60, 
    'x_create_command_group__mutmut_61': x_create_command_group__mutmut_61, 
    'x_create_command_group__mutmut_62': x_create_command_group__mutmut_62, 
    'x_create_command_group__mutmut_63': x_create_command_group__mutmut_63, 
    'x_create_command_group__mutmut_64': x_create_command_group__mutmut_64, 
    'x_create_command_group__mutmut_65': x_create_command_group__mutmut_65, 
    'x_create_command_group__mutmut_66': x_create_command_group__mutmut_66, 
    'x_create_command_group__mutmut_67': x_create_command_group__mutmut_67
}

def create_command_group(*args, **kwargs):
    result = _mutmut_trampoline(x_create_command_group__mutmut_orig, x_create_command_group__mutmut_mutants, args, kwargs)
    return result 

create_command_group.__signature__ = _mutmut_signature(x_create_command_group__mutmut_orig)
x_create_command_group__mutmut_orig.__name__ = 'x_create_command_group'


# <3 🧱🤝💻🪄
