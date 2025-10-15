# provide/foundation/resilience/types.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from enum import Enum

"""Type definitions for resilience patterns."""


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Circuit is open, failing fast
    HALF_OPEN = "half_open"  # Testing if service has recovered


class BackoffStrategy(str, Enum):
    """Backoff strategies for retry delays."""

    FIXED = "fixed"  # Same delay every time
    LINEAR = "linear"  # Linear increase (delay * attempt)
    EXPONENTIAL = "exponential"  # Exponential increase (delay * 2^attempt)
    FIBONACCI = "fibonacci"  # Fibonacci sequence delays


__all__ = [
    "BackoffStrategy",
    "CircuitState",
]


# <3 🧱🤝💪🪄
