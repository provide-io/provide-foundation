# provide/foundation/resilience/defaults.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from provide.foundation.resilience.types import BackoffStrategy

"""Resilience defaults for Foundation configuration."""

# =================================
# Circuit Breaker Defaults
# =================================
DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT = 60.0
DEFAULT_CIRCUIT_BREAKER_STATE = "closed"
DEFAULT_CIRCUIT_BREAKER_FAILURE_COUNT = 0
DEFAULT_CIRCUIT_BREAKER_LAST_FAILURE_TIME = None
DEFAULT_CIRCUIT_BREAKER_NEXT_ATTEMPT_TIME = 0.0
DEFAULT_CIRCUIT_BREAKER_FAILURE_THRESHOLD = 5

# =================================
# Retry Policy Defaults
# =================================
DEFAULT_RETRY_MAX_ATTEMPTS = 3
DEFAULT_RETRY_BASE_DELAY = 1.0
DEFAULT_RETRY_MAX_DELAY = 60.0
DEFAULT_RETRY_JITTER = True
DEFAULT_RETRY_RETRYABLE_ERRORS = None
DEFAULT_RETRY_RETRYABLE_STATUS_CODES = None

# =================================
# Bulkhead Defaults
# =================================
DEFAULT_BULKHEAD_MAX_CONCURRENT = 10
DEFAULT_BULKHEAD_MAX_QUEUE_SIZE = 100
DEFAULT_BULKHEAD_TIMEOUT = 30.0
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


# =================================
# Factory Functions
# =================================


def default_retry_backoff_strategy() -> BackoffStrategy:
    """Factory for default retry backoff strategy."""
    from provide.foundation.resilience.types import BackoffStrategy

    return BackoffStrategy.EXPONENTIAL


__all__ = [
    "DEFAULT_BULKHEAD_MAX_CONCURRENT",
    "DEFAULT_BULKHEAD_MAX_QUEUE_SIZE",
    "DEFAULT_BULKHEAD_TIMEOUT",
    "DEFAULT_CIRCUIT_BREAKER_FAILURE_COUNT",
    "DEFAULT_CIRCUIT_BREAKER_FAILURE_THRESHOLD",
    "DEFAULT_CIRCUIT_BREAKER_LAST_FAILURE_TIME",
    "DEFAULT_CIRCUIT_BREAKER_NEXT_ATTEMPT_TIME",
    "DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT",
    "DEFAULT_CIRCUIT_BREAKER_STATE",
    "DEFAULT_RETRY_BASE_DELAY",
    "DEFAULT_RETRY_JITTER",
    "DEFAULT_RETRY_MAX_ATTEMPTS",
    "DEFAULT_RETRY_MAX_DELAY",
    "DEFAULT_RETRY_RETRYABLE_ERRORS",
    "DEFAULT_RETRY_RETRYABLE_STATUS_CODES",
    "default_retry_backoff_strategy",
]


# <3 🧱🤝💪🪄
