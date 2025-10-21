# provide/foundation/utils/async_helpers.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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


def x_run_async__mutmut_orig(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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


def x_run_async__mutmut_1(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = True) -> T:
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

        # ✅ GOOD: In a sync CLI command
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


def x_run_async__mutmut_2(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            None,
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


def x_run_async__mutmut_3(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            stacklevel=None,
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


def x_run_async__mutmut_4(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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


def x_run_async__mutmut_5(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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


def x_run_async__mutmut_6(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            "XXrun_async() called - consider using native async entry points insteadXX",
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


def x_run_async__mutmut_7(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            "RUN_ASYNC() CALLED - CONSIDER USING NATIVE ASYNC ENTRY POINTS INSTEAD",
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


def x_run_async__mutmut_8(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            stacklevel=3,
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


def x_run_async__mutmut_9(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
        loop = None
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


def x_run_async__mutmut_10(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            None
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


def x_run_async__mutmut_11(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            "XXCannot use run_async() from within an already-running event loop. XX"
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


def x_run_async__mutmut_12(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            "cannot use run_async() from within an already-running event loop. "
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


def x_run_async__mutmut_13(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            "CANNOT USE RUN_ASYNC() FROM WITHIN AN ALREADY-RUNNING EVENT LOOP. "
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


def x_run_async__mutmut_14(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            "XXUse 'await' directly instead. XX"
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


def x_run_async__mutmut_15(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            "use 'await' directly instead. "
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


def x_run_async__mutmut_16(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            "USE 'AWAIT' DIRECTLY INSTEAD. "
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


def x_run_async__mutmut_17(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            "XXThis typically happens when run_async() is called from async code.XX"
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


def x_run_async__mutmut_18(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            "this typically happens when run_async() is called from async code."
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


def x_run_async__mutmut_19(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            "THIS TYPICALLY HAPPENS WHEN RUN_ASYNC() IS CALLED FROM ASYNC CODE."
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


def x_run_async__mutmut_20(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
        if "XXCannot use run_async()XX" in str(e):
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


def x_run_async__mutmut_21(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
        if "cannot use run_async()" in str(e):
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


def x_run_async__mutmut_22(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
        if "CANNOT USE RUN_ASYNC()" in str(e):
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


def x_run_async__mutmut_23(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
        if "Cannot use run_async()" not in str(e):
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


def x_run_async__mutmut_24(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
        if "Cannot use run_async()" in str(None):
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


def x_run_async__mutmut_25(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
        loop = None
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


def x_run_async__mutmut_26(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            loop = None
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


def x_run_async__mutmut_27(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            asyncio.set_event_loop(None)
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


def x_run_async__mutmut_28(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            created_loop = None
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


def x_run_async__mutmut_29(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            created_loop = False
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


def x_run_async__mutmut_30(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            created_loop = None
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


def x_run_async__mutmut_31(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            created_loop = True
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


def x_run_async__mutmut_32(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
        loop = None
        asyncio.set_event_loop(loop)
        created_loop = True

    try:
        return loop.run_until_complete(coro)
    finally:
        # Only close the loop if we created it
        if created_loop:
            with contextlib.suppress(Exception):
                loop.close()


def x_run_async__mutmut_33(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
        asyncio.set_event_loop(None)
        created_loop = True

    try:
        return loop.run_until_complete(coro)
    finally:
        # Only close the loop if we created it
        if created_loop:
            with contextlib.suppress(Exception):
                loop.close()


def x_run_async__mutmut_34(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
        created_loop = None

    try:
        return loop.run_until_complete(coro)
    finally:
        # Only close the loop if we created it
        if created_loop:
            with contextlib.suppress(Exception):
                loop.close()


def x_run_async__mutmut_35(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
        created_loop = False

    try:
        return loop.run_until_complete(coro)
    finally:
        # Only close the loop if we created it
        if created_loop:
            with contextlib.suppress(Exception):
                loop.close()


def x_run_async__mutmut_36(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
        return loop.run_until_complete(None)
    finally:
        # Only close the loop if we created it
        if created_loop:
            with contextlib.suppress(Exception):
                loop.close()


def x_run_async__mutmut_37(coro: Coroutine[None, None, T] | Awaitable[T], *, warn: bool = False) -> T:
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

        # ✅ GOOD: In a sync CLI command
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
            with contextlib.suppress(None):
                loop.close()

x_run_async__mutmut_mutants : ClassVar[MutantDict] = {
'x_run_async__mutmut_1': x_run_async__mutmut_1, 
    'x_run_async__mutmut_2': x_run_async__mutmut_2, 
    'x_run_async__mutmut_3': x_run_async__mutmut_3, 
    'x_run_async__mutmut_4': x_run_async__mutmut_4, 
    'x_run_async__mutmut_5': x_run_async__mutmut_5, 
    'x_run_async__mutmut_6': x_run_async__mutmut_6, 
    'x_run_async__mutmut_7': x_run_async__mutmut_7, 
    'x_run_async__mutmut_8': x_run_async__mutmut_8, 
    'x_run_async__mutmut_9': x_run_async__mutmut_9, 
    'x_run_async__mutmut_10': x_run_async__mutmut_10, 
    'x_run_async__mutmut_11': x_run_async__mutmut_11, 
    'x_run_async__mutmut_12': x_run_async__mutmut_12, 
    'x_run_async__mutmut_13': x_run_async__mutmut_13, 
    'x_run_async__mutmut_14': x_run_async__mutmut_14, 
    'x_run_async__mutmut_15': x_run_async__mutmut_15, 
    'x_run_async__mutmut_16': x_run_async__mutmut_16, 
    'x_run_async__mutmut_17': x_run_async__mutmut_17, 
    'x_run_async__mutmut_18': x_run_async__mutmut_18, 
    'x_run_async__mutmut_19': x_run_async__mutmut_19, 
    'x_run_async__mutmut_20': x_run_async__mutmut_20, 
    'x_run_async__mutmut_21': x_run_async__mutmut_21, 
    'x_run_async__mutmut_22': x_run_async__mutmut_22, 
    'x_run_async__mutmut_23': x_run_async__mutmut_23, 
    'x_run_async__mutmut_24': x_run_async__mutmut_24, 
    'x_run_async__mutmut_25': x_run_async__mutmut_25, 
    'x_run_async__mutmut_26': x_run_async__mutmut_26, 
    'x_run_async__mutmut_27': x_run_async__mutmut_27, 
    'x_run_async__mutmut_28': x_run_async__mutmut_28, 
    'x_run_async__mutmut_29': x_run_async__mutmut_29, 
    'x_run_async__mutmut_30': x_run_async__mutmut_30, 
    'x_run_async__mutmut_31': x_run_async__mutmut_31, 
    'x_run_async__mutmut_32': x_run_async__mutmut_32, 
    'x_run_async__mutmut_33': x_run_async__mutmut_33, 
    'x_run_async__mutmut_34': x_run_async__mutmut_34, 
    'x_run_async__mutmut_35': x_run_async__mutmut_35, 
    'x_run_async__mutmut_36': x_run_async__mutmut_36, 
    'x_run_async__mutmut_37': x_run_async__mutmut_37
}

def run_async(*args, **kwargs):
    result = _mutmut_trampoline(x_run_async__mutmut_orig, x_run_async__mutmut_mutants, args, kwargs)
    return result 

run_async.__signature__ = _mutmut_signature(x_run_async__mutmut_orig)
x_run_async__mutmut_orig.__name__ = 'x_run_async'


__all__ = ["run_async"]


# <3 🧱🤝🧰🪄
