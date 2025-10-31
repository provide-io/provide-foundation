#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
import functools
from typing import Any, TypeVar

from attrs import define, field

from provide.foundation.logger import logger

"""Fallback implementation for graceful degradation."""

T = TypeVar("T")


@define(kw_only=True, slots=True)
class FallbackChain:
    """Chain of fallback strategies for graceful degradation.

    Executes fallback functions in order when primary function fails.
    """

    fallbacks: list[Callable[..., T]] = field(factory=list)
    expected_exceptions: tuple[type[Exception], ...] = field(factory=lambda: (Exception,))

    def add_fallback(self, fallback_func: Callable[..., T]) -> None:
        """Add a fallback function to the chain."""
        self.fallbacks.append(fallback_func)  # type: ignore[arg-type]
        logger.debug(
            "Added fallback to chain",
            fallback_count=len(self.fallbacks),
            fallback_name=getattr(fallback_func, "__name__", "anonymous"),
        )

    def execute(self, primary_func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute primary function with fallback chain (sync)."""
        # Try primary function first
        primary_exception = None
        try:
            result = primary_func(*args, **kwargs)
            logger.trace(
                "Primary function succeeded",
                func=getattr(primary_func, "__name__", "anonymous"),
            )
            return result
        except Exception as e:
            primary_exception = e
            if not isinstance(e, self.expected_exceptions):
                # Unexpected exception type, don't use fallbacks
                logger.debug(
                    "Primary function failed with unexpected exception type",
                    exception_type=type(e).__name__,
                    expected_types=[t.__name__ for t in self.expected_exceptions],
                )
                raise

            logger.warning(
                "Primary function failed, trying fallbacks",
                func=getattr(primary_func, "__name__", "anonymous"),
                error=str(e),
                fallback_count=len(self.fallbacks),
            )

        # Try fallbacks in order
        last_exception = None
        for i, fallback_func in enumerate(self.fallbacks):
            try:
                result = fallback_func(*args, **kwargs)
                logger.info(
                    "Fallback succeeded",
                    fallback_index=i,
                    fallback_name=getattr(fallback_func, "__name__", "anonymous"),
                )
                return result
            except Exception as e:
                last_exception = e
                logger.warning(
                    "Fallback failed",
                    fallback_index=i,
                    fallback_name=getattr(fallback_func, "__name__", "anonymous"),
                    error=str(e),
                )
                continue

        # All fallbacks failed
        logger.error(
            "All fallbacks exhausted",
            primary_func=getattr(primary_func, "__name__", "anonymous"),
            fallback_count=len(self.fallbacks),
        )

        # Raise the last exception from fallbacks, or original if no fallbacks
        if last_exception is not None:
            raise last_exception
        if primary_exception is not None:
            raise primary_exception
        # This should never happen but provide fallback
        raise RuntimeError("Fallback chain execution failed with no recorded exceptions")

    async def execute_async(self, primary_func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute primary function with fallback chain (async)."""
        # Try primary function first
        primary_exception = None
        try:
            if asyncio.iscoroutinefunction(primary_func):
                result = await primary_func(*args, **kwargs)
            else:
                result = primary_func(*args, **kwargs)
            logger.trace(
                "Primary function succeeded",
                func=getattr(primary_func, "__name__", "anonymous"),
            )
            return result
        except Exception as e:
            primary_exception = e
            if not isinstance(e, self.expected_exceptions):
                # Unexpected exception type, don't use fallbacks
                logger.debug(
                    "Primary function failed with unexpected exception type",
                    exception_type=type(e).__name__,
                    expected_types=[t.__name__ for t in self.expected_exceptions],
                )
                raise

            logger.warning(
                "Primary function failed, trying fallbacks",
                func=getattr(primary_func, "__name__", "anonymous"),
                error=str(e),
                fallback_count=len(self.fallbacks),
            )

        # Try fallbacks in order
        last_exception = None
        for i, fallback_func in enumerate(self.fallbacks):
            try:
                if asyncio.iscoroutinefunction(fallback_func):
                    result = await fallback_func(*args, **kwargs)
                else:
                    result = fallback_func(*args, **kwargs)
                logger.info(
                    "Fallback succeeded",
                    fallback_index=i,
                    fallback_name=getattr(fallback_func, "__name__", "anonymous"),
                )
                return result
            except Exception as e:
                last_exception = e
                logger.warning(
                    "Fallback failed",
                    fallback_index=i,
                    fallback_name=getattr(fallback_func, "__name__", "anonymous"),
                    error=str(e),
                )
                continue

        # All fallbacks failed
        logger.error(
            "All fallbacks exhausted",
            primary_func=getattr(primary_func, "__name__", "anonymous"),
            fallback_count=len(self.fallbacks),
        )

        # Raise the last exception from fallbacks, or original if no fallbacks
        if last_exception is not None:
            raise last_exception
        if primary_exception is not None:
            raise primary_exception
        # This should never happen but provide fallback
        raise RuntimeError("Fallback chain execution failed with no recorded exceptions")


def fallback(*fallback_funcs: Callable[..., T]) -> Callable:
    """Decorator to add fallback functions to a primary function.

    Args:
        *fallback_funcs: Functions to use as fallbacks, in order of preference

    Returns:
        Decorated function that uses fallback chain

    """

    def decorator(primary_func: Callable[..., T]) -> Callable[..., T]:
        chain = FallbackChain()
        for fallback_func in fallback_funcs:
            chain.add_fallback(fallback_func)

        if asyncio.iscoroutinefunction(primary_func):

            @functools.wraps(primary_func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await chain.execute_async(primary_func, *args, **kwargs)

            return async_wrapper  # type: ignore[return-value]

        @functools.wraps(primary_func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            return chain.execute(primary_func, *args, **kwargs)

        return sync_wrapper

    return decorator


# 🧱🏗️🔚
