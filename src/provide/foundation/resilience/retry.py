#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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

    def __init__(
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

    def execute_sync(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute synchronous function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Exception: The last exception raised if all retry attempts are exhausted

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

    async def execute_async(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute asynchronous function with retry logic.

        Args:
            func: Async function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful execution

        Raises:
            Exception: The last exception raised if all retry attempts are exhausted

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


# 🧱🏗️🔚
