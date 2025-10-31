#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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

# 🧱🏗️🔚
