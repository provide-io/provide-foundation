from __future__ import annotations

from provide.foundation.resilience.circuit import CircuitBreaker, CircuitState
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

These patterns are used throughout foundation to eliminate code duplication
and provide consistent failure handling.
"""

__all__ = [
    "BackoffStrategy",
    # Circuit breaker
    "CircuitBreaker",
    "CircuitState",
    # Fallback
    "FallbackChain",
    "RetryExecutor",
    # Core retry functionality
    "RetryPolicy",
    "circuit_breaker",
    "fallback",
    # Decorators
    "retry",
]
