#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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


def get_cli_adapter(framework: str = "click") -> CLIAdapter:
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


# 🧱🏗️🔚
