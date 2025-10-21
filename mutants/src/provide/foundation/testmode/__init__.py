# provide/foundation/testmode/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# __init__.py
#
from provide.foundation.testmode.detection import (
    configure_structlog_for_test_safety,
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
    "configure_structlog_for_test_safety",
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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


# <3 🧱🤝🧪🪄
