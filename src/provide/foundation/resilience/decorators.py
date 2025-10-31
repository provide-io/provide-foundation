#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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


def _get_circuit_breaker_registry() -> Registry:
    """Get the Hub registry for circuit breakers."""
    from provide.foundation.hub.manager import get_hub

    return get_hub()._component_registry


def _should_register_for_global_reset() -> bool:
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


F = TypeVar("F", bound=Callable[..., Any])


def _handle_no_parentheses_retry(func: F) -> F:
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


def _validate_retry_parameters(
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


def _build_retry_policy(
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


def _create_retry_wrapper(
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


def retry(
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


def circuit_breaker(
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


async def reset_circuit_breakers_for_testing() -> None:
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


async def reset_test_circuit_breakers() -> None:
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


def fallback(*fallback_funcs: Callable[..., Any]) -> Callable[[F], F]:
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


# 🧱🏗️🔚
