#
# testing.py
#
"""
Testing utilities for Foundation Telemetry setup.
Provides functions to reset state and configure test environments.
"""

import structlog

from provide.foundation.logger.core import (
    _LAZY_SETUP_STATE,
    logger as foundation_logger,
)
from provide.foundation.streams.file import reset_streams


def reset_foundation_state() -> None:
    """
    Internal function to reset structlog and Foundation Telemetry's state.
    """
    # Reset structlog configuration
    structlog.reset_defaults()

    # Reset stream state
    reset_streams()

    # Reset foundation logger state
    foundation_logger._is_configured_by_setup = False
    foundation_logger._active_config = None
    foundation_logger._active_resolved_emoji_config = None
    _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})


def reset_foundation_setup_for_testing() -> None:
    """
    Public test utility to reset Foundation Telemetry's internal state.
    """
    reset_foundation_state()
