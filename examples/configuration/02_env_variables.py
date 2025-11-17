#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Demonstrates configuring Foundation Telemetry using environment variables."""

import os
from pathlib import Path
import sys

# Add src to path for examples
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent  # Go up from examples to project root
# Line removed - project_root already set above
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from provide.foundation import (
    get_hub,
    logger,
)
from provide.foundation.console.output import pout


def example_8_environment_configuration() -> None:
    """Example 8: Demonstrates configuration via environment variables.

    Foundation Telemetry can be configured using `PROVIDE_*` environment variables,
    allowing settings to be changed without code modification.
    """
    pout("\n" + "=" * 60)
    pout(" Demonstrates: Configuring telemetry via environment variables.")
    pout("=" * 60)

    # Set environment variables for this example
    # (In a real scenario, these would be set in the shell or deployment environment)
    original_env = os.environ.copy()
    os.environ.update(
        {
            "PROVIDE_SERVICE_NAME": "env-service-demo",
            "PROVIDE_LOG_LEVEL": "DEBUG",
            "PROVIDE_LOG_CONSOLE_FORMATTER": "json",
            "PROVIDE_LOG_MODULE_LEVELS": "auth.service:TRACE,database:ERROR",
            "PROVIDE_LOG_DAS_EMOJI_ENABLED": "true",
            "PROVIDE_LOG_OMIT_TIMESTAMP": "false",  # Explicitly include timestamps for this demo
        },
    )

    try:
        # Load configuration from environment
        # `get_hub().initialize_foundation()` called without args will use `TelemetryConfig.from_env()`
        get_hub().initialize_foundation()

        logger.info(
            "Configuration loaded from environment variables",
            domain="system",
            action="config_load",
            status="success",
        )

        auth_service_logger = logger.get_logger(
            "auth.service.tokens",
        )  # This is a structlog.BoundLogger
        db_logger = logger.get_logger(
            "database.queries",
        )  # This is a structlog.BoundLogger

        # Use the global `logger` (FoundationLogger instance) for .trace()
        logger.trace(
            "Token validation trace details",
            _foundation_logger_name="auth.service.tokens",
        )
        auth_service_logger.debug(
            "User 'test' authentication check",
        )
        db_logger.warning(
            "DB query warning (should be filtered)",
        )  # ❌ Filtered (database is ERROR)
    finally:
        # Restore original environment to avoid affecting other tests/examples
        for key in original_env:
            os.environ[key] = original_env[key]
        for key in list(os.environ.keys()):  # Handle keys added during this test
            if key not in original_env and key.startswith("PROVIDE_"):
                del os.environ[key]


if __name__ == "__main__":
    example_8_environment_configuration()

# 🧱🏗️🔚
