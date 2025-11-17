#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Demonstrates custom configuration of Foundation Telemetry using TelemetryConfig and LoggingConfig."""

from pathlib import Path
import sys

example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from provide.foundation import (
    LoggingConfig,
    TelemetryConfig,
    get_hub,
    logger,
    pout,  # Foundation console output
)


def example_2_configuration() -> None:
    """Example 2: Demonstrates custom telemetry configuration.

    This example shows how to use `TelemetryConfig` and `LoggingConfig` to
    programmatically define settings like service name, default log level,
    console formatter (JSON), and emoji usage.
    """
    pout("=" * 60)
    pout("🔢 Example 2: Custom Configuration")
    pout(" Demonstrates: Setting service name, JSON format, log level, and emojis.")
    pout("=" * 60)

    config = TelemetryConfig(
        service_name="example-service",
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",  # Output logs as JSON
            logger_name_emoji_prefix_enabled=True,
            das_emoji_prefix_enabled=True,
        ),
    )
    get_hub().initialize_foundation(config)

    logger.info("Service configured with custom settings", config_source="programmatic")
    logger.error(
        "JSON formatted error with custom fields",
        error_id="E456",
        details={"reason": "dependency_failure"},
    )


if __name__ == "__main__":
    example_2_configuration()

# 🧱🏗️🔚
