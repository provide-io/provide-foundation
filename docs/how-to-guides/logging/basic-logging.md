# How to Perform Basic Logging

This guide covers the fundamental patterns for logging in a `provide.foundation` application.

## Logging at Different Severity Levels

The global `logger` instance provides methods for each standard log level.

```python
from provide.foundation import logger, setup_telemetry

# It's best practice to call this once at application startup.
setup_telemetry()

# In order of severity (least to most)
logger.debug("Detailed diagnostic information for developers.")
logger.info("A general informational message about application state.")
logger.warning("Something unexpected happened, but the app can continue.")
logger.error("A serious error occurred; an operation failed.")
logger.critical("A critical failure; the application may be unable to continue.")
```

## Adding Structured Data (Context)

The real power of `provide.foundation` comes from structured logging. Instead of embedding data in strings, pass it as keyword arguments.

#### Good Practice: Structured Data

```python
# ✅ Good: Structured data is searchable and machine-readable.
logger.info("user_login_successful",
    user_id="usr_123",
    email="user@example.com",
    ip_address="192.168.1.1",
)
```
**Output (pretty format):**
`INFO user_login_successful user_id=usr_123 email=user@example.com ip_address=192.168.1.1`

**Output (JSON format):**
`{"event": "user_login_successful", "user_id": "usr_123", ...}`

#### Bad Practice: String Formatting

```python
# ❌ Bad: Data is trapped in a string, making it hard to query.
user_id = "usr_123"
ip = "192.168.1.1"
logger.info(f"User {user_id} successfully logged in from {ip}.")
```

## Using Named Loggers

For better organization in larger applications, create named loggers for different components or modules. This helps you control log levels granularly and identify the source of a log message.

```python
from provide.foundation import get_logger

# Get loggers for different parts of your application
db_logger = get_logger("database")
api_logger = get_logger("api.handler")
auth_logger = get_logger("auth.service")

# These logs will have a 'logger_name' field in their structured output
db_logger.debug("query_executed", table="users", duration_ms=15)
api_logger.info("request_processed", endpoint="/api/users", status=200)
auth_logger.warning("invalid_token_attempt", client_ip="10.0.0.5")
```

## Binding Context to a Logger

If you need to add the same contextual information to many log messages, use `bind()` to create a new logger instance with that context pre-filled.

```python
# Original logger
from provide.foundation import logger

def handle_request(request_id: str, user_id: str):
    # Create a new logger with context bound for this specific request
    request_logger = logger.bind(request_id=request_id, user_id=user_id)

    request_logger.info("request_started")
    # ... do some work ...
    request_logger.debug("data_validated")
    # ... do more work ...
    request_logger.info("request_completed", status_code=200)

# All logs from request_logger will automatically include request_id and user_id.
# The original global `logger` remains unchanged.
```
