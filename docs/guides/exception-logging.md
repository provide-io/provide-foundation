# 🧑‍💻 Guides

## Exception Logging Best Practices

Effective exception logging is one of the most critical aspects of building a maintainable and debuggable application. `provide.foundation` provides powerful tools to ensure your error logs are rich with context and easy to analyze.

### The Golden Rule: Use `logger.exception()`

Whenever you are logging inside an `except` block, you should always use `logger.exception()`. This method works just like `logger.error()`, but with one crucial difference: it automatically captures the current exception's traceback and attaches it to the log record.

**Example:**

```python
from provide.foundation import logger

try:
    # A risky operation that might fail
    result = 1 / 0
except ZeroDivisionError as e:
    # Using .exception() automatically includes the traceback
    logger.exception(
        "Failed to perform calculation",
        operation="division",
        dividend=1,
        divisor=0,
        error_type=type(e).__name__,
    )
```

**Output:**

```
[🔥] Failed to perform calculation operation=division dividend=1 divisor=0 error_type=ZeroDivisionError exc_info=... # Full traceback follows
```

Without the traceback, it would be nearly impossible to pinpoint the exact line of code that caused the error. Using `logger.exception()` ensures this vital information is never lost.

### Adding Rich Context to Errors

When an error occurs, context is king. To debug effectively, you need to know not just *what* happened, but also the state of the system *when* it happened. Because `provide.foundation` is a structured logger, adding this context is simple and clean.

**What to include in your error logs:**

*   **Identifiers**: Any relevant IDs, such as `user_id`, `request_id`, `transaction_id`, or `order_id`.
*   **Parameters**: The inputs to the function or operation that failed.
*   **State**: Any relevant state variables that could have influenced the failure.
*   **Attempt/Retry Counts**: If the operation is part of a retry loop.

**Example:**

```python
def process_payment(user_id: str, amount: float, card_token: str):
    try:
        # Imagine an API call to a payment gateway
        response = make_payment_request(amount, card_token)
        response.raise_for_status() # Raise an exception for non-2xx responses
    except Exception as e:
        logger.exception(
            "Payment processing failed",
            # Rich context for debugging
            user_id=user_id,
            payment_amount=amount,
            card_token_prefix=f"{card_token[:4]}...", # Avoid logging full secrets
            error_message=str(e),
        )
        return False
    return True
```

This structured context allows you to easily search your log aggregation platform for all failed payments for a specific user, or to see if a particular error is correlated with a certain range of payment amounts.

### Using `timed_block` for Errors and Duration

The [`timed_block`](../api-reference/utils.md#timed_block) utility is an elegant way to automatically log the duration and outcome (success or error) of a piece of code. When an exception occurs within its context, it automatically logs an error-level event with the exception details.

**Example:**

```python
from provide.foundation import logger, timed_block

def risky_database_update(user_id: str):
    # timed_block will automatically log the error if one occurs
    with timed_block(logger, "database_update", db_table="users", user_id=user_id):
        # This might raise an exception (e.g., ConnectionError, IntegrityError)
        execute_db_update(f"UPDATE users SET last_login = NOW() WHERE id = '{user_id}'")

try:
    risky_database_update("usr_123")
except Exception:
    # The error is already logged by timed_block, so here we can just
    # perform any necessary cleanup or user-facing error handling.
    pass
```

If `execute_db_update` raises a `ConnectionError`, `timed_block` will catch it, log it, and then re-raise it. The resulting log message would look something like this:

```
[🔥] database_update db_table=users user_id=usr_123 outcome=error error.message='Connection refused' error.type=ConnectionError duration_ms=5.23
```

This single line tells you what failed, why it failed, how long it took before it failed, and all the relevant context.

### Advanced Error Handling

`provide.foundation` also includes a comprehensive system for creating and managing your own structured error classes. For a deeper dive into creating custom error types, defining error context, and using advanced handlers and decorators, please refer to the existing, detailed documentation:

*   [**Foundation Error Handling System**](../foundation-errors.md)
*   [**Error Context Patterns**](../error-context-patterns.md)

---

Next, learn how to optimize the logger for high-throughput environments in the [**Performance Tuning**](./performance-tuning.md) guide.
