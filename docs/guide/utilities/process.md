# Process Management

Subprocess execution and process management utilities.

## Overview

provide.foundation's process module provides robust subprocess execution with automatic error handling, timeout support, output capturing, and both synchronous and asynchronous execution modes. It ensures consistent process management across platforms.

## Basic Execution

### Running Commands

Execute commands with automatic error handling:

```python
from provide.foundation.process import run_command

# Simple command
result = run_command(["ls", "-la"])
print(result.stdout)

# Command with arguments
result = run_command(
    ["git", "status"],
    cwd="/path/to/repo"
)

# Shell command
result = run_command(
    "ls -la | grep .py",
    shell=True
)

# With timeout
result = run_command(
    ["long-running-task"],
    timeout=30.0  # 30 seconds
)
```

### Process Results

Access comprehensive process information:

```python
from provide.foundation.process import run_command

result = run_command(["echo", "Hello"])

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
from provide.foundation.process import run_command
from provide.foundation.errors import ProcessError

try:
    # Raises ProcessError on non-zero exit
    result = run_command(["false"])
except ProcessError as e:
    print(f"Command failed: {e}")
    print(f"Exit code: {e.returncode}")
    print(f"Output: {e.stdout}")
    print(f"Errors: {e.stderr}")

# Disable checking
result = run_command(["false"], check=False)
print(f"Exit code: {result.returncode}")  # Non-zero but no exception
```

### Timeout Handling

Handle command timeouts:

```python
from provide.foundation.process import run_command
from provide.foundation.errors import TimeoutError

try:
    result = run_command(
        ["sleep", "60"],
        timeout=5.0  # 5 second timeout
    )
except TimeoutError as e:
    print(f"Command timed out after {e.timeout} seconds")
    print(f"Partial output: {e.stdout}")
```

## Async Execution

### Async Commands

Run commands asynchronously:

```python
from provide.foundation.process import async_run_command
import asyncio

async def run_async():
    # Single async command
    result = await async_run_command(["echo", "async"])
    print(result.stdout)
    
    # Multiple commands concurrently
    tasks = [
        async_run_command(["task1"]),
        async_run_command(["task2"]),
        async_run_command(["task3"])
    ]
    results = await asyncio.gather(*tasks)
    
    for result in results:
        print(f"Completed: {result.args[0]}")

# Run async function
asyncio.run(run_async())
```

### Streaming Output

Stream output as it's produced:

```python
from provide.foundation.process import stream_command

# Synchronous streaming
for line in stream_command(["ping", "-c", "5", "google.com"]):
    print(f">>> {line}")

# Async streaming
async def stream_async():
    async for line in async_stream_command(["ping", "-c", "5", "google.com"]):
        print(f">>> {line}")
        # Process each line as it arrives
        await process_line(line)
```

## Environment Control

### Custom Environment

Control process environment variables:

```python
from provide.foundation.process import run_command
import os

# Add to existing environment
custom_env = os.environ.copy()
custom_env["MY_VAR"] = "custom_value"

result = run_command(
    ["printenv", "MY_VAR"],
    env=custom_env
)

# Minimal environment
minimal_env = {
    "PATH": "/usr/bin:/bin",
    "HOME": os.environ["HOME"]
}

result = run_command(
    ["env"],
    env=minimal_env
)
```

### Working Directory

Set process working directory:

```python
from pathlib import Path

# With Path object
result = run_command(
    ["pwd"],
    cwd=Path.home() / "projects"
)

# With string
result = run_command(
    ["npm", "install"],
    cwd="/path/to/project"
)
```

## Input/Output

### Sending Input

Send input to processes:

```python
# Send text input
result = run_command(
    ["grep", "pattern"],
    input="line 1\npattern here\nline 3"
)
print(result.stdout)  # "pattern here"

# Interactive input
result = run_command(
    ["python", "-c", "name = input('Name: '); print(f'Hello {name}')"],
    input="Alice\n"
)
```

### Output Options

Control output capturing:

```python
# Capture output (default)
result = run_command(["ls"], capture_output=True)
print(result.stdout)

# Don't capture (output goes to terminal)
result = run_command(["ls"], capture_output=False)
# result.stdout and result.stderr will be None

# Binary output
result = run_command(
    ["cat", "image.png"],
    text=False  # Returns bytes instead of str
)
binary_data = result.stdout  # bytes
```

## Pattern Examples

### Command Pipeline

Build command pipelines:

```python
from provide.foundation.process import run_command

class CommandPipeline:
    """Execute commands in sequence."""
    
    def __init__(self):
        self.commands = []
        self.results = []
    
    def add(self, cmd, **kwargs):
        """Add command to pipeline."""
        self.commands.append((cmd, kwargs))
        return self
    
    def run(self):
        """Execute pipeline."""
        for cmd, kwargs in self.commands:
            try:
                result = run_command(cmd, **kwargs)
                self.results.append(result)
                
                # Use output as input for next command
                if self.results and 'input' not in kwargs:
                    kwargs['input'] = result.stdout
                    
            except ProcessError as e:
                logger.error(f"Pipeline failed at: {cmd}")
                raise
        
        return self.results
    
# Use pipeline
pipeline = CommandPipeline()
results = (
    pipeline
    .add(["echo", "Hello World"])
    .add(["tr", "a-z", "A-Z"])
    .add(["cut", "-d", " ", "-f", "2"])
    .run()
)
print(results[-1].stdout)  # "WORLD"
```

### Process Manager

Manage multiple processes:

```python
from provide.foundation.process import async_run_command
import asyncio

class ProcessManager:
    """Manage multiple concurrent processes."""
    
    def __init__(self, max_concurrent=5):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.running = []
        self.completed = []
    
    async def run_task(self, cmd, **kwargs):
        """Run task with concurrency limit."""
        async with self.semaphore:
            logger.info(f"Starting: {cmd}")
            try:
                result = await async_run_command(cmd, **kwargs)
                self.completed.append(result)
                logger.info(f"Completed: {cmd}")
                return result
            except Exception as e:
                logger.error(f"Failed: {cmd} - {e}")
                raise
    
    async def run_all(self, tasks):
        """Run all tasks concurrently."""
        coroutines = [
            self.run_task(cmd, **kwargs)
            for cmd, kwargs in tasks
        ]
        results = await asyncio.gather(
            *coroutines,
            return_exceptions=True
        )
        return results

# Use manager
async def process_batch():
    manager = ProcessManager(max_concurrent=3)
    
    tasks = [
        (["task1", "--option"], {"timeout": 30}),
        (["task2"], {"cwd": "/tmp"}),
        (["task3"], {"env": {"VAR": "value"}}),
    ]
    
    results = await manager.run_all(tasks)
    
    # Check results
    for result in results:
        if isinstance(result, Exception):
            print(f"Task failed: {result}")
        else:
            print(f"Task output: {result.stdout}")
```

### Safe Script Execution

Execute scripts safely:

```python
from provide.foundation.process import run_command
from provide.foundation import logger
import tempfile
import os

def run_script_safely(script_content: str, interpreter="bash"):
    """Run script content safely."""
    
    # Create temporary script file
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.sh' if interpreter == 'bash' else '.py',
        delete=False
    ) as f:
        f.write(script_content)
        script_path = f.name
    
    try:
        # Make executable if needed
        if interpreter == "bash":
            os.chmod(script_path, 0o755)
        
        # Run script
        result = run_command(
            [interpreter, script_path],
            capture_output=True,
            timeout=60.0,
            check=False  # Handle errors ourselves
        )
        
        if result.returncode != 0:
            logger.error(
                "Script failed",
                exit_code=result.returncode,
                stderr=result.stderr
            )
        
        return result
        
    finally:
        # Clean up
        try:
            os.unlink(script_path)
        except OSError:
            pass

# Use safe execution
script = '''
echo "Starting process..."
for i in {1..5}; do
    echo "Step $i"
    sleep 1
done
echo "Complete!"
'''

result = run_script_safely(script)
print(result.stdout)
```

## Best Practices

### 1. Use Lists for Commands

```python
# Good: List of arguments (safe)
run_command(["rm", "-f", filename])

# Bad: Shell injection risk
run_command(f"rm -f {filename}", shell=True)
```

### 2. Handle Errors

```python
# Good: Explicit error handling
try:
    result = run_command(cmd)
except ProcessError as e:
    logger.error(f"Command failed: {e}")
    # Handle error...
except TimeoutError as e:
    logger.error(f"Command timed out: {e}")
    # Handle timeout...

# Bad: Ignore errors
run_command(cmd, check=False)  # Silent failures
```

### 3. Set Timeouts

```python
# Good: Prevent hanging
result = run_command(
    ["potentially-slow-command"],
    timeout=30.0
)

# Bad: No timeout
result = run_command(["potentially-slow-command"])
# May hang forever
```

### 4. Clean Environment

```python
# Good: Control environment
clean_env = {
    "PATH": os.environ["PATH"],
    "HOME": os.environ["HOME"],
    # Only what's needed
}
run_command(cmd, env=clean_env)

# Bad: Inherit everything
run_command(cmd)  # May have sensitive vars
```

## Related Topics

- [Error Handling](errors.md) - Process error handling
- [Async Operations](../async/index.md) - Async patterns
- [Platform Detection](platform.md) - Platform-specific behavior