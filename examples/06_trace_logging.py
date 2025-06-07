#!/usr/bin/env python3
# examples/pyvider_telemetry/06_trace_logging.py
"""Demonstrates TRACE level logging for ultra-verbose output."""

from pathlib import Path
import sys

# Add src to path for examples
example_dir = Path(__file__).resolve().parent.parent  # Go up one level to `examples`
project_root = example_dir.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from pyvider.telemetry import (  # noqa: E402
    LoggingConfig,
    TelemetryConfig,
    logger,
    setup_telemetry,
)


def example_6_trace_logging() -> None:
    """
    Example 6: Demonstrates the custom TRACE log level.

    TRACE is a highly verbose level, numerically lower than DEBUG. This example
    shows how to enable and use it for detailed diagnostic logging.
    """
    print("\n" + "=" * 60)
    print("👣 Example 6: TRACE Level Logging")
    print(" Demonstrates: Using the ultra-verbose TRACE log level.")
    print("=" * 60)

    # Enable trace level globally or for specific modules
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="TRACE",  # Set TRACE as the default for all loggers
            module_levels={"specific.module": "DEBUG"},  # Example of other module
        )
    )
    setup_telemetry(config)

    logger.trace("Entering function 'process_data'", argument1="value1")
    logger.trace("Processing item", item_id=123, item_data={"key": "val"})

    # Using the special _pyvider_logger_name to emit a trace log as if from another logger
    logger.trace(
        "Database query details for specific module",
        _pyvider_logger_name="database.queries",  # This logger will also use TRACE
        query="SELECT * FROM users WHERE active=TRUE",
        params={"active": True},
        estimated_rows=150,
    )

    logger.get_logger("specific.module").trace(
        "This trace from specific.module will NOT show (its level is DEBUG)"
    )
    logger.get_logger("specific.module").debug(
        "This debug from specific.module WILL show"
    )


if __name__ == "__main__":
    example_6_trace_logging()
    print("\n✅ Example 6 completed.")
