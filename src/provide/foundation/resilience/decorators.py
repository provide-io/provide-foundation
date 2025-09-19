from __future__ import annotations

import asyncio
from collections.abc import Callable
import functools
from typing import Any, TypeVar

from provide.foundation.config.defaults import DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT
from provide.foundation.resilience.circuit import CircuitBreaker
from provide.foundation.resilience.retry import (
    BackoffStrategy,
    RetryExecutor,
    RetryPolicy,
)

"""Resilience decorators for retry, circuit breaker, and fallback patterns."""

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
        raise ValueError("Cannot specify both policy and individual retry parameters")


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
) -> F:
    """Create the retry wrapper for a function."""
    executor = RetryExecutor(policy, on_retry=on_retry)

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
        return _create_retry_wrapper(func, policy, on_retry)

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
