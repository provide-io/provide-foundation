"""
Foundation CLI utilities for consistent command-line interfaces.

Provides standard decorators, utilities, and patterns for building
CLI tools in the provide-io ecosystem.
"""

from provide.foundation.cli.decorators import (
    logging_options,
    config_options,
    output_options,
    standard_options,
    error_handler,
    pass_context,
    version_option,
)
from provide.foundation.cli.utils import (
    echo_json,
    echo_error,
    echo_success,
    echo_warning,
    echo_info,
    setup_cli_logging,
    create_cli_context,
    CliTestRunner,
    assert_cli_success,
    assert_cli_error,
)
from provide.foundation.cli.testing import (
    MockContext,
    isolated_cli_runner,
    temp_config_file,
    create_test_cli,
    mock_logger,
    CliTestCase,
)

__all__ = [
    # Decorators
    "logging_options",
    "config_options", 
    "output_options",
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