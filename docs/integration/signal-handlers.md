# Signal Handler Management

Foundation's CLI provides signal handling for graceful shutdown, but it's designed to coexist with host applications that may have their own signal handling needs.

## Overview

Foundation can optionally manage SIGINT (Ctrl+C) and SIGTERM signals to ensure proper cleanup on interruption. Signal handlers are **automatically restored** during cleanup to avoid interfering with host applications.

## Default Behavior (CLI Mode)

When using Foundation as a CLI application, signal handling is **enabled by default**:

```python
from provide.foundation.cli.shutdown import register_cleanup_handlers

# Register with signal management (default)
register_cleanup_handlers()
```

This will:
1. Save your existing signal handlers
2. Register Foundation's handlers
3. **Automatically restore** original handlers during cleanup

## Library Integration Mode

When using Foundation as a library within another application, **disable** signal management to let your application control signals:

```python
from provide.foundation.cli.shutdown import register_cleanup_handlers

# Register WITHOUT signal management (library mode)
register_cleanup_handlers(manage_signals=False)
```

This ensures:
- Foundation's cleanup still runs via `atexit`
- Your application retains full control of signal handlers
- No interference with host application signal handling

## Automatic Restoration

Foundation **automatically restores** original signal handlers during cleanup. You don't need to manually call `unregister_cleanup_handlers()` in production code.

Restoration happens automatically when:
- Program exits normally
- `atexit` cleanup runs
- Signal handler triggers exit
- Exception causes termination

## Example: Host Application Integration

```python
import signal
from provide.foundation.cli.shutdown import register_cleanup_handlers

def my_app_signal_handler(signum, frame):
    """My application's custom signal handler."""
    print("App handling signal...")
    # Custom cleanup
    sys.exit(0)

# App sets its own handlers FIRST
signal.signal(signal.SIGINT, my_app_signal_handler)
signal.signal(signal.SIGTERM, my_app_signal_handler)

# Foundation registers WITHOUT managing signals
register_cleanup_handlers(manage_signals=False)

# Your handlers remain active
# Foundation cleanup runs via atexit
```

## Testing

For testing, you can manually unregister handlers:

```python
from provide.foundation.cli.shutdown import (
    register_cleanup_handlers,
    unregister_cleanup_handlers,
)

def test_something():
    # Setup
    register_cleanup_handlers()

    # Test code...

    # Teardown
    unregister_cleanup_handlers()
```

## Signal Handler Flow

```
1. Application Startup
   ├─ Host app sets signal handlers (optional)
   ├─ Foundation registers cleanup
   │  ├─ manage_signals=True  → Saves & replaces handlers
   │  └─ manage_signals=False → Preserves existing handlers
   └─ Application runs

2. Signal Received (SIGINT/SIGTERM)
   ├─ manage_signals=True  → Foundation handler runs
   │  ├─ Logs signal
   │  ├─ Runs cleanup (flushes logs, cleans components)
   │  ├─ **Restores original handlers**
   │  └─ Exits
   └─ manage_signals=False → Host handler runs
       └─ atexit eventually calls Foundation cleanup

3. Normal Exit
   ├─ atexit triggers
   ├─ Foundation cleanup runs
   │  ├─ Flushes logs
   │  ├─ Cleans components
   │  └─ **Restores original handlers**
   └─ Program exits
```

## Best Practices

### ✅ DO

- Use `manage_signals=False` when integrating Foundation into existing applications
- Let automatic restoration handle cleanup
- Test signal handling in integration tests

### ❌ DON'T

- Don't manually restore handlers in production code (it's automatic)
- Don't call `unregister_cleanup_handlers()` outside of tests
- Don't assume Foundation's handlers will remain active after exit

## API Reference

### `register_cleanup_handlers(*, manage_signals: bool = True)`

Register Foundation's cleanup handlers.

**Parameters:**
- `manage_signals` (bool): If True, manage SIGINT/SIGTERM. If False, only register atexit cleanup.

**Default:** `True` (signal management enabled)

### `unregister_cleanup_handlers()`

Unregister handlers and restore originals (primarily for testing).

**Note:** Not needed in production - handlers restore automatically.

## Troubleshooting

### "My application's signal handler isn't being called"

**Solution:** Use `manage_signals=False`:
```python
register_cleanup_handlers(manage_signals=False)
```

### "Signal handlers aren't restored after Foundation exits"

**Check:** This should never happen - restoration is automatic. If you're seeing this, please file a bug report with reproduction steps.

### "Tests are interfering with each other"

**Solution:** Call `unregister_cleanup_handlers()` in teardown:
```python
def teardown_method(self):
    unregister_cleanup_handlers()
```
