#!/usr/bin/env python3
# examples/01_quick_start.py
"""
Quick Start Example - Structured Logging with Full Setup

This example demonstrates how to use setup_telemetry() to configure logging,
tracing, and metrics. It shows:
- Using setup_telemetry() for full telemetry configuration
- Different log levels (info, debug, warning, error)
- Structured data in log messages
- When tracing/metrics features are available

Requirements:
    pip install provide-foundation[opentelemetry]  # For tracing/metrics
    # OR
    pip install provide-foundation                 # Basic logging only

Usage:
    python examples/01_quick_start.py
    
    # Or with custom log level via environment
    PROVIDE_LOG_LEVEL=ERROR python examples/01_quick_start.py

Expected output:
    Colored, emoji-prefixed log messages with optional tracing/metrics setup.
"""

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

from provide.foundation import logger, pout, setup_telemetry  # noqa: E402


def example_1_quick_start() -> None:
    """
    Demonstrates basic structured logging with provide.foundation.
    
    Key concepts:
    - setup_telemetry() initializes the logging system
    - logger methods accept a message and keyword arguments for structured data
    - Different log levels control what gets displayed
    - Structured data makes logs searchable and analyzable
    """
    pout("\n" + "=" * 60)
    pout("🚀 Example 1: Quick Start")
    pout(" Demonstrates: Logging with full telemetry setup (tracing/metrics).")
    pout(" Note: If OpenTelemetry dependencies are missing, tracing/metrics are disabled.")
    pout("=" * 60)

    # Initialize with defaults (or environment variables if set)
    # This sets up logging + optional tracing/metrics if dependencies available
    setup_telemetry()

    # Start logging immediately
    logger.info("Application started", version="1.0.0", component="main_app")
    logger.debug("Debugging initial state", state_value=42)
    logger.warning("A potential issue was detected", issue_code="W001")
    logger.error("An error occurred during startup", error_code="E123", critical=False)


if __name__ == "__main__":
    example_1_quick_start()
    pout("\n✅ Example 1 completed.")
