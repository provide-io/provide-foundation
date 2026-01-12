#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Demonstrates usage of named loggers for different components."""

from pathlib import Path
import sys

example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Already have path setup above

from provide.foundation import get_hub, logger, pout
from provide.foundation.logger.config import (
    LoggingConfig,
    TelemetryConfig,
)


def example_3_named_loggers() -> None:
    """Example 3: Demonstrates usage of named loggers for different components.

    Named loggers help in identifying the source of log messages and allow for
    module-specific log level filtering (shown in a later example).
    """
    pout("=" * 60)
    pout("🔢 Example 3: Named Loggers")
    pout(" Demonstrates: Creating and using component-specific loggers.")
    pout("=" * 60)

    # Re-initialize with INFO level for better visibility
    get_hub().initialize_foundation(
        TelemetryConfig(
            logging=LoggingConfig(default_level="INFO"),
        ),
    )

    # Create component-specific loggers
    auth_logger = logger.get_logger("auth.service")
    db_logger = logger.get_logger("database.connection")
    api_logger = logger.get_logger("api.handlers")

    # Each logger's name can be used for emoji prefixing (if enabled)
    # and module-level filtering.

    # Authentication service logs
    auth_logger.info(
        "User login successful",
        user_id="user123",
        session_id="sess_456",
        ip_address="192.168.1.100",
        duration_ms=245,
    )
    auth_logger.info("JWT token issued", user_id="user123", expires_in=3600, scopes=["read", "write"])

    # Database connection logs
    db_logger.info("Connection pool initialized", pool_size=20, initial_connections=5, timeout_ms=5000)
    db_logger.warning("Database connection pool nearing capacity", pool_size=20, current=18, available=2)
    db_logger.info("Query executed successfully", table="users", query_time_ms=12, rows_affected=1)

    # API handler logs
    api_logger.info(
        "HTTP request started",
        method="GET",
        path="/api/users",
        request_id="req-abc123",
        user_agent="Mozilla/5.0",
    )
    api_logger.info(
        "Request processed successfully",
        request_id="req-abc123",
        status_code=200,
        response_time_ms=156,
        response_size_bytes=1024,
    )

    # Show that different components can log independently
    logger.info("Main application event", component="core", event_type="health_check")


if __name__ == "__main__":
    example_3_named_loggers()

# 🧱🏗️🔚
