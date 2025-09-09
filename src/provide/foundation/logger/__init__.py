#
# __init__.py
#
"""
Foundation Telemetry Logger Sub-package.
Re-exports key components related to logging functionality.
"""

# Import trace module early to ensure PrintLogger gets patched
from provide.foundation.logger import trace  # noqa: F401

from provide.foundation.logger.base import (
    FoundationLogger,  # Class definition
    get_logger,  # Factory function
    logger,  # Global instance
    setup_logger,  # Setup function (consistent naming)
    setup_logging,  # Setup function (backward compatibility)
)
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
    "setup_logger",  # Consistent naming
    "setup_logging",  # Backward compatibility
]

# 🐍📝
