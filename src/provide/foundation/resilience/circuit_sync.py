#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Callable
from enum import Enum, auto
import threading
import time
from typing import Any

"""Synchronous circuit breaker implementation."""


class CircuitState(Enum):
    """Represents the state of the circuit breaker."""

    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()


class SyncCircuitBreaker:
    """Synchronous circuit breaker for resilience patterns.

    Uses threading.RLock for thread-safe state management in synchronous code.
    For async code, use AsyncCircuitBreaker instead.
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
        time_source: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the synchronous circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before attempting recovery
            expected_exception: Exception type(s) to catch
            time_source: Optional callable that returns current time (for testing).
                        Defaults to time.time() for production use.
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self._time_source = time_source or time.time
        self._lock = threading.RLock()
        # Initialize state attributes (will be set properly in reset())
        self._state: CircuitState
        self._failure_count: int
        self._last_failure_time: float | None
        self.reset()

    def state(self) -> CircuitState:
        """Get the current state of the circuit breaker."""
        with self._lock:
            if self._state == CircuitState.OPEN and self._can_attempt_recovery():
                # This is a view of the state; the actual transition happens in call()
                return CircuitState.HALF_OPEN
            return self._state

    def failure_count(self) -> int:
        """Get the current failure count."""
        with self._lock:
            return self._failure_count

    def _can_attempt_recovery(self) -> bool:
        """Check if the circuit can attempt recovery."""
        return self._time_source() >= (self._last_failure_time or 0) + self.recovery_timeout

    def call(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute a synchronous function through the circuit breaker.

        Args:
            func: Callable to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from func

        Raises:
            RuntimeError: If circuit is open
            Exception: Whatever exception func raises
        """
        with self._lock:
            current_state = self.state()
            if current_state == CircuitState.OPEN:
                raise RuntimeError("Circuit breaker is open")
            # If HALF_OPEN, we proceed with the call

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e

    def _on_success(self) -> None:
        """Handle a successful call."""
        with self._lock:
            # Success in either CLOSED or HALF_OPEN state resets the breaker.
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._last_failure_time = None

    def _on_failure(self) -> None:
        """Handle a failed call."""
        with self._lock:
            self._failure_count += 1
            if self._failure_count >= self.failure_threshold:
                # This transition happens for failures in CLOSED state
                # or for the single attempt in HALF_OPEN state.
                self._state = CircuitState.OPEN
                self._last_failure_time = self._time_source()

    def reset(self) -> None:
        """Reset the circuit breaker to its initial state."""
        with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._last_failure_time = None


# 🧱🏗️🔚
