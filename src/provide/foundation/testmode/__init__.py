from __future__ import annotations

#
# __init__.py
#
from provide.foundation.testmode.detection import (
    is_in_click_testing,
    is_in_test_mode,
    should_use_shared_registries,
)
from provide.foundation.testmode.internal import (
    reset_hub_state,
    reset_logger_state,
    reset_streams_state,
    reset_structlog_state,
)

"""Foundation Test Mode Support.

This module provides utilities for test mode detection and internal
reset APIs used by testing frameworks. It centralizes all test-related
functionality that Foundation needs for proper test isolation.
"""

__all__ = [
    # Test detection
    "is_in_click_testing",
    "is_in_test_mode",
    # Internal reset APIs (for testkit use)
    "reset_hub_state",
    "reset_logger_state",
    "reset_streams_state",
    "reset_structlog_state",
    "should_use_shared_registries",
]
