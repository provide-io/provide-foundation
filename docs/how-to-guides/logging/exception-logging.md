# How to Log Exceptions

Properly logging exceptions is crucial for debugging. `provide.foundation` provides simple and powerful ways to capture error context.

## Using `logger.exception()`

The `logger.exception()` method is the preferred way to log exceptions. It should be called from within an `except` block. It automatically captures the full stack trace and adds it to the structured log record.

```python
from provide.foundation import logger

def process_data(data):
    try:
        # A risky operation
        key = data["required_key"]
        result = 100 / int(key)
        return result
    except KeyError as e:
        # This will log the error message AND the full traceback
        logger.exception(
            "processing_failed_missing_key",
            error_details=str(e),
            data_preview=str(data)[:50] # Add relevant context
        )
        # It's good practice to re-raise the exception or handle it
        raise
    except ZeroDivisionError:
        logger.exception("processing_failed_division_error")
        raise
```

The output will be a structured log message containing an `exception` field with the full traceback, making it easy for monitoring systems to parse and for developers to debug.

## Using `logger.error()` with `exc_info`

If you need more control, you can use `logger.error()` and pass `exc_info=True`. This has the same effect as `logger.exception()`.

```python
try:
    risky_operation()
except Exception as e:
    # Log the error with the traceback
    logger.error("operation_failed", exc_info=True, error_details=str(e))
```

You can also explicitly log an error *without* the traceback by setting `exc_info=False` or simply omitting it. This is useful for expected errors where a full stack trace is just noise.

```python
def find_user(user_id):
    user = db.get_user(user_id)
    if not user:
        # This is an expected condition, no need for a full traceback.
        logger.warning("user_not_found", user_id=user_id, exc_info=False)
        return None
    return user
```
