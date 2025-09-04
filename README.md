# provide.foundation

**Beautiful, Performant, Structured Logging for Python**

<p align="center">
    <a href="https://pypi.org/project/provide-foundation/">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/provide-foundation.svg">
    </a>
    <a href="https://github.com/provide-io/provide-foundation/actions/workflows/ci.yml">
        <img alt="CI Status" src="https://github.com/provide-io/provide-foundation/actions/workflows/ci.yml/badge.svg">
    </a>
    <a href="https://codecov.io/gh/provide-io/provide-foundation">
        <img src="https://codecov.io/gh/provide-io/provide-foundation/branch/main/graph/badge.svg"/>
    </a>
    <a href="https://github.com/provide-io/provide-foundation/blob/main/LICENSE">
        <img alt="License" src="https://img.shields.io/github/license/provide-io/provide-foundation.svg">
    </a>
</p>

---

**provide.foundation** is a Python telemetry library built on `structlog` that delivers beautiful, performant, and structured logging with zero configuration. Transform your logs from walls of text into instantly scannable, machine-readable output that enhances debugging and monitoring in production applications.

---

## Installation

```bash
# Using uv (recommended)
uv pip install provide-foundation

# Using pip
pip install provide-foundation
```

---

## Quick Start

Get started in seconds with zero configuration:

```python
from provide.foundation import logger

# Start logging immediately - no setup required
logger.info("Application starting")

# Add structured context to any log
logger.info("User logged in", user_id=123, source="oauth")

# Automatic error handling with context
try:
    result = process_payment()
except Exception as e:
    logger.exception("Payment failed", order_id=456, amount=99.99)
```

**Output:**
```
2025-01-15 10:30:45 [info     ] Application starting
2025-01-15 10:30:46 [info     ] User logged in              user_id=123 source=oauth
2025-01-15 10:30:47 [error    ] Payment failed              order_id=456 amount=99.99
```

---

## Core Features

### Zero Configuration
Works immediately upon import with sensible defaults. No boilerplate, no setup functions, just import and log.

### Structured Logging
Every log entry is structured data, making it searchable, filterable, and aggregatable in production:

```python
# Instead of string interpolation...
logger.info(f"Processing order {order_id} for user {user_id}")

# Use structured fields
logger.info("Order processed", order_id=order_id, user_id=user_id)
```

### High Performance
Benchmarked at 14,000+ messages/second with full semantic processing. Thread-safe and async-ready for production workloads.

### Visual Clarity
Smart emoji prefixes and color coding make logs instantly scannable during development while remaining clean in production.

---

## Configuration

### Environment Variables

Configure logging behavior without touching code:

#### Core Settings (FOUNDATION_*)

| Variable | Description | Default |
|----------|-------------|---------|
| `FOUNDATION_SERVICE_NAME` | Service identifier in logs | `None` |
| `FOUNDATION_LOG_LEVEL` | Minimum log level | `DEBUG` |
| `FOUNDATION_LOG_CONSOLE_FORMATTER` | Output format (`key_value` or `json`) | `key_value` |
| `FOUNDATION_LOG_OMIT_TIMESTAMP` | Remove timestamps from console output | `false` |
| `FOUNDATION_LOG_ENABLED_EMOJI_SETS` | Comma-separated emoji sets | `""` |

#### CLI Settings (PROVIDE_*)

When using CLI decorators:

| Variable | Description | Default |
|----------|-------------|---------|
| `PROVIDE_LOG_LEVEL` | Override log level for CLI commands | - |
| `PROVIDE_LOG_FORMAT` | CLI output format | `key_value` |
| `PROVIDE_JSON_OUTPUT` | Force JSON output | `false` |
| `PROVIDE_NO_COLOR` | Disable colored output | `false` |

### Programmatic Configuration

For more control, configure programmatically at startup:

```python
from provide.foundation import setup_telemetry, TelemetryConfig, LoggingConfig

config = TelemetryConfig(
    service_name="api-gateway",
    logging=LoggingConfig(
        default_level="INFO",
        console_formatter="json",
        module_levels={
            "noisy.library": "WARNING",
            "critical.module": "DEBUG",
        }
    )
)

setup_telemetry(config)
```

---

## Advanced Features

### Named Loggers

Create module-specific loggers with automatic namespacing:

```python
from provide.foundation import logger

# Create named loggers for different components
db_logger = logger.get_logger("database")
api_logger = logger.get_logger("api.auth")
cache_logger = logger.get_logger("cache")

# Each logger maintains its own context
db_logger.info("Connection established", pool_size=10)
api_logger.warning("Rate limit approaching", remaining=50)
cache_logger.debug("Cache miss", key="user:123")
```

### Context Binding

Attach persistent context to loggers:

```python
# Create a logger with bound context
request_logger = logger.bind(
    request_id="req-123",
    user_id="user-456",
    ip_address="192.168.1.1"
)

# All logs from this logger include the bound context
request_logger.info("Processing request")
request_logger.info("Request completed", status_code=200)
```

### Timing Utilities

Profile code execution with the `timed_block` context manager:

```python
from provide.foundation import logger, timed_block

# Automatically logs duration and success/failure
with timed_block(logger, "database_query", query="SELECT * FROM users"):
    results = db.execute(query)
    
# Handles exceptions gracefully
try:
    with timed_block(logger, "external_api_call", endpoint="/api/v1/data"):
        response = requests.get(url)
except RequestException:
    pass  # Error logged automatically
```

### Semantic Layers

Define domain-specific logging conventions with semantic layers:

```python
# Enable semantic layers for better context
from provide.foundation import setup_telemetry, TelemetryConfig, LoggingConfig

config = TelemetryConfig(
    logging=LoggingConfig(
        enabled_emoji_sets=["http", "database", "llm"]
    )
)
setup_telemetry(config)

# Log with semantic context
logger.info(
    "API request",
    **{
        "http.method": "POST",
        "http.status_code": 201,
        "http.path": "/api/users",
        "http.duration_ms": 145
    }
)
```

### Error Handling Decorators

Simplify error handling with built-in decorators:

```python
from provide.foundation import retry_on_error, with_error_handling

@retry_on_error(max_attempts=3, delay=1.0)
def flaky_network_call():
    return api.fetch_data()

@with_error_handling(fallback=None, log_errors=True)
def parse_user_input(data):
    return json.loads(data)
```

---

## Integration Examples

### Flask Integration

```python
from flask import Flask, g
from provide.foundation import logger

app = Flask(__name__)

@app.before_request
def before_request():
    g.request_logger = logger.bind(
        request_id=generate_request_id(),
        path=request.path,
        method=request.method
    )
    g.request_logger.info("Request started")

@app.after_request
def after_request(response):
    g.request_logger.info("Request completed", status_code=response.status_code)
    return response
```

### AsyncIO Support

```python
import asyncio
from provide.foundation import logger

async def process_item(item_id):
    task_logger = logger.bind(task_id=item_id)
    task_logger.info("Processing started")
    
    try:
        result = await async_operation(item_id)
        task_logger.info("Processing completed", result=result)
    except Exception as e:
        task_logger.exception("Processing failed")
```

### Testing Support

```python
import pytest
from provide.foundation import logger

@pytest.fixture
def test_logger(caplog):
    """Fixture for testing with structured logs"""
    with caplog.at_level("DEBUG"):
        yield logger.bind(test_run=True)
```

---

## Performance Considerations

### Lazy Evaluation

The logger uses lazy evaluation to minimize performance impact:

```python
# Expensive operations are only evaluated if the log level is active
logger.debug("Query result", result=expensive_calculation())  # Only runs if DEBUG is enabled
```

### Async-Safe Operations

All logging operations are thread-safe and async-safe, suitable for concurrent applications without additional synchronization.

---

## Migration Guide

### From Python's logging module

```python
# Before (standard logging)
import logging
logging.info("User %s logged in from %s", user_id, ip_address)

# After (provide.foundation)
from provide.foundation import logger
logger.info("User logged in", user_id=user_id, ip_address=ip_address)
```

### From print statements

```python
# Before
print(f"DEBUG: Processing {len(items)} items")

# After
logger.debug("Processing items", item_count=len(items))
```

---

## Contributing

We welcome contributions! Please see:
- [DEVELOPMENT.md](DEVELOPMENT.md) - Development setup and guidelines
- [CLAUDE.md](CLAUDE.md) - AI assistant integration notes
- [GitHub Issues](https://github.com/provide-io/provide-foundation/issues) - Bug reports and feature requests

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built by <a href="https://provide.io">Provide</a>
</p>