#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Demonstrates exception logging with automatic traceback inclusion."""

from pathlib import Path
import sys

# Add src to path for examples
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent  # Go up from examples to project root
# Line removed - project_root already set above
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from typing import Never

from provide.foundation import get_hub, logger
from provide.foundation.console.output import pout
from provide.foundation.logger.config import (
    LoggingConfig,
    TelemetryConfig,
)


def example_5_exception_handling() -> None:
    """Example 5: Demonstrates logging exceptions with tracebacks.

    The `logger.exception()` method automatically captures and logs the current
    exception's traceback information along with the error message.
    """
    pout("\n" + "=" * 60)
    pout("💥 Example 5: Exception Handling")
    pout(" Demonstrates: Using logger.exception() to log errors with tracebacks.")
    pout("=" * 60)

    get_hub().initialize_foundation(
        TelemetryConfig(
            logging=LoggingConfig(default_level="INFO"),
        ),
    )

    def risky_operation() -> Never:
        """A function that is expected to raise an exception."""
        sub_operation_data = {"sub_key": "sub_value"}
        raise ValueError(
            f"Something went wrong in the operation with data: {sub_operation_data}",
        )

    def another_risky_operation() -> Never:
        """Another function that raises a different exception."""
        raise ConnectionError("Failed to connect to external service 'alpha'.")

    # Exception logging with full traceback
    try:
        risky_operation()
    except Exception:  # Catches ValueError
        logger.exception(
            "Operation failed unexpectedly",
            operation_name="risky_operation",
            user_id="user_xyz",
        )

    try:
        another_risky_operation()
    except Exception:  # Catches ConnectionError
        logger.exception(
            "Connection error occurred while contacting external API",
            domain="network",
            action="connect",
            status="error",
            target_service="external_api_alpha",
        )


if __name__ == "__main__":
    example_5_exception_handling()

# 🧱🏗️🔚
