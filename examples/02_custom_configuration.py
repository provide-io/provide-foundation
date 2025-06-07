#!/usr/bin/env python3
# examples/pyvider_telemetry/02_custom_configuration.py
"""Demonstrates custom configuration of Pyvider Telemetry using TelemetryConfig and LoggingConfig."""

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


def example_2_configuration() -> None:
    """
    Example 2: Demonstrates custom telemetry configuration.

    This example shows how to use `TelemetryConfig` and `LoggingConfig` to
    programmatically define settings like service name, default log level,
    console formatter (JSON), and emoji usage.
    """
    print("\n" + "=" * 60)
    print("⚙️ Example 2: Custom Configuration")
    print(" Demonstrates: Setting service name, JSON format, log level, and emojis.")
    print("=" * 60)

    config = TelemetryConfig(
        service_name="example-service",
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",  # Output logs as JSON
            logger_name_emoji_prefix_enabled=True,
            das_emoji_prefix_enabled=True,
        ),
    )
    setup_telemetry(config)

    logger.info("Service configured with custom settings", config_source="programmatic")
    logger.error(
        "JSON formatted error with custom fields",
        error_id="E456",
        details={"reason": "dependency_failure"},
    )


if __name__ == "__main__":
    example_2_configuration()
    print("\n✅ Example 2 completed.")
