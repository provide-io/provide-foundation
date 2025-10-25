# How to Log Exceptions

Properly logging exceptions is crucial for debugging. `provide.foundation` provides simple and powerful ways to capture error context.

## Using `logger.exception()`

The `logger.exception()` method is the preferred way to log exceptions. It should be called from within an `except` block and automatically captures the full stack trace.

```python
# From: examples/telemetry/05_exception_handling.py
def risky_operation():
    raise ValueError("Something went wrong")

try:
    risky_operation()
except Exception:
    logger.exception(
        "Operation failed unexpectedly",
        operation_name="risky_operation",
        user_id="user_xyz",
    )
```

## Using `logger.error()` with `exc_info`

For more control, you can use `logger.error()` and pass `exc_info=True` to include the traceback.

```python
try:
    risky_operation()
except Exception as e:
    logger.error("Operation failed", exc_info=True, error_details=str(e))
```

## Next Steps

### Related Guides
- **[Basic Logging](basic-logging.md)**: Core logging patterns
- **[Structured Events](structured-events.md)**: Event-driven logging

### Error Handling & Resilience
- **[Retry Patterns](../resilience/retry.md)**: Automatically retry failed operations
- **[Production Error Handling](../production/monitoring.md)**: Production-ready error handling

### Examples
- See `examples/telemetry/05_exception_handling.py` for comprehensive exception logging examples
- See `examples/production/02_error_handling.py` for production error patterns
