#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Click parameter processing and decorator application.

Handles separation of arguments/options and application of Click decorators
based on parameter introspection and type hints."""

from __future__ import annotations

from typing import Any

from provide.foundation.cli.deps import click
from provide.foundation.hub.introspection import ParameterInfo

__all__ = [
    "apply_click_argument",
    "apply_click_option",
    "separate_arguments_and_options",
]


def separate_arguments_and_options(
    params: list[ParameterInfo],
    force_options: bool = False,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

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
        elif not param.has_default:
            # No explicit hint, no default → argument
            arguments.append(param)
        elif param.concrete_type is bool:
            # Boolean parameters always become flags
            options.append(param)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options or arguments or options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(param)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(param)

    return arguments, options


def apply_click_option(func: Any, param: ParameterInfo) -> Any:
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


def apply_click_argument(func: Any, param: ParameterInfo) -> Any:
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


# 🧱🏗️🔚
