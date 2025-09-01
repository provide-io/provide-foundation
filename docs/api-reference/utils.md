# 📚 API Reference

## Utilities API

This document provides a reference for utility functions available in `provide.foundation`.

### `timed_block`

A powerful context manager to log the duration and outcome of a block of code. It automatically captures the start time, executes the wrapped code block, and then logs a single, rich event with the duration, outcome (`success` or `error`), and any exception details.

```python
@contextmanager
def timed_block(
    logger_instance: "FoundationLogger",
    event_name: str,
    layer_keys: dict[str, Any] | None = None,
    **initial_kvs: Any
) -> Generator[None, None, None]:
```

*   **Parameters**:
    *   `logger_instance` (`FoundationLogger`): The logger instance to use for logging the final event (usually the global `logger`).
    *   `event_name` (`str`): A descriptive name for the event or operation being timed. This will be the main log message.
    *   `layer_keys` (`dict` | `None`): An optional dictionary of pre-defined semantic keys that are relevant to any active telemetry layers (e.g., `{"llm.task": "generation"}`). These are merged with `initial_kvs`.
    *   `**initial_kvs` (`Any`): Additional key-value pairs to include in the log entry from the start of the block.

*   **Behavior**:
    *   **On Success**: If the block completes without an exception, it logs an `info`-level event with `outcome="success"` and the total `duration_ms`.
    *   **On Failure**: If an exception is raised within the block, it logs an `error`-level event with `outcome="error"`, the `duration_ms`, and automatically captures the exception details under `error.message` and `error.type`. The original exception is then re-raised, so you can still handle it with a standard `try...except` block.

**Example:**

```python
from provide.foundation import logger, timed_block
import time

# Example 1: Successful operation
with timed_block(logger, "database_query", db_table="users", query_type="select"):
    time.sleep(0.1) # Simulate work
# Logs: [info] database_query db_table=users query_type=select outcome=success duration_ms=100.23

# Example 2: Failing operation
try:
    with timed_block(logger, "payment_processing", transaction_id="txn_123"):
        raise RuntimeError("Credit card declined")
except RuntimeError:
    # The exception is already logged by timed_block, so we can pass or handle it quietly.
    pass
# Logs: [error] payment_processing transaction_id=txn_123 outcome=error error.message='Credit card declined' error.type=RuntimeError duration_ms=0.45
```

---

Next, learn about the error handling system in the [**Errors API**](./errors.md).
