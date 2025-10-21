# provide/foundation/concurrency/core.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

from provide.foundation.errors import ValidationError

"""Core async utilities for Foundation."""
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


async def x_async_sleep__mutmut_orig(delay: float) -> None:
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


async def x_async_sleep__mutmut_1(delay: float) -> None:
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
    if delay <= 0:
        raise ValidationError("Sleep delay must be non-negative")
    await asyncio.sleep(delay)


async def x_async_sleep__mutmut_2(delay: float) -> None:
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
    if delay < 1:
        raise ValidationError("Sleep delay must be non-negative")
    await asyncio.sleep(delay)


async def x_async_sleep__mutmut_3(delay: float) -> None:
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
        raise ValidationError(None)
    await asyncio.sleep(delay)


async def x_async_sleep__mutmut_4(delay: float) -> None:
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
        raise ValidationError("XXSleep delay must be non-negativeXX")
    await asyncio.sleep(delay)


async def x_async_sleep__mutmut_5(delay: float) -> None:
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
        raise ValidationError("sleep delay must be non-negative")
    await asyncio.sleep(delay)


async def x_async_sleep__mutmut_6(delay: float) -> None:
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
        raise ValidationError("SLEEP DELAY MUST BE NON-NEGATIVE")
    await asyncio.sleep(delay)


async def x_async_sleep__mutmut_7(delay: float) -> None:
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
    await asyncio.sleep(None)

x_async_sleep__mutmut_mutants : ClassVar[MutantDict] = {
'x_async_sleep__mutmut_1': x_async_sleep__mutmut_1, 
    'x_async_sleep__mutmut_2': x_async_sleep__mutmut_2, 
    'x_async_sleep__mutmut_3': x_async_sleep__mutmut_3, 
    'x_async_sleep__mutmut_4': x_async_sleep__mutmut_4, 
    'x_async_sleep__mutmut_5': x_async_sleep__mutmut_5, 
    'x_async_sleep__mutmut_6': x_async_sleep__mutmut_6, 
    'x_async_sleep__mutmut_7': x_async_sleep__mutmut_7
}

def async_sleep(*args, **kwargs):
    result = _mutmut_trampoline(x_async_sleep__mutmut_orig, x_async_sleep__mutmut_mutants, args, kwargs)
    return result 

async_sleep.__signature__ = _mutmut_signature(x_async_sleep__mutmut_orig)
x_async_sleep__mutmut_orig.__name__ = 'x_async_sleep'


async def x_async_gather__mutmut_orig(*awaitables: Awaitable[Any], return_exceptions: bool = False) -> list[Any]:
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


async def x_async_gather__mutmut_1(*awaitables: Awaitable[Any], return_exceptions: bool = True) -> list[Any]:
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


async def x_async_gather__mutmut_2(*awaitables: Awaitable[Any], return_exceptions: bool = False) -> list[Any]:
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
    if awaitables:
        raise ValidationError("At least one awaitable must be provided")

    return await asyncio.gather(*awaitables, return_exceptions=return_exceptions)


async def x_async_gather__mutmut_3(*awaitables: Awaitable[Any], return_exceptions: bool = False) -> list[Any]:
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
        raise ValidationError(None)

    return await asyncio.gather(*awaitables, return_exceptions=return_exceptions)


async def x_async_gather__mutmut_4(*awaitables: Awaitable[Any], return_exceptions: bool = False) -> list[Any]:
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
        raise ValidationError("XXAt least one awaitable must be providedXX")

    return await asyncio.gather(*awaitables, return_exceptions=return_exceptions)


async def x_async_gather__mutmut_5(*awaitables: Awaitable[Any], return_exceptions: bool = False) -> list[Any]:
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
        raise ValidationError("at least one awaitable must be provided")

    return await asyncio.gather(*awaitables, return_exceptions=return_exceptions)


async def x_async_gather__mutmut_6(*awaitables: Awaitable[Any], return_exceptions: bool = False) -> list[Any]:
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
        raise ValidationError("AT LEAST ONE AWAITABLE MUST BE PROVIDED")

    return await asyncio.gather(*awaitables, return_exceptions=return_exceptions)


async def x_async_gather__mutmut_7(*awaitables: Awaitable[Any], return_exceptions: bool = False) -> list[Any]:
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

    return await asyncio.gather(*awaitables, return_exceptions=None)


async def x_async_gather__mutmut_8(*awaitables: Awaitable[Any], return_exceptions: bool = False) -> list[Any]:
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

    return await asyncio.gather(return_exceptions=return_exceptions)


async def x_async_gather__mutmut_9(*awaitables: Awaitable[Any], return_exceptions: bool = False) -> list[Any]:
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

    return await asyncio.gather(*awaitables, )

x_async_gather__mutmut_mutants : ClassVar[MutantDict] = {
'x_async_gather__mutmut_1': x_async_gather__mutmut_1, 
    'x_async_gather__mutmut_2': x_async_gather__mutmut_2, 
    'x_async_gather__mutmut_3': x_async_gather__mutmut_3, 
    'x_async_gather__mutmut_4': x_async_gather__mutmut_4, 
    'x_async_gather__mutmut_5': x_async_gather__mutmut_5, 
    'x_async_gather__mutmut_6': x_async_gather__mutmut_6, 
    'x_async_gather__mutmut_7': x_async_gather__mutmut_7, 
    'x_async_gather__mutmut_8': x_async_gather__mutmut_8, 
    'x_async_gather__mutmut_9': x_async_gather__mutmut_9
}

def async_gather(*args, **kwargs):
    result = _mutmut_trampoline(x_async_gather__mutmut_orig, x_async_gather__mutmut_mutants, args, kwargs)
    return result 

async_gather.__signature__ = _mutmut_signature(x_async_gather__mutmut_orig)
x_async_gather__mutmut_orig.__name__ = 'x_async_gather'


async def x_async_wait_for__mutmut_orig(awaitable: Awaitable[Any], timeout: float | None) -> Any:
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


async def x_async_wait_for__mutmut_1(awaitable: Awaitable[Any], timeout: float | None) -> Any:
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
    if timeout is not None or timeout < 0:
        raise ValidationError("Timeout must be non-negative")

    return await asyncio.wait_for(awaitable, timeout=timeout)


async def x_async_wait_for__mutmut_2(awaitable: Awaitable[Any], timeout: float | None) -> Any:
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
    if timeout is None and timeout < 0:
        raise ValidationError("Timeout must be non-negative")

    return await asyncio.wait_for(awaitable, timeout=timeout)


async def x_async_wait_for__mutmut_3(awaitable: Awaitable[Any], timeout: float | None) -> Any:
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
    if timeout is not None and timeout <= 0:
        raise ValidationError("Timeout must be non-negative")

    return await asyncio.wait_for(awaitable, timeout=timeout)


async def x_async_wait_for__mutmut_4(awaitable: Awaitable[Any], timeout: float | None) -> Any:
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
    if timeout is not None and timeout < 1:
        raise ValidationError("Timeout must be non-negative")

    return await asyncio.wait_for(awaitable, timeout=timeout)


async def x_async_wait_for__mutmut_5(awaitable: Awaitable[Any], timeout: float | None) -> Any:
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
        raise ValidationError(None)

    return await asyncio.wait_for(awaitable, timeout=timeout)


async def x_async_wait_for__mutmut_6(awaitable: Awaitable[Any], timeout: float | None) -> Any:
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
        raise ValidationError("XXTimeout must be non-negativeXX")

    return await asyncio.wait_for(awaitable, timeout=timeout)


async def x_async_wait_for__mutmut_7(awaitable: Awaitable[Any], timeout: float | None) -> Any:
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
        raise ValidationError("timeout must be non-negative")

    return await asyncio.wait_for(awaitable, timeout=timeout)


async def x_async_wait_for__mutmut_8(awaitable: Awaitable[Any], timeout: float | None) -> Any:
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
        raise ValidationError("TIMEOUT MUST BE NON-NEGATIVE")

    return await asyncio.wait_for(awaitable, timeout=timeout)


async def x_async_wait_for__mutmut_9(awaitable: Awaitable[Any], timeout: float | None) -> Any:
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

    return await asyncio.wait_for(None, timeout=timeout)


async def x_async_wait_for__mutmut_10(awaitable: Awaitable[Any], timeout: float | None) -> Any:
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

    return await asyncio.wait_for(awaitable, timeout=None)


async def x_async_wait_for__mutmut_11(awaitable: Awaitable[Any], timeout: float | None) -> Any:
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

    return await asyncio.wait_for(timeout=timeout)


async def x_async_wait_for__mutmut_12(awaitable: Awaitable[Any], timeout: float | None) -> Any:
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

    return await asyncio.wait_for(awaitable, )

x_async_wait_for__mutmut_mutants : ClassVar[MutantDict] = {
'x_async_wait_for__mutmut_1': x_async_wait_for__mutmut_1, 
    'x_async_wait_for__mutmut_2': x_async_wait_for__mutmut_2, 
    'x_async_wait_for__mutmut_3': x_async_wait_for__mutmut_3, 
    'x_async_wait_for__mutmut_4': x_async_wait_for__mutmut_4, 
    'x_async_wait_for__mutmut_5': x_async_wait_for__mutmut_5, 
    'x_async_wait_for__mutmut_6': x_async_wait_for__mutmut_6, 
    'x_async_wait_for__mutmut_7': x_async_wait_for__mutmut_7, 
    'x_async_wait_for__mutmut_8': x_async_wait_for__mutmut_8, 
    'x_async_wait_for__mutmut_9': x_async_wait_for__mutmut_9, 
    'x_async_wait_for__mutmut_10': x_async_wait_for__mutmut_10, 
    'x_async_wait_for__mutmut_11': x_async_wait_for__mutmut_11, 
    'x_async_wait_for__mutmut_12': x_async_wait_for__mutmut_12
}

def async_wait_for(*args, **kwargs):
    result = _mutmut_trampoline(x_async_wait_for__mutmut_orig, x_async_wait_for__mutmut_mutants, args, kwargs)
    return result 

async_wait_for.__signature__ = _mutmut_signature(x_async_wait_for__mutmut_orig)
x_async_wait_for__mutmut_orig.__name__ = 'x_async_wait_for'


def x_async_run__mutmut_orig(main: Callable[[], Awaitable[Any]], *, debug: bool = False) -> Any:
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


def x_async_run__mutmut_1(main: Callable[[], Awaitable[Any]], *, debug: bool = True) -> Any:
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


def x_async_run__mutmut_2(main: Callable[[], Awaitable[Any]], *, debug: bool = False) -> Any:
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
    if callable(main):
        raise ValidationError("Main must be callable")

    return asyncio.run(main(), debug=debug)  # type: ignore[arg-type]


def x_async_run__mutmut_3(main: Callable[[], Awaitable[Any]], *, debug: bool = False) -> Any:
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
    if not callable(None):
        raise ValidationError("Main must be callable")

    return asyncio.run(main(), debug=debug)  # type: ignore[arg-type]


def x_async_run__mutmut_4(main: Callable[[], Awaitable[Any]], *, debug: bool = False) -> Any:
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
        raise ValidationError(None)

    return asyncio.run(main(), debug=debug)  # type: ignore[arg-type]


def x_async_run__mutmut_5(main: Callable[[], Awaitable[Any]], *, debug: bool = False) -> Any:
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
        raise ValidationError("XXMain must be callableXX")

    return asyncio.run(main(), debug=debug)  # type: ignore[arg-type]


def x_async_run__mutmut_6(main: Callable[[], Awaitable[Any]], *, debug: bool = False) -> Any:
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
        raise ValidationError("main must be callable")

    return asyncio.run(main(), debug=debug)  # type: ignore[arg-type]


def x_async_run__mutmut_7(main: Callable[[], Awaitable[Any]], *, debug: bool = False) -> Any:
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
        raise ValidationError("MAIN MUST BE CALLABLE")

    return asyncio.run(main(), debug=debug)  # type: ignore[arg-type]


def x_async_run__mutmut_8(main: Callable[[], Awaitable[Any]], *, debug: bool = False) -> Any:
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

    return asyncio.run(None, debug=debug)  # type: ignore[arg-type]


def x_async_run__mutmut_9(main: Callable[[], Awaitable[Any]], *, debug: bool = False) -> Any:
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

    return asyncio.run(main(), debug=None)  # type: ignore[arg-type]


def x_async_run__mutmut_10(main: Callable[[], Awaitable[Any]], *, debug: bool = False) -> Any:
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

    return asyncio.run(debug=debug)  # type: ignore[arg-type]


def x_async_run__mutmut_11(main: Callable[[], Awaitable[Any]], *, debug: bool = False) -> Any:
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

    return asyncio.run(main(), )  # type: ignore[arg-type]

x_async_run__mutmut_mutants : ClassVar[MutantDict] = {
'x_async_run__mutmut_1': x_async_run__mutmut_1, 
    'x_async_run__mutmut_2': x_async_run__mutmut_2, 
    'x_async_run__mutmut_3': x_async_run__mutmut_3, 
    'x_async_run__mutmut_4': x_async_run__mutmut_4, 
    'x_async_run__mutmut_5': x_async_run__mutmut_5, 
    'x_async_run__mutmut_6': x_async_run__mutmut_6, 
    'x_async_run__mutmut_7': x_async_run__mutmut_7, 
    'x_async_run__mutmut_8': x_async_run__mutmut_8, 
    'x_async_run__mutmut_9': x_async_run__mutmut_9, 
    'x_async_run__mutmut_10': x_async_run__mutmut_10, 
    'x_async_run__mutmut_11': x_async_run__mutmut_11
}

def async_run(*args, **kwargs):
    result = _mutmut_trampoline(x_async_run__mutmut_orig, x_async_run__mutmut_mutants, args, kwargs)
    return result 

async_run.__signature__ = _mutmut_signature(x_async_run__mutmut_orig)
x_async_run__mutmut_orig.__name__ = 'x_async_run'


# <3 🧱🤝🧵🪄
