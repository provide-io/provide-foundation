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

# Backward compatibility alias
CircuitBreaker = SyncCircuitBreaker
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
    # Circuit breaker - async
    "AsyncCircuitBreaker",
    "BackoffStrategy",
    # Bulkhead pattern
    "Bulkhead",
    "BulkheadManager",
    # Circuit breaker - backward compatible alias
    "CircuitBreaker",
    # Circuit breaker - state enum
    "CircuitState",
    # Fallback
    "FallbackChain",
    "RetryExecutor",
    # Core retry functionality
    "RetryPolicy",
    # Circuit breaker - sync
    "SyncCircuitBreaker",
    "circuit_breaker",
    "fallback",
    "get_bulkhead_manager",
    # Decorators
    "retry",
]


# <3 🧱🤝💪🪄
