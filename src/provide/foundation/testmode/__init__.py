# provide/foundation/testmode/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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
    reset_circuit_breaker_state,
    reset_global_coordinator,
    reset_hub_state,
    reset_logger_state,
    reset_streams_state,
    reset_structlog_state,
    reset_version_cache,
)
from provide.foundation.testmode.orchestration import (
    reset_foundation_for_testing,
    reset_foundation_state,
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
    "reset_circuit_breaker_state",
    # Orchestrated reset functions
    "reset_foundation_for_testing",
    "reset_foundation_state",
    "reset_global_coordinator",
    "reset_hub_state",
    "reset_logger_state",
    "reset_streams_state",
    "reset_structlog_state",
    "reset_version_cache",
    "should_use_shared_registries",
]


# <3 🧱🤝🧪🪄
