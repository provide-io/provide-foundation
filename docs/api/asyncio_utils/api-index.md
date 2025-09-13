# Asyncio Utils API

Core async utilities that wrap Python's asyncio with Foundation tracking and validation.

## Overview

The `asyncio_utils` module provides a minimal set of async utilities that add Foundation-specific features like validation and error handling to standard asyncio operations.

## Current API

### async_sleep

Async sleep with Foundation tracking and cancellation support.

```python
from provide.foundation.asyncio_utils import async_sleep

async def main():
    # Sleep for 1 second
    await async_sleep(1.0)
    
    # Raises ValidationError for negative values
    await async_sleep(-1.0)  # ValidationError
```

### async_gather

Run awaitables concurrently with Foundation tracking.

```python
from provide.foundation.asyncio_utils import async_gather

async def fetch_data(n):
    await async_sleep(0.1)
    return n * 2

async def main():
    # Run multiple tasks concurrently
    results = await async_gather(
        fetch_data(1),
        fetch_data(2),
        fetch_data(3)
    )
    # results = [2, 4, 6]
    
    # Return exceptions instead of raising
    results = await async_gather(
        fetch_data(1),
        failing_task(),
        return_exceptions=True
    )
    # results = [2, Exception(...)]
```

### async_wait_for

Wait for an awaitable with optional timeout.

```python
from provide.foundation.asyncio_utils import async_wait_for
import asyncio

async def slow_task():
    await async_sleep(2.0)
    return "done"

async def main():
    # With timeout
    try:
        result = await async_wait_for(slow_task(), timeout=1.0)
    except asyncio.TimeoutError:
        print("Task timed out")
    
    # No timeout
    result = await async_wait_for(slow_task(), timeout=None)
```

### async_run

Run async function with Foundation tracking.

```python
from provide.foundation.asyncio_utils import async_run

async def main():
    await async_sleep(0.1)
    return "hello"

# Run the async function
result = async_run(main)
# result = "hello"

# Run with debug mode
result = async_run(main, debug=True)
```

## Key Features

- **Validation**: All functions validate inputs (e.g., non-negative delays)
- **Error Handling**: Proper error propagation with Foundation's error types
- **Type Safety**: Full type hints for all functions
- **Testing**: Comprehensive test coverage

## Error Handling

All functions raise `ValidationError` for invalid inputs:

```python
from provide.foundation.asyncio_utils import async_sleep, async_wait_for
from provide.foundation.errors import ValidationError

# These raise ValidationError
await async_sleep(-1.0)  # Negative delay
await async_wait_for(coro, timeout=-1.0)  # Negative timeout
await async_gather()  # No awaitables provided
async_run("not callable")  # Non-callable input
```

## Usage Examples

### Combining Multiple Utilities

```python
from provide.foundation.asyncio_utils import (
    async_gather,
    async_sleep,
    async_wait_for,
    async_run
)

async def task_with_timeout(id: int, delay: float):
    await async_sleep(delay)
    return f"Task {id} completed"

async def main():
    # Use async_gather to run multiple tasks
    tasks = await async_gather(
        async_wait_for(task_with_timeout(1, 0.01), timeout=0.1),
        async_wait_for(task_with_timeout(2, 0.01), timeout=0.1),
        async_wait_for(task_with_timeout(3, 0.01), timeout=0.1),
    )
    return tasks

# Run the main function
results = async_run(main)
```

### Error Recovery Pattern

```python
async def unreliable_task():
    if random.random() < 0.5:
        raise Exception("Random failure")
    return "success"

async def main():
    # Gather with error handling
    results = await async_gather(
        unreliable_task(),
        unreliable_task(),
        unreliable_task(),
        return_exceptions=True
    )
    
    # Process results, handling exceptions
    successful = [r for r in results if not isinstance(r, Exception)]
    failed = [r for r in results if isinstance(r, Exception)]
    
    print(f"Successful: {len(successful)}, Failed: {len(failed)}")
```

## API Reference

### Functions

#### async_sleep(delay: float) -> None
Async sleep with validation.
- **delay**: Number of seconds to sleep (must be non-negative)
- **Raises**: ValidationError if delay is negative

#### async_gather(*awaitables, return_exceptions: bool = False) -> list[Any]
Run awaitables concurrently.
- **awaitables**: Awaitable objects to run
- **return_exceptions**: If True, exceptions are returned as results
- **Returns**: List of results in same order as inputs
- **Raises**: ValidationError if no awaitables provided

#### async_wait_for(awaitable, timeout: float | None) -> Any
Wait for awaitable with optional timeout.
- **awaitable**: The awaitable to wait for
- **timeout**: Timeout in seconds (None for no timeout)
- **Returns**: Result of the awaitable
- **Raises**: ValidationError if timeout is negative, asyncio.TimeoutError if timeout exceeded

#### async_run(main: Callable[[], Awaitable[Any]], *, debug: bool = False) -> Any
Run async function.
- **main**: Async function to run
- **debug**: Whether to run in debug mode
- **Returns**: Result of the main function
- **Raises**: ValidationError if main is not callable

## Future Enhancements

For planned features including task management, context managers, error boundaries, and more advanced async patterns, see [Future Async Utilities](../../future-implementations/async-utilities.md).

## Related Documentation

- [Process Module](../process/api-index.md) - For async subprocess execution
- [Resilience Module](../resilience/api-index.md) - For retry and circuit breaker patterns
- [Error Handling](../errors/api-index.md) - For error types and handling