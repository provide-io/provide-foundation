"""Click command and group building functions.

Builds Click CLI commands from framework-agnostic CommandInfo objects.
Supports typing.Annotated for explicit argument/option control.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import click

from provide.foundation import logger
from provide.foundation.cli.errors import CLIBuildError
from provide.foundation.hub.introspection import ParameterInfo, introspect_parameters

if TYPE_CHECKING:
    from provide.foundation.hub.info import CommandInfo
    from provide.foundation.hub.registry import Registry

__all__ = [
    "build_click_command",
    "create_command_group",
    "ensure_parent_groups",
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
        if not registry.get_entry(registry_key, dimension="command"):
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
                dimension="command",
                metadata={
                    "info": info,
                    "description": info.description,
                    "parent": parent,
                    "is_group": True,
                    "auto_created": True,
                },
            )

            logger.debug(f"Auto-created group: {group_path}")


def _separate_arguments_and_options(
    params: list[ParameterInfo],
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options based on hints and defaults.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default → option

    Args:
        params: List of ParameterInfo objects

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = []
    options = []

    for param in params:
        if param.cli_hint == "argument":
            # Explicitly marked as argument
            arguments.append(param)
        elif param.cli_hint == "option":
            # Explicitly marked as option
            options.append(param)
        elif param.has_default:
            # No explicit hint, has default → option
            options.append(param)
        else:
            # No explicit hint, no default → argument
            arguments.append(param)

    return arguments, options


def _apply_click_option(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def _apply_click_argument(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click argument decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    # Arguments can have defaults (makes them optional in Click)
    if param.has_default:
        return click.argument(
            param.name,
            type=param.concrete_type,
            default=param.default,
        )(func)
    else:
        return click.argument(
            param.name,
            type=param.concrete_type,
        )(func)


def _validate_command_entry(entry: Any) -> CommandInfo | None:
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


def build_click_command(
    name: str,
    registry: Registry | None = None,
) -> click.Command | None:
    """Build a Click command from a registered function.

    This function takes a registered command and converts it to a
    Click command with proper options and arguments. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        name: Command name in registry
        registry: Custom registry (defaults to global)

    Returns:
        Click Command or None if not found

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> @register_command("greet")
        >>> def greet(name: Annotated[str, 'option'] = "World"):
        >>>     print(f"Hello, {name}!")
        >>>
        >>> click_cmd = build_click_command("greet")
        >>> # Now click_cmd can be added to a Click group

    """
    from provide.foundation.hub.registry import get_command_registry

    reg = registry or get_command_registry()
    entry = reg.get_entry(name, dimension="command")

    info = _validate_command_entry(entry)
    if not info:
        return None

    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Separate into arguments and options
        arguments, options = _separate_arguments_and_options(params)

        # Start with the base function
        decorated_func = info.func

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = _apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = _apply_click_argument(decorated_func, param)

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

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{name}': {e}",
            command_name=name,
            cause=e,
        ) from e


def _create_subgroup(
    cmd_name: str, entry: Any, groups: dict[str, click.Group], root_group: click.Group
) -> None:
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


def _add_command_to_group(
    cmd_name: str,
    entry: Any,
    groups: dict[str, click.Group],
    root_group: click.Group,
    registry: Registry,
) -> None:
    """Build and add a Click command to the appropriate group.

    Args:
        cmd_name: Command name
        entry: Registry entry
        groups: Dictionary of existing groups
        root_group: Root group
        registry: Command registry

    """
    click_cmd = build_click_command(cmd_name, registry=registry)
    if not click_cmd:
        return

    parent = entry.metadata.get("parent")

    # Update command name if it has a parent
    if parent:
        # Extract the actual command name (without parent prefix)
        parts = cmd_name.split(".")
        parent_parts = parent.split(".")
        # Remove parent parts from command name
        cmd_parts = parts[len(parent_parts) :]
        click_cmd.name = cmd_parts[0] if cmd_parts else parts[-1]

    # Add to parent group or root
    if parent and parent in groups:
        groups[parent].add_command(click_cmd)
    else:
        # Parent not found or no parent, add to root
        root_group.add_command(click_cmd)


def _should_skip_entry(entry: Any) -> bool:
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


def _should_skip_command(entry: Any) -> bool:
    """Check if a command entry should be skipped (hidden or is a group).

    Args:
        entry: Registry entry

    Returns:
        True if command should be skipped

    """
    info = entry.metadata.get("info")
    return not info or info.hidden or entry.metadata.get("is_group")


def create_command_group(
    name: str = "cli",
    commands: list[str] | None = None,
    registry: Registry | None = None,
    **kwargs: Any,
) -> click.Group:
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
        groups: dict[str, click.Group] = {}

        # Get commands to include
        if commands is None:
            commands = reg.list_dimension("command")

        # Sort commands to ensure parents are created before children
        sorted_commands = sorted(commands, key=lambda x: x.count("."))

        # First pass: create all groups
        for cmd_name in sorted_commands:
            entry = reg.get_entry(cmd_name, dimension="command")
            if _should_skip_entry(entry):
                continue

            # Check if this is a group
            if entry and entry.metadata.get("is_group"):
                _create_subgroup(cmd_name, entry, groups, group)

        # Second pass: add commands to groups
        for cmd_name in sorted_commands:
            entry = reg.get_entry(cmd_name, dimension="command")
            if _should_skip_entry(entry) or _should_skip_command(entry):
                continue

            _add_command_to_group(cmd_name, entry, groups, group, reg)

        return group

    except Exception as e:
        if isinstance(e, CLIBuildError):
            raise
        raise CLIBuildError(
            f"Failed to create Click command group '{name}': {e}",
            group_name=name,
            cause=e,
        ) from e
