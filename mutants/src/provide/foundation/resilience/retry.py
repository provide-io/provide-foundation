# provide/foundation/resilience/retry.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
import random
import time
from typing import Any, TypeVar

from attrs import define, field, validators

from provide.foundation.resilience.defaults import (
    DEFAULT_RETRY_BASE_DELAY,
    DEFAULT_RETRY_JITTER,
    DEFAULT_RETRY_MAX_ATTEMPTS,
    DEFAULT_RETRY_MAX_DELAY,
    DEFAULT_RETRY_RETRYABLE_ERRORS,
    DEFAULT_RETRY_RETRYABLE_STATUS_CODES,
    default_retry_backoff_strategy,
)
from provide.foundation.resilience.types import BackoffStrategy

"""Unified retry execution engine and policy configuration.

This module provides the core retry functionality used throughout foundation,
eliminating duplication between decorators and middleware.
"""

T = TypeVar("T")
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


@define(frozen=True, kw_only=True)
class RetryPolicy:
    """Configuration for retry behavior.

    This policy can be used with both the @retry decorator and transport middleware,
    providing a unified configuration model for all retry scenarios.

    Attributes:
        max_attempts: Maximum number of retry attempts (must be >= 1)
        backoff: Backoff strategy to use for delays
        base_delay: Base delay in seconds between retries
        max_delay: Maximum delay in seconds (caps exponential growth)
        jitter: Whether to add random jitter to delays (±25%)
        retryable_errors: Tuple of exception types to retry (None = all)
        retryable_status_codes: Set of HTTP status codes to retry (for middleware)

    """

    max_attempts: int = field(default=DEFAULT_RETRY_MAX_ATTEMPTS, validator=validators.instance_of(int))
    backoff: BackoffStrategy = field(factory=default_retry_backoff_strategy)
    base_delay: float = field(default=DEFAULT_RETRY_BASE_DELAY, validator=validators.instance_of((int, float)))
    max_delay: float = field(default=DEFAULT_RETRY_MAX_DELAY, validator=validators.instance_of((int, float)))
    jitter: bool = field(default=DEFAULT_RETRY_JITTER)
    retryable_errors: tuple[type[Exception], ...] | None = field(default=DEFAULT_RETRY_RETRYABLE_ERRORS)
    retryable_status_codes: set[int] | None = field(default=DEFAULT_RETRY_RETRYABLE_STATUS_CODES)

    @max_attempts.validator
    def _validate_max_attempts(self, attribute: object, value: int) -> None:
        """Validate max_attempts is at least 1."""
        if value < 1:
            raise ValueError("max_attempts must be at least 1")

    @base_delay.validator
    def _validate_base_delay(self, attribute: object, value: float) -> None:
        """Validate base_delay is positive."""
        if value < 0:
            raise ValueError("base_delay must be positive")

    @max_delay.validator
    def _validate_max_delay(self, attribute: object, value: float) -> None:
        """Validate max_delay is positive and >= base_delay."""
        if value < 0:
            raise ValueError("max_delay must be positive")
        if value < self.base_delay:
            raise ValueError("max_delay must be >= base_delay")

    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for a given attempt number.

        Args:
            attempt: Attempt number (1-based)

        Returns:
            Delay in seconds

        """
        if attempt <= 0:
            return 0

        if self.backoff == BackoffStrategy.FIXED:
            delay = self.base_delay
        elif self.backoff == BackoffStrategy.LINEAR:
            delay = self.base_delay * attempt
        elif self.backoff == BackoffStrategy.EXPONENTIAL:
            delay = self.base_delay * (2 ** (attempt - 1))
        elif self.backoff == BackoffStrategy.FIBONACCI:
            # Calculate fibonacci number for attempt
            a, b = 0, 1
            for _ in range(attempt):
                a, b = b, a + b
            delay = self.base_delay * a
        else:
            delay = self.base_delay

        # Cap at max delay
        delay = min(delay, self.max_delay)

        # Add jitter if configured (±25% random variation)
        if self.jitter:
            jitter_factor = 0.75 + (random.random() * 0.5)  # nosec B311 - Retry jitter timing
            delay *= jitter_factor

        return delay

    def should_retry(self, error: Exception, attempt: int) -> bool:
        """Determine if an error should be retried.

        Args:
            error: The exception that occurred
            attempt: Current attempt number (1-based)

        Returns:
            True if should retry, False otherwise

        """
        # Check attempt limit
        if attempt >= self.max_attempts:
            return False

        # Check error type if filter is configured
        if self.retryable_errors is not None:
            return isinstance(error, self.retryable_errors)

        # Default to retry for any error
        return True

    def should_retry_response(self, response: Any, attempt: int) -> bool:
        """Check if HTTP response should be retried.

        Args:
            response: Response object with status attribute
            attempt: Current attempt number (1-based)

        Returns:
            True if should retry, False otherwise

        """
        # Check attempt limit
        if attempt >= self.max_attempts:
            return False

        # Check status code if configured
        if self.retryable_status_codes is not None:
            return getattr(response, "status", None) in self.retryable_status_codes

        # Default to no retry for responses
        return False

    def __str__(self) -> str:
        """Human-readable string representation."""
        return (
            f"RetryPolicy(max_attempts={self.max_attempts}, "
            f"backoff={self.backoff.value}, base_delay={self.base_delay}s)"
        )


class RetryExecutor:
    """Unified retry execution engine.

    This executor handles the actual retry loop logic for both sync and async
    functions, using a RetryPolicy for configuration. It's used internally by
    both the @retry decorator and RetryMiddleware.
    """

    def xǁRetryExecutorǁ__init____mutmut_orig(
        self,
        policy: RetryPolicy,
        on_retry: Callable[[int, Exception], None] | None = None,
        time_source: Callable[[], float] | None = None,
        sleep_func: Callable[[float], None] | None = None,
        async_sleep_func: Callable[[float], Awaitable[None]] | None = None,
    ) -> None:
        """Initialize retry executor.

        Args:
            policy: Retry policy configuration
            on_retry: Optional callback for retry events (attempt, error)
            time_source: Optional callable that returns current time (for testing).
                        Defaults to time.time() for production use.
            sleep_func: Optional synchronous sleep function (for testing).
                       Defaults to time.sleep() for production use.
            async_sleep_func: Optional asynchronous sleep function (for testing).
                             Defaults to asyncio.sleep() for production use.

        """
        self.policy = policy
        self.on_retry = on_retry
        self._time_source = time_source or time.time
        self._sleep = sleep_func or time.sleep
        self._async_sleep = async_sleep_func or asyncio.sleep

    def xǁRetryExecutorǁ__init____mutmut_1(
        self,
        policy: RetryPolicy,
        on_retry: Callable[[int, Exception], None] | None = None,
        time_source: Callable[[], float] | None = None,
        sleep_func: Callable[[float], None] | None = None,
        async_sleep_func: Callable[[float], Awaitable[None]] | None = None,
    ) -> None:
        """Initialize retry executor.

        Args:
            policy: Retry policy configuration
            on_retry: Optional callback for retry events (attempt, error)
            time_source: Optional callable that returns current time (for testing).
                        Defaults to time.time() for production use.
            sleep_func: Optional synchronous sleep function (for testing).
                       Defaults to time.sleep() for production use.
            async_sleep_func: Optional asynchronous sleep function (for testing).
                             Defaults to asyncio.sleep() for production use.

        """
        self.policy = None
        self.on_retry = on_retry
        self._time_source = time_source or time.time
        self._sleep = sleep_func or time.sleep
        self._async_sleep = async_sleep_func or asyncio.sleep

    def xǁRetryExecutorǁ__init____mutmut_2(
        self,
        policy: RetryPolicy,
        on_retry: Callable[[int, Exception], None] | None = None,
        time_source: Callable[[], float] | None = None,
        sleep_func: Callable[[float], None] | None = None,
        async_sleep_func: Callable[[float], Awaitable[None]] | None = None,
    ) -> None:
        """Initialize retry executor.

        Args:
            policy: Retry policy configuration
            on_retry: Optional callback for retry events (attempt, error)
            time_source: Optional callable that returns current time (for testing).
                        Defaults to time.time() for production use.
            sleep_func: Optional synchronous sleep function (for testing).
                       Defaults to time.sleep() for production use.
            async_sleep_func: Optional asynchronous sleep function (for testing).
                             Defaults to asyncio.sleep() for production use.

        """
        self.policy = policy
        self.on_retry = None
        self._time_source = time_source or time.time
        self._sleep = sleep_func or time.sleep
        self._async_sleep = async_sleep_func or asyncio.sleep

    def xǁRetryExecutorǁ__init____mutmut_3(
        self,
        policy: RetryPolicy,
        on_retry: Callable[[int, Exception], None] | None = None,
        time_source: Callable[[], float] | None = None,
        sleep_func: Callable[[float], None] | None = None,
        async_sleep_func: Callable[[float], Awaitable[None]] | None = None,
    ) -> None:
        """Initialize retry executor.

        Args:
            policy: Retry policy configuration
            on_retry: Optional callback for retry events (attempt, error)
            time_source: Optional callable that returns current time (for testing).
                        Defaults to time.time() for production use.
            sleep_func: Optional synchronous sleep function (for testing).
                       Defaults to time.sleep() for production use.
            async_sleep_func: Optional asynchronous sleep function (for testing).
                             Defaults to asyncio.sleep() for production use.

        """
        self.policy = policy
        self.on_retry = on_retry
        self._time_source = None
        self._sleep = sleep_func or time.sleep
        self._async_sleep = async_sleep_func or asyncio.sleep

    def xǁRetryExecutorǁ__init____mutmut_4(
        self,
        policy: RetryPolicy,
        on_retry: Callable[[int, Exception], None] | None = None,
        time_source: Callable[[], float] | None = None,
        sleep_func: Callable[[float], None] | None = None,
        async_sleep_func: Callable[[float], Awaitable[None]] | None = None,
    ) -> None:
        """Initialize retry executor.

        Args:
            policy: Retry policy configuration
            on_retry: Optional callback for retry events (attempt, error)
            time_source: Optional callable that returns current time (for testing).
                        Defaults to time.time() for production use.
            sleep_func: Optional synchronous sleep function (for testing).
                       Defaults to time.sleep() for production use.
            async_sleep_func: Optional asynchronous sleep function (for testing).
                             Defaults to asyncio.sleep() for production use.

        """
        self.policy = policy
        self.on_retry = on_retry
        self._time_source = time_source and time.time
        self._sleep = sleep_func or time.sleep
        self._async_sleep = async_sleep_func or asyncio.sleep

    def xǁRetryExecutorǁ__init____mutmut_5(
        self,
        policy: RetryPolicy,
        on_retry: Callable[[int, Exception], None] | None = None,
        time_source: Callable[[], float] | None = None,
        sleep_func: Callable[[float], None] | None = None,
        async_sleep_func: Callable[[float], Awaitable[None]] | None = None,
    ) -> None:
        """Initialize retry executor.

        Args:
            policy: Retry policy configuration
            on_retry: Optional callback for retry events (attempt, error)
            time_source: Optional callable that returns current time (for testing).
                        Defaults to time.time() for production use.
            sleep_func: Optional synchronous sleep function (for testing).
                       Defaults to time.sleep() for production use.
            async_sleep_func: Optional asynchronous sleep function (for testing).
                             Defaults to asyncio.sleep() for production use.

        """
        self.policy = policy
        self.on_retry = on_retry
        self._time_source = time_source or time.time
        self._sleep = None
        self._async_sleep = async_sleep_func or asyncio.sleep

    def xǁRetryExecutorǁ__init____mutmut_6(
        self,
        policy: RetryPolicy,
        on_retry: Callable[[int, Exception], None] | None = None,
        time_source: Callable[[], float] | None = None,
        sleep_func: Callable[[float], None] | None = None,
        async_sleep_func: Callable[[float], Awaitable[None]] | None = None,
    ) -> None:
        """Initialize retry executor.

        Args:
            policy: Retry policy configuration
            on_retry: Optional callback for retry events (attempt, error)
            time_source: Optional callable that returns current time (for testing).
                        Defaults to time.time() for production use.
            sleep_func: Optional synchronous sleep function (for testing).
                       Defaults to time.sleep() for production use.
            async_sleep_func: Optional asynchronous sleep function (for testing).
                             Defaults to asyncio.sleep() for production use.

        """
        self.policy = policy
        self.on_retry = on_retry
        self._time_source = time_source or time.time
        self._sleep = sleep_func and time.sleep
        self._async_sleep = async_sleep_func or asyncio.sleep

    def xǁRetryExecutorǁ__init____mutmut_7(
        self,
        policy: RetryPolicy,
        on_retry: Callable[[int, Exception], None] | None = None,
        time_source: Callable[[], float] | None = None,
        sleep_func: Callable[[float], None] | None = None,
        async_sleep_func: Callable[[float], Awaitable[None]] | None = None,
    ) -> None:
        """Initialize retry executor.

        Args:
            policy: Retry policy configuration
            on_retry: Optional callback for retry events (attempt, error)
            time_source: Optional callable that returns current time (for testing).
                        Defaults to time.time() for production use.
            sleep_func: Optional synchronous sleep function (for testing).
                       Defaults to time.sleep() for production use.
            async_sleep_func: Optional asynchronous sleep function (for testing).
                             Defaults to asyncio.sleep() for production use.

        """
        self.policy = policy
        self.on_retry = on_retry
        self._time_source = time_source or time.time
        self._sleep = sleep_func or time.sleep
        self._async_sleep = None

    def xǁRetryExecutorǁ__init____mutmut_8(
        self,
        policy: RetryPolicy,
        on_retry: Callable[[int, Exception], None] | None = None,
        time_source: Callable[[], float] | None = None,
        sleep_func: Callable[[float], None] | None = None,
        async_sleep_func: Callable[[float], Awaitable[None]] | None = None,
    ) -> None:
        """Initialize retry executor.

        Args:
            policy: Retry policy configuration
            on_retry: Optional callback for retry events (attempt, error)
            time_source: Optional callable that returns current time (for testing).
                        Defaults to time.time() for production use.
            sleep_func: Optional synchronous sleep function (for testing).
                       Defaults to time.sleep() for production use.
            async_sleep_func: Optional asynchronous sleep function (for testing).
                             Defaults to asyncio.sleep() for production use.

        """
        self.policy = policy
        self.on_retry = on_retry
        self._time_source = time_source or time.time
        self._sleep = sleep_func or time.sleep
        self._async_sleep = async_sleep_func and asyncio.sleep
    
    xǁRetryExecutorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRetryExecutorǁ__init____mutmut_1': xǁRetryExecutorǁ__init____mutmut_1, 
        'xǁRetryExecutorǁ__init____mutmut_2': xǁRetryExecutorǁ__init____mutmut_2, 
        'xǁRetryExecutorǁ__init____mutmut_3': xǁRetryExecutorǁ__init____mutmut_3, 
        'xǁRetryExecutorǁ__init____mutmut_4': xǁRetryExecutorǁ__init____mutmut_4, 
        'xǁRetryExecutorǁ__init____mutmut_5': xǁRetryExecutorǁ__init____mutmut_5, 
        'xǁRetryExecutorǁ__init____mutmut_6': xǁRetryExecutorǁ__init____mutmut_6, 
        'xǁRetryExecutorǁ__init____mutmut_7': xǁRetryExecutorǁ__init____mutmut_7, 
        'xǁRetryExecutorǁ__init____mutmut_8': xǁRetryExecutorǁ__init____mutmut_8
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRetryExecutorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁRetryExecutorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁRetryExecutorǁ__init____mutmut_orig)
    xǁRetryExecutorǁ__init____mutmut_orig.__name__ = 'xǁRetryExecutorǁ__init__'

    def xǁRetryExecutorǁexecute_sync__mutmut_orig(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_1(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = ""

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_2(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(None, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_3(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, None):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_4(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_5(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, ):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_6(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(2, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_7(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts - 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_8(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 2):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_9(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(**kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_10(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, )
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_11(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = None

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_12(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt > self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_13(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        None,
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_14(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=None,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_15(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=None,
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_16(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=None,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_17(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_18(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_19(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_20(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_21(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(None),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_22(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(None).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_23(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_24(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(None, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_25(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, None):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_26(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_27(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, ):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_28(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = None

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_29(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(None)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_30(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    None,
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_31(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=None,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_32(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=None,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_33(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=None,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_34(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=None,
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_35(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=None,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_36(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_37(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_38(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_39(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_40(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_41(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_42(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(None),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_43(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(None).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_44(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(None, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_45(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, None)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_46(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_47(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, )
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_48(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning(None, error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_49(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=None)

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_50(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning(error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_51(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", )

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_52(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("XXRetry callback failedXX", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_53(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_54(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("RETRY CALLBACK FAILED", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_55(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(None))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_56(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(None)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_57(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_58(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError(None)

    def xǁRetryExecutorǁexecute_sync__mutmut_59(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("XXNo exception captured during retry attemptsXX")

    def xǁRetryExecutorǁexecute_sync__mutmut_60(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("no exception captured during retry attempts")

    def xǁRetryExecutorǁexecute_sync__mutmut_61(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                self._sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("NO EXCEPTION CAPTURED DURING RETRY ATTEMPTS")
    
    xǁRetryExecutorǁexecute_sync__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRetryExecutorǁexecute_sync__mutmut_1': xǁRetryExecutorǁexecute_sync__mutmut_1, 
        'xǁRetryExecutorǁexecute_sync__mutmut_2': xǁRetryExecutorǁexecute_sync__mutmut_2, 
        'xǁRetryExecutorǁexecute_sync__mutmut_3': xǁRetryExecutorǁexecute_sync__mutmut_3, 
        'xǁRetryExecutorǁexecute_sync__mutmut_4': xǁRetryExecutorǁexecute_sync__mutmut_4, 
        'xǁRetryExecutorǁexecute_sync__mutmut_5': xǁRetryExecutorǁexecute_sync__mutmut_5, 
        'xǁRetryExecutorǁexecute_sync__mutmut_6': xǁRetryExecutorǁexecute_sync__mutmut_6, 
        'xǁRetryExecutorǁexecute_sync__mutmut_7': xǁRetryExecutorǁexecute_sync__mutmut_7, 
        'xǁRetryExecutorǁexecute_sync__mutmut_8': xǁRetryExecutorǁexecute_sync__mutmut_8, 
        'xǁRetryExecutorǁexecute_sync__mutmut_9': xǁRetryExecutorǁexecute_sync__mutmut_9, 
        'xǁRetryExecutorǁexecute_sync__mutmut_10': xǁRetryExecutorǁexecute_sync__mutmut_10, 
        'xǁRetryExecutorǁexecute_sync__mutmut_11': xǁRetryExecutorǁexecute_sync__mutmut_11, 
        'xǁRetryExecutorǁexecute_sync__mutmut_12': xǁRetryExecutorǁexecute_sync__mutmut_12, 
        'xǁRetryExecutorǁexecute_sync__mutmut_13': xǁRetryExecutorǁexecute_sync__mutmut_13, 
        'xǁRetryExecutorǁexecute_sync__mutmut_14': xǁRetryExecutorǁexecute_sync__mutmut_14, 
        'xǁRetryExecutorǁexecute_sync__mutmut_15': xǁRetryExecutorǁexecute_sync__mutmut_15, 
        'xǁRetryExecutorǁexecute_sync__mutmut_16': xǁRetryExecutorǁexecute_sync__mutmut_16, 
        'xǁRetryExecutorǁexecute_sync__mutmut_17': xǁRetryExecutorǁexecute_sync__mutmut_17, 
        'xǁRetryExecutorǁexecute_sync__mutmut_18': xǁRetryExecutorǁexecute_sync__mutmut_18, 
        'xǁRetryExecutorǁexecute_sync__mutmut_19': xǁRetryExecutorǁexecute_sync__mutmut_19, 
        'xǁRetryExecutorǁexecute_sync__mutmut_20': xǁRetryExecutorǁexecute_sync__mutmut_20, 
        'xǁRetryExecutorǁexecute_sync__mutmut_21': xǁRetryExecutorǁexecute_sync__mutmut_21, 
        'xǁRetryExecutorǁexecute_sync__mutmut_22': xǁRetryExecutorǁexecute_sync__mutmut_22, 
        'xǁRetryExecutorǁexecute_sync__mutmut_23': xǁRetryExecutorǁexecute_sync__mutmut_23, 
        'xǁRetryExecutorǁexecute_sync__mutmut_24': xǁRetryExecutorǁexecute_sync__mutmut_24, 
        'xǁRetryExecutorǁexecute_sync__mutmut_25': xǁRetryExecutorǁexecute_sync__mutmut_25, 
        'xǁRetryExecutorǁexecute_sync__mutmut_26': xǁRetryExecutorǁexecute_sync__mutmut_26, 
        'xǁRetryExecutorǁexecute_sync__mutmut_27': xǁRetryExecutorǁexecute_sync__mutmut_27, 
        'xǁRetryExecutorǁexecute_sync__mutmut_28': xǁRetryExecutorǁexecute_sync__mutmut_28, 
        'xǁRetryExecutorǁexecute_sync__mutmut_29': xǁRetryExecutorǁexecute_sync__mutmut_29, 
        'xǁRetryExecutorǁexecute_sync__mutmut_30': xǁRetryExecutorǁexecute_sync__mutmut_30, 
        'xǁRetryExecutorǁexecute_sync__mutmut_31': xǁRetryExecutorǁexecute_sync__mutmut_31, 
        'xǁRetryExecutorǁexecute_sync__mutmut_32': xǁRetryExecutorǁexecute_sync__mutmut_32, 
        'xǁRetryExecutorǁexecute_sync__mutmut_33': xǁRetryExecutorǁexecute_sync__mutmut_33, 
        'xǁRetryExecutorǁexecute_sync__mutmut_34': xǁRetryExecutorǁexecute_sync__mutmut_34, 
        'xǁRetryExecutorǁexecute_sync__mutmut_35': xǁRetryExecutorǁexecute_sync__mutmut_35, 
        'xǁRetryExecutorǁexecute_sync__mutmut_36': xǁRetryExecutorǁexecute_sync__mutmut_36, 
        'xǁRetryExecutorǁexecute_sync__mutmut_37': xǁRetryExecutorǁexecute_sync__mutmut_37, 
        'xǁRetryExecutorǁexecute_sync__mutmut_38': xǁRetryExecutorǁexecute_sync__mutmut_38, 
        'xǁRetryExecutorǁexecute_sync__mutmut_39': xǁRetryExecutorǁexecute_sync__mutmut_39, 
        'xǁRetryExecutorǁexecute_sync__mutmut_40': xǁRetryExecutorǁexecute_sync__mutmut_40, 
        'xǁRetryExecutorǁexecute_sync__mutmut_41': xǁRetryExecutorǁexecute_sync__mutmut_41, 
        'xǁRetryExecutorǁexecute_sync__mutmut_42': xǁRetryExecutorǁexecute_sync__mutmut_42, 
        'xǁRetryExecutorǁexecute_sync__mutmut_43': xǁRetryExecutorǁexecute_sync__mutmut_43, 
        'xǁRetryExecutorǁexecute_sync__mutmut_44': xǁRetryExecutorǁexecute_sync__mutmut_44, 
        'xǁRetryExecutorǁexecute_sync__mutmut_45': xǁRetryExecutorǁexecute_sync__mutmut_45, 
        'xǁRetryExecutorǁexecute_sync__mutmut_46': xǁRetryExecutorǁexecute_sync__mutmut_46, 
        'xǁRetryExecutorǁexecute_sync__mutmut_47': xǁRetryExecutorǁexecute_sync__mutmut_47, 
        'xǁRetryExecutorǁexecute_sync__mutmut_48': xǁRetryExecutorǁexecute_sync__mutmut_48, 
        'xǁRetryExecutorǁexecute_sync__mutmut_49': xǁRetryExecutorǁexecute_sync__mutmut_49, 
        'xǁRetryExecutorǁexecute_sync__mutmut_50': xǁRetryExecutorǁexecute_sync__mutmut_50, 
        'xǁRetryExecutorǁexecute_sync__mutmut_51': xǁRetryExecutorǁexecute_sync__mutmut_51, 
        'xǁRetryExecutorǁexecute_sync__mutmut_52': xǁRetryExecutorǁexecute_sync__mutmut_52, 
        'xǁRetryExecutorǁexecute_sync__mutmut_53': xǁRetryExecutorǁexecute_sync__mutmut_53, 
        'xǁRetryExecutorǁexecute_sync__mutmut_54': xǁRetryExecutorǁexecute_sync__mutmut_54, 
        'xǁRetryExecutorǁexecute_sync__mutmut_55': xǁRetryExecutorǁexecute_sync__mutmut_55, 
        'xǁRetryExecutorǁexecute_sync__mutmut_56': xǁRetryExecutorǁexecute_sync__mutmut_56, 
        'xǁRetryExecutorǁexecute_sync__mutmut_57': xǁRetryExecutorǁexecute_sync__mutmut_57, 
        'xǁRetryExecutorǁexecute_sync__mutmut_58': xǁRetryExecutorǁexecute_sync__mutmut_58, 
        'xǁRetryExecutorǁexecute_sync__mutmut_59': xǁRetryExecutorǁexecute_sync__mutmut_59, 
        'xǁRetryExecutorǁexecute_sync__mutmut_60': xǁRetryExecutorǁexecute_sync__mutmut_60, 
        'xǁRetryExecutorǁexecute_sync__mutmut_61': xǁRetryExecutorǁexecute_sync__mutmut_61
    }
    
    def execute_sync(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRetryExecutorǁexecute_sync__mutmut_orig"), object.__getattribute__(self, "xǁRetryExecutorǁexecute_sync__mutmut_mutants"), args, kwargs, self)
        return result 
    
    execute_sync.__signature__ = _mutmut_signature(xǁRetryExecutorǁexecute_sync__mutmut_orig)
    xǁRetryExecutorǁexecute_sync__mutmut_orig.__name__ = 'xǁRetryExecutorǁexecute_sync'

    async def xǁRetryExecutorǁexecute_async__mutmut_orig(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_1(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = ""

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_2(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(None, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_3(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, None):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_4(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_5(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, ):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_6(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(2, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_7(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts - 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_8(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 2):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_9(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(**kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_10(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, )
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_11(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = None

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_12(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt > self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_13(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        None,
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_14(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=None,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_15(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=None,
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_16(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=None,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_17(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_18(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_19(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_20(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_21(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(None),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_22(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(None).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_23(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_24(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(None, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_25(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, None):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_26(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_27(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, ):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_28(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = None

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_29(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(None)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_30(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    None,
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_31(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=None,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_32(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=None,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_33(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=None,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_34(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=None,
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_35(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=None,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_36(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_37(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_38(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_39(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_40(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_41(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_42(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(None),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_43(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(None).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_44(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(None):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_45(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(None, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_46(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, None)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_47(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_48(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, )
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_49(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(None, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_50(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, None)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_51(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_52(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, )
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_53(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning(None, error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_54(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=None)

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_55(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning(error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_56(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", )

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_57(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("XXRetry callback failedXX", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_58(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_59(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("RETRY CALLBACK FAILED", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_60(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(None))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_61(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(None)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_62(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is None:
            raise last_exception
        else:
            raise RuntimeError("No exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_63(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError(None)

    async def xǁRetryExecutorǁexecute_async__mutmut_64(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("XXNo exception captured during async retry attemptsXX")

    async def xǁRetryExecutorǁexecute_async__mutmut_65(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("no exception captured during async retry attempts")

    async def xǁRetryExecutorǁexecute_async__mutmut_66(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Last exception if all retries are exhausted

        """
        last_exception = None

        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Don't retry on last attempt - log and raise
                if attempt >= self.policy.max_attempts:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"All {self.policy.max_attempts} retry attempts failed",
                        attempts=self.policy.max_attempts,
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                    raise

                # Check if we should retry this error
                if not self.policy.should_retry(e, attempt):
                    raise

                # Calculate delay
                delay = self.policy.calculate_delay(attempt)

                # Log retry attempt
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().info(
                    f"Retry {attempt}/{self.policy.max_attempts} after {delay:.2f}s",
                    attempt=attempt,
                    max_attempts=self.policy.max_attempts,
                    delay=delay,
                    error=str(e),
                    error_type=type(e).__name__,
                )

                # Call retry callback if provided
                if self.on_retry:
                    try:
                        if asyncio.iscoroutinefunction(self.on_retry):
                            await self.on_retry(attempt, e)
                        else:
                            self.on_retry(attempt, e)
                    except Exception as callback_error:
                        from provide.foundation.hub.foundation import get_foundation_logger

                        get_foundation_logger().warning("Retry callback failed", error=str(callback_error))

                # Wait before retry
                await self._async_sleep(delay)

        # Should never reach here, but for safety
        if last_exception is not None:
            raise last_exception
        else:
            raise RuntimeError("NO EXCEPTION CAPTURED DURING ASYNC RETRY ATTEMPTS")
    
    xǁRetryExecutorǁexecute_async__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRetryExecutorǁexecute_async__mutmut_1': xǁRetryExecutorǁexecute_async__mutmut_1, 
        'xǁRetryExecutorǁexecute_async__mutmut_2': xǁRetryExecutorǁexecute_async__mutmut_2, 
        'xǁRetryExecutorǁexecute_async__mutmut_3': xǁRetryExecutorǁexecute_async__mutmut_3, 
        'xǁRetryExecutorǁexecute_async__mutmut_4': xǁRetryExecutorǁexecute_async__mutmut_4, 
        'xǁRetryExecutorǁexecute_async__mutmut_5': xǁRetryExecutorǁexecute_async__mutmut_5, 
        'xǁRetryExecutorǁexecute_async__mutmut_6': xǁRetryExecutorǁexecute_async__mutmut_6, 
        'xǁRetryExecutorǁexecute_async__mutmut_7': xǁRetryExecutorǁexecute_async__mutmut_7, 
        'xǁRetryExecutorǁexecute_async__mutmut_8': xǁRetryExecutorǁexecute_async__mutmut_8, 
        'xǁRetryExecutorǁexecute_async__mutmut_9': xǁRetryExecutorǁexecute_async__mutmut_9, 
        'xǁRetryExecutorǁexecute_async__mutmut_10': xǁRetryExecutorǁexecute_async__mutmut_10, 
        'xǁRetryExecutorǁexecute_async__mutmut_11': xǁRetryExecutorǁexecute_async__mutmut_11, 
        'xǁRetryExecutorǁexecute_async__mutmut_12': xǁRetryExecutorǁexecute_async__mutmut_12, 
        'xǁRetryExecutorǁexecute_async__mutmut_13': xǁRetryExecutorǁexecute_async__mutmut_13, 
        'xǁRetryExecutorǁexecute_async__mutmut_14': xǁRetryExecutorǁexecute_async__mutmut_14, 
        'xǁRetryExecutorǁexecute_async__mutmut_15': xǁRetryExecutorǁexecute_async__mutmut_15, 
        'xǁRetryExecutorǁexecute_async__mutmut_16': xǁRetryExecutorǁexecute_async__mutmut_16, 
        'xǁRetryExecutorǁexecute_async__mutmut_17': xǁRetryExecutorǁexecute_async__mutmut_17, 
        'xǁRetryExecutorǁexecute_async__mutmut_18': xǁRetryExecutorǁexecute_async__mutmut_18, 
        'xǁRetryExecutorǁexecute_async__mutmut_19': xǁRetryExecutorǁexecute_async__mutmut_19, 
        'xǁRetryExecutorǁexecute_async__mutmut_20': xǁRetryExecutorǁexecute_async__mutmut_20, 
        'xǁRetryExecutorǁexecute_async__mutmut_21': xǁRetryExecutorǁexecute_async__mutmut_21, 
        'xǁRetryExecutorǁexecute_async__mutmut_22': xǁRetryExecutorǁexecute_async__mutmut_22, 
        'xǁRetryExecutorǁexecute_async__mutmut_23': xǁRetryExecutorǁexecute_async__mutmut_23, 
        'xǁRetryExecutorǁexecute_async__mutmut_24': xǁRetryExecutorǁexecute_async__mutmut_24, 
        'xǁRetryExecutorǁexecute_async__mutmut_25': xǁRetryExecutorǁexecute_async__mutmut_25, 
        'xǁRetryExecutorǁexecute_async__mutmut_26': xǁRetryExecutorǁexecute_async__mutmut_26, 
        'xǁRetryExecutorǁexecute_async__mutmut_27': xǁRetryExecutorǁexecute_async__mutmut_27, 
        'xǁRetryExecutorǁexecute_async__mutmut_28': xǁRetryExecutorǁexecute_async__mutmut_28, 
        'xǁRetryExecutorǁexecute_async__mutmut_29': xǁRetryExecutorǁexecute_async__mutmut_29, 
        'xǁRetryExecutorǁexecute_async__mutmut_30': xǁRetryExecutorǁexecute_async__mutmut_30, 
        'xǁRetryExecutorǁexecute_async__mutmut_31': xǁRetryExecutorǁexecute_async__mutmut_31, 
        'xǁRetryExecutorǁexecute_async__mutmut_32': xǁRetryExecutorǁexecute_async__mutmut_32, 
        'xǁRetryExecutorǁexecute_async__mutmut_33': xǁRetryExecutorǁexecute_async__mutmut_33, 
        'xǁRetryExecutorǁexecute_async__mutmut_34': xǁRetryExecutorǁexecute_async__mutmut_34, 
        'xǁRetryExecutorǁexecute_async__mutmut_35': xǁRetryExecutorǁexecute_async__mutmut_35, 
        'xǁRetryExecutorǁexecute_async__mutmut_36': xǁRetryExecutorǁexecute_async__mutmut_36, 
        'xǁRetryExecutorǁexecute_async__mutmut_37': xǁRetryExecutorǁexecute_async__mutmut_37, 
        'xǁRetryExecutorǁexecute_async__mutmut_38': xǁRetryExecutorǁexecute_async__mutmut_38, 
        'xǁRetryExecutorǁexecute_async__mutmut_39': xǁRetryExecutorǁexecute_async__mutmut_39, 
        'xǁRetryExecutorǁexecute_async__mutmut_40': xǁRetryExecutorǁexecute_async__mutmut_40, 
        'xǁRetryExecutorǁexecute_async__mutmut_41': xǁRetryExecutorǁexecute_async__mutmut_41, 
        'xǁRetryExecutorǁexecute_async__mutmut_42': xǁRetryExecutorǁexecute_async__mutmut_42, 
        'xǁRetryExecutorǁexecute_async__mutmut_43': xǁRetryExecutorǁexecute_async__mutmut_43, 
        'xǁRetryExecutorǁexecute_async__mutmut_44': xǁRetryExecutorǁexecute_async__mutmut_44, 
        'xǁRetryExecutorǁexecute_async__mutmut_45': xǁRetryExecutorǁexecute_async__mutmut_45, 
        'xǁRetryExecutorǁexecute_async__mutmut_46': xǁRetryExecutorǁexecute_async__mutmut_46, 
        'xǁRetryExecutorǁexecute_async__mutmut_47': xǁRetryExecutorǁexecute_async__mutmut_47, 
        'xǁRetryExecutorǁexecute_async__mutmut_48': xǁRetryExecutorǁexecute_async__mutmut_48, 
        'xǁRetryExecutorǁexecute_async__mutmut_49': xǁRetryExecutorǁexecute_async__mutmut_49, 
        'xǁRetryExecutorǁexecute_async__mutmut_50': xǁRetryExecutorǁexecute_async__mutmut_50, 
        'xǁRetryExecutorǁexecute_async__mutmut_51': xǁRetryExecutorǁexecute_async__mutmut_51, 
        'xǁRetryExecutorǁexecute_async__mutmut_52': xǁRetryExecutorǁexecute_async__mutmut_52, 
        'xǁRetryExecutorǁexecute_async__mutmut_53': xǁRetryExecutorǁexecute_async__mutmut_53, 
        'xǁRetryExecutorǁexecute_async__mutmut_54': xǁRetryExecutorǁexecute_async__mutmut_54, 
        'xǁRetryExecutorǁexecute_async__mutmut_55': xǁRetryExecutorǁexecute_async__mutmut_55, 
        'xǁRetryExecutorǁexecute_async__mutmut_56': xǁRetryExecutorǁexecute_async__mutmut_56, 
        'xǁRetryExecutorǁexecute_async__mutmut_57': xǁRetryExecutorǁexecute_async__mutmut_57, 
        'xǁRetryExecutorǁexecute_async__mutmut_58': xǁRetryExecutorǁexecute_async__mutmut_58, 
        'xǁRetryExecutorǁexecute_async__mutmut_59': xǁRetryExecutorǁexecute_async__mutmut_59, 
        'xǁRetryExecutorǁexecute_async__mutmut_60': xǁRetryExecutorǁexecute_async__mutmut_60, 
        'xǁRetryExecutorǁexecute_async__mutmut_61': xǁRetryExecutorǁexecute_async__mutmut_61, 
        'xǁRetryExecutorǁexecute_async__mutmut_62': xǁRetryExecutorǁexecute_async__mutmut_62, 
        'xǁRetryExecutorǁexecute_async__mutmut_63': xǁRetryExecutorǁexecute_async__mutmut_63, 
        'xǁRetryExecutorǁexecute_async__mutmut_64': xǁRetryExecutorǁexecute_async__mutmut_64, 
        'xǁRetryExecutorǁexecute_async__mutmut_65': xǁRetryExecutorǁexecute_async__mutmut_65, 
        'xǁRetryExecutorǁexecute_async__mutmut_66': xǁRetryExecutorǁexecute_async__mutmut_66
    }
    
    def execute_async(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRetryExecutorǁexecute_async__mutmut_orig"), object.__getattribute__(self, "xǁRetryExecutorǁexecute_async__mutmut_mutants"), args, kwargs, self)
        return result 
    
    execute_async.__signature__ = _mutmut_signature(xǁRetryExecutorǁexecute_async__mutmut_orig)
    xǁRetryExecutorǁexecute_async__mutmut_orig.__name__ = 'xǁRetryExecutorǁexecute_async'


# <3 🧱🤝💪🪄
