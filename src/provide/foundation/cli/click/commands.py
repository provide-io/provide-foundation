"""Click command building and integration.

Builds individual Click commands from CommandInfo objects and integrates
them with Click groups.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from provide.foundation.cli.click.hierarchy import validate_command_entry
from provide.foundation.cli.click.parameters import (
    apply_click_argument,
    apply_click_option,
    separate_arguments_and_options,
)
from provide.foundation.cli.deps import click
from provide.foundation.cli.errors import CLIBuildError
from provide.foundation.hub.categories import ComponentCategory
from provide.foundation.hub.introspection import introspect_parameters

if TYPE_CHECKING:
    from provide.foundation.hub.registry import Registry

__all__ = [
    "add_command_to_group",
    "build_click_command",
    "build_click_command_from_info",
]


def build_click_command_from_info(info: Any) -> click.Command:
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
    entry = reg.get_entry(name, dimension=ComponentCategory.COMMAND.value)

    info = validate_command_entry(entry)
    if not info:
        return None

    # Build the command using the pure builder function
    return build_click_command_from_info(info)


def add_command_to_group(
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
