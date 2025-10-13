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

The output will be a structured log message containing an `exception` field with the full traceback.

## Using `logger.error()` with `exc_info`

For more control, you can use `logger.error()` and pass `exc_info=True` to include the traceback.

```python
try:
    risky_operation()
except Exception as e:
    logger.error("Operation failed", exc_info=True, error_details=str(e))
```

To log an error *without* the traceback, simply omit `exc_info=True`. This is useful for expected errors where a stack trace is unnecessary.

```python
# From: examples/production/02_error_handling.py
from provide.foundation.errors import ValidationError

def fetch_user_profile(user_id: str):
    if user_id == "invalid":
        # This is an expected validation error, no traceback needed.
        logger.warning("Invalid user ID provided", user_id=user_id)
        raise ValidationError(f"Invalid user ID: {user_id}")
    # ...
```
