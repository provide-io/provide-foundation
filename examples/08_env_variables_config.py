#!/usr/bin/env python3
# examples/foundation_telemetry/08_env_variables_config.py
"""Demonstrates configuring Foundation Telemetry using environment variables."""

import os
from pathlib import Path
import sys

# Add src to path for examples
example_dir = Path(__file__).resolve().parent.parent  # Go up one level to `examples`
project_root = example_dir.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from provide.foundation import (  # noqa: E402
    logger,
    setup_telemetry,
)


def example_8_environment_configuration() -> None:
    """
    Example 8: Demonstrates configuration via environment variables.

    Foundation Telemetry can be configured using `FOUNDATION_*` environment variables,
    allowing settings to be changed without code modification.
    """
    print("\n" + "=" * 60)
    print("🌍 Example 8: Environment Configuration")
    print(" Demonstrates: Configuring telemetry via environment variables.")
    print("=" * 60)

    # Set environment variables for this example
    # (In a real scenario, these would be set in the shell or deployment environment)
    original_env = os.environ.copy()
    os.environ.update(
        {
            "FOUNDATION_SERVICE_NAME": "env-service-demo",
            "FOUNDATION_LOG_LEVEL": "DEBUG",
            "FOUNDATION_LOG_CONSOLE_FORMATTER": "json",
            "FOUNDATION_LOG_MODULE_LEVELS": "auth.service:TRACE,database:ERROR",
            "FOUNDATION_LOG_DAS_EMOJI_ENABLED": "true",
            "FOUNDATION_LOG_OMIT_TIMESTAMP": "false",  # Explicitly include timestamps for this demo
        }
    )

    try:
        # Load configuration from environment
        # `setup_telemetry()` called without args will use `TelemetryConfig.from_env()`
        setup_telemetry()

        logger.info(
            "Configuration loaded from environment variables",
            domain="system",
            action="config_load",
            status="success",
        )

        auth_service_logger = logger.get_logger(
            "auth.service.tokens"
        )  # This is a structlog.BoundLogger
        db_logger = logger.get_logger(
            "database.queries"
        )  # This is a structlog.BoundLogger

        # Use the global `logger` (FoundationLogger instance) for .trace()
        logger.trace(
            "Token validation trace details",
            _foundation_logger_name="auth.service.tokens",
        )  # ✅ Shows (auth.service is TRACE)
        auth_service_logger.debug(
            "User 'test' authentication check"
        )  # ✅ Shows (.debug is fine on BoundLogger)

        db_logger.warning(
            "DB query warning (should be filtered)"
        )  # ❌ Filtered (database is ERROR)
        db_logger.error("DB connection error (should show)")  # ✅ Shows
    finally:
        # Restore original environment to avoid affecting other tests/examples
        for key in original_env:
            os.environ[key] = original_env[key]
        for key in list(os.environ.keys()):  # Handle keys added during this test
            if key not in original_env and key.startswith("FOUNDATION_"):
                del os.environ[key]


if __name__ == "__main__":
    example_8_environment_configuration()
    print("\n✅ Example 8 completed.")
