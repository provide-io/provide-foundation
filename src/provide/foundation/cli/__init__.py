"""
Foundation CLI utilities for consistent command-line interfaces.

Provides standard decorators, utilities, and patterns for building
CLI tools in the provide-io ecosystem.
"""

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
from provide.foundation.cli.testing import (
    CliTestCase,
    MockContext,
    create_test_cli,
    isolated_cli_runner,
    mock_logger,
    temp_config_file,
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

__all__ = [
    # Decorators
    "logging_options",
    "config_options",
    "output_options",
    "flexible_options",
    "standard_options",
    "error_handler",
    "pass_context",
    "version_option",
    # Utilities
    "echo_json",
    "echo_error",
    "echo_success",
    "echo_warning",
    "echo_info",
    "setup_cli_logging",
    "create_cli_context",
    # Testing
    "CliTestRunner",
    "assert_cli_success",
    "assert_cli_error",
    "MockContext",
    "isolated_cli_runner",
    "temp_config_file",
    "create_test_cli",
    "mock_logger",
    "CliTestCase",
]
