# Process Management

Subprocess execution and process management utilities.

## Overview

`provide.foundation`'s process module provides robust subprocess execution with automatic error handling, timeout support, output capturing, and both synchronous and asynchronous execution modes.

## Basic Execution

### Running Commands

Execute commands with automatic error handling:

```python
from provide.foundation.process.sync.execution import run

# Simple command
result = run(["ls", "-la"])
print(result.stdout)

# Command with arguments
result = run(
    ["git", "status"],
    cwd="/path/to/repo"
)

# Shell command
from provide.foundation.process.sync.shell import shell
result = shell(
    "ls -la | grep .py"
)
```

### Process Results

Access comprehensive process information:

```python
from provide.foundation.process.sync.execution import run

result = run(["echo", "Hello"])

# Access results
print(f"Exit code: {result.returncode}")
print(f"Output: {result.stdout}")
print(f"Errors: {result.stderr}")
print(f"Command: {result.args}")

# Check success
if result.returncode == 0:
    print("Command succeeded")
else:
    print(f"Command failed with code {result.returncode}")
```

## Error Handling

### Automatic Checking

Commands check exit codes by default:

```python
from provide.foundation.process.sync.execution import run
from provide.foundation.errors.process import ProcessError

try:
    # Raises ProcessError on non-zero exit
    result = run(["false"])
except ProcessError as e:
    print(f"Command failed: {e}")
    print(f"Exit code: {e.returncode}")
    print(f"Output: {e.stdout}")
    print(f"Errors: {e.stderr}")

# Disable checking
result = run(["false"], check=False)
print(f"Exit code: {result.returncode}")  # Non-zero but no exception
```

### Timeout Handling

Handle command timeouts:

```python
from provide.foundation.process.sync.execution import run
from provide.foundation.errors.process import ProcessTimeoutError

try:
    result = run(
        ["sleep", "60"],
        timeout=5.0  # 5 second timeout
    )
except ProcessTimeoutError as e:
    print(f"Command timed out after {e.timeout} seconds")
    print(f"Partial output: {e.stdout}")
```

## Async Execution

### Async Commands

Run commands asynchronously:

```python
from provide.foundation.process.aio.execution import run as async_run
import asyncio

async def run_async():
    # Single async command
    result = await async_run(["echo", "async"])
    print(result.stdout)

    # Multiple commands concurrently
    tasks = [
        async_run(["echo", "task1"]),
        async_run(["echo", "task2"]),
        async_run(["echo", "task3"])
    ]
    results = await asyncio.gather(*tasks)

    for result in results:
        print(f"Completed: {result.args[0]}")

# Run async function
asyncio.run(run_async())
```

## Related Topics

- [Error Handling](errors.md) - Process error handling
- [Async Logging](../logging/async.md) - Async logging patterns
- [Platform Detection](platform.md) - Platform-specific behavior