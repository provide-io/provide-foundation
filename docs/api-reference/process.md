# Process Execution API

The `provide.foundation.process` module provides safe, logging-integrated subprocess execution with both synchronous and asynchronous support.

## Overview

The process module provides:
- Safe subprocess execution with structured logging
- Timeout and error handling
- Environment variable management
- Output streaming capabilities
- Both sync and async APIs

## Quick Start

```python
from provide.foundation import process

# Simple command execution
result = process.run_command(["ls", "-la"])
print(result.stdout)

# Get just the output
output = process.run_command_simple(["git", "status"])

# Stream output line by line
for line in process.stream_command(["npm", "install"]):
    print(f"npm: {line}")

# Async execution
import asyncio
result = await process.async_run_command(["python", "script.py"])
```

## Synchronous API

### `run_command(cmd, **kwargs) -> CompletedProcess`

Executes a command and returns detailed results.

**Parameters:**
- `cmd: list[str]` - Command and arguments as a list
- `cwd: str | Path | None` - Working directory
- `env: Mapping[str, str] | None` - Environment variables
- `capture_output: bool = True` - Capture stdout/stderr
- `check: bool = True` - Raise exception on non-zero exit
- `timeout: float | None` - Timeout in seconds
- `text: bool = True` - Decode output as text
- `input: str | None` - Input to send to process
- `shell: bool = False` - Run through shell

**Returns:** `CompletedProcess` object with:
- `args: list[str]` - Command arguments
- `returncode: int` - Exit code
- `stdout: str` - Standard output
- `stderr: str` - Standard error
- `cwd: str | None` - Working directory used
- `env: dict[str, str] | None` - Environment used

**Example:**
```python
result = process.run_command(
    ["git", "clone", "https://github.com/user/repo.git"],
    cwd="/tmp",
    timeout=30
)

if result.returncode == 0:
    print("Clone successful")
    print(result.stdout)
```

### `run_command_simple(cmd, **kwargs) -> str`

Executes a command and returns stdout as a string.

**Parameters:** Same as `run_command`

**Returns:** Stripped stdout string

**Example:**
```python
branch = process.run_command_simple(["git", "branch", "--show-current"])
print(f"Current branch: {branch}")
```

### `stream_command(cmd, **kwargs) -> Iterator[str]`

Streams command output line by line.

**Parameters:**
- `cmd: list[str]` - Command and arguments
- `cwd: str | Path | None` - Working directory
- `env: Mapping[str, str] | None` - Environment variables
- `timeout: float | None` - Timeout in seconds

**Yields:** Lines of output from the command

**Example:**
```python
for line in process.stream_command(["docker", "build", "."]):
    if "Step" in line:
        print(line)
```

## Asynchronous API

### `async_run_command(cmd, **kwargs) -> CompletedProcess`

Async version of `run_command`.

**Parameters:** Similar to `run_command` but `input` is bytes

**Example:**
```python
import asyncio

async def run_tests():
    result = await process.async_run_command(
        ["pytest", "tests/"],
        timeout=60
    )
    return result.returncode == 0

success = asyncio.run(run_tests())
```

### `async_stream_command(cmd, **kwargs) -> AsyncIterator[str]`

Async version of `stream_command`.

**Example:**
```python
async def watch_logs():
    async for line in process.async_stream_command(["tail", "-f", "app.log"]):
        if "ERROR" in line:
            print(f"Error detected: {line}")
```

## Error Handling

### `ProcessError`

Raised when a process fails (non-zero exit code).

**Attributes:**
- `message: str` - Error description
- `code: str` - Error code
- `context: dict` - Additional context including:
  - `command: str` - Command that failed
  - `returncode: int` - Exit code
  - `stdout: str | None` - Captured stdout
  - `stderr: str | None` - Captured stderr

**Example:**
```python
from provide.foundation.process import ProcessError

try:
    process.run_command(["false"])
except ProcessError as e:
    print(f"Command failed: {e}")
    print(f"Exit code: {e.context['returncode']}")
    print(f"Error output: {e.context.get('stderr', '')}")
```

### `TimeoutError`

Raised when a process exceeds the timeout.

**Example:**
```python
from provide.foundation.process import TimeoutError

try:
    process.run_command(["sleep", "100"], timeout=1)
except TimeoutError as e:
    print(f"Command timed out: {e}")
```

## Common Patterns

### Running with Custom Environment

```python
# Add to existing environment
import os
env = os.environ.copy()
env["MY_VAR"] = "value"

result = process.run_command(["myapp"], env=env)

# Or use only specific variables
result = process.run_command(
    ["myapp"],
    env={"PATH": "/usr/bin", "HOME": "/home/user"}
)
```

### Handling Different Working Directories

```python
from pathlib import Path

# Using string path
result = process.run_command(["npm", "install"], cwd="/path/to/project")

# Using Path object
project_dir = Path.home() / "projects" / "myapp"
result = process.run_command(["npm", "install"], cwd=project_dir)
```

### Input/Output Piping

```python
# Send input to process
result = process.run_command(
    ["grep", "error"],
    input="line1\nerror on line2\nline3"
)

# Pipe between commands manually
data = process.run_command_simple(["cat", "file.txt"])
result = process.run_command(["grep", "pattern"], input=data)
```

### Error Recovery with Retry

```python
from provide.foundation.errors.decorators import retry_on_error
from provide.foundation.process import ProcessError

@retry_on_error(max_attempts=3, exceptions=(ProcessError,))
def deploy():
    return process.run_command(["./deploy.sh"], timeout=300)

try:
    result = deploy()
    print("Deployment successful")
except ProcessError:
    print("Deployment failed after 3 attempts")
```

### Parallel Execution

```python
import asyncio

async def run_parallel_tests():
    tasks = [
        process.async_run_command(["pytest", "tests/unit"]),
        process.async_run_command(["pytest", "tests/integration"]),
        process.async_run_command(["pytest", "tests/e2e"])
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Test suite {i} failed: {result}")
        elif result.returncode != 0:
            print(f"Test suite {i} failed with code {result.returncode}")
        else:
            print(f"Test suite {i} passed")
```

### Real-time Output Processing

```python
def build_with_progress():
    for line in process.stream_command(["docker", "build", "."]):
        # Parse Docker build output
        if line.startswith("Step"):
            step_num = line.split()[1].strip(":")
            print(f"Building step {step_num}")
        elif "Successfully built" in line:
            image_id = line.split()[-1]
            print(f"Built image: {image_id}")
            return image_id
```

## Logging Integration

All process execution is automatically logged with structured logging:

```python
# Commands are logged with emojis for visual parsing
result = process.run_command(["git", "pull"])
# Logs: 🚀 Running command: git pull

# Failures are logged with context
try:
    process.run_command(["false"])
except ProcessError:
    pass
# Logs: ❌ Command failed: exit code 1

# Timeouts are logged
try:
    process.run_command(["sleep", "100"], timeout=1)
except TimeoutError:
    pass
# Logs: ⏱️ Command timed out after 1.0s
```

## Best Practices

1. **Always use lists for commands** - Avoid shell injection:
   ```python
   # Good
   process.run_command(["grep", pattern, "file.txt"])
   
   # Bad - vulnerable to injection
   process.run_command(f"grep {pattern} file.txt", shell=True)
   ```

2. **Set appropriate timeouts** - Prevent hanging:
   ```python
   result = process.run_command(["curl", url], timeout=30)
   ```

3. **Handle errors explicitly**:
   ```python
   try:
       result = process.run_command(["risky-command"])
   except ProcessError as e:
       # Log error and recover
       plog.error("Command failed", **e.context)
       # Use fallback behavior
   ```

4. **Use streaming for long-running commands**:
   ```python
   # Don't buffer large outputs
   for line in process.stream_command(["find", "/", "-name", "*.log"]):
       process_line(line)
   ```

5. **Clean up resources in async code**:
   ```python
   async def monitor():
       try:
           async for line in process.async_stream_command(["tail", "-f", "log"]):
               await process_line(line)
       finally:
           # Cleanup code here
           pass
   ```

## See Also

- [Platform Detection](platform.md) - For platform-specific commands
- [Error Handling](errors.md) - For error recovery patterns
- [Logger](logger.md) - For logging configuration