#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Foundation Logger Configuration Module.

Re-exports all configuration classes for convenient importing."""

from __future__ import annotations

from provide.foundation.logger.config.logging import LoggingConfig
from provide.foundation.logger.config.telemetry import TelemetryConfig

__all__ = [
    "LoggingConfig",
    "TelemetryConfig",
]

# 🧱🏗️🔚
