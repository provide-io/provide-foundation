# 🧑‍💻 Guides

## Exception Logging Best Practices

Effective exception logging is one of the most critical aspects of building a maintainable and debuggable application. `provide.foundation` provides powerful tools to ensure your error logs are rich with context and easy to analyze.

### Use `logger.exception()`

!!! tip "The Golden Rule of Exception Logging"
    Whenever you are logging inside an `except` block, you should always use `logger.exception()`. This method works just like `logger.error()`, but with one crucial difference: **it automatically captures the current exception's traceback** and attaches it to the log record.

Without the traceback, it is nearly impossible to pinpoint the exact line of code that caused the error. Using `logger.exception()` ensures this vital information is never lost.

```python
from provide.foundation import logger

try:
    result = 1 / 0
except ZeroDivisionError as e:
    # Using .exception() automatically includes the traceback
    logger.exception(
        "Failed to perform calculation",
        operation="division",
        error_type=type(e).__name__,
    )
```

### Adding Rich Context to Errors

When an error occurs, context is king. To debug effectively, you need to know not just *what* happened, but also the state of the system *when* it happened. Because `provide.foundation` is a structured logger, adding this context is simple and clean.

**What to include in your error logs:**

*   **Identifiers**: Any relevant IDs, such as `user_id`, `request_id`, or `transaction_id`.
*   **Parameters**: The inputs to the function or operation that failed.
*   **State**: Any relevant state variables that could have influenced the failure.

```python
def process_payment(user_id: str, amount: float, card_token: str):
    try:
        response = make_payment_request(amount, card_token)
        response.raise_for_status()
    except Exception as e:
        logger.exception(
            "Payment processing failed",
            user_id=user_id,
            payment_amount=amount,
            card_token_prefix=f"{card_token[:4]}...",
            error_message=str(e),
        )
        return False
    return True
```

!!! danger "Never Log Raw Secrets"
    In the example above, note that we are logging `card_token_prefix` and not the raw `card_token`. Never include sensitive data like passwords, API keys, or full credit card information in your logs. Always redact, truncate, or omit them entirely.

### Using `timed_block` for Errors and Duration

The [`timed_block`](../api-reference/utils.md#timed_block) utility is an elegant way to automatically log the duration and outcome of a piece of code. When an exception occurs within its context, it automatically logs an `error`-level event with the exception details and then re-raises the exception.

```python
from provide.foundation import logger, timed_block

def risky_database_update(user_id: str):
    with timed_block(logger, "database_update", initial_kvs={"db_table": "users", "user_id": user_id}):
        # This might raise a ConnectionError
        execute_db_update(f"UPDATE users SET ... WHERE id = '{user_id}'")

try:
    risky_database_update("usr_123")
except Exception:
    # The error is already logged by timed_block, so here we can just
    # perform any necessary cleanup or user-facing error handling.
    pass
```

If an exception occurs, `timed_block` provides a single, powerful log message with the what, why, when, and how long of the failure:

`[🔥] database_update failed db_table=users user_id=usr_123 duration_seconds=0.005 error='Connection refused' error_type=ConnectionError exc_info=...`

### Advanced Error Handling

`provide.foundation` also includes a comprehensive system for creating and managing your own structured error classes. For a deeper dive, please refer to the existing, detailed documentation:

*   [**Foundation Error Handling System**](../foundation-errors.md)
*   [**Error Context Patterns**](../error-context-patterns.md)

---

Next, learn how to optimize the logger for high-throughput environments in the [**Performance Tuning**](./performance-tuning.md) guide.
