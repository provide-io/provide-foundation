#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

#
# __init__.py
#
# Side-effect import: registers TRACE log level (must be imported before logger use)
from provide.foundation.logger import trace  # noqa: F401
from provide.foundation.logger.base import (
    FoundationLogger,  # Class definition
    get_logger,  # Factory function
    logger,  # Global instance
)
from provide.foundation.logger.config import (
    LoggingConfig,
    TelemetryConfig,
)
from provide.foundation.logger.core import (
    is_debug_enabled,
    is_trace_enabled,
)

"""Foundation Telemetry Logger Sub-package.
Re-exports key components related to logging functionality.
"""

__all__ = [
    "FoundationLogger",
    "LoggingConfig",
    "TelemetryConfig",
    "get_logger",
    "is_debug_enabled",
    "is_trace_enabled",
    "logger",
]

# 🧱🏗️🔚
