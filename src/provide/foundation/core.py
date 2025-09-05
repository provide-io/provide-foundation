#
# core.py
#
"""
Foundation Telemetry Core Setup Functions.
"""

from provide.foundation.setup import (
    setup_telemetry,
    shutdown_foundation_telemetry,
    reset_foundation_setup_for_testing,
)
from provide.foundation.logger.setup.emoji_resolver import ResolvedEmojiConfig

__all__ = [
    "setup_telemetry",
    "shutdown_foundation_telemetry", 
    "reset_foundation_setup_for_testing",
    "ResolvedEmojiConfig",
]