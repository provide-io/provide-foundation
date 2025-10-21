# provide/foundation/resilience/circuit_async.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
from collections.abc import Callable
import time
from typing import Any

from provide.foundation.resilience.circuit_sync import CircuitState

"""Asynchronous circuit breaker implementation."""
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


class AsyncCircuitBreaker:
    """Asynchronous circuit breaker for resilience patterns.

    Uses asyncio.Lock for async-safe state management.
    For synchronous code, use SyncCircuitBreaker instead.
    """

    def xǁAsyncCircuitBreakerǁ__init____mutmut_orig(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
        time_source: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the asynchronous circuit breaker.

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
        # Create lock directly - asyncio.Lock() can be created outside event loop
        # and will bind when first awaited
        self._lock = asyncio.Lock()
        # Initialize state
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: float | None = None

    def xǁAsyncCircuitBreakerǁ__init____mutmut_1(
        self,
        failure_threshold: int = 6,
        recovery_timeout: float = 30.0,
        expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
        time_source: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the asynchronous circuit breaker.

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
        # Create lock directly - asyncio.Lock() can be created outside event loop
        # and will bind when first awaited
        self._lock = asyncio.Lock()
        # Initialize state
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: float | None = None

    def xǁAsyncCircuitBreakerǁ__init____mutmut_2(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 31.0,
        expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
        time_source: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the asynchronous circuit breaker.

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
        # Create lock directly - asyncio.Lock() can be created outside event loop
        # and will bind when first awaited
        self._lock = asyncio.Lock()
        # Initialize state
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: float | None = None

    def xǁAsyncCircuitBreakerǁ__init____mutmut_3(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
        time_source: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the asynchronous circuit breaker.

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
        # Create lock directly - asyncio.Lock() can be created outside event loop
        # and will bind when first awaited
        self._lock = asyncio.Lock()
        # Initialize state
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: float | None = None

    def xǁAsyncCircuitBreakerǁ__init____mutmut_4(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
        time_source: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the asynchronous circuit breaker.

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
        # Create lock directly - asyncio.Lock() can be created outside event loop
        # and will bind when first awaited
        self._lock = asyncio.Lock()
        # Initialize state
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: float | None = None

    def xǁAsyncCircuitBreakerǁ__init____mutmut_5(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
        time_source: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the asynchronous circuit breaker.

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
        # Create lock directly - asyncio.Lock() can be created outside event loop
        # and will bind when first awaited
        self._lock = asyncio.Lock()
        # Initialize state
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: float | None = None

    def xǁAsyncCircuitBreakerǁ__init____mutmut_6(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
        time_source: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the asynchronous circuit breaker.

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
        # Create lock directly - asyncio.Lock() can be created outside event loop
        # and will bind when first awaited
        self._lock = asyncio.Lock()
        # Initialize state
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: float | None = None

    def xǁAsyncCircuitBreakerǁ__init____mutmut_7(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
        time_source: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the asynchronous circuit breaker.

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
        # Create lock directly - asyncio.Lock() can be created outside event loop
        # and will bind when first awaited
        self._lock = asyncio.Lock()
        # Initialize state
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: float | None = None

    def xǁAsyncCircuitBreakerǁ__init____mutmut_8(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
        time_source: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the asynchronous circuit breaker.

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
        # Create lock directly - asyncio.Lock() can be created outside event loop
        # and will bind when first awaited
        self._lock = None
        # Initialize state
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: float | None = None

    def xǁAsyncCircuitBreakerǁ__init____mutmut_9(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
        time_source: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the asynchronous circuit breaker.

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
        # Create lock directly - asyncio.Lock() can be created outside event loop
        # and will bind when first awaited
        self._lock = asyncio.Lock()
        # Initialize state
        self._state = None
        self._failure_count = 0
        self._last_failure_time: float | None = None

    def xǁAsyncCircuitBreakerǁ__init____mutmut_10(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
        time_source: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the asynchronous circuit breaker.

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
        # Create lock directly - asyncio.Lock() can be created outside event loop
        # and will bind when first awaited
        self._lock = asyncio.Lock()
        # Initialize state
        self._state = CircuitState.CLOSED
        self._failure_count = None
        self._last_failure_time: float | None = None

    def xǁAsyncCircuitBreakerǁ__init____mutmut_11(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
        time_source: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the asynchronous circuit breaker.

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
        # Create lock directly - asyncio.Lock() can be created outside event loop
        # and will bind when first awaited
        self._lock = asyncio.Lock()
        # Initialize state
        self._state = CircuitState.CLOSED
        self._failure_count = 1
        self._last_failure_time: float | None = None

    def xǁAsyncCircuitBreakerǁ__init____mutmut_12(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
        time_source: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the asynchronous circuit breaker.

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
        # Create lock directly - asyncio.Lock() can be created outside event loop
        # and will bind when first awaited
        self._lock = asyncio.Lock()
        # Initialize state
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: float | None = ""
    
    xǁAsyncCircuitBreakerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAsyncCircuitBreakerǁ__init____mutmut_1': xǁAsyncCircuitBreakerǁ__init____mutmut_1, 
        'xǁAsyncCircuitBreakerǁ__init____mutmut_2': xǁAsyncCircuitBreakerǁ__init____mutmut_2, 
        'xǁAsyncCircuitBreakerǁ__init____mutmut_3': xǁAsyncCircuitBreakerǁ__init____mutmut_3, 
        'xǁAsyncCircuitBreakerǁ__init____mutmut_4': xǁAsyncCircuitBreakerǁ__init____mutmut_4, 
        'xǁAsyncCircuitBreakerǁ__init____mutmut_5': xǁAsyncCircuitBreakerǁ__init____mutmut_5, 
        'xǁAsyncCircuitBreakerǁ__init____mutmut_6': xǁAsyncCircuitBreakerǁ__init____mutmut_6, 
        'xǁAsyncCircuitBreakerǁ__init____mutmut_7': xǁAsyncCircuitBreakerǁ__init____mutmut_7, 
        'xǁAsyncCircuitBreakerǁ__init____mutmut_8': xǁAsyncCircuitBreakerǁ__init____mutmut_8, 
        'xǁAsyncCircuitBreakerǁ__init____mutmut_9': xǁAsyncCircuitBreakerǁ__init____mutmut_9, 
        'xǁAsyncCircuitBreakerǁ__init____mutmut_10': xǁAsyncCircuitBreakerǁ__init____mutmut_10, 
        'xǁAsyncCircuitBreakerǁ__init____mutmut_11': xǁAsyncCircuitBreakerǁ__init____mutmut_11, 
        'xǁAsyncCircuitBreakerǁ__init____mutmut_12': xǁAsyncCircuitBreakerǁ__init____mutmut_12
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAsyncCircuitBreakerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁAsyncCircuitBreakerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁAsyncCircuitBreakerǁ__init____mutmut_orig)
    xǁAsyncCircuitBreakerǁ__init____mutmut_orig.__name__ = 'xǁAsyncCircuitBreakerǁ__init__'

    async def xǁAsyncCircuitBreakerǁstate__mutmut_orig(self) -> CircuitState:
        """Get the current state of the circuit breaker.

        Returns:
            Current circuit state
        """
        async with self._lock:
            if self._state == CircuitState.OPEN and self._can_attempt_recovery():
                # This is a view of the state; the actual transition happens in call()
                return CircuitState.HALF_OPEN
            return self._state

    async def xǁAsyncCircuitBreakerǁstate__mutmut_1(self) -> CircuitState:
        """Get the current state of the circuit breaker.

        Returns:
            Current circuit state
        """
        async with self._lock:
            if self._state == CircuitState.OPEN or self._can_attempt_recovery():
                # This is a view of the state; the actual transition happens in call()
                return CircuitState.HALF_OPEN
            return self._state

    async def xǁAsyncCircuitBreakerǁstate__mutmut_2(self) -> CircuitState:
        """Get the current state of the circuit breaker.

        Returns:
            Current circuit state
        """
        async with self._lock:
            if self._state != CircuitState.OPEN and self._can_attempt_recovery():
                # This is a view of the state; the actual transition happens in call()
                return CircuitState.HALF_OPEN
            return self._state
    
    xǁAsyncCircuitBreakerǁstate__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAsyncCircuitBreakerǁstate__mutmut_1': xǁAsyncCircuitBreakerǁstate__mutmut_1, 
        'xǁAsyncCircuitBreakerǁstate__mutmut_2': xǁAsyncCircuitBreakerǁstate__mutmut_2
    }
    
    def state(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAsyncCircuitBreakerǁstate__mutmut_orig"), object.__getattribute__(self, "xǁAsyncCircuitBreakerǁstate__mutmut_mutants"), args, kwargs, self)
        return result 
    
    state.__signature__ = _mutmut_signature(xǁAsyncCircuitBreakerǁstate__mutmut_orig)
    xǁAsyncCircuitBreakerǁstate__mutmut_orig.__name__ = 'xǁAsyncCircuitBreakerǁstate'

    async def failure_count(self) -> int:
        """Get the current failure count.

        Returns:
            Current failure count
        """
        async with self._lock:
            return self._failure_count

    def xǁAsyncCircuitBreakerǁ_can_attempt_recovery__mutmut_orig(self) -> bool:
        """Check if the circuit can attempt recovery."""
        return self._time_source() >= (self._last_failure_time or 0) + self.recovery_timeout

    def xǁAsyncCircuitBreakerǁ_can_attempt_recovery__mutmut_1(self) -> bool:
        """Check if the circuit can attempt recovery."""
        return self._time_source() > (self._last_failure_time or 0) + self.recovery_timeout

    def xǁAsyncCircuitBreakerǁ_can_attempt_recovery__mutmut_2(self) -> bool:
        """Check if the circuit can attempt recovery."""
        return self._time_source() >= (self._last_failure_time or 0) - self.recovery_timeout

    def xǁAsyncCircuitBreakerǁ_can_attempt_recovery__mutmut_3(self) -> bool:
        """Check if the circuit can attempt recovery."""
        return self._time_source() >= (self._last_failure_time and 0) + self.recovery_timeout

    def xǁAsyncCircuitBreakerǁ_can_attempt_recovery__mutmut_4(self) -> bool:
        """Check if the circuit can attempt recovery."""
        return self._time_source() >= (self._last_failure_time or 1) + self.recovery_timeout
    
    xǁAsyncCircuitBreakerǁ_can_attempt_recovery__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAsyncCircuitBreakerǁ_can_attempt_recovery__mutmut_1': xǁAsyncCircuitBreakerǁ_can_attempt_recovery__mutmut_1, 
        'xǁAsyncCircuitBreakerǁ_can_attempt_recovery__mutmut_2': xǁAsyncCircuitBreakerǁ_can_attempt_recovery__mutmut_2, 
        'xǁAsyncCircuitBreakerǁ_can_attempt_recovery__mutmut_3': xǁAsyncCircuitBreakerǁ_can_attempt_recovery__mutmut_3, 
        'xǁAsyncCircuitBreakerǁ_can_attempt_recovery__mutmut_4': xǁAsyncCircuitBreakerǁ_can_attempt_recovery__mutmut_4
    }
    
    def _can_attempt_recovery(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAsyncCircuitBreakerǁ_can_attempt_recovery__mutmut_orig"), object.__getattribute__(self, "xǁAsyncCircuitBreakerǁ_can_attempt_recovery__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _can_attempt_recovery.__signature__ = _mutmut_signature(xǁAsyncCircuitBreakerǁ_can_attempt_recovery__mutmut_orig)
    xǁAsyncCircuitBreakerǁ_can_attempt_recovery__mutmut_orig.__name__ = 'xǁAsyncCircuitBreakerǁ_can_attempt_recovery'

    async def xǁAsyncCircuitBreakerǁcall__mutmut_orig(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute an asynchronous function through the circuit breaker.

        Args:
            func: Async callable to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from func

        Raises:
            RuntimeError: If circuit is open
            Exception: Whatever exception func raises
        """
        async with self._lock:
            # Check state directly to avoid deadlock
            if self._state == CircuitState.OPEN and not self._can_attempt_recovery():
                raise RuntimeError("Circuit breaker is open")
            # If HALF_OPEN or recovery possible, we proceed with the call

        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
        except self.expected_exception as e:
            await self._on_failure()
            raise e

    async def xǁAsyncCircuitBreakerǁcall__mutmut_1(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute an asynchronous function through the circuit breaker.

        Args:
            func: Async callable to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from func

        Raises:
            RuntimeError: If circuit is open
            Exception: Whatever exception func raises
        """
        async with self._lock:
            # Check state directly to avoid deadlock
            if self._state == CircuitState.OPEN or not self._can_attempt_recovery():
                raise RuntimeError("Circuit breaker is open")
            # If HALF_OPEN or recovery possible, we proceed with the call

        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
        except self.expected_exception as e:
            await self._on_failure()
            raise e

    async def xǁAsyncCircuitBreakerǁcall__mutmut_2(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute an asynchronous function through the circuit breaker.

        Args:
            func: Async callable to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from func

        Raises:
            RuntimeError: If circuit is open
            Exception: Whatever exception func raises
        """
        async with self._lock:
            # Check state directly to avoid deadlock
            if self._state != CircuitState.OPEN and not self._can_attempt_recovery():
                raise RuntimeError("Circuit breaker is open")
            # If HALF_OPEN or recovery possible, we proceed with the call

        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
        except self.expected_exception as e:
            await self._on_failure()
            raise e

    async def xǁAsyncCircuitBreakerǁcall__mutmut_3(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute an asynchronous function through the circuit breaker.

        Args:
            func: Async callable to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from func

        Raises:
            RuntimeError: If circuit is open
            Exception: Whatever exception func raises
        """
        async with self._lock:
            # Check state directly to avoid deadlock
            if self._state == CircuitState.OPEN and self._can_attempt_recovery():
                raise RuntimeError("Circuit breaker is open")
            # If HALF_OPEN or recovery possible, we proceed with the call

        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
        except self.expected_exception as e:
            await self._on_failure()
            raise e

    async def xǁAsyncCircuitBreakerǁcall__mutmut_4(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute an asynchronous function through the circuit breaker.

        Args:
            func: Async callable to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from func

        Raises:
            RuntimeError: If circuit is open
            Exception: Whatever exception func raises
        """
        async with self._lock:
            # Check state directly to avoid deadlock
            if self._state == CircuitState.OPEN and not self._can_attempt_recovery():
                raise RuntimeError(None)
            # If HALF_OPEN or recovery possible, we proceed with the call

        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
        except self.expected_exception as e:
            await self._on_failure()
            raise e

    async def xǁAsyncCircuitBreakerǁcall__mutmut_5(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute an asynchronous function through the circuit breaker.

        Args:
            func: Async callable to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from func

        Raises:
            RuntimeError: If circuit is open
            Exception: Whatever exception func raises
        """
        async with self._lock:
            # Check state directly to avoid deadlock
            if self._state == CircuitState.OPEN and not self._can_attempt_recovery():
                raise RuntimeError("XXCircuit breaker is openXX")
            # If HALF_OPEN or recovery possible, we proceed with the call

        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
        except self.expected_exception as e:
            await self._on_failure()
            raise e

    async def xǁAsyncCircuitBreakerǁcall__mutmut_6(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute an asynchronous function through the circuit breaker.

        Args:
            func: Async callable to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from func

        Raises:
            RuntimeError: If circuit is open
            Exception: Whatever exception func raises
        """
        async with self._lock:
            # Check state directly to avoid deadlock
            if self._state == CircuitState.OPEN and not self._can_attempt_recovery():
                raise RuntimeError("circuit breaker is open")
            # If HALF_OPEN or recovery possible, we proceed with the call

        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
        except self.expected_exception as e:
            await self._on_failure()
            raise e

    async def xǁAsyncCircuitBreakerǁcall__mutmut_7(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute an asynchronous function through the circuit breaker.

        Args:
            func: Async callable to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from func

        Raises:
            RuntimeError: If circuit is open
            Exception: Whatever exception func raises
        """
        async with self._lock:
            # Check state directly to avoid deadlock
            if self._state == CircuitState.OPEN and not self._can_attempt_recovery():
                raise RuntimeError("CIRCUIT BREAKER IS OPEN")
            # If HALF_OPEN or recovery possible, we proceed with the call

        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
        except self.expected_exception as e:
            await self._on_failure()
            raise e

    async def xǁAsyncCircuitBreakerǁcall__mutmut_8(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute an asynchronous function through the circuit breaker.

        Args:
            func: Async callable to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from func

        Raises:
            RuntimeError: If circuit is open
            Exception: Whatever exception func raises
        """
        async with self._lock:
            # Check state directly to avoid deadlock
            if self._state == CircuitState.OPEN and not self._can_attempt_recovery():
                raise RuntimeError("Circuit breaker is open")
            # If HALF_OPEN or recovery possible, we proceed with the call

        try:
            result = None
            await self._on_success()
            return result
        except self.expected_exception as e:
            await self._on_failure()
            raise e

    async def xǁAsyncCircuitBreakerǁcall__mutmut_9(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute an asynchronous function through the circuit breaker.

        Args:
            func: Async callable to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from func

        Raises:
            RuntimeError: If circuit is open
            Exception: Whatever exception func raises
        """
        async with self._lock:
            # Check state directly to avoid deadlock
            if self._state == CircuitState.OPEN and not self._can_attempt_recovery():
                raise RuntimeError("Circuit breaker is open")
            # If HALF_OPEN or recovery possible, we proceed with the call

        try:
            result = await func(**kwargs)
            await self._on_success()
            return result
        except self.expected_exception as e:
            await self._on_failure()
            raise e

    async def xǁAsyncCircuitBreakerǁcall__mutmut_10(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute an asynchronous function through the circuit breaker.

        Args:
            func: Async callable to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from func

        Raises:
            RuntimeError: If circuit is open
            Exception: Whatever exception func raises
        """
        async with self._lock:
            # Check state directly to avoid deadlock
            if self._state == CircuitState.OPEN and not self._can_attempt_recovery():
                raise RuntimeError("Circuit breaker is open")
            # If HALF_OPEN or recovery possible, we proceed with the call

        try:
            result = await func(*args, )
            await self._on_success()
            return result
        except self.expected_exception as e:
            await self._on_failure()
            raise e
    
    xǁAsyncCircuitBreakerǁcall__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAsyncCircuitBreakerǁcall__mutmut_1': xǁAsyncCircuitBreakerǁcall__mutmut_1, 
        'xǁAsyncCircuitBreakerǁcall__mutmut_2': xǁAsyncCircuitBreakerǁcall__mutmut_2, 
        'xǁAsyncCircuitBreakerǁcall__mutmut_3': xǁAsyncCircuitBreakerǁcall__mutmut_3, 
        'xǁAsyncCircuitBreakerǁcall__mutmut_4': xǁAsyncCircuitBreakerǁcall__mutmut_4, 
        'xǁAsyncCircuitBreakerǁcall__mutmut_5': xǁAsyncCircuitBreakerǁcall__mutmut_5, 
        'xǁAsyncCircuitBreakerǁcall__mutmut_6': xǁAsyncCircuitBreakerǁcall__mutmut_6, 
        'xǁAsyncCircuitBreakerǁcall__mutmut_7': xǁAsyncCircuitBreakerǁcall__mutmut_7, 
        'xǁAsyncCircuitBreakerǁcall__mutmut_8': xǁAsyncCircuitBreakerǁcall__mutmut_8, 
        'xǁAsyncCircuitBreakerǁcall__mutmut_9': xǁAsyncCircuitBreakerǁcall__mutmut_9, 
        'xǁAsyncCircuitBreakerǁcall__mutmut_10': xǁAsyncCircuitBreakerǁcall__mutmut_10
    }
    
    def call(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAsyncCircuitBreakerǁcall__mutmut_orig"), object.__getattribute__(self, "xǁAsyncCircuitBreakerǁcall__mutmut_mutants"), args, kwargs, self)
        return result 
    
    call.__signature__ = _mutmut_signature(xǁAsyncCircuitBreakerǁcall__mutmut_orig)
    xǁAsyncCircuitBreakerǁcall__mutmut_orig.__name__ = 'xǁAsyncCircuitBreakerǁcall'

    async def xǁAsyncCircuitBreakerǁ_on_success__mutmut_orig(self) -> None:
        """Handle a successful call."""
        async with self._lock:
            # Success in either CLOSED or HALF_OPEN state resets the breaker.
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._last_failure_time = None

    async def xǁAsyncCircuitBreakerǁ_on_success__mutmut_1(self) -> None:
        """Handle a successful call."""
        async with self._lock:
            # Success in either CLOSED or HALF_OPEN state resets the breaker.
            self._state = None
            self._failure_count = 0
            self._last_failure_time = None

    async def xǁAsyncCircuitBreakerǁ_on_success__mutmut_2(self) -> None:
        """Handle a successful call."""
        async with self._lock:
            # Success in either CLOSED or HALF_OPEN state resets the breaker.
            self._state = CircuitState.CLOSED
            self._failure_count = None
            self._last_failure_time = None

    async def xǁAsyncCircuitBreakerǁ_on_success__mutmut_3(self) -> None:
        """Handle a successful call."""
        async with self._lock:
            # Success in either CLOSED or HALF_OPEN state resets the breaker.
            self._state = CircuitState.CLOSED
            self._failure_count = 1
            self._last_failure_time = None

    async def xǁAsyncCircuitBreakerǁ_on_success__mutmut_4(self) -> None:
        """Handle a successful call."""
        async with self._lock:
            # Success in either CLOSED or HALF_OPEN state resets the breaker.
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._last_failure_time = ""
    
    xǁAsyncCircuitBreakerǁ_on_success__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAsyncCircuitBreakerǁ_on_success__mutmut_1': xǁAsyncCircuitBreakerǁ_on_success__mutmut_1, 
        'xǁAsyncCircuitBreakerǁ_on_success__mutmut_2': xǁAsyncCircuitBreakerǁ_on_success__mutmut_2, 
        'xǁAsyncCircuitBreakerǁ_on_success__mutmut_3': xǁAsyncCircuitBreakerǁ_on_success__mutmut_3, 
        'xǁAsyncCircuitBreakerǁ_on_success__mutmut_4': xǁAsyncCircuitBreakerǁ_on_success__mutmut_4
    }
    
    def _on_success(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAsyncCircuitBreakerǁ_on_success__mutmut_orig"), object.__getattribute__(self, "xǁAsyncCircuitBreakerǁ_on_success__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _on_success.__signature__ = _mutmut_signature(xǁAsyncCircuitBreakerǁ_on_success__mutmut_orig)
    xǁAsyncCircuitBreakerǁ_on_success__mutmut_orig.__name__ = 'xǁAsyncCircuitBreakerǁ_on_success'

    async def xǁAsyncCircuitBreakerǁ_on_failure__mutmut_orig(self) -> None:
        """Handle a failed call."""
        async with self._lock:
            self._failure_count += 1
            if self._failure_count >= self.failure_threshold:
                # This transition happens for failures in CLOSED state
                # or for the single attempt in HALF_OPEN state.
                self._state = CircuitState.OPEN
                self._last_failure_time = self._time_source()

    async def xǁAsyncCircuitBreakerǁ_on_failure__mutmut_1(self) -> None:
        """Handle a failed call."""
        async with self._lock:
            self._failure_count = 1
            if self._failure_count >= self.failure_threshold:
                # This transition happens for failures in CLOSED state
                # or for the single attempt in HALF_OPEN state.
                self._state = CircuitState.OPEN
                self._last_failure_time = self._time_source()

    async def xǁAsyncCircuitBreakerǁ_on_failure__mutmut_2(self) -> None:
        """Handle a failed call."""
        async with self._lock:
            self._failure_count -= 1
            if self._failure_count >= self.failure_threshold:
                # This transition happens for failures in CLOSED state
                # or for the single attempt in HALF_OPEN state.
                self._state = CircuitState.OPEN
                self._last_failure_time = self._time_source()

    async def xǁAsyncCircuitBreakerǁ_on_failure__mutmut_3(self) -> None:
        """Handle a failed call."""
        async with self._lock:
            self._failure_count += 2
            if self._failure_count >= self.failure_threshold:
                # This transition happens for failures in CLOSED state
                # or for the single attempt in HALF_OPEN state.
                self._state = CircuitState.OPEN
                self._last_failure_time = self._time_source()

    async def xǁAsyncCircuitBreakerǁ_on_failure__mutmut_4(self) -> None:
        """Handle a failed call."""
        async with self._lock:
            self._failure_count += 1
            if self._failure_count > self.failure_threshold:
                # This transition happens for failures in CLOSED state
                # or for the single attempt in HALF_OPEN state.
                self._state = CircuitState.OPEN
                self._last_failure_time = self._time_source()

    async def xǁAsyncCircuitBreakerǁ_on_failure__mutmut_5(self) -> None:
        """Handle a failed call."""
        async with self._lock:
            self._failure_count += 1
            if self._failure_count >= self.failure_threshold:
                # This transition happens for failures in CLOSED state
                # or for the single attempt in HALF_OPEN state.
                self._state = None
                self._last_failure_time = self._time_source()

    async def xǁAsyncCircuitBreakerǁ_on_failure__mutmut_6(self) -> None:
        """Handle a failed call."""
        async with self._lock:
            self._failure_count += 1
            if self._failure_count >= self.failure_threshold:
                # This transition happens for failures in CLOSED state
                # or for the single attempt in HALF_OPEN state.
                self._state = CircuitState.OPEN
                self._last_failure_time = None
    
    xǁAsyncCircuitBreakerǁ_on_failure__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAsyncCircuitBreakerǁ_on_failure__mutmut_1': xǁAsyncCircuitBreakerǁ_on_failure__mutmut_1, 
        'xǁAsyncCircuitBreakerǁ_on_failure__mutmut_2': xǁAsyncCircuitBreakerǁ_on_failure__mutmut_2, 
        'xǁAsyncCircuitBreakerǁ_on_failure__mutmut_3': xǁAsyncCircuitBreakerǁ_on_failure__mutmut_3, 
        'xǁAsyncCircuitBreakerǁ_on_failure__mutmut_4': xǁAsyncCircuitBreakerǁ_on_failure__mutmut_4, 
        'xǁAsyncCircuitBreakerǁ_on_failure__mutmut_5': xǁAsyncCircuitBreakerǁ_on_failure__mutmut_5, 
        'xǁAsyncCircuitBreakerǁ_on_failure__mutmut_6': xǁAsyncCircuitBreakerǁ_on_failure__mutmut_6
    }
    
    def _on_failure(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAsyncCircuitBreakerǁ_on_failure__mutmut_orig"), object.__getattribute__(self, "xǁAsyncCircuitBreakerǁ_on_failure__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _on_failure.__signature__ = _mutmut_signature(xǁAsyncCircuitBreakerǁ_on_failure__mutmut_orig)
    xǁAsyncCircuitBreakerǁ_on_failure__mutmut_orig.__name__ = 'xǁAsyncCircuitBreakerǁ_on_failure'

    async def xǁAsyncCircuitBreakerǁreset__mutmut_orig(self) -> None:
        """Reset the circuit breaker to its initial state."""
        async with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._last_failure_time = None

    async def xǁAsyncCircuitBreakerǁreset__mutmut_1(self) -> None:
        """Reset the circuit breaker to its initial state."""
        async with self._lock:
            self._state = None
            self._failure_count = 0
            self._last_failure_time = None

    async def xǁAsyncCircuitBreakerǁreset__mutmut_2(self) -> None:
        """Reset the circuit breaker to its initial state."""
        async with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = None
            self._last_failure_time = None

    async def xǁAsyncCircuitBreakerǁreset__mutmut_3(self) -> None:
        """Reset the circuit breaker to its initial state."""
        async with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = 1
            self._last_failure_time = None

    async def xǁAsyncCircuitBreakerǁreset__mutmut_4(self) -> None:
        """Reset the circuit breaker to its initial state."""
        async with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._last_failure_time = ""
    
    xǁAsyncCircuitBreakerǁreset__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAsyncCircuitBreakerǁreset__mutmut_1': xǁAsyncCircuitBreakerǁreset__mutmut_1, 
        'xǁAsyncCircuitBreakerǁreset__mutmut_2': xǁAsyncCircuitBreakerǁreset__mutmut_2, 
        'xǁAsyncCircuitBreakerǁreset__mutmut_3': xǁAsyncCircuitBreakerǁreset__mutmut_3, 
        'xǁAsyncCircuitBreakerǁreset__mutmut_4': xǁAsyncCircuitBreakerǁreset__mutmut_4
    }
    
    def reset(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAsyncCircuitBreakerǁreset__mutmut_orig"), object.__getattribute__(self, "xǁAsyncCircuitBreakerǁreset__mutmut_mutants"), args, kwargs, self)
        return result 
    
    reset.__signature__ = _mutmut_signature(xǁAsyncCircuitBreakerǁreset__mutmut_orig)
    xǁAsyncCircuitBreakerǁreset__mutmut_orig.__name__ = 'xǁAsyncCircuitBreakerǁreset'


# <3 🧱🤝💪🪄
