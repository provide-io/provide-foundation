# Streams API Reference

Stream management utilities for Foundation logging output including console, file, and testing streams.

## Overview

The streams module provides comprehensive stream management for Foundation logging, enabling output redirection, file logging, console detection, and testing support. It handles thread-safe stream operations and provides utilities for managing different output destinations.

## Quick Start

```python
from provide.foundation.streams import (
    get_log_stream, configure_file_logging, 
    supports_color, write_to_console
)

# Get current log stream
current_stream = get_log_stream()

# Configure file logging
configure_file_logging('/var/log/myapp.log')

# Check console capabilities
if supports_color():
    write_to_console('\033[32mGreen text\033[0m\n')
else:
    write_to_console('Plain text\n')
```

## Core Stream Functions

### `get_log_stream() -> TextIO`

Get the currently active log stream.

**Returns**: The active text stream for logging output

```python
from provide.foundation.streams import get_log_stream

# Get current stream
stream = get_log_stream()
print(f"Current stream: {stream}")

# Write directly to current stream
stream.write("Direct message\n")
stream.flush()
```

### `set_log_stream_for_testing(stream: TextIO | None) -> None`

Set the log stream for testing purposes.

**Parameters**:
- `stream: TextIO | None` - Stream to redirect to, or None to reset to stderr

```python
import io
from provide.foundation.streams import set_log_stream_for_testing

# Redirect to StringIO for testing
test_stream = io.StringIO()
set_log_stream_for_testing(test_stream)

# Log messages will go to test_stream
logger.info("test_message")
output = test_stream.getvalue()

# Reset to stderr
set_log_stream_for_testing(None)
```

### `ensure_stderr_default() -> None`

Ensure the log stream defaults to stderr if it's currently stdout.

```python
from provide.foundation.streams import ensure_stderr_default, get_log_stream
import sys

# If stream is stdout, this will change it to stderr
current = get_log_stream()
print(f"Before: {current}")

ensure_stderr_default()

current = get_log_stream()
print(f"After: {current}")  # Will be stderr if it was stdout
```

## File Stream Functions

### `configure_file_logging(log_file_path: str | None) -> None`

Configure file-based logging output.

**Parameters**:
- `log_file_path: str | None` - Path to log file, or None to disable file logging

```python
from provide.foundation.streams import configure_file_logging

# Enable file logging
configure_file_logging('/var/log/myapp.log')

# Disable file logging (revert to console)
configure_file_logging(None)

# With directory creation
configure_file_logging('/var/log/apps/myapp/debug.log')  # Creates directories
```

### `flush_log_streams() -> None`

Flush all active log streams to ensure data is written.

```python
from provide.foundation.streams import flush_log_streams

# Ensure all buffered log data is written
flush_log_streams()
```

### `close_log_streams() -> None`

Close file log streams and reset to stderr.

```python
from provide.foundation.streams import close_log_streams

# Clean shutdown - close file handles and reset
close_log_streams()
```

### `reset_streams() -> None`

Reset all stream state (primarily for testing).

```python
from provide.foundation.streams import reset_streams

def teardown_test():
    # Reset all stream state after test
    reset_streams()
```

## Console Stream Functions

### `get_console_stream() -> TextIO`

Get the appropriate console stream for output.

```python
from provide.foundation.streams import get_console_stream

console = get_console_stream()
console.write("Console output\n")
console.flush()
```

### `is_tty() -> bool`

Check if the current stream is a TTY (terminal).

**Returns**: True if the current stream is connected to a terminal

```python
from provide.foundation.streams import is_tty

if is_tty():
    # Interactive terminal - can use colors, cursor positioning
    print("Running in terminal")
else:
    # Non-interactive - file, pipe, etc.
    print("Running non-interactively")
```

### `supports_color() -> bool`

Check if the current stream supports color output.

**Returns**: True if color output is supported and enabled

```python
from provide.foundation.streams import supports_color

if supports_color():
    # Use ANSI color codes
    message = '\033[32mSUCCESS\033[0m'
else:
    # Plain text only
    message = 'SUCCESS'

print(message)
```

**Color Support Logic**:
- Returns False if `NO_COLOR` environment variable is set
- Returns True if `FORCE_COLOR` environment variable is set  
- Otherwise returns True if connected to a TTY

### `write_to_console(message: str, stream: TextIO | None = None) -> None`

Write a message to the console stream with error handling.

**Parameters**:
- `message: str` - Message to write to console
- `stream: TextIO | None` - Optional specific stream, defaults to current console stream

```python
from provide.foundation.streams import write_to_console

# Write to current console stream
write_to_console("Hello, console!\n")

# Write to specific stream
import sys
write_to_console("Error message\n", sys.stderr)

# With color support check
from provide.foundation.streams import supports_color

if supports_color():
    write_to_console('\033[31mERROR:\033[0m Something went wrong\n')
else:
    write_to_console('ERROR: Something went wrong\n')
```

## Testing Utilities

### Stream Redirection for Testing

```python
import io
from provide.foundation.streams import set_log_stream_for_testing
from provide.foundation.testing.streams import reset_log_stream

def test_logging_output():
    # Capture log output
    captured_output = io.StringIO()
    set_log_stream_for_testing(captured_output)
    
    # Your test code here
    logger.info("test_message", data="value")
    
    # Verify output
    output = captured_output.getvalue()
    assert "test_message" in output
    
    # Clean up
    reset_log_stream()
```

### Test Stream Management

```python
from provide.foundation.testing.streams import (
    set_log_stream_for_testing,
    get_current_log_stream,
    reset_log_stream
)

class TestWithStreams:
    def setup_method(self):
        self.test_stream = io.StringIO()
        set_log_stream_for_testing(self.test_stream)
    
    def teardown_method(self):
        reset_log_stream()
    
    def test_something(self):
        logger.info("test_event")
        output = self.test_stream.getvalue()
        assert "test_event" in output
```

## Advanced Usage

### Multi-Stream Configuration

```python
from provide.foundation.streams import configure_file_logging, get_log_stream
import sys

class MultiStreamLogger:
    def __init__(self, file_path: str | None = None):
        self.console_stream = sys.stderr
        self.file_stream = None
        
        if file_path:
            configure_file_logging(file_path)
            self.file_stream = get_log_stream()
    
    def log_to_both(self, message: str):
        # Log to console
        self.console_stream.write(f"[CONSOLE] {message}\n")
        self.console_stream.flush()
        
        # Log to file if configured
        if self.file_stream and self.file_stream != self.console_stream:
            self.file_stream.write(f"[FILE] {message}\n")
            self.file_stream.flush()
```

### Environment-Aware Stream Configuration

```python
import os
from provide.foundation.streams import configure_file_logging, supports_color

def setup_environment_streams():
    """Configure streams based on environment."""
    
    # Production - log to file
    if os.getenv('ENVIRONMENT') == 'production':
        log_file = os.getenv('LOG_FILE', '/var/log/app.log')
        configure_file_logging(log_file)
        
    # Development - console with colors
    elif os.getenv('ENVIRONMENT') == 'development':
        configure_file_logging(None)  # Console only
        
    # CI/CD - console without colors
    elif os.getenv('CI'):
        configure_file_logging(None)
        os.environ['NO_COLOR'] = '1'
        
    return {
        'file_logging': bool(os.getenv('LOG_FILE')),
        'color_support': supports_color(),
        'is_tty': is_tty()
    }
```

### Stream Context Manager

```python
import contextlib
from typing import TextIO
from provide.foundation.streams import get_log_stream, set_log_stream_for_testing

@contextlib.contextmanager
def temporary_stream(stream: TextIO):
    """Context manager for temporarily changing log stream."""
    original_stream = get_log_stream()
    try:
        set_log_stream_for_testing(stream)
        yield stream
    finally:
        set_log_stream_for_testing(original_stream)

# Usage
import io
with temporary_stream(io.StringIO()) as temp_stream:
    logger.info("temporary_message")
    captured = temp_stream.getvalue()
    print(f"Captured: {captured}")
# Stream automatically restored
```

### Performance Monitoring

```python
import time
from provide.foundation.streams import flush_log_streams

def benchmark_stream_performance(message_count: int = 10000):
    """Benchmark stream write performance."""
    
    start_time = time.time()
    
    for i in range(message_count):
        logger.info("benchmark_message", iteration=i)
    
    # Force flush to measure actual write time
    flush_log_streams()
    
    elapsed = time.time() - start_time
    messages_per_sec = message_count / elapsed
    
    return {
        'messages_per_second': messages_per_sec,
        'total_time': elapsed,
        'average_latency_us': (elapsed / message_count) * 1_000_000
    }
```

## Error Handling

### Stream Failure Recovery

```python
from provide.foundation.streams import get_log_stream, configure_file_logging
import sys

def safe_stream_operation():
    """Demonstrate safe stream operations with error handling."""
    
    try:
        # Attempt file logging
        configure_file_logging('/restricted/path/app.log')
        
    except PermissionError:
        # Fall back to console
        configure_file_logging(None)
        logger.warning("file_logging_failed", 
                      reason="permission_denied",
                      fallback="console")
    
    # Verify stream is working
    current_stream = get_log_stream()
    try:
        current_stream.write("test\n")
        current_stream.flush()
    except Exception as e:
        # Ultimate fallback to stderr
        sys.stderr.write(f"Stream failure: {e}\n")
        configure_file_logging(None)
```

### Graceful Shutdown

```python
import atexit
from provide.foundation.streams import close_log_streams, flush_log_streams

def setup_graceful_shutdown():
    """Setup graceful stream shutdown."""
    
    def cleanup_streams():
        try:
            # Flush any remaining data
            flush_log_streams()
            # Close file handles
            close_log_streams()
        except Exception as e:
            print(f"Error during stream cleanup: {e}", file=sys.stderr)
    
    # Register cleanup on exit
    atexit.register(cleanup_streams)

# Call during application startup
setup_graceful_shutdown()
```

## Thread Safety

All stream operations are thread-safe using internal locking:

```python
import threading
from provide.foundation.streams import get_log_stream, write_to_console

def worker_thread(worker_id: int):
    """Worker thread that safely uses streams."""
    
    for i in range(1000):
        # Thread-safe stream access
        current_stream = get_log_stream()
        
        # Thread-safe console writing
        write_to_console(f"Worker {worker_id}: Message {i}\n")

# Safe to run multiple threads
threads = [
    threading.Thread(target=worker_thread, args=(i,))
    for i in range(10)
]

for t in threads:
    t.start()
for t in threads:
    t.join()
```

## Best Practices

### 1. Always Use Stream Functions

```python
# ✅ Good - Use stream functions
from provide.foundation.streams import get_log_stream
stream = get_log_stream()
stream.write("message\n")

# ❌ Bad - Direct sys.stderr access
import sys
sys.stderr.write("message\n")
```

### 2. Flush Important Messages

```python
from provide.foundation.streams import flush_log_streams

# Critical messages should be flushed immediately
logger.error("critical_error", details="system_failure")
flush_log_streams()
```

### 3. Test Stream Isolation

```python
import io
from provide.foundation.streams import set_log_stream_for_testing

def test_with_isolated_stream():
    test_stream = io.StringIO()
    set_log_stream_for_testing(test_stream)
    
    try:
        # Test code here
        logger.info("test_message")
        output = test_stream.getvalue()
        assert "test_message" in output
    finally:
        # Always reset
        set_log_stream_for_testing(None)
```

### 4. Environment-Specific Configuration

```python
import os
from provide.foundation.streams import configure_file_logging

# Configure based on environment
log_file = os.getenv('APP_LOG_FILE')
if log_file:
    configure_file_logging(log_file)
else:
    configure_file_logging(None)  # Console output
```

## See Also

- [Logger API](../logger/api-index.md) - Main logging interface
- [Process API](../process/api-index.md) - Process execution with stream handling
- [Testing Guide](../../guide/testing.md) - Testing with stream redirection
- [Configuration Guide](../../guide/config/index.md) - Environment-based stream setup