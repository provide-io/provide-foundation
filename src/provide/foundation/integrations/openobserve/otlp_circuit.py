#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import threading
import time
from typing import Any, Literal

"""Circuit breaker pattern for OTLP connection failures.

This prevents log spam when OTLP endpoint is unreachable by:
- Tracking failure counts and timestamps
- Automatically disabling OTLP after threshold failures
- Implementing exponential backoff before retry attempts
- Auto-recovering after cooldown period
"""

CircuitState = Literal["closed", "open", "half_open"]


class OTLPCircuitBreaker:
    """Circuit breaker for OTLP connections with exponential backoff.

    States:
        - closed: Normal operation, requests allowed
        - open: Too many failures, requests blocked
        - half_open: Testing if service recovered

    Examples:
        >>> breaker = OTLPCircuitBreaker(failure_threshold=3, timeout=60.0)
        >>> if breaker.can_attempt():
        ...     success = send_otlp_log()
        ...     if success:
        ...         breaker.record_success()
        ...     else:
        ...         breaker.record_failure()
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        half_open_timeout: float = 10.0,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting half-open (doubles each time)
            half_open_timeout: Seconds to wait in half-open before trying again
        """
        self.failure_threshold = failure_threshold
        self.base_timeout = timeout
        self.half_open_timeout = half_open_timeout

        self._state: CircuitState = "closed"
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self._last_attempt_time: float | None = None
        self._open_count = 0  # Track how many times we've opened
        self._lock = threading.Lock()

    @property
    def state(self) -> CircuitState:
        """Get current circuit state."""
        with self._lock:
            return self._state

    def can_attempt(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def record_success(self) -> None:
        """Record a successful operation."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            # Don't reset _open_count completely, but decay it
            if self._open_count > 0:
                self._open_count = max(0, self._open_count - 1)

    def record_failure(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == "half_open":
                # Failed during recovery attempt, go back to open
                self._state = "open"
                self._open_count += 1
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "open"
                self._open_count += 1

    def reset(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            self._open_count = 0

    def get_stats(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "state": self._state,
                "failure_count": self._failure_count,
                "open_count": self._open_count,
                "last_failure_time": self._last_failure_time,
                "last_attempt_time": self._last_attempt_time,
                "current_timeout": self.base_timeout * (2 ** min(self._open_count, 10)),
            }


# Global circuit breaker instance
_otlp_circuit_breaker: OTLPCircuitBreaker | None = None
_circuit_breaker_lock = threading.Lock()


def get_otlp_circuit_breaker() -> OTLPCircuitBreaker:
    """Get the global OTLP circuit breaker instance.

    Returns:
        Shared OTLPCircuitBreaker instance
    """
    global _otlp_circuit_breaker

    if _otlp_circuit_breaker is None:
        with _circuit_breaker_lock:
            if _otlp_circuit_breaker is None:
                _otlp_circuit_breaker = OTLPCircuitBreaker(
                    failure_threshold=5,  # Open after 5 failures
                    timeout=30.0,  # Start with 30s timeout
                    half_open_timeout=10.0,  # Wait 10s between half-open attempts
                )

    return _otlp_circuit_breaker


def reset_otlp_circuit_breaker() -> None:
    """Reset the global circuit breaker (primarily for testing)."""
    global _otlp_circuit_breaker

    with _circuit_breaker_lock:
        if _otlp_circuit_breaker is not None:
            _otlp_circuit_breaker.reset()


__all__ = [
    "OTLPCircuitBreaker",
    "get_otlp_circuit_breaker",
    "reset_otlp_circuit_breaker",
]

# 🧱🏗️🔚
