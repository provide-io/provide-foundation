from __future__ import annotations

import inspect
from typing import Any

import click

from provide.foundation.hub.foundation import get_foundation_logger
from provide.foundation.hub.info import CommandInfo
from provide.foundation.hub.registry import Registry, get_command_registry
from provide.foundation.hub.type_mapping import extract_click_type

"""Click command and group building functions."""


def ensure_parent_groups(parent_path: str, registry: Registry) -> None:
    """Ensure all parent groups in the path exist, creating them if needed."""
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

            get_foundation_logger().debug(f"Auto-created group: {group_path}")


def _separate_arguments_and_options(
    sig: inspect.Signature,
) -> tuple[list[tuple[str, inspect.Parameter]], list[tuple[str, inspect.Parameter]]]:
    """Separate function parameters into arguments and options."""
    params = list(sig.parameters.items())
    arguments = []
    options = []

    for param_name, param in params:
        if param_name in ("self", "cls", "ctx"):
            continue

        has_default = param.default != inspect.Parameter.empty
        if has_default:
            options.append((param_name, param))
        else:
            arguments.append((param_name, param))

    return arguments, options


def _apply_click_option(func: Any, param_name: str, param: inspect.Parameter) -> Any:
    """Apply a Click option decorator to a function."""
    option_name = f"--{param_name.replace('_', '-')}"

    if param.annotation != inspect.Parameter.empty:
        # Extract the actual type from unions/optionals
        param_type = extract_click_type(param.annotation)

        # Use type annotation
        if param_type is bool:
            return click.option(
                option_name,
                is_flag=True,
                default=param.default,
                help=f"{param_name} flag",
            )(func)
        else:
            return click.option(
                option_name,
                type=param_type,
                default=param.default,
                help=f"{param_name} option",
            )(func)
    else:
        return click.option(
            option_name,
            default=param.default,
            help=f"{param_name} option",
        )(func)


def _apply_click_argument(func: Any, param_name: str, param: inspect.Parameter) -> Any:
    """Apply a Click argument decorator to a function."""
    if param.annotation != inspect.Parameter.empty:
        # Extract the actual type from unions/optionals
        param_type = extract_click_type(param.annotation)
        return click.argument(
            param_name,
            type=param_type,
        )(func)
    else:
        return click.argument(param_name)(func)


def _validate_command_entry(entry: Any) -> CommandInfo | None:
    """Validate and extract command info from registry entry."""
    if not entry:
        return None

    info = entry.metadata.get("info")
    if not info:
        return None

    # If it's already a Click command, return it for special handling
    if info.click_command:
        return info

    if not callable(info.func):
        return None

    return info


def build_click_command(
    name: str,
    registry: Registry | None = None,
) -> click.Command | None:
    """Build a Click command from a registered function.

    This function takes a registered command and converts it to a
    Click command with proper options and arguments based on the
    function signature.

    Args:
        name: Command name in registry
        registry: Custom registry (defaults to global)

    Returns:
        Click Command or None if not found

    Example:
        >>> @register_command("greet")
        >>> def greet(name: str = "World"):
        >>>     print(f"Hello, {name}!")
        >>>
        >>> click_cmd = build_click_command("greet")
        >>> # Now click_cmd can be added to a Click group

    """
    reg = registry or get_command_registry()
    entry = reg.get_entry(name, dimension="command")

    info = _validate_command_entry(entry)
    if not info:
        return None

    # If it's already a Click command, return it
    if info.click_command:
        return info.click_command

    # Build Click command from function signature
    sig = inspect.signature(info.func)
    arguments, options = _separate_arguments_and_options(sig)

    # Start with the base function
    decorated_func = info.func

    # Process options in reverse order (for decorator stacking)
    for param_name, param in reversed(options):
        decorated_func = _apply_click_option(decorated_func, param_name, param)

    # Process arguments in reverse order
    # When we apply decorators programmatically, the last one applied
    # becomes the outermost decorator, which Click sees first
    for param_name, param in reversed(arguments):
        decorated_func = _apply_click_argument(decorated_func, param_name, param)

    # Create the Click command with the decorated function
    cmd = click.Command(
        name=info.name,
        callback=decorated_func,
        help=info.description,
        hidden=info.hidden,
    )

    # Copy over the params from the decorated function (Click stores them there)
    # Note: Click params are in reverse order of decoration, but for the Command
    # we need them in the correct positional order
    if hasattr(decorated_func, "__click_params__"):
        cmd.params = list(reversed(decorated_func.__click_params__))

    return cmd


def _create_subgroup(
    cmd_name: str, entry: Any, groups: dict[str, click.Group], root_group: click.Group
) -> None:
    """Create a Click subgroup and add it to the appropriate parent."""
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
    cmd_name: str, entry: Any, groups: dict[str, click.Group], root_group: click.Group, registry: Registry
) -> None:
    """Build and add a Click command to the appropriate group."""
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
    """Check if an entry should be skipped during processing."""
    if not entry:
        return True

    info = entry.metadata.get("info")
    return not info


def _should_skip_command(entry: Any) -> bool:
    """Check if a command entry should be skipped (hidden or is a group)."""
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
    reg = registry or get_command_registry()
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
        if entry.metadata.get("is_group"):
            _create_subgroup(cmd_name, entry, groups, group)

    # Second pass: add commands to groups
    for cmd_name in sorted_commands:
        entry = reg.get_entry(cmd_name, dimension="command")
        if _should_skip_entry(entry) or _should_skip_command(entry):
            continue

        _add_command_to_group(cmd_name, entry, groups, group, reg)

    return group


__all__ = [
    "build_click_command",
    "create_command_group",
    "ensure_parent_groups",
]
