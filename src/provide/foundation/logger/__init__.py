#
# __init__.py
#
"""
Foundation Telemetry Logger Sub-package.
Re-exports key components related to logging functionality.
"""

from provide.foundation.logger.base import (
    FoundationLogger,  # Class definition
    logger,  # Global instance
)
from provide.foundation.logger.config import (
    LoggingConfig,
    TelemetryConfig,
)
from provide.foundation.logger.emoji_matrix import (
    PRIMARY_EMOJI,  # Legacy/default domain emojis
    SECONDARY_EMOJI,  # Legacy/default action emojis
    TERTIARY_EMOJI,  # Legacy/default status emojis
    show_emoji_matrix,  # Utility to display emoji configurations
)

__all__ = [
    "PRIMARY_EMOJI",
    "SECONDARY_EMOJI",
    "TERTIARY_EMOJI",
    "FoundationLogger",
    "logger",
    "show_emoji_matrix",
    "LoggingConfig",
    "TelemetryConfig",
]

# 🐍📝
