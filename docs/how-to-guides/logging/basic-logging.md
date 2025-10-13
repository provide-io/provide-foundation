# How to Perform Basic Logging

This guide covers the fundamental patterns for logging in a `provide.foundation` application.

## Logging at Different Severity Levels

The global `logger` instance provides methods for each standard log level.

```python
# From: examples/telemetry/01_basic_logging.py
from provide.foundation import logger, setup_telemetry

setup_telemetry()

logger.debug("Diagnostic information for developers.")
logger.info("A general informational message about application state.")
logger.warning("Something unexpected happened, but the app can continue.")
logger.error("A serious error occurred; an operation failed.")
```

## Adding Structured Data (Context)

Pass contextual information as keyword arguments. This is the core of structured logging.

```python
# From: examples/telemetry/01_basic_logging.py
logger.info(
    "User session started",
    user_id="user_123",
    session_id="sess_456",
    source="web_app",
)
```

## Using Named Loggers

For better organization, create named loggers for different components. This helps identify the source of a log and allows for module-specific log level filtering.

```python
# From: examples/telemetry/03_named_loggers.py
from provide.foundation import logger

auth_logger = logger.get_logger("auth.service")
db_logger = logger.get_logger("database.connection")

auth_logger.info("User login successful", user_id="user123")
db_logger.info("Connection pool initialized", pool_size=20)
```

## Binding Context to a Logger

Use `bind()` to create a new logger instance with context that will be included in all its subsequent log messages.

```python
# From: examples/production/02_error_handling.py (conceptual)
def handle_request(request_id: str, user_id: str):
    request_logger = logger.bind(request_id=request_id, user_id=user_id)

    request_logger.info("request_started")
    # ... do some work ...
    request_logger.info("request_completed", status_code=200)
```
