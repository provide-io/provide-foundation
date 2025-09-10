"""
Resilience decorators for retry, circuit breaker, and fallback patterns.
"""

import asyncio
import functools
import time
from typing import Any, Callable, TypeVar

from attrs import define, field

from provide.foundation.config.defaults import DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT
from provide.foundation.resilience.retry import BackoffStrategy, RetryExecutor, RetryPolicy

F = TypeVar("F", bound=Callable[..., Any])


def _get_logger():
    """Get logger instance lazily to avoid circular imports."""
    from provide.foundation.logger import logger
    return logger


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
    """
    Decorator for retrying operations on errors.
    
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
        executor = RetryExecutor(RetryPolicy())
        
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                return await executor.execute_async(func, *args, **kwargs)
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                return executor.execute_sync(func, *args, **kwargs)
            return sync_wrapper
    
    # Build policy if not provided
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ValueError(
            "Cannot specify both policy and individual retry parameters"
        )
    
    if policy is None:
        # Build policy from parameters
        policy_kwargs = {}
        
        if max_attempts is not None:
            policy_kwargs['max_attempts'] = max_attempts
        if base_delay is not None:
            policy_kwargs['base_delay'] = base_delay
        if backoff is not None:
            policy_kwargs['backoff'] = backoff
        if max_delay is not None:
            policy_kwargs['max_delay'] = max_delay
        if jitter is not None:
            policy_kwargs['jitter'] = jitter
        if exceptions:
            policy_kwargs['retryable_errors'] = exceptions
        
        policy = RetryPolicy(**policy_kwargs)
    
    def decorator(func: F) -> F:
        executor = RetryExecutor(policy, on_retry=on_retry)
        
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                return await executor.execute_async(func, *args, **kwargs)
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                return executor.execute_sync(func, *args, **kwargs)
            return sync_wrapper
    
    return decorator


# Import CircuitBreaker from circuit module
from provide.foundation.resilience.circuit import CircuitBreaker


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
        def sync_wrapper(*args, **kwargs):
            return breaker.call(func, *args, **kwargs)
        
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await breaker.call_async(func, *args, **kwargs)
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        else:
            return sync_wrapper  # type: ignore
    
    return decorator


def fallback(*fallback_funcs: Callable[..., Any]) -> Callable[[F], F]:
    """
    Fallback decorator using FallbackChain.
    
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
            async def async_wrapper(*args, **kwargs):
                return await chain.execute_async(func, *args, **kwargs)
            return async_wrapper  # type: ignore
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                return chain.execute(func, *args, **kwargs)
            return sync_wrapper  # type: ignore
    
    return decorator