# 📚 API Reference

## Logger API

This document provides a detailed reference for the core logging interface of `provide.foundation`.

### The Global `logger` Instance

The primary entry point for all logging is the global `logger` instance.

```python
from provide.foundation import logger

logger: FoundationLogger
```

This is a pre-configured instance of the `FoundationLogger` class that is ready for immediate use. It is the recommended interface for most logging needs.

### `FoundationLogger` Class

This is the class that powers the global `logger` instance.

#### `get_logger(name: str | None = None)`

Creates or retrieves a named logger instance. Using named loggers is a best practice for applications with multiple components, as it allows you to easily identify the source of a log message and configure per-module log levels.

*   **Parameters**:
    *   `name` (str | None): A dot-separated name for the logger (e.g., `"api.v1.users"`). If `None`, the default logger is returned.
*   **Returns**: A `structlog` `BoundLogger` instance, ready for use.

**Example:**

```python
# Get a logger for a specific component
db_logger = logger.get_logger("database.connections")

# All messages from this logger will be associated with its name
db_logger.info("Connection pool initialized.")
```

#### Logging Methods

All logging methods on the `FoundationLogger` instance share a common signature.

```python
def <level>(self, event: str, *args: Any, **kwargs: Any) -> None:
```

*   **Parameters**:
    *   `event` (str): The main, human-readable log message. It can be a format string if `*args` are provided.
    *   `*args` (Any): If `event` is a format string, these arguments will be interpolated into it.
    *   `**kwargs` (Any): The structured context for the log event. These key-value pairs are the core of structured logging.

**Available Methods:**

*   `logger.debug(event, **context)`: For detailed, verbose information useful during development and troubleshooting.
*   `logger.info(event, **context)`: For informational messages that highlight the normal progress of an application.
*   `logger.warning(event, **context)`: For indicating a potential problem or an unexpected event that does not prevent the current operation from completing.
*   `logger.error(event, **context)`: For error conditions that failed the current operation but do not necessarily mean the entire application has failed.
*   `logger.critical(event, **context)`: For severe errors that may cause the entire application to terminate.
*   `logger.exception(event, **context)`: Should be called from within an `except` block. It has the same signature as `logger.error` but automatically captures and records the full exception traceback.

**Special `trace` Method:**

`provide.foundation` includes a `trace` method for ultra-verbose logging, even more detailed than `DEBUG`.

```python
def trace(self, event: str, *args: Any, **kwargs: Any) -> None:
```

This method is useful for tracing the execution flow within a complex function or for dumping large data structures for debugging purposes. The `TRACE` log level must be enabled via configuration to see these messages.

**Example of Different Levels:**

```python
logger.debug("Checking user permissions", user_id="usr_123", required_permission="admin")
logger.info("User authenticated successfully", user_id="usr_123")
logger.warning("API key is about to expire", key_id="key_abc", expiry_days=3)

try:
    1 / 0
except ZeroDivisionError:
    logger.exception("Calculation failed", operation="report_generation")

logger.critical("Could not connect to primary database. Shutting down.", db_host="prod.db")
```

---

Next, learn about the data classes used to configure the logger in the [**Configuration API**](./config.md).
