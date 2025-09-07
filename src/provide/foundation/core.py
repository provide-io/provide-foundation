#
# core.py
#
"""
Foundation Telemetry Core Setup Functions.
"""

from provide.foundation.logger.setup.emoji_resolver import ResolvedEmojiConfig
from provide.foundation.setup import (
    reset_foundation_setup_for_testing,
    setup_telemetry,
    shutdown_foundation_telemetry,
)

__all__ = [
    "ResolvedEmojiConfig",
    "reset_foundation_setup_for_testing",
    "setup_telemetry",
    "shutdown_foundation_telemetry",
]
