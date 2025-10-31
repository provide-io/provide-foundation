#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Async-sync bridge utilities for Foundation.

Provides utilities for bridging async and sync code, particularly useful
for CLI commands that need to call async clients or functions."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Coroutine
import contextlib
from typing import TypeVar

T = TypeVar("T")


def run_async(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
    """Run an async coroutine from sync context.

    **IMPORTANT CONSTRAINTS:**

    This is a bridge utility for running async code from sync contexts (e.g., CLI commands).
    It should NOT be used in async contexts - use `await` directly instead.

    **When to use:**
    - CLI commands that need to call async client methods
    - Sync utility functions that need to call async APIs
    - Test fixtures that need to run async code synchronously

    **When NOT to use:**
    - Inside async functions (use `await` instead)
    - In performance-critical loops (creates event loop overhead)
    - With long-running coroutines (blocks the thread)

    **Limitations:**
    - Creates a new event loop if one doesn't exist (has overhead)
    - Blocks the calling thread until coroutine completes
    - Cannot run multiple coroutines concurrently
    - Should not be nested (will raise RuntimeError)

    Args:
        coro: Async coroutine or awaitable to run
        warn: If True, logs a warning when used (for debugging)

    Returns:
        Result from the coroutine

    Raises:
        RuntimeError: If called from within an already-running event loop

    Example:
        ```python
        from provide.foundation.utils.async_helpers import run_async

        async def fetch_data():
            client = UniversalClient()
            return await client.get("https://api.example.com/data")

        result = run_async(fetch_data())

        # ❌ BAD: Inside an async function
        async def my_async_function():
            result = run_async(some_coro())  # Wrong! Use await instead
        ```

    Note:
        Consider refactoring to use native async entry points instead of
        bridging sync/async boundaries. This function is a convenience for
        specific use cases, not a general-purpose async executor.

    """
    # Emit warning if requested (for debugging/auditing)
    if warn:
        import warnings

        warnings.warn(
            "run_async() called - consider using native async entry points instead",
            stacklevel=2,
        )

    # Try to get the current running loop (will raise if not in async context)
    try:
        loop = asyncio.get_running_loop()
        # If we get here, we're in an async context - should use await instead
        raise RuntimeError(
            "Cannot use run_async() from within an already-running event loop. "
            "Use 'await' directly instead. "
            "This typically happens when run_async() is called from async code."
        )
    except RuntimeError as e:
        # Re-raise if it's our custom error message
        if "Cannot use run_async()" in str(e):
            raise
        # Otherwise, no running loop which is what we expect
        pass

    # Try to get or create an event loop
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            # Loop exists but is closed, create a new one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            created_loop = True
        else:
            # Reuse existing loop
            created_loop = False
    except RuntimeError:
        # No loop exists, create one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        created_loop = True

    try:
        return loop.run_until_complete(coro)
    finally:
        # Only close the loop if we created it
        if created_loop:
            with contextlib.suppress(Exception):
                loop.close()


__all__ = ["run_async"]

# 🧱🏗️🔚
