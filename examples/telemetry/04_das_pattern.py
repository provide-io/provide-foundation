#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Demonstrates Domain-Action-Status (DAS) structured logging."""

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
    LoggingConfig,
    TelemetryConfig,
    get_hub,
    logger,
    pout,
)


def example_4_das_logging() -> None:
    """Example 4: Demonstrates Domain-Action-Status (DAS) structured logging.

    DAS logging provides semantic meaning to log events by categorizing them
    with `domain`, `action`, and `status` keys, which are then visually
    represented by emojis if DAS emoji prefixing is enabled.
    """
    pout("\n" + "=" * 60)
    pout(
        " Demonstrates: Using domain, action, status for semantic, emoji-enhanced logs.",
    )
    pout("=" * 60)

    # Ensure DAS emojis are enabled with INFO level for better visibility
    hub = get_hub()
    hub.initialize_foundation(
        TelemetryConfig(
            logging=LoggingConfig(
                das_emoji_prefix_enabled=True,
                default_level="INFO",
            ),
        )
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

# 🧱🏗️🔚
