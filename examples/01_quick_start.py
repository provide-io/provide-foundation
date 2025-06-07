#!/usr/bin/env python3
# examples/pyvider_telemetry/01_quick_start.py
"""Demonstrates quick start with default Pyvider Telemetry configuration."""

from pathlib import Path
import sys

# Add src to path for examples
# This allows the example script to find the `pyvider.telemetry` module
# when run directly from the `examples` directory or the project root.
example_dir = Path(__file__).resolve().parent.parent  # Go up one level to `examples`
project_root = example_dir.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from pyvider.telemetry import logger, setup_telemetry  # noqa: E402


def example_1_quick_start() -> None:
    """
    Example 1: Demonstrates quick start logging with default configuration.

    This shows how to start logging immediately after calling `setup_telemetry()`
    without any custom configuration. It relies on built-in defaults or
    environment variables if set.
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
