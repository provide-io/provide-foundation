# provide/foundation/cli/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.cli.base import CLIAdapter
from provide.foundation.cli.decorators import (
    config_options,
    error_handler,
    flexible_options,
    logging_options,
    output_options,
    pass_context,
    standard_options,
    version_option,
)

# Centralized Click dependency handling
from provide.foundation.cli.deps import _HAS_CLICK, click  # noqa: F401
from provide.foundation.cli.errors import (
    CLIAdapterNotFoundError,
    CLIBuildError,
    CLIError,
    InvalidCLIHintError,
)
from provide.foundation.cli.utils import (
    CliTestRunner,
    assert_cli_error,
    assert_cli_success,
    create_cli_context,
    echo_error,
    echo_info,
    echo_json,
    echo_success,
    echo_warning,
    setup_cli_logging,
)

"""Foundation CLI Subsystem.

Provides a framework for building command-line interfaces through a
framework-agnostic adapter pattern. It defines the structure and lifecycle
for CLI applications, into which user-defined commands are plugged.
"""

__all__ = [
    # Dependency flags
    "_HAS_CLICK",
    # Adapter system
    "CLIAdapter",
    "CLIAdapterNotFoundError",
    "CLIBuildError",
    "CLIError",
    # Utilities
    "CliTestRunner",
    "InvalidCLIHintError",
    "assert_cli_error",
    "assert_cli_success",
    # Decorators
    "config_options",
    "create_cli_context",
    "echo_error",
    "echo_info",
    "echo_json",
    "echo_success",
    "echo_warning",
    "error_handler",
    "flexible_options",
    "get_cli_adapter",
    "logging_options",
    "output_options",
    "pass_context",
    "setup_cli_logging",
    "standard_options",
    "version_option",
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


def x_get_cli_adapter__mutmut_orig(framework: str = "click") -> CLIAdapter:
    """Get CLI adapter for specified framework.

    Args:
        framework: CLI framework name ('click', 'typer', etc.)

    Returns:
        CLIAdapter instance for the framework

    Raises:
        CLIAdapterNotFoundError: If framework adapter is not available
        ValueError: If framework name is unknown

    Examples:
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """
    if framework == "click":
        try:
            from provide.foundation.cli.click import ClickAdapter

            return ClickAdapter()
        except ImportError as e:
            if "click" in str(e).lower():
                raise CLIAdapterNotFoundError(
                    framework="click",
                    package="cli",
                ) from e
            raise

    raise ValueError(f"Unknown CLI framework: {framework}. Supported frameworks: click")


def x_get_cli_adapter__mutmut_1(framework: str = "XXclickXX") -> CLIAdapter:
    """Get CLI adapter for specified framework.

    Args:
        framework: CLI framework name ('click', 'typer', etc.)

    Returns:
        CLIAdapter instance for the framework

    Raises:
        CLIAdapterNotFoundError: If framework adapter is not available
        ValueError: If framework name is unknown

    Examples:
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """
    if framework == "click":
        try:
            from provide.foundation.cli.click import ClickAdapter

            return ClickAdapter()
        except ImportError as e:
            if "click" in str(e).lower():
                raise CLIAdapterNotFoundError(
                    framework="click",
                    package="cli",
                ) from e
            raise

    raise ValueError(f"Unknown CLI framework: {framework}. Supported frameworks: click")


def x_get_cli_adapter__mutmut_2(framework: str = "CLICK") -> CLIAdapter:
    """Get CLI adapter for specified framework.

    Args:
        framework: CLI framework name ('click', 'typer', etc.)

    Returns:
        CLIAdapter instance for the framework

    Raises:
        CLIAdapterNotFoundError: If framework adapter is not available
        ValueError: If framework name is unknown

    Examples:
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """
    if framework == "click":
        try:
            from provide.foundation.cli.click import ClickAdapter

            return ClickAdapter()
        except ImportError as e:
            if "click" in str(e).lower():
                raise CLIAdapterNotFoundError(
                    framework="click",
                    package="cli",
                ) from e
            raise

    raise ValueError(f"Unknown CLI framework: {framework}. Supported frameworks: click")


def x_get_cli_adapter__mutmut_3(framework: str = "click") -> CLIAdapter:
    """Get CLI adapter for specified framework.

    Args:
        framework: CLI framework name ('click', 'typer', etc.)

    Returns:
        CLIAdapter instance for the framework

    Raises:
        CLIAdapterNotFoundError: If framework adapter is not available
        ValueError: If framework name is unknown

    Examples:
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """
    if framework != "click":
        try:
            from provide.foundation.cli.click import ClickAdapter

            return ClickAdapter()
        except ImportError as e:
            if "click" in str(e).lower():
                raise CLIAdapterNotFoundError(
                    framework="click",
                    package="cli",
                ) from e
            raise

    raise ValueError(f"Unknown CLI framework: {framework}. Supported frameworks: click")


def x_get_cli_adapter__mutmut_4(framework: str = "click") -> CLIAdapter:
    """Get CLI adapter for specified framework.

    Args:
        framework: CLI framework name ('click', 'typer', etc.)

    Returns:
        CLIAdapter instance for the framework

    Raises:
        CLIAdapterNotFoundError: If framework adapter is not available
        ValueError: If framework name is unknown

    Examples:
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """
    if framework == "XXclickXX":
        try:
            from provide.foundation.cli.click import ClickAdapter

            return ClickAdapter()
        except ImportError as e:
            if "click" in str(e).lower():
                raise CLIAdapterNotFoundError(
                    framework="click",
                    package="cli",
                ) from e
            raise

    raise ValueError(f"Unknown CLI framework: {framework}. Supported frameworks: click")


def x_get_cli_adapter__mutmut_5(framework: str = "click") -> CLIAdapter:
    """Get CLI adapter for specified framework.

    Args:
        framework: CLI framework name ('click', 'typer', etc.)

    Returns:
        CLIAdapter instance for the framework

    Raises:
        CLIAdapterNotFoundError: If framework adapter is not available
        ValueError: If framework name is unknown

    Examples:
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """
    if framework == "CLICK":
        try:
            from provide.foundation.cli.click import ClickAdapter

            return ClickAdapter()
        except ImportError as e:
            if "click" in str(e).lower():
                raise CLIAdapterNotFoundError(
                    framework="click",
                    package="cli",
                ) from e
            raise

    raise ValueError(f"Unknown CLI framework: {framework}. Supported frameworks: click")


def x_get_cli_adapter__mutmut_6(framework: str = "click") -> CLIAdapter:
    """Get CLI adapter for specified framework.

    Args:
        framework: CLI framework name ('click', 'typer', etc.)

    Returns:
        CLIAdapter instance for the framework

    Raises:
        CLIAdapterNotFoundError: If framework adapter is not available
        ValueError: If framework name is unknown

    Examples:
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """
    if framework == "click":
        try:
            from provide.foundation.cli.click import ClickAdapter

            return ClickAdapter()
        except ImportError as e:
            if "XXclickXX" in str(e).lower():
                raise CLIAdapterNotFoundError(
                    framework="click",
                    package="cli",
                ) from e
            raise

    raise ValueError(f"Unknown CLI framework: {framework}. Supported frameworks: click")


def x_get_cli_adapter__mutmut_7(framework: str = "click") -> CLIAdapter:
    """Get CLI adapter for specified framework.

    Args:
        framework: CLI framework name ('click', 'typer', etc.)

    Returns:
        CLIAdapter instance for the framework

    Raises:
        CLIAdapterNotFoundError: If framework adapter is not available
        ValueError: If framework name is unknown

    Examples:
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """
    if framework == "click":
        try:
            from provide.foundation.cli.click import ClickAdapter

            return ClickAdapter()
        except ImportError as e:
            if "CLICK" in str(e).lower():
                raise CLIAdapterNotFoundError(
                    framework="click",
                    package="cli",
                ) from e
            raise

    raise ValueError(f"Unknown CLI framework: {framework}. Supported frameworks: click")


def x_get_cli_adapter__mutmut_8(framework: str = "click") -> CLIAdapter:
    """Get CLI adapter for specified framework.

    Args:
        framework: CLI framework name ('click', 'typer', etc.)

    Returns:
        CLIAdapter instance for the framework

    Raises:
        CLIAdapterNotFoundError: If framework adapter is not available
        ValueError: If framework name is unknown

    Examples:
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """
    if framework == "click":
        try:
            from provide.foundation.cli.click import ClickAdapter

            return ClickAdapter()
        except ImportError as e:
            if "click" not in str(e).lower():
                raise CLIAdapterNotFoundError(
                    framework="click",
                    package="cli",
                ) from e
            raise

    raise ValueError(f"Unknown CLI framework: {framework}. Supported frameworks: click")


def x_get_cli_adapter__mutmut_9(framework: str = "click") -> CLIAdapter:
    """Get CLI adapter for specified framework.

    Args:
        framework: CLI framework name ('click', 'typer', etc.)

    Returns:
        CLIAdapter instance for the framework

    Raises:
        CLIAdapterNotFoundError: If framework adapter is not available
        ValueError: If framework name is unknown

    Examples:
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """
    if framework == "click":
        try:
            from provide.foundation.cli.click import ClickAdapter

            return ClickAdapter()
        except ImportError as e:
            if "click" in str(e).upper():
                raise CLIAdapterNotFoundError(
                    framework="click",
                    package="cli",
                ) from e
            raise

    raise ValueError(f"Unknown CLI framework: {framework}. Supported frameworks: click")


def x_get_cli_adapter__mutmut_10(framework: str = "click") -> CLIAdapter:
    """Get CLI adapter for specified framework.

    Args:
        framework: CLI framework name ('click', 'typer', etc.)

    Returns:
        CLIAdapter instance for the framework

    Raises:
        CLIAdapterNotFoundError: If framework adapter is not available
        ValueError: If framework name is unknown

    Examples:
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """
    if framework == "click":
        try:
            from provide.foundation.cli.click import ClickAdapter

            return ClickAdapter()
        except ImportError as e:
            if "click" in str(None).lower():
                raise CLIAdapterNotFoundError(
                    framework="click",
                    package="cli",
                ) from e
            raise

    raise ValueError(f"Unknown CLI framework: {framework}. Supported frameworks: click")


def x_get_cli_adapter__mutmut_11(framework: str = "click") -> CLIAdapter:
    """Get CLI adapter for specified framework.

    Args:
        framework: CLI framework name ('click', 'typer', etc.)

    Returns:
        CLIAdapter instance for the framework

    Raises:
        CLIAdapterNotFoundError: If framework adapter is not available
        ValueError: If framework name is unknown

    Examples:
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """
    if framework == "click":
        try:
            from provide.foundation.cli.click import ClickAdapter

            return ClickAdapter()
        except ImportError as e:
            if "click" in str(e).lower():
                raise CLIAdapterNotFoundError(
                    framework=None,
                    package="cli",
                ) from e
            raise

    raise ValueError(f"Unknown CLI framework: {framework}. Supported frameworks: click")


def x_get_cli_adapter__mutmut_12(framework: str = "click") -> CLIAdapter:
    """Get CLI adapter for specified framework.

    Args:
        framework: CLI framework name ('click', 'typer', etc.)

    Returns:
        CLIAdapter instance for the framework

    Raises:
        CLIAdapterNotFoundError: If framework adapter is not available
        ValueError: If framework name is unknown

    Examples:
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """
    if framework == "click":
        try:
            from provide.foundation.cli.click import ClickAdapter

            return ClickAdapter()
        except ImportError as e:
            if "click" in str(e).lower():
                raise CLIAdapterNotFoundError(
                    framework="click",
                    package=None,
                ) from e
            raise

    raise ValueError(f"Unknown CLI framework: {framework}. Supported frameworks: click")


def x_get_cli_adapter__mutmut_13(framework: str = "click") -> CLIAdapter:
    """Get CLI adapter for specified framework.

    Args:
        framework: CLI framework name ('click', 'typer', etc.)

    Returns:
        CLIAdapter instance for the framework

    Raises:
        CLIAdapterNotFoundError: If framework adapter is not available
        ValueError: If framework name is unknown

    Examples:
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """
    if framework == "click":
        try:
            from provide.foundation.cli.click import ClickAdapter

            return ClickAdapter()
        except ImportError as e:
            if "click" in str(e).lower():
                raise CLIAdapterNotFoundError(
                    package="cli",
                ) from e
            raise

    raise ValueError(f"Unknown CLI framework: {framework}. Supported frameworks: click")


def x_get_cli_adapter__mutmut_14(framework: str = "click") -> CLIAdapter:
    """Get CLI adapter for specified framework.

    Args:
        framework: CLI framework name ('click', 'typer', etc.)

    Returns:
        CLIAdapter instance for the framework

    Raises:
        CLIAdapterNotFoundError: If framework adapter is not available
        ValueError: If framework name is unknown

    Examples:
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """
    if framework == "click":
        try:
            from provide.foundation.cli.click import ClickAdapter

            return ClickAdapter()
        except ImportError as e:
            if "click" in str(e).lower():
                raise CLIAdapterNotFoundError(
                    framework="click",
                    ) from e
            raise

    raise ValueError(f"Unknown CLI framework: {framework}. Supported frameworks: click")


def x_get_cli_adapter__mutmut_15(framework: str = "click") -> CLIAdapter:
    """Get CLI adapter for specified framework.

    Args:
        framework: CLI framework name ('click', 'typer', etc.)

    Returns:
        CLIAdapter instance for the framework

    Raises:
        CLIAdapterNotFoundError: If framework adapter is not available
        ValueError: If framework name is unknown

    Examples:
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """
    if framework == "click":
        try:
            from provide.foundation.cli.click import ClickAdapter

            return ClickAdapter()
        except ImportError as e:
            if "click" in str(e).lower():
                raise CLIAdapterNotFoundError(
                    framework="XXclickXX",
                    package="cli",
                ) from e
            raise

    raise ValueError(f"Unknown CLI framework: {framework}. Supported frameworks: click")


def x_get_cli_adapter__mutmut_16(framework: str = "click") -> CLIAdapter:
    """Get CLI adapter for specified framework.

    Args:
        framework: CLI framework name ('click', 'typer', etc.)

    Returns:
        CLIAdapter instance for the framework

    Raises:
        CLIAdapterNotFoundError: If framework adapter is not available
        ValueError: If framework name is unknown

    Examples:
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """
    if framework == "click":
        try:
            from provide.foundation.cli.click import ClickAdapter

            return ClickAdapter()
        except ImportError as e:
            if "click" in str(e).lower():
                raise CLIAdapterNotFoundError(
                    framework="CLICK",
                    package="cli",
                ) from e
            raise

    raise ValueError(f"Unknown CLI framework: {framework}. Supported frameworks: click")


def x_get_cli_adapter__mutmut_17(framework: str = "click") -> CLIAdapter:
    """Get CLI adapter for specified framework.

    Args:
        framework: CLI framework name ('click', 'typer', etc.)

    Returns:
        CLIAdapter instance for the framework

    Raises:
        CLIAdapterNotFoundError: If framework adapter is not available
        ValueError: If framework name is unknown

    Examples:
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """
    if framework == "click":
        try:
            from provide.foundation.cli.click import ClickAdapter

            return ClickAdapter()
        except ImportError as e:
            if "click" in str(e).lower():
                raise CLIAdapterNotFoundError(
                    framework="click",
                    package="XXcliXX",
                ) from e
            raise

    raise ValueError(f"Unknown CLI framework: {framework}. Supported frameworks: click")


def x_get_cli_adapter__mutmut_18(framework: str = "click") -> CLIAdapter:
    """Get CLI adapter for specified framework.

    Args:
        framework: CLI framework name ('click', 'typer', etc.)

    Returns:
        CLIAdapter instance for the framework

    Raises:
        CLIAdapterNotFoundError: If framework adapter is not available
        ValueError: If framework name is unknown

    Examples:
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """
    if framework == "click":
        try:
            from provide.foundation.cli.click import ClickAdapter

            return ClickAdapter()
        except ImportError as e:
            if "click" in str(e).lower():
                raise CLIAdapterNotFoundError(
                    framework="click",
                    package="CLI",
                ) from e
            raise

    raise ValueError(f"Unknown CLI framework: {framework}. Supported frameworks: click")


def x_get_cli_adapter__mutmut_19(framework: str = "click") -> CLIAdapter:
    """Get CLI adapter for specified framework.

    Args:
        framework: CLI framework name ('click', 'typer', etc.)

    Returns:
        CLIAdapter instance for the framework

    Raises:
        CLIAdapterNotFoundError: If framework adapter is not available
        ValueError: If framework name is unknown

    Examples:
        >>> adapter = get_cli_adapter('click')
        >>> command = adapter.build_command(command_info)

    """
    if framework == "click":
        try:
            from provide.foundation.cli.click import ClickAdapter

            return ClickAdapter()
        except ImportError as e:
            if "click" in str(e).lower():
                raise CLIAdapterNotFoundError(
                    framework="click",
                    package="cli",
                ) from e
            raise

    raise ValueError(None)

x_get_cli_adapter__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_cli_adapter__mutmut_1': x_get_cli_adapter__mutmut_1, 
    'x_get_cli_adapter__mutmut_2': x_get_cli_adapter__mutmut_2, 
    'x_get_cli_adapter__mutmut_3': x_get_cli_adapter__mutmut_3, 
    'x_get_cli_adapter__mutmut_4': x_get_cli_adapter__mutmut_4, 
    'x_get_cli_adapter__mutmut_5': x_get_cli_adapter__mutmut_5, 
    'x_get_cli_adapter__mutmut_6': x_get_cli_adapter__mutmut_6, 
    'x_get_cli_adapter__mutmut_7': x_get_cli_adapter__mutmut_7, 
    'x_get_cli_adapter__mutmut_8': x_get_cli_adapter__mutmut_8, 
    'x_get_cli_adapter__mutmut_9': x_get_cli_adapter__mutmut_9, 
    'x_get_cli_adapter__mutmut_10': x_get_cli_adapter__mutmut_10, 
    'x_get_cli_adapter__mutmut_11': x_get_cli_adapter__mutmut_11, 
    'x_get_cli_adapter__mutmut_12': x_get_cli_adapter__mutmut_12, 
    'x_get_cli_adapter__mutmut_13': x_get_cli_adapter__mutmut_13, 
    'x_get_cli_adapter__mutmut_14': x_get_cli_adapter__mutmut_14, 
    'x_get_cli_adapter__mutmut_15': x_get_cli_adapter__mutmut_15, 
    'x_get_cli_adapter__mutmut_16': x_get_cli_adapter__mutmut_16, 
    'x_get_cli_adapter__mutmut_17': x_get_cli_adapter__mutmut_17, 
    'x_get_cli_adapter__mutmut_18': x_get_cli_adapter__mutmut_18, 
    'x_get_cli_adapter__mutmut_19': x_get_cli_adapter__mutmut_19
}

def get_cli_adapter(*args, **kwargs):
    result = _mutmut_trampoline(x_get_cli_adapter__mutmut_orig, x_get_cli_adapter__mutmut_mutants, args, kwargs)
    return result 

get_cli_adapter.__signature__ = _mutmut_signature(x_get_cli_adapter__mutmut_orig)
x_get_cli_adapter__mutmut_orig.__name__ = 'x_get_cli_adapter'


# <3 🧱🤝💻🪄
