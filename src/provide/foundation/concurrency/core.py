#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

from provide.foundation.errors import ValidationError

"""Core async utilities for Foundation."""


async def async_sleep(delay: float) -> None:
    """Async sleep with Foundation tracking and cancellation support.

    Args:
        delay: Number of seconds to sleep

    Raises:
        ValidationError: If delay is negative

    Example:
        >>> import asyncio
        >>> async def main():
        ...     await async_sleep(0.1)
        >>> asyncio.run(main())

    """
    if delay < 0:
        raise ValidationError("Sleep delay must be non-negative")
    await asyncio.sleep(delay)


async def async_gather(*awaitables: Awaitable[Any], return_exceptions: bool = False) -> list[Any]:
    """Run awaitables concurrently with Foundation tracking.

    Args:
        *awaitables: Awaitable objects to run concurrently
        return_exceptions: If True, exceptions are returned as results

    Returns:
        List of results in the same order as input awaitables

    Raises:
        ValidationError: If no awaitables provided

    Example:
        >>> import asyncio
        >>> async def fetch_data(n):
        ...     await async_sleep(0.1)
        ...     return n * 2
        >>> async def main():
        ...     results = await async_gather(
        ...         fetch_data(1), fetch_data(2), fetch_data(3)
        ...     )
        ...     return results
        >>> asyncio.run(main())
        [2, 4, 6]

    """
    if not awaitables:
        raise ValidationError("At least one awaitable must be provided")

    return await asyncio.gather(*awaitables, return_exceptions=return_exceptions)


async def async_wait_for(awaitable: Awaitable[Any], timeout: float | None) -> Any:
    """Wait for an awaitable with optional timeout.

    Args:
        awaitable: The awaitable to wait for
        timeout: Timeout in seconds (None for no timeout)

    Returns:
        Result of the awaitable

    Raises:
        ValidationError: If timeout is negative
        asyncio.TimeoutError: If timeout is exceeded

    Example:
        >>> import asyncio
        >>> async def slow_task():
        ...     await async_sleep(0.2)
        ...     return "done"
        >>> async def main():
        ...     try:
        ...         result = await async_wait_for(slow_task(), timeout=0.1)
        ...     except asyncio.TimeoutError:
        ...         result = "timed out"
        ...     return result
        >>> asyncio.run(main())
        'timed out'

    """
    if timeout is not None and timeout < 0:
        raise ValidationError("Timeout must be non-negative")

    return await asyncio.wait_for(awaitable, timeout=timeout)


def async_run(main: Callable[[], Awaitable[Any]], *, debug: bool = False) -> Any:
    """Run async function with Foundation tracking.

    Args:
        main: Async function to run
        debug: Whether to run in debug mode

    Returns:
        Result of the main function

    Raises:
        ValidationError: If main is not callable

    Example:
        >>> async def main():
        ...     await async_sleep(0.1)
        ...     return "hello"
        >>> result = async_run(main)
        >>> result
        'hello'

    """
    if not callable(main):
        raise ValidationError("Main must be callable")

    return asyncio.run(main(), debug=debug)  # type: ignore[arg-type]


# 🧱🏗️🔚
