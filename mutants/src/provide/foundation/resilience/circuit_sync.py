# provide/foundation/resilience/circuit_sync.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Callable
from enum import Enum, auto
import threading
import time
from typing import Any

"""Synchronous circuit breaker implementation."""
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

    def xǁSyncCircuitBreakerǁ__init____mutmut_orig(
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

    def xǁSyncCircuitBreakerǁ__init____mutmut_1(
        self,
        failure_threshold: int = 6,
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

    def xǁSyncCircuitBreakerǁ__init____mutmut_2(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 31.0,
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

    def xǁSyncCircuitBreakerǁ__init____mutmut_3(
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
        self.failure_threshold = None
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self._time_source = time_source or time.time
        self._lock = threading.RLock()
        # Initialize state attributes (will be set properly in reset())
        self._state: CircuitState
        self._failure_count: int
        self._last_failure_time: float | None
        self.reset()

    def xǁSyncCircuitBreakerǁ__init____mutmut_4(
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
        self.recovery_timeout = None
        self.expected_exception = expected_exception
        self._time_source = time_source or time.time
        self._lock = threading.RLock()
        # Initialize state attributes (will be set properly in reset())
        self._state: CircuitState
        self._failure_count: int
        self._last_failure_time: float | None
        self.reset()

    def xǁSyncCircuitBreakerǁ__init____mutmut_5(
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
        self.expected_exception = None
        self._time_source = time_source or time.time
        self._lock = threading.RLock()
        # Initialize state attributes (will be set properly in reset())
        self._state: CircuitState
        self._failure_count: int
        self._last_failure_time: float | None
        self.reset()

    def xǁSyncCircuitBreakerǁ__init____mutmut_6(
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
        self._time_source = None
        self._lock = threading.RLock()
        # Initialize state attributes (will be set properly in reset())
        self._state: CircuitState
        self._failure_count: int
        self._last_failure_time: float | None
        self.reset()

    def xǁSyncCircuitBreakerǁ__init____mutmut_7(
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
        self._time_source = time_source and time.time
        self._lock = threading.RLock()
        # Initialize state attributes (will be set properly in reset())
        self._state: CircuitState
        self._failure_count: int
        self._last_failure_time: float | None
        self.reset()

    def xǁSyncCircuitBreakerǁ__init____mutmut_8(
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
        self._lock = None
        # Initialize state attributes (will be set properly in reset())
        self._state: CircuitState
        self._failure_count: int
        self._last_failure_time: float | None
        self.reset()

    xǁSyncCircuitBreakerǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁSyncCircuitBreakerǁ__init____mutmut_1": xǁSyncCircuitBreakerǁ__init____mutmut_1,
        "xǁSyncCircuitBreakerǁ__init____mutmut_2": xǁSyncCircuitBreakerǁ__init____mutmut_2,
        "xǁSyncCircuitBreakerǁ__init____mutmut_3": xǁSyncCircuitBreakerǁ__init____mutmut_3,
        "xǁSyncCircuitBreakerǁ__init____mutmut_4": xǁSyncCircuitBreakerǁ__init____mutmut_4,
        "xǁSyncCircuitBreakerǁ__init____mutmut_5": xǁSyncCircuitBreakerǁ__init____mutmut_5,
        "xǁSyncCircuitBreakerǁ__init____mutmut_6": xǁSyncCircuitBreakerǁ__init____mutmut_6,
        "xǁSyncCircuitBreakerǁ__init____mutmut_7": xǁSyncCircuitBreakerǁ__init____mutmut_7,
        "xǁSyncCircuitBreakerǁ__init____mutmut_8": xǁSyncCircuitBreakerǁ__init____mutmut_8,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁSyncCircuitBreakerǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁSyncCircuitBreakerǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁSyncCircuitBreakerǁ__init____mutmut_orig)
    xǁSyncCircuitBreakerǁ__init____mutmut_orig.__name__ = "xǁSyncCircuitBreakerǁ__init__"

    def xǁSyncCircuitBreakerǁstate__mutmut_orig(self) -> CircuitState:
        """Get the current state of the circuit breaker."""
        with self._lock:
            if self._state == CircuitState.OPEN and self._can_attempt_recovery():
                # This is a view of the state; the actual transition happens in call()
                return CircuitState.HALF_OPEN
            return self._state

    def xǁSyncCircuitBreakerǁstate__mutmut_1(self) -> CircuitState:
        """Get the current state of the circuit breaker."""
        with self._lock:
            if self._state == CircuitState.OPEN or self._can_attempt_recovery():
                # This is a view of the state; the actual transition happens in call()
                return CircuitState.HALF_OPEN
            return self._state

    def xǁSyncCircuitBreakerǁstate__mutmut_2(self) -> CircuitState:
        """Get the current state of the circuit breaker."""
        with self._lock:
            if self._state != CircuitState.OPEN and self._can_attempt_recovery():
                # This is a view of the state; the actual transition happens in call()
                return CircuitState.HALF_OPEN
            return self._state

    xǁSyncCircuitBreakerǁstate__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁSyncCircuitBreakerǁstate__mutmut_1": xǁSyncCircuitBreakerǁstate__mutmut_1,
        "xǁSyncCircuitBreakerǁstate__mutmut_2": xǁSyncCircuitBreakerǁstate__mutmut_2,
    }

    def state(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁSyncCircuitBreakerǁstate__mutmut_orig"),
            object.__getattribute__(self, "xǁSyncCircuitBreakerǁstate__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    state.__signature__ = _mutmut_signature(xǁSyncCircuitBreakerǁstate__mutmut_orig)
    xǁSyncCircuitBreakerǁstate__mutmut_orig.__name__ = "xǁSyncCircuitBreakerǁstate"

    def failure_count(self) -> int:
        """Get the current failure count."""
        with self._lock:
            return self._failure_count

    def xǁSyncCircuitBreakerǁ_can_attempt_recovery__mutmut_orig(self) -> bool:
        """Check if the circuit can attempt recovery."""
        return self._time_source() >= (self._last_failure_time or 0) + self.recovery_timeout

    def xǁSyncCircuitBreakerǁ_can_attempt_recovery__mutmut_1(self) -> bool:
        """Check if the circuit can attempt recovery."""
        return self._time_source() > (self._last_failure_time or 0) + self.recovery_timeout

    def xǁSyncCircuitBreakerǁ_can_attempt_recovery__mutmut_2(self) -> bool:
        """Check if the circuit can attempt recovery."""
        return self._time_source() >= (self._last_failure_time or 0) - self.recovery_timeout

    def xǁSyncCircuitBreakerǁ_can_attempt_recovery__mutmut_3(self) -> bool:
        """Check if the circuit can attempt recovery."""
        return self._time_source() >= (self._last_failure_time and 0) + self.recovery_timeout

    def xǁSyncCircuitBreakerǁ_can_attempt_recovery__mutmut_4(self) -> bool:
        """Check if the circuit can attempt recovery."""
        return self._time_source() >= (self._last_failure_time or 1) + self.recovery_timeout

    xǁSyncCircuitBreakerǁ_can_attempt_recovery__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁSyncCircuitBreakerǁ_can_attempt_recovery__mutmut_1": xǁSyncCircuitBreakerǁ_can_attempt_recovery__mutmut_1,
        "xǁSyncCircuitBreakerǁ_can_attempt_recovery__mutmut_2": xǁSyncCircuitBreakerǁ_can_attempt_recovery__mutmut_2,
        "xǁSyncCircuitBreakerǁ_can_attempt_recovery__mutmut_3": xǁSyncCircuitBreakerǁ_can_attempt_recovery__mutmut_3,
        "xǁSyncCircuitBreakerǁ_can_attempt_recovery__mutmut_4": xǁSyncCircuitBreakerǁ_can_attempt_recovery__mutmut_4,
    }

    def _can_attempt_recovery(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁSyncCircuitBreakerǁ_can_attempt_recovery__mutmut_orig"),
            object.__getattribute__(self, "xǁSyncCircuitBreakerǁ_can_attempt_recovery__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _can_attempt_recovery.__signature__ = _mutmut_signature(
        xǁSyncCircuitBreakerǁ_can_attempt_recovery__mutmut_orig
    )
    xǁSyncCircuitBreakerǁ_can_attempt_recovery__mutmut_orig.__name__ = (
        "xǁSyncCircuitBreakerǁ_can_attempt_recovery"
    )

    def xǁSyncCircuitBreakerǁcall__mutmut_orig(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
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

    def xǁSyncCircuitBreakerǁcall__mutmut_1(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
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
            current_state = None
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

    def xǁSyncCircuitBreakerǁcall__mutmut_2(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
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
            if current_state != CircuitState.OPEN:
                raise RuntimeError("Circuit breaker is open")
            # If HALF_OPEN, we proceed with the call

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e

    def xǁSyncCircuitBreakerǁcall__mutmut_3(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
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
                raise RuntimeError(None)
            # If HALF_OPEN, we proceed with the call

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e

    def xǁSyncCircuitBreakerǁcall__mutmut_4(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
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
                raise RuntimeError("XXCircuit breaker is openXX")
            # If HALF_OPEN, we proceed with the call

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e

    def xǁSyncCircuitBreakerǁcall__mutmut_5(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
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
                raise RuntimeError("circuit breaker is open")
            # If HALF_OPEN, we proceed with the call

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e

    def xǁSyncCircuitBreakerǁcall__mutmut_6(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
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
                raise RuntimeError("CIRCUIT BREAKER IS OPEN")
            # If HALF_OPEN, we proceed with the call

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e

    def xǁSyncCircuitBreakerǁcall__mutmut_7(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
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
            result = None
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e

    def xǁSyncCircuitBreakerǁcall__mutmut_8(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
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
            result = func(**kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e

    def xǁSyncCircuitBreakerǁcall__mutmut_9(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
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
            result = func(
                *args,
            )
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e

    xǁSyncCircuitBreakerǁcall__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁSyncCircuitBreakerǁcall__mutmut_1": xǁSyncCircuitBreakerǁcall__mutmut_1,
        "xǁSyncCircuitBreakerǁcall__mutmut_2": xǁSyncCircuitBreakerǁcall__mutmut_2,
        "xǁSyncCircuitBreakerǁcall__mutmut_3": xǁSyncCircuitBreakerǁcall__mutmut_3,
        "xǁSyncCircuitBreakerǁcall__mutmut_4": xǁSyncCircuitBreakerǁcall__mutmut_4,
        "xǁSyncCircuitBreakerǁcall__mutmut_5": xǁSyncCircuitBreakerǁcall__mutmut_5,
        "xǁSyncCircuitBreakerǁcall__mutmut_6": xǁSyncCircuitBreakerǁcall__mutmut_6,
        "xǁSyncCircuitBreakerǁcall__mutmut_7": xǁSyncCircuitBreakerǁcall__mutmut_7,
        "xǁSyncCircuitBreakerǁcall__mutmut_8": xǁSyncCircuitBreakerǁcall__mutmut_8,
        "xǁSyncCircuitBreakerǁcall__mutmut_9": xǁSyncCircuitBreakerǁcall__mutmut_9,
    }

    def call(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁSyncCircuitBreakerǁcall__mutmut_orig"),
            object.__getattribute__(self, "xǁSyncCircuitBreakerǁcall__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    call.__signature__ = _mutmut_signature(xǁSyncCircuitBreakerǁcall__mutmut_orig)
    xǁSyncCircuitBreakerǁcall__mutmut_orig.__name__ = "xǁSyncCircuitBreakerǁcall"

    def xǁSyncCircuitBreakerǁ_on_success__mutmut_orig(self) -> None:
        """Handle a successful call."""
        with self._lock:
            # Success in either CLOSED or HALF_OPEN state resets the breaker.
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._last_failure_time = None

    def xǁSyncCircuitBreakerǁ_on_success__mutmut_1(self) -> None:
        """Handle a successful call."""
        with self._lock:
            # Success in either CLOSED or HALF_OPEN state resets the breaker.
            self._state = None
            self._failure_count = 0
            self._last_failure_time = None

    def xǁSyncCircuitBreakerǁ_on_success__mutmut_2(self) -> None:
        """Handle a successful call."""
        with self._lock:
            # Success in either CLOSED or HALF_OPEN state resets the breaker.
            self._state = CircuitState.CLOSED
            self._failure_count = None
            self._last_failure_time = None

    def xǁSyncCircuitBreakerǁ_on_success__mutmut_3(self) -> None:
        """Handle a successful call."""
        with self._lock:
            # Success in either CLOSED or HALF_OPEN state resets the breaker.
            self._state = CircuitState.CLOSED
            self._failure_count = 1
            self._last_failure_time = None

    def xǁSyncCircuitBreakerǁ_on_success__mutmut_4(self) -> None:
        """Handle a successful call."""
        with self._lock:
            # Success in either CLOSED or HALF_OPEN state resets the breaker.
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._last_failure_time = ""

    xǁSyncCircuitBreakerǁ_on_success__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁSyncCircuitBreakerǁ_on_success__mutmut_1": xǁSyncCircuitBreakerǁ_on_success__mutmut_1,
        "xǁSyncCircuitBreakerǁ_on_success__mutmut_2": xǁSyncCircuitBreakerǁ_on_success__mutmut_2,
        "xǁSyncCircuitBreakerǁ_on_success__mutmut_3": xǁSyncCircuitBreakerǁ_on_success__mutmut_3,
        "xǁSyncCircuitBreakerǁ_on_success__mutmut_4": xǁSyncCircuitBreakerǁ_on_success__mutmut_4,
    }

    def _on_success(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁSyncCircuitBreakerǁ_on_success__mutmut_orig"),
            object.__getattribute__(self, "xǁSyncCircuitBreakerǁ_on_success__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _on_success.__signature__ = _mutmut_signature(xǁSyncCircuitBreakerǁ_on_success__mutmut_orig)
    xǁSyncCircuitBreakerǁ_on_success__mutmut_orig.__name__ = "xǁSyncCircuitBreakerǁ_on_success"

    def xǁSyncCircuitBreakerǁ_on_failure__mutmut_orig(self) -> None:
        """Handle a failed call."""
        with self._lock:
            self._failure_count += 1
            if self._failure_count >= self.failure_threshold:
                # This transition happens for failures in CLOSED state
                # or for the single attempt in HALF_OPEN state.
                self._state = CircuitState.OPEN
                self._last_failure_time = self._time_source()

    def xǁSyncCircuitBreakerǁ_on_failure__mutmut_1(self) -> None:
        """Handle a failed call."""
        with self._lock:
            self._failure_count = 1
            if self._failure_count >= self.failure_threshold:
                # This transition happens for failures in CLOSED state
                # or for the single attempt in HALF_OPEN state.
                self._state = CircuitState.OPEN
                self._last_failure_time = self._time_source()

    def xǁSyncCircuitBreakerǁ_on_failure__mutmut_2(self) -> None:
        """Handle a failed call."""
        with self._lock:
            self._failure_count -= 1
            if self._failure_count >= self.failure_threshold:
                # This transition happens for failures in CLOSED state
                # or for the single attempt in HALF_OPEN state.
                self._state = CircuitState.OPEN
                self._last_failure_time = self._time_source()

    def xǁSyncCircuitBreakerǁ_on_failure__mutmut_3(self) -> None:
        """Handle a failed call."""
        with self._lock:
            self._failure_count += 2
            if self._failure_count >= self.failure_threshold:
                # This transition happens for failures in CLOSED state
                # or for the single attempt in HALF_OPEN state.
                self._state = CircuitState.OPEN
                self._last_failure_time = self._time_source()

    def xǁSyncCircuitBreakerǁ_on_failure__mutmut_4(self) -> None:
        """Handle a failed call."""
        with self._lock:
            self._failure_count += 1
            if self._failure_count > self.failure_threshold:
                # This transition happens for failures in CLOSED state
                # or for the single attempt in HALF_OPEN state.
                self._state = CircuitState.OPEN
                self._last_failure_time = self._time_source()

    def xǁSyncCircuitBreakerǁ_on_failure__mutmut_5(self) -> None:
        """Handle a failed call."""
        with self._lock:
            self._failure_count += 1
            if self._failure_count >= self.failure_threshold:
                # This transition happens for failures in CLOSED state
                # or for the single attempt in HALF_OPEN state.
                self._state = None
                self._last_failure_time = self._time_source()

    def xǁSyncCircuitBreakerǁ_on_failure__mutmut_6(self) -> None:
        """Handle a failed call."""
        with self._lock:
            self._failure_count += 1
            if self._failure_count >= self.failure_threshold:
                # This transition happens for failures in CLOSED state
                # or for the single attempt in HALF_OPEN state.
                self._state = CircuitState.OPEN
                self._last_failure_time = None

    xǁSyncCircuitBreakerǁ_on_failure__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁSyncCircuitBreakerǁ_on_failure__mutmut_1": xǁSyncCircuitBreakerǁ_on_failure__mutmut_1,
        "xǁSyncCircuitBreakerǁ_on_failure__mutmut_2": xǁSyncCircuitBreakerǁ_on_failure__mutmut_2,
        "xǁSyncCircuitBreakerǁ_on_failure__mutmut_3": xǁSyncCircuitBreakerǁ_on_failure__mutmut_3,
        "xǁSyncCircuitBreakerǁ_on_failure__mutmut_4": xǁSyncCircuitBreakerǁ_on_failure__mutmut_4,
        "xǁSyncCircuitBreakerǁ_on_failure__mutmut_5": xǁSyncCircuitBreakerǁ_on_failure__mutmut_5,
        "xǁSyncCircuitBreakerǁ_on_failure__mutmut_6": xǁSyncCircuitBreakerǁ_on_failure__mutmut_6,
    }

    def _on_failure(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁSyncCircuitBreakerǁ_on_failure__mutmut_orig"),
            object.__getattribute__(self, "xǁSyncCircuitBreakerǁ_on_failure__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _on_failure.__signature__ = _mutmut_signature(xǁSyncCircuitBreakerǁ_on_failure__mutmut_orig)
    xǁSyncCircuitBreakerǁ_on_failure__mutmut_orig.__name__ = "xǁSyncCircuitBreakerǁ_on_failure"

    def xǁSyncCircuitBreakerǁreset__mutmut_orig(self) -> None:
        """Reset the circuit breaker to its initial state."""
        with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._last_failure_time = None

    def xǁSyncCircuitBreakerǁreset__mutmut_1(self) -> None:
        """Reset the circuit breaker to its initial state."""
        with self._lock:
            self._state = None
            self._failure_count = 0
            self._last_failure_time = None

    def xǁSyncCircuitBreakerǁreset__mutmut_2(self) -> None:
        """Reset the circuit breaker to its initial state."""
        with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = None
            self._last_failure_time = None

    def xǁSyncCircuitBreakerǁreset__mutmut_3(self) -> None:
        """Reset the circuit breaker to its initial state."""
        with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = 1
            self._last_failure_time = None

    def xǁSyncCircuitBreakerǁreset__mutmut_4(self) -> None:
        """Reset the circuit breaker to its initial state."""
        with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._last_failure_time = ""

    xǁSyncCircuitBreakerǁreset__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁSyncCircuitBreakerǁreset__mutmut_1": xǁSyncCircuitBreakerǁreset__mutmut_1,
        "xǁSyncCircuitBreakerǁreset__mutmut_2": xǁSyncCircuitBreakerǁreset__mutmut_2,
        "xǁSyncCircuitBreakerǁreset__mutmut_3": xǁSyncCircuitBreakerǁreset__mutmut_3,
        "xǁSyncCircuitBreakerǁreset__mutmut_4": xǁSyncCircuitBreakerǁreset__mutmut_4,
    }

    def reset(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁSyncCircuitBreakerǁreset__mutmut_orig"),
            object.__getattribute__(self, "xǁSyncCircuitBreakerǁreset__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    reset.__signature__ = _mutmut_signature(xǁSyncCircuitBreakerǁreset__mutmut_orig)
    xǁSyncCircuitBreakerǁreset__mutmut_orig.__name__ = "xǁSyncCircuitBreakerǁreset"


# <3 🧱🤝💪🪄
