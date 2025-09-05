# Process API Reference

Safe subprocess execution utilities with async support and comprehensive error handling.

## Overview

The process module provides secure subprocess execution with automatic logging, timeout handling, and both synchronous and asynchronous interfaces. It wraps Python's subprocess module with Foundation's structured logging and error handling.

## Quick Start

```python
from provide.foundation.process import run_command, run_command_async
import asyncio

# Synchronous execution
result = run_command(['git', 'status'])
if result.returncode == 0:
    print(f"Output: {result.stdout}")

# Asynchronous execution
async def async_example():
    result = await run_command_async(['ls', '-la'])
    return result.stdout

# Run with timeout
result = run_command(['sleep', '10'], timeout=5.0)  # Will timeout
```

## Synchronous API

### `run_command(command, **kwargs) -> CommandResult`

Execute a command synchronously with comprehensive result handling.

**Parameters**:
- `command: list[str]` - Command and arguments to execute
- `cwd: str | Path | None = None` - Working directory
- `timeout: float | None = None` - Timeout in seconds
- `capture_output: bool = True` - Capture stdout/stderr
- `text: bool = True` - Decode output as text
- `encoding: str = 'utf-8'` - Text encoding
- `env: dict[str, str] | None = None` - Environment variables
- `shell: bool = False` - Execute via shell (security risk)

**Returns**: `CommandResult` object with execution details

```python
from provide.foundation.process import run_command

# Basic command execution
result = run_command(['python', '--version'])
print(f"Python version: {result.stdout.strip()}")

# With working directory
result = run_command(['git', 'log', '--oneline'], cwd='/path/to/repo')

# With timeout
try:
    result = run_command(['long_running_script.sh'], timeout=30.0)
except TimeoutExpired:
    print("Command timed out")

# With custom environment
result = run_command(['env'], env={'CUSTOM_VAR': 'value'})
```

### `run_shell_command(command, **kwargs) -> CommandResult`

Execute a shell command (convenience wrapper for shell=True).

**Security Warning**: Only use with trusted input to avoid shell injection.

```python
from provide.foundation.process import run_shell_command

# Shell command with pipes
result = run_shell_command('ls -la | grep .py | wc -l')
file_count = int(result.stdout.strip())

# Environment variable expansion
result = run_shell_command('echo $HOME')
home_dir = result.stdout.strip()
```

## Asynchronous API

### `run_command_async(command, **kwargs) -> CommandResult`

Execute a command asynchronously using asyncio.

```python
import asyncio
from provide.foundation.process import run_command_async

async def run_multiple_commands():
    # Run commands concurrently
    tasks = [
        run_command_async(['git', 'status']),
        run_command_async(['git', 'log', '-1', '--oneline']),
        run_command_async(['git', 'branch'])
    ]
    
    results = await asyncio.gather(*tasks)
    
    for i, result in enumerate(results):
        print(f"Command {i}: {result.stdout}")

# Run the async function
asyncio.run(run_multiple_commands())
```

### `run_shell_command_async(command, **kwargs) -> CommandResult`

Execute a shell command asynchronously.

```python
async def async_shell_example():
    # Complex shell pipeline
    result = await run_shell_command_async(
        'find . -name "*.py" | xargs grep -l "TODO" | head -5'
    )
    
    todo_files = result.stdout.strip().split('\n')
    return todo_files
```

## Result Objects

### `CommandResult`

Contains comprehensive information about command execution.

**Attributes**:
- `returncode: int` - Exit code (0 = success)
- `stdout: str` - Standard output content
- `stderr: str` - Standard error content  
- `command: list[str]` - Command that was executed
- `duration_ms: float` - Execution time in milliseconds
- `pid: int | None` - Process ID
- `timed_out: bool` - Whether execution timed out

**Methods**:
- `was_successful() -> bool` - Check if command succeeded (returncode == 0)
- `raise_on_error() -> None` - Raise exception if command failed
- `to_dict() -> dict` - Convert to dictionary for logging

```python
from provide.foundation.process import run_command

result = run_command(['pytest', 'tests/'])

# Check success
if result.was_successful():
    print("All tests passed!")
    test_output = result.stdout
else:
    print(f"Tests failed with exit code: {result.returncode}")
    error_output = result.stderr

# Get execution details
print(f"Test run took {result.duration_ms:.2f}ms")

# Log structured result
logger.info("test_execution_completed", **result.to_dict())

# Raise on error
try:
    result.raise_on_error()
except ProcessExecutionError as e:
    logger.error("command_failed", error=str(e))
```

## Error Handling

### Exception Types

```python
from provide.foundation.process import (
    ProcessExecutionError,
    ProcessTimeoutError,
    ProcessSecurityError
)

try:
    result = run_command(['invalid_command'])
except ProcessExecutionError as e:
    logger.error("process_execution_failed",
                command=e.command,
                returncode=e.returncode,
                stderr=e.stderr)

except ProcessTimeoutError as e:
    logger.error("process_timeout",
                command=e.command,
                timeout=e.timeout)

except ProcessSecurityError as e:
    logger.error("process_security_violation",
                command=e.command,
                reason=e.reason)
```

### Safe Error Handling

```python
def safe_command_execution(command):
    """Execute command with comprehensive error handling."""
    
    try:
        result = run_command(command, timeout=30.0)
        
        if result.was_successful():
            logger.info("command_succeeded", 
                       command=command,
                       duration_ms=result.duration_ms)
            return result.stdout
        else:
            logger.warning("command_failed",
                          command=command,
                          returncode=result.returncode,
                          stderr=result.stderr)
            return None
            
    except ProcessTimeoutError:
        logger.error("command_timeout", command=command, timeout=30.0)
        return None
        
    except ProcessExecutionError as e:
        logger.error("command_execution_error", 
                    command=command,
                    error=str(e))
        return None
```

## Security Features

### Command Validation

```python
from provide.foundation.process import validate_command, run_command

def secure_git_operation(operation, *args):
    """Safely execute git operations."""
    
    # Validate command structure
    command = ['git', operation] + list(args)
    
    # Security checks
    if not validate_command(command):
        raise ProcessSecurityError("Invalid command structure")
    
    # Whitelist allowed operations
    allowed_operations = {'status', 'log', 'diff', 'branch', 'show'}
    if operation not in allowed_operations:
        raise ProcessSecurityError(f"Operation '{operation}' not allowed")
    
    return run_command(command)

# Usage
result = secure_git_operation('status')
result = secure_git_operation('log', '--oneline', '-10')
```

### Input Sanitization

```python
import shlex
from provide.foundation.process import run_command

def sanitized_grep(pattern, filename):
    """Safely search for pattern in file."""
    
    # Sanitize inputs to prevent injection
    safe_pattern = shlex.quote(pattern)
    safe_filename = shlex.quote(filename)
    
    command = ['grep', safe_pattern, safe_filename]
    return run_command(command)

# Safe usage
result = sanitized_grep('user input; rm -rf /', 'data.txt')
# Executes: grep 'user input; rm -rf /' 'data.txt'
```

### Environment Isolation

```python
from provide.foundation.process import run_command
import os

def isolated_command_execution(command):
    """Execute command in isolated environment."""
    
    # Create minimal environment
    safe_env = {
        'PATH': '/usr/local/bin:/usr/bin:/bin',
        'HOME': '/tmp',
        'TMPDIR': '/tmp',
        'LANG': 'C.UTF-8'
    }
    
    # Remove potentially dangerous variables
    dangerous_vars = {'LD_PRELOAD', 'LD_LIBRARY_PATH', 'PYTHONPATH'}
    current_env = {k: v for k, v in os.environ.items() 
                   if k not in dangerous_vars}
    
    # Merge safe environment
    execution_env = {**safe_env, **current_env}
    
    return run_command(command, env=execution_env)
```

## Advanced Usage

### Process Monitoring

```python
from provide.foundation.process import run_command
from provide.foundation import logger

def monitored_command(command, **kwargs):
    """Execute command with detailed monitoring."""
    
    logger.info("process_starting", command=command)
    
    start_time = time.time()
    
    try:
        result = run_command(command, **kwargs)
        
        logger.info("process_completed",
                   command=command,
                   returncode=result.returncode,
                   duration_ms=result.duration_ms,
                   stdout_lines=len(result.stdout.split('\n')),
                   stderr_lines=len(result.stderr.split('\n')))
        
        return result
        
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.error("process_failed",
                    command=command,
                    error=str(e),
                    duration_ms=duration_ms)
        raise
```

### Batch Processing

```python
async def process_batch_commands(commands):
    """Process multiple commands with controlled concurrency."""
    
    semaphore = asyncio.Semaphore(5)  # Limit concurrent processes
    
    async def execute_with_semaphore(cmd):
        async with semaphore:
            return await run_command_async(cmd)
    
    # Execute all commands concurrently (but limited)
    tasks = [execute_with_semaphore(cmd) for cmd in commands]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results
    successful = []
    failed = []
    
    for cmd, result in zip(commands, results):
        if isinstance(result, Exception):
            failed.append((cmd, result))
        else:
            successful.append((cmd, result))
    
    logger.info("batch_processing_completed",
               total_commands=len(commands),
               successful=len(successful),
               failed=len(failed))
    
    return successful, failed
```

### Stream Processing

```python
import subprocess
from provide.foundation import logger

def stream_command_output(command):
    """Execute command and stream output in real-time."""
    
    logger.info("streaming_process_started", command=command)
    
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    output_lines = []
    
    try:
        for line in process.stdout:
            line = line.rstrip()
            output_lines.append(line)
            
            # Log each line in real-time
            logger.debug("process_output_line",
                        command=command,
                        line=line,
                        line_number=len(output_lines))
            
            # Also print to console
            print(f"[{len(output_lines):04d}] {line}")
        
        returncode = process.wait()
        
        logger.info("streaming_process_completed",
                   command=command,
                   returncode=returncode,
                   total_lines=len(output_lines))
        
        return CommandResult(
            returncode=returncode,
            stdout='\n'.join(output_lines),
            stderr='',
            command=command,
            duration_ms=0,  # Not tracked in streaming mode
            pid=process.pid
        )
        
    except KeyboardInterrupt:
        process.terminate()
        logger.warning("process_interrupted", command=command)
        raise
```

## Configuration

### Global Process Settings

```python
from provide.foundation.process import configure_process_execution

# Configure global defaults
configure_process_execution(
    default_timeout=60.0,           # Default timeout for all commands
    max_concurrent_processes=10,    # Limit concurrent async processes
    log_all_executions=True,        # Log every process execution
    security_mode='strict',         # strict/permissive security
    default_encoding='utf-8'        # Default text encoding
)
```

### Environment-Specific Configuration

```python
import os
from provide.foundation.process import run_command

def get_process_config():
    """Get environment-appropriate process configuration."""
    
    if os.getenv('CI') == 'true':
        # CI environment - faster timeouts, more logging
        return {
            'timeout': 300.0,           # 5 minute timeout
            'capture_output': True,
            'log_level': 'DEBUG'
        }
    elif os.getenv('ENVIRONMENT') == 'production':
        # Production - conservative timeouts, minimal logging
        return {
            'timeout': 30.0,
            'capture_output': False,    # Don't capture large outputs
            'log_level': 'WARNING'
        }
    else:
        # Development - permissive settings
        return {
            'timeout': 120.0,
            'capture_output': True,
            'log_level': 'INFO'
        }
```

## Integration Examples

### Git Operations

```python
from provide.foundation.process import run_command

class GitRepository:
    def __init__(self, repo_path):
        self.repo_path = repo_path
    
    def get_status(self):
        """Get git status."""
        result = run_command(['git', 'status', '--porcelain'], 
                           cwd=self.repo_path)
        result.raise_on_error()
        return result.stdout.strip().split('\n')
    
    def get_current_branch(self):
        """Get current branch name."""
        result = run_command(['git', 'branch', '--show-current'],
                           cwd=self.repo_path)
        result.raise_on_error()
        return result.stdout.strip()
    
    def get_commit_count(self, since_ref='HEAD~10'):
        """Get commit count since reference."""
        result = run_command(['git', 'rev-list', '--count', 
                            f'{since_ref}..HEAD'],
                           cwd=self.repo_path)
        result.raise_on_error()
        return int(result.stdout.strip())

# Usage
repo = GitRepository('/path/to/repo')
status = repo.get_status()
branch = repo.get_current_branch()
```

### Docker Integration

```python
async def docker_operations():
    """Manage Docker containers."""
    
    # List running containers
    result = await run_command_async(['docker', 'ps', '--format', 'json'])
    containers = [json.loads(line) for line in result.stdout.strip().split('\n')]
    
    # Start container with logging
    logger.info("starting_container", image="nginx:latest")
    result = await run_command_async(['docker', 'run', '-d', 'nginx:latest'])
    container_id = result.stdout.strip()
    
    # Monitor container logs
    logs_result = await run_command_async(['docker', 'logs', container_id])
    logger.info("container_logs", 
               container_id=container_id,
               log_lines=len(logs_result.stdout.split('\n')))
    
    return container_id
```

### System Administration

```python
def system_health_check():
    """Perform system health checks."""
    
    checks = {}
    
    # Disk usage
    result = run_command(['df', '-h'])
    if result.was_successful():
        checks['disk_usage'] = 'healthy'
    
    # Memory usage
    result = run_command(['free', '-m'])
    if result.was_successful():
        memory_lines = result.stdout.split('\n')
        checks['memory_usage'] = 'healthy'
    
    # Network connectivity
    result = run_command(['ping', '-c', '1', 'google.com'], timeout=5.0)
    checks['network'] = 'healthy' if result.was_successful() else 'degraded'
    
    # Log overall health
    all_healthy = all(status == 'healthy' for status in checks.values())
    logger.info("system_health_check_completed",
               overall_status='healthy' if all_healthy else 'degraded',
               **checks)
    
    return checks
```

## Best Practices

### 1. Always Use Lists for Commands

```python
# ✅ Good - Safe from injection
run_command(['grep', user_pattern, filename])

# ❌ Bad - Vulnerable to injection
run_shell_command(f'grep {user_pattern} {filename}')
```

### 2. Set Appropriate Timeouts

```python
# ✅ Good - Reasonable timeouts
run_command(['git', 'clone', repo_url], timeout=300.0)  # 5 minutes
run_command(['pytest'], timeout=1800.0)                # 30 minutes

# ❌ Bad - No timeout (could hang forever)
run_command(['long_running_script'])
```

### 3. Handle Errors Gracefully

```python
# ✅ Good - Comprehensive error handling
try:
    result = run_command(['make', 'build'])
    if result.was_successful():
        logger.info("build_successful")
    else:
        logger.error("build_failed", stderr=result.stderr)
        
except ProcessTimeoutError:
    logger.error("build_timeout")
    
except ProcessExecutionError as e:
    logger.error("build_error", error=str(e))
```

### 4. Use Structured Logging

```python
# ✅ Good - Structured process logging
logger.info("process_execution",
           command=command,
           duration_ms=result.duration_ms,
           returncode=result.returncode,
           output_size=len(result.stdout))
```

## Thread Safety

Process execution functions are thread-safe:

```python
import threading
from provide.foundation.process import run_command

def worker(worker_id):
    result = run_command(['echo', f'Worker {worker_id}'])
    return result.stdout

# Safe to run from multiple threads
threads = [
    threading.Thread(target=worker, args=(i,)) 
    for i in range(10)
]

for t in threads:
    t.start()
```

## See Also

- [Platform API](../platform/) - Platform detection for process configuration
- [Logging API](../logger/) - Structured logging integration
- [Utils API](../utils/) - Environment and utility functions
- [Process Guide](../../guide/utilities/process.md) - Process execution patterns