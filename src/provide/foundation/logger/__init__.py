from __future__ import annotations

#
# __init__.py
#

from provide.foundation.logger import trace  # noqa: F401
from provide.foundation.logger.base import (
    FoundationLogger,  # Class definition
    get_logger,  # Factory function
    logger,  # Global instance
)

"""Foundation Telemetry Logger Sub-package.
Re-exports key components related to logging functionality.
"""
from provide.foundation.logger.config import (
    LoggingConfig,
    TelemetryConfig,
)

__all__ = [
    "FoundationLogger",
    "LoggingConfig",
    "TelemetryConfig",
    "get_logger",
    "logger",
]

# 🐍📝
