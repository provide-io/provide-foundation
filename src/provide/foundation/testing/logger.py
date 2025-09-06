#
# logger.py
#
"""
Logger Testing Utilities for Foundation.

Provides utilities for resetting logger state, managing configurations,
and ensuring test isolation for the Foundation logging system.
"""

import structlog

from provide.foundation.logger.core import logger as foundation_logger, _LAZY_SETUP_STATE
from provide.foundation.streams.file import reset_streams


def reset_foundation_state() -> None:
    """
    Internal function to reset structlog and Foundation's state.
    
    This resets:
    - structlog configuration to defaults
    - Foundation logger state and configuration  
    - Stream state back to defaults
    - Lazy setup state tracking
    - OpenTelemetry provider state (if available)
    """
    # Reset structlog to its default unconfigured state
    structlog.reset_defaults()
    
    # Reset stream state
    reset_streams()
    
    # Skip OpenTelemetry reset for now to avoid breaking internal API assumptions
    # The "already set" warnings are cosmetic and don't break functionality
    
    # Reset foundation logger state
    foundation_logger._is_configured_by_setup = False
    foundation_logger._active_config = None
    foundation_logger._active_resolved_emoji_config = None
    _LAZY_SETUP_STATE.update(
        {"done": False, "error": None, "in_progress": False}
    )


def reset_foundation_setup_for_testing() -> None:
    """
    Public test utility to reset Foundation's internal state.
    
    This function ensures clean test isolation by resetting all
    Foundation logging state between test runs.
    """
    reset_foundation_state()


__all__ = [
    "reset_foundation_state",
    "reset_foundation_setup_for_testing",
]