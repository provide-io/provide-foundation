#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Demonstrates module-specific log level configuration."""

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


def example_7_module_level_filtering() -> None:
    """Example 7: Demonstrates module-specific log level configuration.

    This allows different parts of an application to have varying log verbosity
    (e.g., more verbose for a problematic module, less for noisy ones).
    """
    pout("\n" + "=" * 60)
    pout("🎛️ Example 7: Module-Level Filtering")
    pout(" Demonstrates: Setting different log levels for different modules.")
    pout("=" * 60)

    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",  # Default level for unspecified modules
            module_levels={
                "auth": "DEBUG",  # Verbose logging for 'auth' module and its submodules
                "database": "ERROR",  # Only errors from 'database' module
                "network.comms": "WARNING",  # Warnings and above for 'network.comms'
            },
        ),
    )
    get_hub().initialize_foundation(config)

    # Loggers for different modules
    auth_logger = logger.get_logger("auth.service")  # Will use DEBUG
    db_logger = logger.get_logger("database.connection")  # Will use ERROR
    net_comms_logger = logger.get_logger("network.comms.client")  # Will use WARNING
    other_logger = logger.get_logger("other.component")  # Will use default INFO

    auth_logger.debug(
        "Token validation details",
        token_id="tkn_short",
    )
    db_logger.info("Query executed successfully")  # ❌ Filtered (database is ERROR)
    db_logger.warning("Slow query detected: 2500ms")  # ❌ Filtered

    net_comms_logger.info(
        "Packet sent successfully",
    )  # ❌ Filtered (network.comms is WARNING)

    other_logger.debug(
        "Debug details for other component",
    )  # ❌ Filtered (default is INFO)


if __name__ == "__main__":
    example_7_module_level_filtering()

# 🧱🏗️🔚
