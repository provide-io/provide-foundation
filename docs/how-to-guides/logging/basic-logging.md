# How to Perform Basic Logging

This guide covers the fundamental patterns for logging in a `provide.foundation` application. You'll learn how to log messages at different severity levels, add structured data for context, use emoji-enhanced logging, and configure logging for different environments.

## Quick Start

The simplest way to use Foundation's logger:

```python
# From: examples/telemetry/01_basic_logging.py
from provide.foundation import logger

# Logger auto-initializes on first use - no setup required!
logger.info("Application started")
```

That's it! No configuration files, no complex setup. The logger works out of the box with sensible defaults.

## Logging at Different Severity Levels

The global `logger` instance provides methods for each standard log level:

```python
from provide.foundation import logger

# DEBUG: Diagnostic information for developers
logger.debug("Cache lookup", key="user:123", hit=True)

# INFO: General informational messages (default level)
logger.info("User logged in", user_id="user_123")

# WARNING: Something unexpected happened, but app can continue
logger.warning("API rate limit approaching", current=95, limit=100)

# ERROR: A serious error occurred; an operation failed
logger.error("Failed to connect to database", error="ConnectionRefused")

# CRITICAL: A critical failure that may prevent the application from continuing
logger.critical("Out of memory", available_mb=50, required_mb=500)
```

## Adding Structured Data (Context)

Pass contextual information as keyword arguments. This is the core of **structured logging**:

```python
logger.info(
    "user_session_started",  # Event name
    user_id="user_123",       # Structured fields
    session_id="sess_456",
    source="web_app",
    ip_address="192.168.1.1"
)
```

### Why Structured Logging?

Traditional logging:
```python
# ❌ Hard to parse, search, and analyze
logging.info(f"User user_123 started session sess_456 from web_app")
```

Structured logging:
```python
# ✅ Easy to parse, search, filter, and aggregate
logger.info("session_started", user_id="user_123", session_id="sess_456", source="web_app")
```

Benefits:
- **Searchable**: Find all logs for `user_id="user_123"`
- **Aggregatable**: Count sessions by `source`
- **Analyzable**: Track patterns across fields
- **Machine-readable**: JSON output for log aggregation systems

## Event-Based Logging Pattern

Foundation encourages an **event-based** logging pattern:

```python
# Use event names as the first argument
logger.info("order_created", order_id="order_123", amount=99.99)
logger.info("payment_processed", order_id="order_123", method="credit_card")
logger.info("email_sent", order_id="order_123", recipient="user@example.com")
```

This creates a **timeline of events** that's easy to track and analyze.

### Domain-Action-Status Pattern

For complex operations, use the Domain-Action-Status pattern:

```python
# Domain: database | Action: connect | Status: (implied by log level)
logger.info("database_connect_started", host="localhost", port=5432)
logger.info("database_connect_success", connection_time_ms=150)

# Or explicitly:
logger.error("database_connect_failed", error="timeout", retry_count=3)
```

## Emoji-Enhanced Logging

Foundation supports **emoji prefixes** for visual log parsing (enabled by default in console output):

```python
logger.info("app_started", emoji="🚀")
logger.info("data_loaded", emoji="📊", records=1000)
logger.warning("cache_miss", emoji="⚠️", key="user:123")
logger.error("connection_failed", emoji="❌", service="database")
```

Output:
```
🚀 app_started
📊 data_loaded | records=1000
⚠️  cache_miss | key=user:123
❌ connection_failed | service=database
```

### Disable Emojis

```python
from provide.foundation import get_hub, LoggingConfig, TelemetryConfig

get_hub().initialize_foundation(
    TelemetryConfig(
        logging=LoggingConfig(
            logger_name_emoji_prefix_enabled=False,
            das_emoji_prefix_enabled=False,
        ),
    )
)
```

Or via environment variables:
```bash
export PROVIDE_LOG_LOGGER_NAME_EMOJI_ENABLED=false
export PROVIDE_LOG_DAS_EMOJI_ENABLED=false
```

## Using Named Loggers

For better organization, create named loggers for different components:

```python
# From: examples/telemetry/03_named_loggers.py
from provide.foundation import get_logger

# Create component-specific loggers
auth_logger = get_logger("auth.service")
db_logger = get_logger("database.connection")
api_logger = get_logger("api.handler")

# Each logger includes its name in the output
auth_logger.info("login_success", user_id="user123")
# Output: [auth.service] login_success | user_id=user123

db_logger.info("pool_initialized", pool_size=20)
# Output: [database.connection] pool_initialized | pool_size=20

api_logger.info("request_received", path="/api/users", method="GET")
# Output: [api.handler] request_received | path=/api/users | method=GET
```

### When to Use Named Loggers

- **Large applications**: Separate logs by module or component
- **Libraries**: Use your library name for namespacing
- **Microservices**: Identify which service component generated the log

## Binding Context to a Logger

Use `bind()` to create a logger instance with **persistent context**:

```python
def handle_request(request_id: str, user_id: str):
    # Create a logger with request-specific context
    request_logger = logger.bind(request_id=request_id, user_id=user_id)

    # All logs from this logger will include request_id and user_id
    request_logger.info("request_started")
    # Output: request_started | request_id=abc123 | user_id=user_456

    request_logger.info("database_query", table="users", duration_ms=45)
    # Output: database_query | request_id=abc123 | user_id=user_456 | table=users | duration_ms=45

    request_logger.info("request_completed", status_code=200)
    # Output: request_completed | request_id=abc123 | user_id=user_456 | status_code=200
```

This is extremely useful for:
- **Request tracing**: Track a request through your application
- **User context**: Include user information in all relevant logs
- **Transaction tracking**: Follow a database transaction
- **Distributed tracing**: Correlation IDs across services

## Configuration Options

### Console vs JSON Output

**Console** (default for development):
```python
from provide.foundation import get_hub, LoggingConfig, TelemetryConfig

config = TelemetryConfig(
    logging=LoggingConfig(
        console_formatter="key_value"
    )
)
get_hub().initialize_foundation(config)
```

Output:
```
2025-10-24 14:30:15 [INFO] user_login | user_id=user_123 | ip=192.168.1.1
```

**JSON** (recommended for production):
```python
from provide.foundation import get_hub, LoggingConfig, TelemetryConfig

config = TelemetryConfig(
    logging=LoggingConfig(
        console_formatter="json"
    )
)
get_hub().initialize_foundation(config)
```

Output:
```json
{"timestamp": "2025-10-24T14:30:15.123Z", "level": "info", "event": "user_login", "user_id": "user_123", "ip": "192.168.1.1"}
```

### Set Log Level

```python
# Via initialization
from provide.foundation import get_hub, LoggingConfig, TelemetryConfig

config = TelemetryConfig(
    logging=LoggingConfig(
        default_level="DEBUG"
    )
)
get_hub().initialize_foundation(config)

# Via environment variable
# export PROVIDE_LOG_LEVEL=DEBUG
```

Log levels (in order of severity):
1. **DEBUG**: Detailed diagnostic information
2. **INFO**: General informational messages (default)
3. **WARNING**: Warning messages
4. **ERROR**: Error messages
5. **CRITICAL**: Critical failures

### Module-Level Log Control

Control log levels for specific modules:

```python
from provide.foundation import get_hub, LoggingConfig, TelemetryConfig

config = TelemetryConfig(
    logging=LoggingConfig(
        default_level="INFO",  # Default level
        module_levels={
            "urllib3": "WARNING",      # Suppress urllib3 debug/info
            "asyncio": "INFO",          # Show asyncio info+
            "myapp.database": "DEBUG",  # Verbose logging for database module
        }
    )
)

get_hub().initialize_foundation(config)
```

Or via environment variable:
```bash
export PROVIDE_LOG_MODULE_LEVELS="urllib3:WARNING,asyncio:INFO,myapp.database:DEBUG"
```

## Logging Performance Metrics

Log performance metrics for operations:

```python
import time

def process_data(data_id: str):
    start_time = time.time()
    logger.info("processing_started", data_id=data_id)

    try:
        # Process data
        result = perform_processing(data_id)

        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            "processing_completed",
            data_id=data_id,
            duration_ms=round(duration_ms, 2),
            records_processed=len(result),
            emoji="✅"
        )
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.error(
            "processing_failed",
            data_id=data_id,
            duration_ms=round(duration_ms, 2),
            error=str(e),
            emoji="❌"
        )
        raise
```

## Logging Errors with Context

Always include context when logging errors:

```python
try:
    result = divide(a, b)
except ZeroDivisionError as e:
    logger.error(
        "division_error",
        numerator=a,
        denominator=b,
        error=str(e),
        error_type=type(e).__name__
    )
    raise
except Exception as e:
    logger.exception(  # Automatically includes stack trace
        "unexpected_error",
        operation="division",
        error=str(e)
    )
    raise
```

For more details on exception logging, see [Exception Logging](exception-logging.md).

## Best Practices

### ✅ DO: Use Event Names

```python
# ✅ Good: Clear event name
logger.info("user_registered", user_id="user_123", source="web")

# ❌ Bad: Generic message
logger.info("Something happened with user_123")
```

### ✅ DO: Include Context

```python
# ✅ Good: Rich context
logger.error("api_request_failed", endpoint="/users", status=500, duration_ms=1234)

# ❌ Bad: No context
logger.error("Request failed")
```

### ✅ DO: Use Consistent Field Names

```python
# ✅ Good: Consistent naming
logger.info("request_started", user_id="user_123", request_id="req_456")
logger.info("request_completed", user_id="user_123", request_id="req_456")

# ❌ Bad: Inconsistent naming
logger.info("request_started", user="user_123", req_id="req_456")
logger.info("request_completed", user_id="user_123", request_id="req_456")
```

### ✅ DO: Log at Appropriate Levels

```python
# ✅ Good: Appropriate levels
logger.debug("cache_lookup", key="user:123", hit=True)  # Diagnostic
logger.info("user_login", user_id="user_123")            # Informational
logger.warning("rate_limit_approached", usage=95)        # Warning
logger.error("database_connection_failed")                # Error

# ❌ Bad: Everything at INFO
logger.info("cache hit")        # Should be DEBUG
logger.info("CONNECTION FAILED")  # Should be ERROR
```

### ✅ DO: Use bind() for Request Context

```python
# ✅ Good: Bind request context
def handle_request(request_id):
    request_logger = logger.bind(request_id=request_id)
    request_logger.info("processing_started")
    request_logger.info("processing_completed")

# ❌ Bad: Repeat context everywhere
def handle_request(request_id):
    logger.info("processing_started", request_id=request_id)
    logger.info("processing_completed", request_id=request_id)
```

### ❌ DON'T: Log Sensitive Data

```python
# ❌ NEVER: Log passwords, tokens, credit cards
logger.info("user_login", password=user_password)  # DANGEROUS!

# ✅ Good: Mask or omit sensitive data
logger.info("user_login", user_id=user_id)  # Safe
```

### ❌ DON'T: Use String Formatting

```python
# ❌ Bad: String formatting loses structure
logger.info(f"User {user_id} logged in from {ip}")

# ✅ Good: Structured fields
logger.info("user_login", user_id=user_id, ip=ip)
```

## Common Patterns

### API Request Logging

```python
@app.route("/api/users/<user_id>")
def get_user(user_id):
    request_logger = logger.bind(
        request_id=request.headers.get("X-Request-ID"),
        endpoint="/api/users",
        method="GET",
        user_id=user_id
    )

    request_logger.info("api_request_received")

    try:
        user = database.get_user(user_id)
        request_logger.info("api_request_success", status=200)
        return jsonify(user), 200
    except UserNotFound:
        request_logger.warning("user_not_found", status=404)
        return jsonify({"error": "not found"}), 404
    except Exception as e:
        request_logger.error("api_request_failed", status=500, error=str(e))
        return jsonify({"error": "internal error"}), 500
```

### Background Task Logging

```python
def process_background_task(task_id, data):
    task_logger = logger.bind(task_id=task_id, task_type="data_processing")

    task_logger.info("task_started", records=len(data))

    processed = 0
    errors = 0

    for record in data:
        try:
            process_record(record)
            processed += 1
        except Exception as e:
            errors += 1
            task_logger.warning("record_processing_failed", record_id=record.id, error=str(e))

    task_logger.info(
        "task_completed",
        total=len(data),
        processed=processed,
        errors=errors,
        success_rate=round(processed / len(data) * 100, 2)
    )
```

### Database Operation Logging

```python
def execute_query(sql, params):
    query_logger = logger.bind(operation="database_query")

    start_time = time.time()
    query_logger.debug("query_started", sql=sql[:100])  # Truncate long queries

    try:
        result = database.execute(sql, params)
        duration_ms = (time.time() - start_time) * 1000

        query_logger.info(
            "query_completed",
            duration_ms=round(duration_ms, 2),
            rows_affected=result.rowcount
        )

        return result
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000

        query_logger.error(
            "query_failed",
            duration_ms=round(duration_ms, 2),
            error=str(e),
            error_type=type(e).__name__
        )
        raise
```

## Next Steps

### Related Logging Guides
- **[Exception Logging](exception-logging.md)**: Learn how to log exceptions with full context
- **[Structured Events](structured-events.md)**: Advanced patterns for event-driven logging
- **[Custom Processors](custom-processors.md)**: Extend logging with custom processors

### Integration & Production
- **[CLI Commands](../cli/commands.md)**: Use Foundation logging in CLI applications
- **[Production Patterns](../production/monitoring.md)**: Production logging best practices
- **[Configuration](../configuration/env-variables.md)**: Configure logging via environment variables

### Understanding Foundation
- **[Architecture](../../explanation/architecture.md)**: Understand how the logging system works

---

**Tip**: Start with simple `logger.info()` calls and add structure as your needs grow. Foundation makes it easy to evolve from basic to advanced logging patterns.
