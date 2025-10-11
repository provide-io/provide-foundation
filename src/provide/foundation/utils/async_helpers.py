"""Async-sync bridge utilities for Foundation.

Provides utilities for bridging async and sync code, particularly useful
for CLI commands that need to call async clients or functions.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Coroutine
import contextlib
from typing import TypeVar

T = TypeVar("T")


def run_async(coro: Coroutine[None, None, T] | Awaitable[T]) -> T:
    """Run an async coroutine from sync context.

    This is useful for CLI commands that need to call async client methods.
    It handles event loop management properly, creating a new loop if needed.

    Args:
        coro: Async coroutine or awaitable to run

    Returns:
        Result from the coroutine

    Example:
        ```python
        from provide.foundation.utils.async_helpers import run_async

        # In a sync CLI command
        async def fetch_data():
            client = UniversalClient()
            return await client.get("https://api.example.com/data")

        result = run_async(fetch_data())
        ```

    Note:
        This creates or reuses an event loop appropriately. It's safe to call
        from contexts where an event loop may or may not exist.

    """
    # Try to get the current running loop (will raise if not in async context)
    try:
        loop = asyncio.get_running_loop()
        # If we get here, we're in an async context - should use await instead
        raise RuntimeError(
            "Cannot use run_async() from within an already-running event loop. Use 'await' directly instead."
        )
    except RuntimeError:
        pass  # No running loop, which is what we expect

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
