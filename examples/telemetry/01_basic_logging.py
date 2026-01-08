#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Simple Start Example - Zero Setup Logging

This example demonstrates the simplest possible usage of provide.foundation.
No setup required - just import and use the logger immediately.

Usage:
    uv add provide-foundation
    python examples/telemetry/01_basic_logging.py

Expected output:
    Colored, emoji-prefixed log messages with structured data.

To see INFO-level messages:
    PROVIDE_LOG_LEVEL=INFO python examples/telemetry/01_basic_logging.py"""

from pathlib import Path
import sys

# Add src to path for examples
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent
# Line removed - project_root already set above
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Simple import and immediate usage - no setup needed
from provide.foundation import logger, pout


def simple_logging_example() -> None:
    """Demonstrates the simplest possible logging usage.

    Key points:
    - No setup_telemetry() call needed
    - Works with base install: uv add provide-foundation
    - Automatic initialization on first use
    - Structured logging with emoji prefixes
    """
    pout("\n" + "=" * 60)
    pout("✨ Simple Start - Zero Setup Required")
    pout(" Just import logger and start logging immediately!")
    pout("=" * 60)

    # Start logging immediately - no configuration needed
    logger.info("Hello from provide.foundation!", component="simple_example")

    # Structured logging with context
    logger.info(
        "User session started",
        user_id="user_123",
        session_id="sess_456",
        source="web_app",
    )

    # Different log levels
    logger.debug("Debug information", debug_level=1)
    logger.warning("This is a warning", severity="low")
    logger.error("Something went wrong", error_code="ERR001")

    # Exception logging
    try:
        pass
    except ZeroDivisionError:
        logger.exception("Division by zero occurred", operation="calculate")

    logger.info("Example completed successfully!")


if __name__ == "__main__":
    simple_logging_example()
    pout("\n🎉 That's it! No setup required - logging just works.")
    pout("💡 For advanced features like tracing, see other examples.")

# 🧱🏗️🔚
