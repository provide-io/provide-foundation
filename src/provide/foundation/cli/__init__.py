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
    create_test_cli,
    isolated_cli_runner,
    temp_config_file,
)
from provide.foundation.testing.cli import MockContext
from provide.foundation.testing.logger import mock_logger
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
    "CliTestCase",
    # Testing
    "CliTestRunner",
    "MockContext",
    "assert_cli_error",
    "assert_cli_success",
    "config_options",
    "create_cli_context",
    "create_test_cli",
    "echo_error",
    "echo_info",
    # Utilities
    "echo_json",
    "echo_success",
    "echo_warning",
    "error_handler",
    "flexible_options",
    "isolated_cli_runner",
    # Decorators
    "logging_options",
    "mock_logger",
    "output_options",
    "pass_context",
    "setup_cli_logging",
    "standard_options",
    "temp_config_file",
    "version_option",
]
