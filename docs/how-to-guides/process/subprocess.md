# How to Execute Subprocesses

Foundation provides secure subprocess execution with integrated logging and security features.

## Synchronous Execution

### Basic Command Execution

```python
from provide.foundation.process import run

# Run command
result = run(["ls", "-la"])

print(result.stdout)      # Command output
print(result.returncode)  # Exit code
```

### Shell Commands

```python
from provide.foundation.process import shell

# Run shell command
result = shell("ls -la | grep README")

print(result.stdout)
```

### Simple Execution

```python
from provide.foundation.process import run_simple

# Run command, raise on error
output = run_simple(["git", "status"])
print(output)  # Just the stdout
```

### Streaming Output

```python
from provide.foundation.process import stream

# Stream command output line-by-line
for line in stream(["tail", "-f", "logfile.txt"]):
    print(line)  # Process each line as it arrives
```

## Asynchronous Execution

### Async Commands

```python
from provide.foundation.process import async_run
import asyncio

async def run_command():
    result = await async_run(["ls", "-la"])
    print(result.stdout)

asyncio.run(run_command())
```

### Async Shell

```python
from provide.foundation.process import async_shell
import asyncio

async def run_shell():
    result = await async_shell("echo 'Hello'")
    print(result.stdout)

asyncio.run(run_shell())
```

### Async Streaming

```python
from provide.foundation.process import async_stream
import asyncio

async def stream_output():
    async for line in async_stream(["tail", "-f", "log.txt"]):
        print(line)

asyncio.run(stream_output())
```

## Process Management

### Managed Process

```python
from provide.foundation.process import ManagedProcess

# Create managed process
proc = ManagedProcess(["python", "server.py"])

# Start process
proc.start()

# Wait for output
output = proc.wait_for_output(pattern="Server started", timeout=10)

# Stop process
proc.stop()
```

### Wait for Output

```python
from provide.foundation.process import wait_for_process_output
import subprocess

proc = subprocess.Popen(["python", "app.py"], stdout=subprocess.PIPE)

# Wait for specific output
success = wait_for_process_output(
    proc,
    pattern="Ready to accept connections",
    timeout=30
)

if success:
    print("Application started successfully")
```

## Process Control (Linux)

**Requires**: `provide-foundation[process]` extra on Linux

```python
from provide.foundation.process import (
    set_process_title,
    set_name,
    set_death_signal,
    set_no_new_privs
)

# Set process title (visible in ps/top)
set_process_title("my-worker")

# Set process name (Linux prctl)
if is_linux():
    set_name("worker-1")

    # Set death signal (kill when parent dies)
    import signal
    set_death_signal(signal.SIGTERM)

    # Disable privilege escalation
    set_no_new_privs()
```

## Exit Utilities

```python
from provide.foundation.process import (
    exit_success,
    exit_error,
    exit_interrupted
)

# Exit with success
exit_success()  # Exit code 0

# Exit with error
exit_error("Operation failed", code=1)

# Exit on interruption (Ctrl+C)
try:
    do_work()
except KeyboardInterrupt:
    exit_interrupted()  # Exit code 130
```

## Security Features

Foundation's process execution includes:

- **Command validation**: Prevents command injection
- **Environment scrubbing**: Removes sensitive variables
- **Automatic logging**: All executions logged securely
- **Secret masking**: Secrets masked in logs

```python
from provide.foundation.process import run
from provide.foundation import logger

# Execution automatically logged with masked secrets
result = run([
    "curl",
    "-H", "Authorization: Bearer secret-token",
    "https://api.example.com"
])

# Log shows: Authorization: Bearer ***MASKED***
```

## Best Practices

### ✅ DO: Use List Arguments

```python
# ✅ Good: Safe from injection
from provide.foundation.process import run

result = run(["git", "log", "--oneline", user_input])

# ❌ Bad: Shell injection risk
result = shell(f"git log --oneline {user_input}")
```

### ✅ DO: Handle Errors

```python
# ✅ Good: Check return code
from provide.foundation.process import run, ProcessError

try:
    result = run(["command", "arg"])
    if result.returncode != 0:
        handle_error(result.stderr)
except ProcessError as e:
    logger.error("command_failed", error=str(e))
```

### ✅ DO: Use Async for Concurrent Commands

```python
# ✅ Good: Run commands concurrently
from provide.foundation.process import async_run
import asyncio

async def run_all():
    results = await asyncio.gather(
        async_run(["command1"]),
        async_run(["command2"]),
        async_run(["command3"])
    )

asyncio.run(run_all())
```

## Common Patterns

### Run with Timeout

```python
from provide.foundation.process import run

try:
    result = run(["long-running-command"], timeout=30)
except TimeoutError:
    print("Command timed out")
```

### Capture and Log Output

```python
from provide.foundation.process import run
from provide.foundation import logger

result = run(["deployment-script"])

logger.info(
    "deployment_executed",
    exit_code=result.returncode,
    output_lines=len(result.stdout.split("\n"))
)
```

## Next Steps

- **[Platform Detection](../platform/platform-detection.md)**: Platform-aware execution
- **[Security](../security/security-utilities.md)**: Secure command execution
- **[Logging](../logging/basic-logging.md)**: Log process execution

---

**Tip**: Always use list-based arguments instead of shell strings to prevent injection attacks.
