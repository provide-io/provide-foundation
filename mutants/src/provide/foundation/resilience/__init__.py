# provide/foundation/resilience/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.resilience.bulkhead import (
    Bulkhead,
    BulkheadManager,
    get_bulkhead_manager,
)
from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
from provide.foundation.resilience.circuit_sync import (
    CircuitState,
    SyncCircuitBreaker,
)
from provide.foundation.resilience.decorators import circuit_breaker, fallback, retry
from provide.foundation.resilience.fallback import FallbackChain
from provide.foundation.resilience.retry import (
    BackoffStrategy,
    RetryExecutor,
    RetryPolicy,
)

"""Resilience patterns for handling failures and improving reliability.

This module provides unified implementations of common resilience patterns:
- Retry with configurable backoff strategies
- Circuit breaker for failing fast
- Fallback for graceful degradation
- Bulkhead for resource isolation

These patterns are used throughout foundation to eliminate code duplication
and provide consistent failure handling.
"""

__all__ = [
    "AsyncCircuitBreaker",
    "BackoffStrategy",
    "Bulkhead",
    "BulkheadManager",
    "CircuitState",
    "FallbackChain",
    "RetryExecutor",
    "RetryPolicy",
    "SyncCircuitBreaker",
    "circuit_breaker",
    "fallback",
    "get_bulkhead_manager",
    "retry",
]
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


# <3 🧱🤝💪🪄
