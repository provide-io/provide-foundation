# 📚 API Reference

## Utilities API

This document provides a reference for utility functions available in `provide.foundation`.

### `timed_block`

A powerful context manager to log the duration and outcome of a block of code. It automatically captures the start time, executes the wrapped code block, and then logs a single, rich event with the duration, outcome, and any exception details.

```python
@contextmanager
def timed_block(
    logger_instance: "FoundationLogger",
    event_name: str,
    layer_keys: dict[str, Any] | None = None,
    initial_kvs: dict[str, Any] | None = None,
    **extra_kvs: Any,
) -> Generator[dict[str, Any], None, None]:
```

*   **Parameters**:
    *   `logger_instance` (`FoundationLogger`): The logger instance to use for logging the final event (usually the global `logger`).
    *   `event_name` (`str`): A descriptive name for the event or operation being timed. This will be the main log message.
    *   `layer_keys` (`dict` | `None`): An optional dictionary of pre-defined semantic keys that are relevant to any active telemetry layers.
    *   `initial_kvs` (`dict` | `None`): An optional dictionary of key-value pairs to include in the log entry from the start.
    *   `**extra_kvs` (`Any`): Additional key-value pairs to include in the log entry.

*   **Yields**:
    *   A mutable dictionary that can be updated from within the `with` block to add more context to the final log message.

*   **Behavior**:
    *   **On Success**: If the block completes without an exception, it logs an `info`-level event with the final context and the total `duration_seconds`.
    *   **On Failure**: If an exception is raised, it logs an `error`-level event with the context, `duration_seconds`, and automatically captures the exception details under `error` and `error_type`. The original exception is then re-raised.

**Example:**

```python
from provide.foundation import logger, timed_block
import time

with timed_block(logger, "database_query", db_table="users") as ctx:
    ctx["query_type"] = "select" # Add context from within the block
    time.sleep(0.1) # Simulate work
    ctx["rows_returned"] = 50

# Logs: [info] database_query completed db_table=users query_type=select rows_returned=50 duration_seconds=0.1
```

---

Next, learn about the error handling system in the [**Errors API**](./errors.md).