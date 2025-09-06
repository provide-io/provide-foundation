# Logger API

The `provide.foundation.logger` module provides structured logging with emoji-enhanced visual parsing, built on `structlog` with zero configuration required.

## Overview

The logger system provides:
- **Global Logger Instance** - Ready-to-use logger with structured output
- **Factory Functions** - Create named/scoped loggers
- **Configuration** - Telemetry and logging configuration classes
- **Emoji System** - Visual log parsing with semantic emoji prefixes
- **Performance** - High-performance logging (>14,000 msg/sec)
- **Thread Safety** - Async-compatible with thread safety

## Quick Start

```python
from provide.foundation import logger

# Simple logging
logger.info("Application started", version="1.0.0")
logger.warning("Low memory", available_mb=128)
logger.error("Database connection failed", host="localhost", retry=3)

# With context binding
user_logger = logger.bind(user_id="user123", session="sess456")
user_logger.info("User action", action="login", ip="192.168.1.1")
```

## Core API

### Global Logger Instance

#### `logger`

The global logger instance - primary interface for application logging.

```python
from provide.foundation import logger

# Standard log levels
logger.trace("Detailed execution flow")  # Most verbose
logger.debug("Debug information")
logger.info("General information") 
logger.warning("Warning conditions")
logger.error("Error conditions")
logger.critical("Critical conditions")  # Least verbose

# Exception logging with automatic traceback
try:
    result = 1 / 0
except Exception:
    logger.exception("Calculation failed", operation="division")
```

#### Context Binding

Create contextual loggers that include additional fields in all messages:

```python
# Bind context for request processing
request_logger = logger.bind(
    request_id="req-123",
    user_id="user-456", 
    endpoint="/api/users"
)

request_logger.info("Processing request")
request_logger.info("Query completed", rows=42, duration_ms=150)
# All messages include request_id, user_id, endpoint
```

### Factory Functions

#### `get_logger(name=None)`

Create named logger instances for modules or components.

**Parameters:**
- `name` (str, optional): Logger name (defaults to caller module)

**Returns:** Logger instance

```python
from provide.foundation import get_logger

# Module-specific logger
module_logger = get_logger("database")
module_logger.info("Connection established")

# Auto-named from module
logger = get_logger()  # Uses __name__ of calling module
```

#### `setup_logging(config=None)`

Configure logging system with custom settings.

**Parameters:**
- `config` (LoggingConfig, optional): Logging configuration

```python
from provide.foundation import setup_logging, LoggingConfig

# Custom configuration
config = LoggingConfig(
    level="DEBUG",
    console_formatter="json",
    log_file="app.log",
    omit_timestamp=False
)
setup_logging(config)
```

## Configuration Classes

### `LoggingConfig`

Configuration for logging behavior and output formatting.

```python
from provide.foundation import LoggingConfig

config = LoggingConfig(
    level="INFO",                    # Minimum log level
    console_formatter="key_value",   # Output format: key_value | json
    omit_timestamp=False,           # Include timestamps in console
    log_file=None,                  # Optional file logging
    module_levels={}                # Per-module log levels
)
```

**Attributes:**
- `level` (str): Minimum log level ("TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
- `console_formatter` (str): Console output format ("key_value" or "json")
- `omit_timestamp` (bool): Remove timestamps from console output
- `log_file` (str | Path, optional): Path to log file
- `module_levels` (dict[str, str]): Per-module log level overrides

### `TelemetryConfig`

Higher-level telemetry configuration including service identification.

```python
from provide.foundation import TelemetryConfig

config = TelemetryConfig(
    service_name="my-service",      # Service identifier in logs
    environment="production",       # Environment (dev/staging/prod)
    debug=False,                   # Enable debug mode
    logging=LoggingConfig(          # Nested logging config
        level="INFO",
        log_file="/var/log/service.log"
    )
)
```

**Attributes:**
- `service_name` (str, optional): Service name included in all logs
- `environment` (str): Deployment environment
- `debug` (bool): Debug mode flag
- `logging` (LoggingConfig): Logging-specific configuration

## Environment Configuration

All configuration can be controlled through environment variables:

| Variable | Description | Default |
|----------|-------------|---------||
| `PROVIDE_SERVICE_NAME` | Service identifier in logs | `None` |
| `PROVIDE_LOG_LEVEL` | Minimum log level | `DEBUG` |
| `PROVIDE_LOG_CONSOLE_FORMATTER` | Output format | `key_value` |
| `PROVIDE_LOG_OMIT_TIMESTAMP` | Remove timestamps | `false` |
| `PROVIDE_LOG_FILE` | Log to file path | `None` |
| `PROVIDE_LOG_MODULE_LEVELS` | Per-module levels | `""` |
| `PROVIDE_ENV` | Environment name | `dev` |
| `PROVIDE_DEBUG` | Enable debug mode | `false` |

```python
import os
from provide.foundation import setup_telemetry

# Configure via environment
os.environ["PROVIDE_SERVICE_NAME"] = "web-api"
os.environ["PROVIDE_LOG_LEVEL"] = "INFO" 
os.environ["PROVIDE_LOG_FILE"] = "/var/log/api.log"

setup_telemetry()  # Uses environment configuration
```

## Emoji System

### Visual Log Parsing

The logger uses emoji prefixes to provide immediate visual context:

```
[▶️] Application started version=1.0.0
[⚠️] Low memory available_mb=128  
[🔥] Database connection failed host=localhost retry=3
```

### Emoji Configuration

#### `show_emoji_matrix()`

Display available emoji mappings for different domains.

```python
from provide.foundation import show_emoji_matrix

show_emoji_matrix()
# Displays table of emoji mappings for different contexts
```

## Output Formats

### Key-Value Format (Default)

Human-readable format for development and debugging:

```
[▶️] User login successful user_id=user123 session_id=sess456 ip=192.168.1.1 duration_ms=45
[⚠️] Rate limit approaching user_id=user123 requests_count=95 limit=100 window_minutes=60
[🔥] Database timeout database=users operation=SELECT timeout_seconds=30 retry_count=3
```

### JSON Format

Machine-readable format for production log analysis:

```json
{"timestamp": "2024-01-15T10:30:45.123Z", "level": "info", "message": "User login successful", "user_id": "user123", "session_id": "sess456", "ip": "192.168.1.1", "duration_ms": 45}
```

Configure JSON output:

```python
from provide.foundation import LoggingConfig, setup_logging

config = LoggingConfig(console_formatter="json")
setup_logging(config)
```

## Best Practices

### 1. Use Structured Fields

```python
# Good: Structured data for analysis
logger.info("order_processed", 
           order_id="ord-123",
           user_id="user-456", 
           amount=99.99,
           items_count=3)

# Avoid: Unstructured messages
logger.info("Order ord-123 processed for user-456 with 3 items totaling $99.99")
```

### 2. Consistent Field Naming

```python
# Use consistent field names across your application
logger.info("request_received", request_id="req-123", user_id="user-456")
logger.info("request_completed", request_id="req-123", user_id="user-456", duration_ms=150)
```

### 3. Contextual Binding

```python
# Bind context early in request/operation lifecycle
request_logger = logger.bind(
    request_id=generate_request_id(),
    user_id=get_current_user_id(),
    operation="user_update"
)

# Use throughout operation
request_logger.info("Validation started")
request_logger.info("Database query completed", rows=1)
request_logger.info("Operation successful")
```

## See Also

- [Base Logger](base.md) - Core logger implementation
- [Configuration](config.md) - Configuration details
- [Processors](processors.md) - Log processing pipeline
- [Emoji Matrix](emoji.md) - Emoji mapping system
- [User Guide: Logging](../../guide/logging/index.md) - Usage patterns