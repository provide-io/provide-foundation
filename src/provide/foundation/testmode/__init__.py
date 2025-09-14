#
# __init__.py
#
"""Foundation Test Mode Support.

This module provides utilities for test mode detection and internal
reset APIs used by testing frameworks. It centralizes all test-related
functionality that Foundation needs for proper test isolation.
"""

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

__all__ = [
    # Test detection
    "is_in_click_testing",
    "is_in_test_mode",
    "should_use_shared_registries",
    # Internal reset APIs (for testkit use)
    "reset_hub_state",
    "reset_logger_state",
    "reset_streams_state",
    "reset_structlog_state",
]