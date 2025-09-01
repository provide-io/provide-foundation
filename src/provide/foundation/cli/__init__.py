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
)
from provide.foundation.cli.utils import (
    echo_json,
    echo_error,
    echo_success,
    echo_warning,
    echo_info,
    setup_cli_logging,
    create_cli_context,
)

__all__ = [
    # Decorators
    "logging_options",
    "config_options", 
    "output_options",
    "standard_options",
    "error_handler",
    # Utilities
    "echo_json",
    "echo_error",
    "echo_success",
    "echo_warning",
    "echo_info",
    "setup_cli_logging",
    "create_cli_context",
]