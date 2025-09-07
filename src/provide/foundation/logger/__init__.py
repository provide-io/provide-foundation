#
# __init__.py
#
"""
Foundation Telemetry Logger Sub-package.
Re-exports key components related to logging functionality.
"""

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
from provide.foundation.eventsets.display import (
    show_event_matrix,  # Utility to display event set configurations
)

__all__ = [
    "show_event_matrix",
    "FoundationLogger",
    "LoggingConfig",
    "TelemetryConfig",
    "get_logger",
    "logger",
    "setup_logger",  # Consistent naming
    "setup_logging",  # Backward compatibility
]

# 🐍📝
