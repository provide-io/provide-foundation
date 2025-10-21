# provide/foundation/resilience/decorators.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
from collections.abc import Callable
import functools
import inspect
import threading
from typing import TYPE_CHECKING, Any, TypeVar

from provide.foundation.errors.config import ConfigurationError
from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker
from provide.foundation.resilience.defaults import DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT
from provide.foundation.resilience.retry import (
    BackoffStrategy,
    RetryExecutor,
    RetryPolicy,
)

if TYPE_CHECKING:
    from provide.foundation.hub.registry import Registry

"""Resilience decorators for retry, circuit breaker, and fallback patterns."""

# Circuit breaker registry dimensions
CIRCUIT_BREAKER_DIMENSION = "circuit_breaker"
CIRCUIT_BREAKER_TEST_DIMENSION = "circuit_breaker_test"

# Counter for generating unique circuit breaker names (protected by lock)
_circuit_breaker_counter = 0
_circuit_breaker_counter_lock = threading.Lock()
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


def _get_circuit_breaker_registry() -> Registry:
    """Get the Hub registry for circuit breakers."""
    from provide.foundation.hub.manager import get_hub

    return get_hub()._component_registry


def x__should_register_for_global_reset__mutmut_orig() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" in filename or "test_" in filename or "conftest" in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_1() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = None
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" in filename or "test_" in filename or "conftest" in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_2() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is not None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" in filename or "test_" in filename or "conftest" in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_3() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return False

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" in filename or "test_" in filename or "conftest" in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_4() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = None
            if frame is None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" in filename or "test_" in filename or "conftest" in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_5() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is not None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" in filename or "test_" in filename or "conftest" in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_6() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                return

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" in filename or "test_" in filename or "conftest" in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_7() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            filename = None

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" in filename or "test_" in filename or "conftest" in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_8() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" in filename or "test_" in filename and "conftest" in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_9() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" in filename and "test_" in filename or "conftest" in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_10() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "XX/tests/XX" in filename or "test_" in filename or "conftest" in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_11() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/TESTS/" in filename or "test_" in filename or "conftest" in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_12() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" not in filename or "test_" in filename or "conftest" in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_13() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" in filename or "XXtest_XX" in filename or "conftest" in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_14() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" in filename or "TEST_" in filename or "conftest" in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_15() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" in filename or "test_" not in filename or "conftest" in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_16() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" in filename or "test_" in filename or "XXconftestXX" in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_17() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" in filename or "test_" in filename or "CONFTEST" in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_18() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" in filename or "test_" in filename or "conftest" not in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_19() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" in filename or "test_" in filename or "conftest" in filename:
                return True

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_20() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" in filename or "test_" in filename or "conftest" in filename:
                return False

        return False
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


def x__should_register_for_global_reset__mutmut_21() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" in filename or "test_" in filename or "conftest" in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return False

x__should_register_for_global_reset__mutmut_mutants : ClassVar[MutantDict] = {
'x__should_register_for_global_reset__mutmut_1': x__should_register_for_global_reset__mutmut_1, 
    'x__should_register_for_global_reset__mutmut_2': x__should_register_for_global_reset__mutmut_2, 
    'x__should_register_for_global_reset__mutmut_3': x__should_register_for_global_reset__mutmut_3, 
    'x__should_register_for_global_reset__mutmut_4': x__should_register_for_global_reset__mutmut_4, 
    'x__should_register_for_global_reset__mutmut_5': x__should_register_for_global_reset__mutmut_5, 
    'x__should_register_for_global_reset__mutmut_6': x__should_register_for_global_reset__mutmut_6, 
    'x__should_register_for_global_reset__mutmut_7': x__should_register_for_global_reset__mutmut_7, 
    'x__should_register_for_global_reset__mutmut_8': x__should_register_for_global_reset__mutmut_8, 
    'x__should_register_for_global_reset__mutmut_9': x__should_register_for_global_reset__mutmut_9, 
    'x__should_register_for_global_reset__mutmut_10': x__should_register_for_global_reset__mutmut_10, 
    'x__should_register_for_global_reset__mutmut_11': x__should_register_for_global_reset__mutmut_11, 
    'x__should_register_for_global_reset__mutmut_12': x__should_register_for_global_reset__mutmut_12, 
    'x__should_register_for_global_reset__mutmut_13': x__should_register_for_global_reset__mutmut_13, 
    'x__should_register_for_global_reset__mutmut_14': x__should_register_for_global_reset__mutmut_14, 
    'x__should_register_for_global_reset__mutmut_15': x__should_register_for_global_reset__mutmut_15, 
    'x__should_register_for_global_reset__mutmut_16': x__should_register_for_global_reset__mutmut_16, 
    'x__should_register_for_global_reset__mutmut_17': x__should_register_for_global_reset__mutmut_17, 
    'x__should_register_for_global_reset__mutmut_18': x__should_register_for_global_reset__mutmut_18, 
    'x__should_register_for_global_reset__mutmut_19': x__should_register_for_global_reset__mutmut_19, 
    'x__should_register_for_global_reset__mutmut_20': x__should_register_for_global_reset__mutmut_20, 
    'x__should_register_for_global_reset__mutmut_21': x__should_register_for_global_reset__mutmut_21
}

def _should_register_for_global_reset(*args, **kwargs):
    result = _mutmut_trampoline(x__should_register_for_global_reset__mutmut_orig, x__should_register_for_global_reset__mutmut_mutants, args, kwargs)
    return result 

_should_register_for_global_reset.__signature__ = _mutmut_signature(x__should_register_for_global_reset__mutmut_orig)
x__should_register_for_global_reset__mutmut_orig.__name__ = 'x__should_register_for_global_reset'


F = TypeVar("F", bound=Callable[..., Any])


def x__handle_no_parentheses_retry__mutmut_orig(func: F) -> F:
    """Handle @retry decorator used without parentheses."""
    executor = RetryExecutor(RetryPolicy())

    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return await executor.execute_async(func, *args, **kwargs)

        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper  # type: ignore[return-value]


def x__handle_no_parentheses_retry__mutmut_1(func: F) -> F:
    """Handle @retry decorator used without parentheses."""
    executor = None

    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return await executor.execute_async(func, *args, **kwargs)

        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper  # type: ignore[return-value]


def x__handle_no_parentheses_retry__mutmut_2(func: F) -> F:
    """Handle @retry decorator used without parentheses."""
    executor = RetryExecutor(None)

    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return await executor.execute_async(func, *args, **kwargs)

        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper  # type: ignore[return-value]


def x__handle_no_parentheses_retry__mutmut_3(func: F) -> F:
    """Handle @retry decorator used without parentheses."""
    executor = RetryExecutor(RetryPolicy())

    if asyncio.iscoroutinefunction(None):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return await executor.execute_async(func, *args, **kwargs)

        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper  # type: ignore[return-value]

x__handle_no_parentheses_retry__mutmut_mutants : ClassVar[MutantDict] = {
'x__handle_no_parentheses_retry__mutmut_1': x__handle_no_parentheses_retry__mutmut_1, 
    'x__handle_no_parentheses_retry__mutmut_2': x__handle_no_parentheses_retry__mutmut_2, 
    'x__handle_no_parentheses_retry__mutmut_3': x__handle_no_parentheses_retry__mutmut_3
}

def _handle_no_parentheses_retry(*args, **kwargs):
    result = _mutmut_trampoline(x__handle_no_parentheses_retry__mutmut_orig, x__handle_no_parentheses_retry__mutmut_mutants, args, kwargs)
    return result 

_handle_no_parentheses_retry.__signature__ = _mutmut_signature(x__handle_no_parentheses_retry__mutmut_orig)
x__handle_no_parentheses_retry__mutmut_orig.__name__ = 'x__handle_no_parentheses_retry'


def x__validate_retry_parameters__mutmut_orig(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_1(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None or any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_2(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_3(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        None
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_4(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_5(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            None,
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_6(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code=None,
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_7(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_8(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=None,
        )


def x__validate_retry_parameters__mutmut_9(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_10(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_11(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_12(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            )


def x__validate_retry_parameters__mutmut_13(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "XXCannot specify both policy and individual retry parametersXX",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_14(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_15(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "CANNOT SPECIFY BOTH POLICY AND INDIVIDUAL RETRY PARAMETERS",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_16(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="XXCONFLICTING_RETRY_CONFIGXX",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_17(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="conflicting_retry_config",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_18(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_19(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("XXmax_attemptsXX", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_20(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("MAX_ATTEMPTS", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_21(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("XXbase_delayXX", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_22(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("BASE_DELAY", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_23(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("XXbackoffXX", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_24(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("BACKOFF", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_25(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("XXmax_delayXX", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_26(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("MAX_DELAY", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_27(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("XXjitterXX", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_28(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("JITTER", jitter),
                ]
                if value is not None
            ],
        )


def x__validate_retry_parameters__mutmut_29(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is None
            ],
        )

x__validate_retry_parameters__mutmut_mutants : ClassVar[MutantDict] = {
'x__validate_retry_parameters__mutmut_1': x__validate_retry_parameters__mutmut_1, 
    'x__validate_retry_parameters__mutmut_2': x__validate_retry_parameters__mutmut_2, 
    'x__validate_retry_parameters__mutmut_3': x__validate_retry_parameters__mutmut_3, 
    'x__validate_retry_parameters__mutmut_4': x__validate_retry_parameters__mutmut_4, 
    'x__validate_retry_parameters__mutmut_5': x__validate_retry_parameters__mutmut_5, 
    'x__validate_retry_parameters__mutmut_6': x__validate_retry_parameters__mutmut_6, 
    'x__validate_retry_parameters__mutmut_7': x__validate_retry_parameters__mutmut_7, 
    'x__validate_retry_parameters__mutmut_8': x__validate_retry_parameters__mutmut_8, 
    'x__validate_retry_parameters__mutmut_9': x__validate_retry_parameters__mutmut_9, 
    'x__validate_retry_parameters__mutmut_10': x__validate_retry_parameters__mutmut_10, 
    'x__validate_retry_parameters__mutmut_11': x__validate_retry_parameters__mutmut_11, 
    'x__validate_retry_parameters__mutmut_12': x__validate_retry_parameters__mutmut_12, 
    'x__validate_retry_parameters__mutmut_13': x__validate_retry_parameters__mutmut_13, 
    'x__validate_retry_parameters__mutmut_14': x__validate_retry_parameters__mutmut_14, 
    'x__validate_retry_parameters__mutmut_15': x__validate_retry_parameters__mutmut_15, 
    'x__validate_retry_parameters__mutmut_16': x__validate_retry_parameters__mutmut_16, 
    'x__validate_retry_parameters__mutmut_17': x__validate_retry_parameters__mutmut_17, 
    'x__validate_retry_parameters__mutmut_18': x__validate_retry_parameters__mutmut_18, 
    'x__validate_retry_parameters__mutmut_19': x__validate_retry_parameters__mutmut_19, 
    'x__validate_retry_parameters__mutmut_20': x__validate_retry_parameters__mutmut_20, 
    'x__validate_retry_parameters__mutmut_21': x__validate_retry_parameters__mutmut_21, 
    'x__validate_retry_parameters__mutmut_22': x__validate_retry_parameters__mutmut_22, 
    'x__validate_retry_parameters__mutmut_23': x__validate_retry_parameters__mutmut_23, 
    'x__validate_retry_parameters__mutmut_24': x__validate_retry_parameters__mutmut_24, 
    'x__validate_retry_parameters__mutmut_25': x__validate_retry_parameters__mutmut_25, 
    'x__validate_retry_parameters__mutmut_26': x__validate_retry_parameters__mutmut_26, 
    'x__validate_retry_parameters__mutmut_27': x__validate_retry_parameters__mutmut_27, 
    'x__validate_retry_parameters__mutmut_28': x__validate_retry_parameters__mutmut_28, 
    'x__validate_retry_parameters__mutmut_29': x__validate_retry_parameters__mutmut_29
}

def _validate_retry_parameters(*args, **kwargs):
    result = _mutmut_trampoline(x__validate_retry_parameters__mutmut_orig, x__validate_retry_parameters__mutmut_mutants, args, kwargs)
    return result 

_validate_retry_parameters.__signature__ = _mutmut_signature(x__validate_retry_parameters__mutmut_orig)
x__validate_retry_parameters__mutmut_orig.__name__ = 'x__validate_retry_parameters'


def x__build_retry_policy__mutmut_orig(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_1(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = None

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_2(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_3(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = None
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_4(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["XXmax_attemptsXX"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_5(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["MAX_ATTEMPTS"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_6(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_7(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = None
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_8(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["XXbase_delayXX"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_9(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["BASE_DELAY"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_10(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_11(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = None
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_12(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["XXbackoffXX"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_13(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["BACKOFF"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_14(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_15(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = None
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_16(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["XXmax_delayXX"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_17(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["MAX_DELAY"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_18(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_19(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = None
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_20(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["XXjitterXX"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_21(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["JITTER"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_22(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = None

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_23(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["XXretryable_errorsXX"] = exceptions

    return RetryPolicy(**policy_kwargs)


def x__build_retry_policy__mutmut_24(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["RETRYABLE_ERRORS"] = exceptions

    return RetryPolicy(**policy_kwargs)

x__build_retry_policy__mutmut_mutants : ClassVar[MutantDict] = {
'x__build_retry_policy__mutmut_1': x__build_retry_policy__mutmut_1, 
    'x__build_retry_policy__mutmut_2': x__build_retry_policy__mutmut_2, 
    'x__build_retry_policy__mutmut_3': x__build_retry_policy__mutmut_3, 
    'x__build_retry_policy__mutmut_4': x__build_retry_policy__mutmut_4, 
    'x__build_retry_policy__mutmut_5': x__build_retry_policy__mutmut_5, 
    'x__build_retry_policy__mutmut_6': x__build_retry_policy__mutmut_6, 
    'x__build_retry_policy__mutmut_7': x__build_retry_policy__mutmut_7, 
    'x__build_retry_policy__mutmut_8': x__build_retry_policy__mutmut_8, 
    'x__build_retry_policy__mutmut_9': x__build_retry_policy__mutmut_9, 
    'x__build_retry_policy__mutmut_10': x__build_retry_policy__mutmut_10, 
    'x__build_retry_policy__mutmut_11': x__build_retry_policy__mutmut_11, 
    'x__build_retry_policy__mutmut_12': x__build_retry_policy__mutmut_12, 
    'x__build_retry_policy__mutmut_13': x__build_retry_policy__mutmut_13, 
    'x__build_retry_policy__mutmut_14': x__build_retry_policy__mutmut_14, 
    'x__build_retry_policy__mutmut_15': x__build_retry_policy__mutmut_15, 
    'x__build_retry_policy__mutmut_16': x__build_retry_policy__mutmut_16, 
    'x__build_retry_policy__mutmut_17': x__build_retry_policy__mutmut_17, 
    'x__build_retry_policy__mutmut_18': x__build_retry_policy__mutmut_18, 
    'x__build_retry_policy__mutmut_19': x__build_retry_policy__mutmut_19, 
    'x__build_retry_policy__mutmut_20': x__build_retry_policy__mutmut_20, 
    'x__build_retry_policy__mutmut_21': x__build_retry_policy__mutmut_21, 
    'x__build_retry_policy__mutmut_22': x__build_retry_policy__mutmut_22, 
    'x__build_retry_policy__mutmut_23': x__build_retry_policy__mutmut_23, 
    'x__build_retry_policy__mutmut_24': x__build_retry_policy__mutmut_24
}

def _build_retry_policy(*args, **kwargs):
    result = _mutmut_trampoline(x__build_retry_policy__mutmut_orig, x__build_retry_policy__mutmut_mutants, args, kwargs)
    return result 

_build_retry_policy.__signature__ = _mutmut_signature(x__build_retry_policy__mutmut_orig)
x__build_retry_policy__mutmut_orig.__name__ = 'x__build_retry_policy'


def x__create_retry_wrapper__mutmut_orig(
    func: F,
    policy: RetryPolicy,
    on_retry: Callable[[int, Exception], None] | None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> F:
    """Create the retry wrapper for a function."""
    executor = RetryExecutor(
        policy,
        on_retry=on_retry,
        time_source=time_source,
        sleep_func=sleep_func,
        async_sleep_func=async_sleep_func,
    )

    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return await executor.execute_async(func, *args, **kwargs)

        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper  # type: ignore[return-value]


def x__create_retry_wrapper__mutmut_1(
    func: F,
    policy: RetryPolicy,
    on_retry: Callable[[int, Exception], None] | None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> F:
    """Create the retry wrapper for a function."""
    executor = None

    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return await executor.execute_async(func, *args, **kwargs)

        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper  # type: ignore[return-value]


def x__create_retry_wrapper__mutmut_2(
    func: F,
    policy: RetryPolicy,
    on_retry: Callable[[int, Exception], None] | None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> F:
    """Create the retry wrapper for a function."""
    executor = RetryExecutor(
        None,
        on_retry=on_retry,
        time_source=time_source,
        sleep_func=sleep_func,
        async_sleep_func=async_sleep_func,
    )

    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return await executor.execute_async(func, *args, **kwargs)

        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper  # type: ignore[return-value]


def x__create_retry_wrapper__mutmut_3(
    func: F,
    policy: RetryPolicy,
    on_retry: Callable[[int, Exception], None] | None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> F:
    """Create the retry wrapper for a function."""
    executor = RetryExecutor(
        policy,
        on_retry=None,
        time_source=time_source,
        sleep_func=sleep_func,
        async_sleep_func=async_sleep_func,
    )

    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return await executor.execute_async(func, *args, **kwargs)

        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper  # type: ignore[return-value]


def x__create_retry_wrapper__mutmut_4(
    func: F,
    policy: RetryPolicy,
    on_retry: Callable[[int, Exception], None] | None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> F:
    """Create the retry wrapper for a function."""
    executor = RetryExecutor(
        policy,
        on_retry=on_retry,
        time_source=None,
        sleep_func=sleep_func,
        async_sleep_func=async_sleep_func,
    )

    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return await executor.execute_async(func, *args, **kwargs)

        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper  # type: ignore[return-value]


def x__create_retry_wrapper__mutmut_5(
    func: F,
    policy: RetryPolicy,
    on_retry: Callable[[int, Exception], None] | None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> F:
    """Create the retry wrapper for a function."""
    executor = RetryExecutor(
        policy,
        on_retry=on_retry,
        time_source=time_source,
        sleep_func=None,
        async_sleep_func=async_sleep_func,
    )

    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return await executor.execute_async(func, *args, **kwargs)

        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper  # type: ignore[return-value]


def x__create_retry_wrapper__mutmut_6(
    func: F,
    policy: RetryPolicy,
    on_retry: Callable[[int, Exception], None] | None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> F:
    """Create the retry wrapper for a function."""
    executor = RetryExecutor(
        policy,
        on_retry=on_retry,
        time_source=time_source,
        sleep_func=sleep_func,
        async_sleep_func=None,
    )

    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return await executor.execute_async(func, *args, **kwargs)

        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper  # type: ignore[return-value]


def x__create_retry_wrapper__mutmut_7(
    func: F,
    policy: RetryPolicy,
    on_retry: Callable[[int, Exception], None] | None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> F:
    """Create the retry wrapper for a function."""
    executor = RetryExecutor(
        on_retry=on_retry,
        time_source=time_source,
        sleep_func=sleep_func,
        async_sleep_func=async_sleep_func,
    )

    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return await executor.execute_async(func, *args, **kwargs)

        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper  # type: ignore[return-value]


def x__create_retry_wrapper__mutmut_8(
    func: F,
    policy: RetryPolicy,
    on_retry: Callable[[int, Exception], None] | None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> F:
    """Create the retry wrapper for a function."""
    executor = RetryExecutor(
        policy,
        time_source=time_source,
        sleep_func=sleep_func,
        async_sleep_func=async_sleep_func,
    )

    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return await executor.execute_async(func, *args, **kwargs)

        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper  # type: ignore[return-value]


def x__create_retry_wrapper__mutmut_9(
    func: F,
    policy: RetryPolicy,
    on_retry: Callable[[int, Exception], None] | None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> F:
    """Create the retry wrapper for a function."""
    executor = RetryExecutor(
        policy,
        on_retry=on_retry,
        sleep_func=sleep_func,
        async_sleep_func=async_sleep_func,
    )

    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return await executor.execute_async(func, *args, **kwargs)

        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper  # type: ignore[return-value]


def x__create_retry_wrapper__mutmut_10(
    func: F,
    policy: RetryPolicy,
    on_retry: Callable[[int, Exception], None] | None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> F:
    """Create the retry wrapper for a function."""
    executor = RetryExecutor(
        policy,
        on_retry=on_retry,
        time_source=time_source,
        async_sleep_func=async_sleep_func,
    )

    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return await executor.execute_async(func, *args, **kwargs)

        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper  # type: ignore[return-value]


def x__create_retry_wrapper__mutmut_11(
    func: F,
    policy: RetryPolicy,
    on_retry: Callable[[int, Exception], None] | None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> F:
    """Create the retry wrapper for a function."""
    executor = RetryExecutor(
        policy,
        on_retry=on_retry,
        time_source=time_source,
        sleep_func=sleep_func,
        )

    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return await executor.execute_async(func, *args, **kwargs)

        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper  # type: ignore[return-value]


def x__create_retry_wrapper__mutmut_12(
    func: F,
    policy: RetryPolicy,
    on_retry: Callable[[int, Exception], None] | None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> F:
    """Create the retry wrapper for a function."""
    executor = RetryExecutor(
        policy,
        on_retry=on_retry,
        time_source=time_source,
        sleep_func=sleep_func,
        async_sleep_func=async_sleep_func,
    )

    if asyncio.iscoroutinefunction(None):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return await executor.execute_async(func, *args, **kwargs)

        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper  # type: ignore[return-value]

x__create_retry_wrapper__mutmut_mutants : ClassVar[MutantDict] = {
'x__create_retry_wrapper__mutmut_1': x__create_retry_wrapper__mutmut_1, 
    'x__create_retry_wrapper__mutmut_2': x__create_retry_wrapper__mutmut_2, 
    'x__create_retry_wrapper__mutmut_3': x__create_retry_wrapper__mutmut_3, 
    'x__create_retry_wrapper__mutmut_4': x__create_retry_wrapper__mutmut_4, 
    'x__create_retry_wrapper__mutmut_5': x__create_retry_wrapper__mutmut_5, 
    'x__create_retry_wrapper__mutmut_6': x__create_retry_wrapper__mutmut_6, 
    'x__create_retry_wrapper__mutmut_7': x__create_retry_wrapper__mutmut_7, 
    'x__create_retry_wrapper__mutmut_8': x__create_retry_wrapper__mutmut_8, 
    'x__create_retry_wrapper__mutmut_9': x__create_retry_wrapper__mutmut_9, 
    'x__create_retry_wrapper__mutmut_10': x__create_retry_wrapper__mutmut_10, 
    'x__create_retry_wrapper__mutmut_11': x__create_retry_wrapper__mutmut_11, 
    'x__create_retry_wrapper__mutmut_12': x__create_retry_wrapper__mutmut_12
}

def _create_retry_wrapper(*args, **kwargs):
    result = _mutmut_trampoline(x__create_retry_wrapper__mutmut_orig, x__create_retry_wrapper__mutmut_mutants, args, kwargs)
    return result 

_create_retry_wrapper.__signature__ = _mutmut_signature(x__create_retry_wrapper__mutmut_orig)
x__create_retry_wrapper__mutmut_orig.__name__ = 'x__create_retry_wrapper'


def x_retry__mutmut_orig(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_1(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) or not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_2(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 or callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_3(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) != 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_4(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 2 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_5(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(None) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_6(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[1]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_7(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_8(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = None
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_9(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[1]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_10(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(None)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_11(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(None, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_12(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, None, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_13(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, None, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_14(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, None, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_15(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, None, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_16(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, None)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_17(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_18(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_19(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_20(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_21(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_22(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, )

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_23(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is not None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_24(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = None

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_25(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(None, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_26(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, None, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_27(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, None, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_28(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, None, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_29(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, None, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_30(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, None)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_31(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_32(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_33(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_34(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_35(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_36(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, )

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_37(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            None,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_38(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            None,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_39(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            None,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_40(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=None,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_41(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=None,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_42(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=None,
        )

    return decorator


def x_retry__mutmut_43(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_44(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_45(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_46(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_47(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def x_retry__mutmut_48(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            )

    return decorator

x_retry__mutmut_mutants : ClassVar[MutantDict] = {
'x_retry__mutmut_1': x_retry__mutmut_1, 
    'x_retry__mutmut_2': x_retry__mutmut_2, 
    'x_retry__mutmut_3': x_retry__mutmut_3, 
    'x_retry__mutmut_4': x_retry__mutmut_4, 
    'x_retry__mutmut_5': x_retry__mutmut_5, 
    'x_retry__mutmut_6': x_retry__mutmut_6, 
    'x_retry__mutmut_7': x_retry__mutmut_7, 
    'x_retry__mutmut_8': x_retry__mutmut_8, 
    'x_retry__mutmut_9': x_retry__mutmut_9, 
    'x_retry__mutmut_10': x_retry__mutmut_10, 
    'x_retry__mutmut_11': x_retry__mutmut_11, 
    'x_retry__mutmut_12': x_retry__mutmut_12, 
    'x_retry__mutmut_13': x_retry__mutmut_13, 
    'x_retry__mutmut_14': x_retry__mutmut_14, 
    'x_retry__mutmut_15': x_retry__mutmut_15, 
    'x_retry__mutmut_16': x_retry__mutmut_16, 
    'x_retry__mutmut_17': x_retry__mutmut_17, 
    'x_retry__mutmut_18': x_retry__mutmut_18, 
    'x_retry__mutmut_19': x_retry__mutmut_19, 
    'x_retry__mutmut_20': x_retry__mutmut_20, 
    'x_retry__mutmut_21': x_retry__mutmut_21, 
    'x_retry__mutmut_22': x_retry__mutmut_22, 
    'x_retry__mutmut_23': x_retry__mutmut_23, 
    'x_retry__mutmut_24': x_retry__mutmut_24, 
    'x_retry__mutmut_25': x_retry__mutmut_25, 
    'x_retry__mutmut_26': x_retry__mutmut_26, 
    'x_retry__mutmut_27': x_retry__mutmut_27, 
    'x_retry__mutmut_28': x_retry__mutmut_28, 
    'x_retry__mutmut_29': x_retry__mutmut_29, 
    'x_retry__mutmut_30': x_retry__mutmut_30, 
    'x_retry__mutmut_31': x_retry__mutmut_31, 
    'x_retry__mutmut_32': x_retry__mutmut_32, 
    'x_retry__mutmut_33': x_retry__mutmut_33, 
    'x_retry__mutmut_34': x_retry__mutmut_34, 
    'x_retry__mutmut_35': x_retry__mutmut_35, 
    'x_retry__mutmut_36': x_retry__mutmut_36, 
    'x_retry__mutmut_37': x_retry__mutmut_37, 
    'x_retry__mutmut_38': x_retry__mutmut_38, 
    'x_retry__mutmut_39': x_retry__mutmut_39, 
    'x_retry__mutmut_40': x_retry__mutmut_40, 
    'x_retry__mutmut_41': x_retry__mutmut_41, 
    'x_retry__mutmut_42': x_retry__mutmut_42, 
    'x_retry__mutmut_43': x_retry__mutmut_43, 
    'x_retry__mutmut_44': x_retry__mutmut_44, 
    'x_retry__mutmut_45': x_retry__mutmut_45, 
    'x_retry__mutmut_46': x_retry__mutmut_46, 
    'x_retry__mutmut_47': x_retry__mutmut_47, 
    'x_retry__mutmut_48': x_retry__mutmut_48
}

def retry(*args, **kwargs):
    result = _mutmut_trampoline(x_retry__mutmut_orig, x_retry__mutmut_mutants, args, kwargs)
    return result 

retry.__signature__ = _mutmut_signature(x_retry__mutmut_orig)
x_retry__mutmut_orig.__name__ = 'x_retry'


def x_circuit_breaker__mutmut_orig(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_1(
    failure_threshold: int = 6,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_2(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_3(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = None
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_4(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = None

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_5(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = None

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_6(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry and _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_7(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(None):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_8(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = None

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_9(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=None,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_10(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=None,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_11(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=None,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_12(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=None,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_13(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_14(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_15(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_16(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_17(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter = 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_18(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter -= 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_19(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 2
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_20(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = None

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_21(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(None, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_22(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, None, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_23(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=None)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_24(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_25(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_26(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, )
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_27(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(None, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_28(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, None, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_29(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=None)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_30(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_31(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_32(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, )

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_33(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = None

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_34(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=None,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_35(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=None,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_36(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=None,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_37(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=None,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_38(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_39(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_40(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_41(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_42(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter = 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_43(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter -= 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_44(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 2
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_45(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = None

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_46(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(None, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_47(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, None, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_48(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=None)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_49(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_50(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_51(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, )
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_52(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(None, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_53(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, None, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_54(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=None)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_55(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_56(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def x_circuit_breaker__mutmut_57(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    expected_exception_tuple: tuple[type[Exception], ...]
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        breaker: SyncCircuitBreaker | AsyncCircuitBreaker
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore[return-value]
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, )

            return sync_wrapper  # type: ignore[return-value]

    return decorator

x_circuit_breaker__mutmut_mutants : ClassVar[MutantDict] = {
'x_circuit_breaker__mutmut_1': x_circuit_breaker__mutmut_1, 
    'x_circuit_breaker__mutmut_2': x_circuit_breaker__mutmut_2, 
    'x_circuit_breaker__mutmut_3': x_circuit_breaker__mutmut_3, 
    'x_circuit_breaker__mutmut_4': x_circuit_breaker__mutmut_4, 
    'x_circuit_breaker__mutmut_5': x_circuit_breaker__mutmut_5, 
    'x_circuit_breaker__mutmut_6': x_circuit_breaker__mutmut_6, 
    'x_circuit_breaker__mutmut_7': x_circuit_breaker__mutmut_7, 
    'x_circuit_breaker__mutmut_8': x_circuit_breaker__mutmut_8, 
    'x_circuit_breaker__mutmut_9': x_circuit_breaker__mutmut_9, 
    'x_circuit_breaker__mutmut_10': x_circuit_breaker__mutmut_10, 
    'x_circuit_breaker__mutmut_11': x_circuit_breaker__mutmut_11, 
    'x_circuit_breaker__mutmut_12': x_circuit_breaker__mutmut_12, 
    'x_circuit_breaker__mutmut_13': x_circuit_breaker__mutmut_13, 
    'x_circuit_breaker__mutmut_14': x_circuit_breaker__mutmut_14, 
    'x_circuit_breaker__mutmut_15': x_circuit_breaker__mutmut_15, 
    'x_circuit_breaker__mutmut_16': x_circuit_breaker__mutmut_16, 
    'x_circuit_breaker__mutmut_17': x_circuit_breaker__mutmut_17, 
    'x_circuit_breaker__mutmut_18': x_circuit_breaker__mutmut_18, 
    'x_circuit_breaker__mutmut_19': x_circuit_breaker__mutmut_19, 
    'x_circuit_breaker__mutmut_20': x_circuit_breaker__mutmut_20, 
    'x_circuit_breaker__mutmut_21': x_circuit_breaker__mutmut_21, 
    'x_circuit_breaker__mutmut_22': x_circuit_breaker__mutmut_22, 
    'x_circuit_breaker__mutmut_23': x_circuit_breaker__mutmut_23, 
    'x_circuit_breaker__mutmut_24': x_circuit_breaker__mutmut_24, 
    'x_circuit_breaker__mutmut_25': x_circuit_breaker__mutmut_25, 
    'x_circuit_breaker__mutmut_26': x_circuit_breaker__mutmut_26, 
    'x_circuit_breaker__mutmut_27': x_circuit_breaker__mutmut_27, 
    'x_circuit_breaker__mutmut_28': x_circuit_breaker__mutmut_28, 
    'x_circuit_breaker__mutmut_29': x_circuit_breaker__mutmut_29, 
    'x_circuit_breaker__mutmut_30': x_circuit_breaker__mutmut_30, 
    'x_circuit_breaker__mutmut_31': x_circuit_breaker__mutmut_31, 
    'x_circuit_breaker__mutmut_32': x_circuit_breaker__mutmut_32, 
    'x_circuit_breaker__mutmut_33': x_circuit_breaker__mutmut_33, 
    'x_circuit_breaker__mutmut_34': x_circuit_breaker__mutmut_34, 
    'x_circuit_breaker__mutmut_35': x_circuit_breaker__mutmut_35, 
    'x_circuit_breaker__mutmut_36': x_circuit_breaker__mutmut_36, 
    'x_circuit_breaker__mutmut_37': x_circuit_breaker__mutmut_37, 
    'x_circuit_breaker__mutmut_38': x_circuit_breaker__mutmut_38, 
    'x_circuit_breaker__mutmut_39': x_circuit_breaker__mutmut_39, 
    'x_circuit_breaker__mutmut_40': x_circuit_breaker__mutmut_40, 
    'x_circuit_breaker__mutmut_41': x_circuit_breaker__mutmut_41, 
    'x_circuit_breaker__mutmut_42': x_circuit_breaker__mutmut_42, 
    'x_circuit_breaker__mutmut_43': x_circuit_breaker__mutmut_43, 
    'x_circuit_breaker__mutmut_44': x_circuit_breaker__mutmut_44, 
    'x_circuit_breaker__mutmut_45': x_circuit_breaker__mutmut_45, 
    'x_circuit_breaker__mutmut_46': x_circuit_breaker__mutmut_46, 
    'x_circuit_breaker__mutmut_47': x_circuit_breaker__mutmut_47, 
    'x_circuit_breaker__mutmut_48': x_circuit_breaker__mutmut_48, 
    'x_circuit_breaker__mutmut_49': x_circuit_breaker__mutmut_49, 
    'x_circuit_breaker__mutmut_50': x_circuit_breaker__mutmut_50, 
    'x_circuit_breaker__mutmut_51': x_circuit_breaker__mutmut_51, 
    'x_circuit_breaker__mutmut_52': x_circuit_breaker__mutmut_52, 
    'x_circuit_breaker__mutmut_53': x_circuit_breaker__mutmut_53, 
    'x_circuit_breaker__mutmut_54': x_circuit_breaker__mutmut_54, 
    'x_circuit_breaker__mutmut_55': x_circuit_breaker__mutmut_55, 
    'x_circuit_breaker__mutmut_56': x_circuit_breaker__mutmut_56, 
    'x_circuit_breaker__mutmut_57': x_circuit_breaker__mutmut_57
}

def circuit_breaker(*args, **kwargs):
    result = _mutmut_trampoline(x_circuit_breaker__mutmut_orig, x_circuit_breaker__mutmut_mutants, args, kwargs)
    return result 

circuit_breaker.__signature__ = _mutmut_signature(x_circuit_breaker__mutmut_orig)
x_circuit_breaker__mutmut_orig.__name__ = 'x_circuit_breaker'


async def x_reset_circuit_breakers_for_testing__mutmut_orig() -> None:
    """Reset all circuit breaker instances for test isolation.

    This function is called by the test framework to ensure
    circuit breaker state doesn't leak between tests.

    Note: This is an async function because AsyncCircuitBreaker has async methods.
    Both sync and async circuit breakers are reset using their reset() method.
    """
    registry = _get_circuit_breaker_registry()
    for name in registry.list_dimension(CIRCUIT_BREAKER_DIMENSION):
        breaker = registry.get(name, dimension=CIRCUIT_BREAKER_DIMENSION)
        if breaker:
            if isinstance(breaker, AsyncCircuitBreaker):
                await breaker.reset()
            else:
                breaker.reset()


async def x_reset_circuit_breakers_for_testing__mutmut_1() -> None:
    """Reset all circuit breaker instances for test isolation.

    This function is called by the test framework to ensure
    circuit breaker state doesn't leak between tests.

    Note: This is an async function because AsyncCircuitBreaker has async methods.
    Both sync and async circuit breakers are reset using their reset() method.
    """
    registry = None
    for name in registry.list_dimension(CIRCUIT_BREAKER_DIMENSION):
        breaker = registry.get(name, dimension=CIRCUIT_BREAKER_DIMENSION)
        if breaker:
            if isinstance(breaker, AsyncCircuitBreaker):
                await breaker.reset()
            else:
                breaker.reset()


async def x_reset_circuit_breakers_for_testing__mutmut_2() -> None:
    """Reset all circuit breaker instances for test isolation.

    This function is called by the test framework to ensure
    circuit breaker state doesn't leak between tests.

    Note: This is an async function because AsyncCircuitBreaker has async methods.
    Both sync and async circuit breakers are reset using their reset() method.
    """
    registry = _get_circuit_breaker_registry()
    for name in registry.list_dimension(None):
        breaker = registry.get(name, dimension=CIRCUIT_BREAKER_DIMENSION)
        if breaker:
            if isinstance(breaker, AsyncCircuitBreaker):
                await breaker.reset()
            else:
                breaker.reset()


async def x_reset_circuit_breakers_for_testing__mutmut_3() -> None:
    """Reset all circuit breaker instances for test isolation.

    This function is called by the test framework to ensure
    circuit breaker state doesn't leak between tests.

    Note: This is an async function because AsyncCircuitBreaker has async methods.
    Both sync and async circuit breakers are reset using their reset() method.
    """
    registry = _get_circuit_breaker_registry()
    for name in registry.list_dimension(CIRCUIT_BREAKER_DIMENSION):
        breaker = None
        if breaker:
            if isinstance(breaker, AsyncCircuitBreaker):
                await breaker.reset()
            else:
                breaker.reset()


async def x_reset_circuit_breakers_for_testing__mutmut_4() -> None:
    """Reset all circuit breaker instances for test isolation.

    This function is called by the test framework to ensure
    circuit breaker state doesn't leak between tests.

    Note: This is an async function because AsyncCircuitBreaker has async methods.
    Both sync and async circuit breakers are reset using their reset() method.
    """
    registry = _get_circuit_breaker_registry()
    for name in registry.list_dimension(CIRCUIT_BREAKER_DIMENSION):
        breaker = registry.get(None, dimension=CIRCUIT_BREAKER_DIMENSION)
        if breaker:
            if isinstance(breaker, AsyncCircuitBreaker):
                await breaker.reset()
            else:
                breaker.reset()


async def x_reset_circuit_breakers_for_testing__mutmut_5() -> None:
    """Reset all circuit breaker instances for test isolation.

    This function is called by the test framework to ensure
    circuit breaker state doesn't leak between tests.

    Note: This is an async function because AsyncCircuitBreaker has async methods.
    Both sync and async circuit breakers are reset using their reset() method.
    """
    registry = _get_circuit_breaker_registry()
    for name in registry.list_dimension(CIRCUIT_BREAKER_DIMENSION):
        breaker = registry.get(name, dimension=None)
        if breaker:
            if isinstance(breaker, AsyncCircuitBreaker):
                await breaker.reset()
            else:
                breaker.reset()


async def x_reset_circuit_breakers_for_testing__mutmut_6() -> None:
    """Reset all circuit breaker instances for test isolation.

    This function is called by the test framework to ensure
    circuit breaker state doesn't leak between tests.

    Note: This is an async function because AsyncCircuitBreaker has async methods.
    Both sync and async circuit breakers are reset using their reset() method.
    """
    registry = _get_circuit_breaker_registry()
    for name in registry.list_dimension(CIRCUIT_BREAKER_DIMENSION):
        breaker = registry.get(dimension=CIRCUIT_BREAKER_DIMENSION)
        if breaker:
            if isinstance(breaker, AsyncCircuitBreaker):
                await breaker.reset()
            else:
                breaker.reset()


async def x_reset_circuit_breakers_for_testing__mutmut_7() -> None:
    """Reset all circuit breaker instances for test isolation.

    This function is called by the test framework to ensure
    circuit breaker state doesn't leak between tests.

    Note: This is an async function because AsyncCircuitBreaker has async methods.
    Both sync and async circuit breakers are reset using their reset() method.
    """
    registry = _get_circuit_breaker_registry()
    for name in registry.list_dimension(CIRCUIT_BREAKER_DIMENSION):
        breaker = registry.get(name, )
        if breaker:
            if isinstance(breaker, AsyncCircuitBreaker):
                await breaker.reset()
            else:
                breaker.reset()

x_reset_circuit_breakers_for_testing__mutmut_mutants : ClassVar[MutantDict] = {
'x_reset_circuit_breakers_for_testing__mutmut_1': x_reset_circuit_breakers_for_testing__mutmut_1, 
    'x_reset_circuit_breakers_for_testing__mutmut_2': x_reset_circuit_breakers_for_testing__mutmut_2, 
    'x_reset_circuit_breakers_for_testing__mutmut_3': x_reset_circuit_breakers_for_testing__mutmut_3, 
    'x_reset_circuit_breakers_for_testing__mutmut_4': x_reset_circuit_breakers_for_testing__mutmut_4, 
    'x_reset_circuit_breakers_for_testing__mutmut_5': x_reset_circuit_breakers_for_testing__mutmut_5, 
    'x_reset_circuit_breakers_for_testing__mutmut_6': x_reset_circuit_breakers_for_testing__mutmut_6, 
    'x_reset_circuit_breakers_for_testing__mutmut_7': x_reset_circuit_breakers_for_testing__mutmut_7
}

def reset_circuit_breakers_for_testing(*args, **kwargs):
    result = _mutmut_trampoline(x_reset_circuit_breakers_for_testing__mutmut_orig, x_reset_circuit_breakers_for_testing__mutmut_mutants, args, kwargs)
    return result 

reset_circuit_breakers_for_testing.__signature__ = _mutmut_signature(x_reset_circuit_breakers_for_testing__mutmut_orig)
x_reset_circuit_breakers_for_testing__mutmut_orig.__name__ = 'x_reset_circuit_breakers_for_testing'


async def x_reset_test_circuit_breakers__mutmut_orig() -> None:
    """Reset circuit breaker instances created in test files.

    This function resets circuit breakers that were created within test files
    to ensure proper test isolation without affecting production circuit breakers.

    Note: This is an async function because AsyncCircuitBreaker has async methods.
    Both sync and async circuit breakers are reset using their reset() method.
    """
    registry = _get_circuit_breaker_registry()
    for name in registry.list_dimension(CIRCUIT_BREAKER_TEST_DIMENSION):
        breaker = registry.get(name, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)
        if breaker:
            if isinstance(breaker, AsyncCircuitBreaker):
                await breaker.reset()
            else:
                breaker.reset()


async def x_reset_test_circuit_breakers__mutmut_1() -> None:
    """Reset circuit breaker instances created in test files.

    This function resets circuit breakers that were created within test files
    to ensure proper test isolation without affecting production circuit breakers.

    Note: This is an async function because AsyncCircuitBreaker has async methods.
    Both sync and async circuit breakers are reset using their reset() method.
    """
    registry = None
    for name in registry.list_dimension(CIRCUIT_BREAKER_TEST_DIMENSION):
        breaker = registry.get(name, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)
        if breaker:
            if isinstance(breaker, AsyncCircuitBreaker):
                await breaker.reset()
            else:
                breaker.reset()


async def x_reset_test_circuit_breakers__mutmut_2() -> None:
    """Reset circuit breaker instances created in test files.

    This function resets circuit breakers that were created within test files
    to ensure proper test isolation without affecting production circuit breakers.

    Note: This is an async function because AsyncCircuitBreaker has async methods.
    Both sync and async circuit breakers are reset using their reset() method.
    """
    registry = _get_circuit_breaker_registry()
    for name in registry.list_dimension(None):
        breaker = registry.get(name, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)
        if breaker:
            if isinstance(breaker, AsyncCircuitBreaker):
                await breaker.reset()
            else:
                breaker.reset()


async def x_reset_test_circuit_breakers__mutmut_3() -> None:
    """Reset circuit breaker instances created in test files.

    This function resets circuit breakers that were created within test files
    to ensure proper test isolation without affecting production circuit breakers.

    Note: This is an async function because AsyncCircuitBreaker has async methods.
    Both sync and async circuit breakers are reset using their reset() method.
    """
    registry = _get_circuit_breaker_registry()
    for name in registry.list_dimension(CIRCUIT_BREAKER_TEST_DIMENSION):
        breaker = None
        if breaker:
            if isinstance(breaker, AsyncCircuitBreaker):
                await breaker.reset()
            else:
                breaker.reset()


async def x_reset_test_circuit_breakers__mutmut_4() -> None:
    """Reset circuit breaker instances created in test files.

    This function resets circuit breakers that were created within test files
    to ensure proper test isolation without affecting production circuit breakers.

    Note: This is an async function because AsyncCircuitBreaker has async methods.
    Both sync and async circuit breakers are reset using their reset() method.
    """
    registry = _get_circuit_breaker_registry()
    for name in registry.list_dimension(CIRCUIT_BREAKER_TEST_DIMENSION):
        breaker = registry.get(None, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)
        if breaker:
            if isinstance(breaker, AsyncCircuitBreaker):
                await breaker.reset()
            else:
                breaker.reset()


async def x_reset_test_circuit_breakers__mutmut_5() -> None:
    """Reset circuit breaker instances created in test files.

    This function resets circuit breakers that were created within test files
    to ensure proper test isolation without affecting production circuit breakers.

    Note: This is an async function because AsyncCircuitBreaker has async methods.
    Both sync and async circuit breakers are reset using their reset() method.
    """
    registry = _get_circuit_breaker_registry()
    for name in registry.list_dimension(CIRCUIT_BREAKER_TEST_DIMENSION):
        breaker = registry.get(name, dimension=None)
        if breaker:
            if isinstance(breaker, AsyncCircuitBreaker):
                await breaker.reset()
            else:
                breaker.reset()


async def x_reset_test_circuit_breakers__mutmut_6() -> None:
    """Reset circuit breaker instances created in test files.

    This function resets circuit breakers that were created within test files
    to ensure proper test isolation without affecting production circuit breakers.

    Note: This is an async function because AsyncCircuitBreaker has async methods.
    Both sync and async circuit breakers are reset using their reset() method.
    """
    registry = _get_circuit_breaker_registry()
    for name in registry.list_dimension(CIRCUIT_BREAKER_TEST_DIMENSION):
        breaker = registry.get(dimension=CIRCUIT_BREAKER_TEST_DIMENSION)
        if breaker:
            if isinstance(breaker, AsyncCircuitBreaker):
                await breaker.reset()
            else:
                breaker.reset()


async def x_reset_test_circuit_breakers__mutmut_7() -> None:
    """Reset circuit breaker instances created in test files.

    This function resets circuit breakers that were created within test files
    to ensure proper test isolation without affecting production circuit breakers.

    Note: This is an async function because AsyncCircuitBreaker has async methods.
    Both sync and async circuit breakers are reset using their reset() method.
    """
    registry = _get_circuit_breaker_registry()
    for name in registry.list_dimension(CIRCUIT_BREAKER_TEST_DIMENSION):
        breaker = registry.get(name, )
        if breaker:
            if isinstance(breaker, AsyncCircuitBreaker):
                await breaker.reset()
            else:
                breaker.reset()

x_reset_test_circuit_breakers__mutmut_mutants : ClassVar[MutantDict] = {
'x_reset_test_circuit_breakers__mutmut_1': x_reset_test_circuit_breakers__mutmut_1, 
    'x_reset_test_circuit_breakers__mutmut_2': x_reset_test_circuit_breakers__mutmut_2, 
    'x_reset_test_circuit_breakers__mutmut_3': x_reset_test_circuit_breakers__mutmut_3, 
    'x_reset_test_circuit_breakers__mutmut_4': x_reset_test_circuit_breakers__mutmut_4, 
    'x_reset_test_circuit_breakers__mutmut_5': x_reset_test_circuit_breakers__mutmut_5, 
    'x_reset_test_circuit_breakers__mutmut_6': x_reset_test_circuit_breakers__mutmut_6, 
    'x_reset_test_circuit_breakers__mutmut_7': x_reset_test_circuit_breakers__mutmut_7
}

def reset_test_circuit_breakers(*args, **kwargs):
    result = _mutmut_trampoline(x_reset_test_circuit_breakers__mutmut_orig, x_reset_test_circuit_breakers__mutmut_mutants, args, kwargs)
    return result 

reset_test_circuit_breakers.__signature__ = _mutmut_signature(x_reset_test_circuit_breakers__mutmut_orig)
x_reset_test_circuit_breakers__mutmut_orig.__name__ = 'x_reset_test_circuit_breakers'


def x_fallback__mutmut_orig(*fallback_funcs: Callable[..., Any]) -> Callable[[F], F]:
    """Fallback decorator using FallbackChain.

    Args:
        *fallback_funcs: Functions to use as fallbacks, in order of preference

    Returns:
        Decorated function with fallback chain

    Examples:
        >>> def backup_api():
        ...     return "backup result"
        ...
        >>> @fallback(backup_api)
        ... def primary_api():
        ...     return external_api_call()

    """
    from provide.foundation.resilience.fallback import FallbackChain

    def decorator(func: F) -> F:
        chain = FallbackChain()
        for fallback_func in fallback_funcs:
            chain.add_fallback(fallback_func)

        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await chain.execute_async(func, *args, **kwargs)

            return async_wrapper  # type: ignore

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            return chain.execute(func, *args, **kwargs)

        return sync_wrapper  # type: ignore

    return decorator


def x_fallback__mutmut_1(*fallback_funcs: Callable[..., Any]) -> Callable[[F], F]:
    """Fallback decorator using FallbackChain.

    Args:
        *fallback_funcs: Functions to use as fallbacks, in order of preference

    Returns:
        Decorated function with fallback chain

    Examples:
        >>> def backup_api():
        ...     return "backup result"
        ...
        >>> @fallback(backup_api)
        ... def primary_api():
        ...     return external_api_call()

    """
    from provide.foundation.resilience.fallback import FallbackChain

    def decorator(func: F) -> F:
        chain = None
        for fallback_func in fallback_funcs:
            chain.add_fallback(fallback_func)

        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await chain.execute_async(func, *args, **kwargs)

            return async_wrapper  # type: ignore

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            return chain.execute(func, *args, **kwargs)

        return sync_wrapper  # type: ignore

    return decorator


def x_fallback__mutmut_2(*fallback_funcs: Callable[..., Any]) -> Callable[[F], F]:
    """Fallback decorator using FallbackChain.

    Args:
        *fallback_funcs: Functions to use as fallbacks, in order of preference

    Returns:
        Decorated function with fallback chain

    Examples:
        >>> def backup_api():
        ...     return "backup result"
        ...
        >>> @fallback(backup_api)
        ... def primary_api():
        ...     return external_api_call()

    """
    from provide.foundation.resilience.fallback import FallbackChain

    def decorator(func: F) -> F:
        chain = FallbackChain()
        for fallback_func in fallback_funcs:
            chain.add_fallback(None)

        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await chain.execute_async(func, *args, **kwargs)

            return async_wrapper  # type: ignore

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            return chain.execute(func, *args, **kwargs)

        return sync_wrapper  # type: ignore

    return decorator


def x_fallback__mutmut_3(*fallback_funcs: Callable[..., Any]) -> Callable[[F], F]:
    """Fallback decorator using FallbackChain.

    Args:
        *fallback_funcs: Functions to use as fallbacks, in order of preference

    Returns:
        Decorated function with fallback chain

    Examples:
        >>> def backup_api():
        ...     return "backup result"
        ...
        >>> @fallback(backup_api)
        ... def primary_api():
        ...     return external_api_call()

    """
    from provide.foundation.resilience.fallback import FallbackChain

    def decorator(func: F) -> F:
        chain = FallbackChain()
        for fallback_func in fallback_funcs:
            chain.add_fallback(fallback_func)

        if asyncio.iscoroutinefunction(None):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await chain.execute_async(func, *args, **kwargs)

            return async_wrapper  # type: ignore

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            return chain.execute(func, *args, **kwargs)

        return sync_wrapper  # type: ignore

    return decorator

x_fallback__mutmut_mutants : ClassVar[MutantDict] = {
'x_fallback__mutmut_1': x_fallback__mutmut_1, 
    'x_fallback__mutmut_2': x_fallback__mutmut_2, 
    'x_fallback__mutmut_3': x_fallback__mutmut_3
}

def fallback(*args, **kwargs):
    result = _mutmut_trampoline(x_fallback__mutmut_orig, x_fallback__mutmut_mutants, args, kwargs)
    return result 

fallback.__signature__ = _mutmut_signature(x_fallback__mutmut_orig)
x_fallback__mutmut_orig.__name__ = 'x_fallback'


# <3 🧱🤝💪🪄
