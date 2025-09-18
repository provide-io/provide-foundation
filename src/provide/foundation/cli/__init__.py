from __future__ import annotations

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

"""Foundation CLI utilities for consistent command-line interfaces.

Provides standard decorators, utilities, and patterns for building
CLI tools in the provide-io ecosystem.
"""

__all__ = [
    # Utilities
    "CliTestRunner",
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
    "logging_options",
    "output_options",
    "pass_context",
    "setup_cli_logging",
    "standard_options",
    "version_option",
]
