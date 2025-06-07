#!/usr/bin/env python3
# examples/pyvider_telemetry/04_das_logging.py
"""Demonstrates Domain-Action-Status (DAS) structured logging."""

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


def example_4_das_logging() -> None:
    """
    Example 4: Demonstrates Domain-Action-Status (DAS) structured logging.

    DAS logging provides semantic meaning to log events by categorizing them
    with `domain`, `action`, and `status` keys, which are then visually
    represented by emojis if DAS emoji prefixing is enabled.
    """
    print("\n" + "=" * 60)
    print("🏗️ Example 4: Domain-Action-Status (DAS) Logging")
    print(
        " Demonstrates: Using domain, action, status for semantic, emoji-enhanced logs."
    )
    print("=" * 60)

    # Ensure DAS emojis are enabled (default is True, but explicit for clarity)
    setup_telemetry(
        TelemetryConfig(logging=LoggingConfig(das_emoji_prefix_enabled=True))
    )

    # Authentication events
    logger.info(
        "User login attempt",
        domain="auth",
        action="login",
        status="success",
        user_id="user123",
        ip_address="192.168.1.100",
    )

    logger.warning(
        "Failed login attempt",
        domain="auth",
        action="login",
        status="failure",
        username="baduser",
        reason="invalid_password",
    )

    # Database operations
    logger.info(
        "Database query executed",
        domain="database",
        action="query",
        status="success",
        table="users",
        duration_ms=45,
        rows_returned=10,
    )

    logger.error(
        "Database connection failed",
        domain="database",
        action="connect",
        status="error",
        db_host="db.example.com",
        error_details="Timeout during handshake",
    )

    # System events
    logger.info(
        "Service startup completed",
        domain="system",
        action="start",
        status="complete",
        startup_time_ms=2500,
        modules_loaded=15,
    )


if __name__ == "__main__":
    example_4_das_logging()
    print("\n✅ Example 4 completed.")
