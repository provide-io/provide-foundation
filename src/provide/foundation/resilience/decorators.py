from __future__ import annotations

import asyncio
from collections.abc import Callable
import functools
import inspect
from typing import Any, TypeVar

from provide.foundation.config.defaults import DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT
from provide.foundation.errors.config import ConfigurationError
from provide.foundation.resilience.circuit import CircuitBreaker
from provide.foundation.resilience.retry import (
    BackoffStrategy,
    RetryExecutor,
    RetryPolicy,
)

"""Resilience decorators for retry, circuit breaker, and fallback patterns."""

# Global registry of circuit breaker instances for testing
_circuit_breaker_instances: list[CircuitBreaker] = []

# Separate registry for circuit breakers created in test files
_test_circuit_breaker_instances: list[CircuitBreaker] = []


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

        return async_wrapper

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper


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

        return async_wrapper

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper


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


# Import CircuitBreaker from circuit module


def circuit_breaker(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception types that trigger the breaker.

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

    """
    breaker = CircuitBreaker(
        failure_threshold=failure_threshold,
        recovery_timeout=recovery_timeout,
        expected_exception=expected_exception,
    )

    # Register for appropriate cleanup based on context
    if _should_register_for_global_reset():
        # Production circuit breakers
        _circuit_breaker_instances.append(breaker)
    else:
        # Test circuit breakers go to separate registry for isolated reset
        _test_circuit_breaker_instances.append(breaker)

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            return breaker.call(func, *args, **kwargs)

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return await breaker.call_async(func, *args, **kwargs)

        if asyncio.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        return sync_wrapper  # type: ignore

    return decorator


def reset_circuit_breakers_for_testing() -> None:
    """Reset all circuit breaker instances for test isolation.

    This function is called by the test framework to ensure
    circuit breaker state doesn't leak between tests.
    """
    for breaker in _circuit_breaker_instances:
        breaker.reset()


def reset_test_circuit_breakers() -> None:
    """Reset circuit breaker instances created in test files.

    This function resets circuit breakers that were created within test files
    to ensure proper test isolation without affecting production circuit breakers.
    """
    for breaker in _test_circuit_breaker_instances:
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
