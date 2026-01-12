#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Quick Start Example - Structured Logging with Full Setup

This example demonstrates how to use Foundation's Hub-based initialization,
which automatically configures logging, tracing, and metrics. It shows:
- Using Hub.initialize_foundation() for full telemetry configuration
- Different log levels (info, debug, warning, error)
- Structured data in log messages
- When tracing/metrics features are available

Requirements:
    uv add provide-foundation[opentelemetry]  # For tracing/metrics
    # OR
    uv add provide-foundation                 # Basic logging only

Usage:
    python examples/telemetry/02_structured_logging.py

    # Or with custom log level via environment
    PROVIDE_LOG_LEVEL=ERROR python examples/telemetry/02_structured_logging.py

Expected output:
    Colored, emoji-prefixed log messages with optional tracing/metrics setup."""

from pathlib import Path
import sys

# Add src to path for examples
# This allows the example script to find the `provide.foundation` module
# when run directly from the `examples` directory or the project root.
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent  # Go up from examples to project root
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from provide.foundation import get_hub, logger, pout
from provide.foundation.logger.config import (
    LoggingConfig,
    TelemetryConfig,
)


def example_1_quick_start() -> None:
    """Demonstrates basic structured logging with provide.foundation.

    Key concepts:
    - Hub.initialize_foundation() initializes the logging system
    - logger methods accept a message and keyword arguments for structured data
    - Different log levels control what gets displayed
    - Structured data makes logs searchable and analyzable
    """
    pout("\n" + "=" * 60)
    pout("🚀 Example 1: Quick Start")
    pout(" Demonstrates: Logging with full telemetry setup (tracing/metrics).")
    pout(" Note: If OpenTelemetry dependencies are missing, tracing/metrics are disabled.")
    pout("=" * 60)

    # Initialize with INFO level for better visibility in examples
    # This sets up logging + optional tracing/metrics if dependencies available
    hub = get_hub()
    hub.initialize_foundation(
        TelemetryConfig(
            logging=LoggingConfig(default_level="INFO"),
        )
    )

    # Start logging immediately
    logger.info("Application started", version="1.0.0", component="main_app")
    logger.debug("Debugging initial state", state_value=42)
    logger.warning("A potential issue was detected", issue_code="W001")
    logger.error("An error occurred during startup", error_code="E123", critical=False)


if __name__ == "__main__":
    example_1_quick_start()

# 🧱🏗️🔚
