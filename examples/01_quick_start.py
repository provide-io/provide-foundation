#!/usr/bin/env python3
# examples/01_quick_start.py
"""
Quick Start Example - Basic Structured Logging

This example demonstrates the simplest way to get started with provide.foundation's
logging system. It shows how to:
- Initialize the telemetry system with default settings
- Use different log levels (info, debug, warning, error)
- Include structured data in log messages

Usage:
    python examples/01_quick_start.py
    
    # Or with custom log level via environment
    PROVIDE_LOG_LEVEL=ERROR python examples/01_quick_start.py

Expected output:
    Colored, emoji-prefixed log messages at different levels with structured data.
"""

from pathlib import Path
import sys

# Add src to path for examples
# This allows the example script to find the `provide.foundation` module
# when run directly from the `examples` directory or the project root.
example_dir = Path(__file__).resolve().parent.parent  # Go up one level to `examples`
project_root = example_dir.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from provide.foundation import logger, setup_telemetry  # noqa: E402


def example_1_quick_start() -> None:
    """
    Demonstrates basic structured logging with provide.foundation.
    
    Key concepts:
    - setup_telemetry() initializes the logging system
    - logger methods accept a message and keyword arguments for structured data
    - Different log levels control what gets displayed
    - Structured data makes logs searchable and analyzable
    """
    print("\n" + "=" * 60)
    print("🚀 Example 1: Quick Start")
    print(" Demonstrates: Logging with default settings after simple setup.")
    print("=" * 60)

    # Initialize with defaults (or environment variables if set)
    setup_telemetry()

    # Start logging immediately
    logger.info("Application started", version="1.0.0", component="main_app")
    logger.debug("Debugging initial state", state_value=42)
    logger.warning("A potential issue was detected", issue_code="W001")
    logger.error("An error occurred during startup", error_code="E123", critical=False)


if __name__ == "__main__":
    example_1_quick_start()
    print("\n✅ Example 1 completed.")
