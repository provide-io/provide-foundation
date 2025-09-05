# Logger Factory Functions

Factory functions for creating and configuring loggers with simplified interfaces.

## Overview

The factories module provides convenience functions that wrap the core logger functionality with simpler, more user-friendly interfaces:

- **get_logger()**: Create named logger instances
- **setup_logging()**: Simple logging configuration for basic use cases

These functions are designed for quick setup and common usage patterns, abstracting away the complexity of the full configuration system.

## Usage Patterns

### Creating Named Loggers

```python
from provide.foundation.logger import get_logger

# Module-specific logger
log = get_logger(__name__)
log.info("Module initialized", module=__name__)

# Domain-specific logger  
db_log = get_logger("database")
db_log.debug("Connection established", host="localhost", port=5432)

# Service-specific logger
api_log = get_logger("api.auth")
api_log.info("User authenticated", user_id=12345, method="oauth2")
```

### Simple Logging Setup

```python
from provide.foundation.logger import setup_logging

# Basic development setup
setup_logging(level="DEBUG")

# Production JSON logging
setup_logging(
    level="INFO", 
    json_logs=True,
    log_file="/var/log/application.log"
)

# Custom configuration with additional options
setup_logging(
    level="WARNING",
    json_logs=False,
    enable_emoji=True,
    profile="production"
)
```

## Configuration Options

### Log Levels

Supported log level formats:

```python
# String levels (case insensitive)
setup_logging(level="DEBUG")    # Most verbose
setup_logging(level="INFO")     # Standard production  
setup_logging(level="WARNING")  # Warnings and errors only
setup_logging(level="ERROR")    # Errors only
setup_logging(level="CRITICAL") # Critical errors only

# Numeric levels (Python logging standard)
setup_logging(level=10)  # DEBUG
setup_logging(level=20)  # INFO
setup_logging(level=30)  # WARNING
setup_logging(level=40)  # ERROR
setup_logging(level=50)  # CRITICAL
```

### Output Formats

```python
# Human-readable key-value format (default)
setup_logging(json_logs=False)
# Output: timestamp=2024-01-15T10:30:45 level=INFO event=user_login user_id=123

# Structured JSON format
setup_logging(json_logs=True)  
# Output: {"timestamp":"2024-01-15T10:30:45","level":"INFO","event":"user_login","user_id":123}
```

### File Logging

```python
# Log to file in addition to console
setup_logging(log_file="/var/log/app.log")

# JSON logs to file for log aggregation
setup_logging(
    json_logs=True,
    log_file="/var/log/app.json"
)

# Structured logging directory
from pathlib import Path
setup_logging(log_file=Path("/var/log/myapp/application.log"))
```

## Advanced Configuration

The setup_logging function accepts additional configuration options via **kwargs:

```python
setup_logging(
    level="INFO",
    json_logs=True,
    log_file="/var/log/app.log",
    # Additional TelemetryConfig options
    profile="production",
    enable_emoji=False,
    debug=False,
    service_name="my-application",
    service_version="1.0.0"
)
```

## Integration with Full Configuration

For complex configurations, use the full configuration system:

```python
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
from provide.foundation.setup import setup_telemetry

# Full configuration control
logging_config = LoggingConfig(
    default_level="INFO",
    console_formatter="json",
    log_file=Path("/var/log/app.log"),
    enable_colors=False
)

telemetry_config = TelemetryConfig(
    logging=logging_config,
    profile="production",
    service_name="my-service"
)

# Apply configuration
setup_telemetry(telemetry_config)

# Then use factory functions normally
log = get_logger(__name__)
log.info("Application configured")
```

## Error Handling

The factory functions handle common error conditions gracefully:

```python
# Invalid log levels default to INFO
setup_logging(level="INVALID")  # Uses INFO level

# Missing file paths create parent directories
setup_logging(log_file="/non/existent/path/app.log")  # Creates directories

# Invalid file paths fall back to console only
setup_logging(log_file="/dev/null/invalid")  # Logs to console only
```

## Performance Considerations

- **get_logger()**: Very lightweight, just delegates to global logger
- **setup_logging()**: One-time configuration cost, subsequent logging is fast  
- **Named loggers**: No additional performance cost vs direct logger usage
- **File logging**: Minimal overhead with proper buffering

## Examples

### Development Setup

```python
from provide.foundation.logger import setup_logging, get_logger

# Quick development setup
setup_logging(level="DEBUG")

# Use throughout application
log = get_logger(__name__)
log.debug("Starting application")
```

### Production Setup

```python
import os
from provide.foundation.logger import setup_logging, get_logger

# Production configuration from environment
setup_logging(
    level=os.getenv("LOG_LEVEL", "INFO"),
    json_logs=True,
    log_file=f"/var/log/{os.getenv('SERVICE_NAME', 'app')}.log"
)

# Service loggers
auth_log = get_logger("auth")
db_log = get_logger("database")  
api_log = get_logger("api")

auth_log.info("Authentication service initialized")
```

### Testing Setup

```python
from provide.foundation.logger import setup_logging, get_logger

# Test-friendly setup
setup_logging(level="WARNING")  # Reduce test noise

# Test-specific logger
test_log = get_logger("tests")
test_log.error("Test failure", test="test_user_login", reason="timeout")
```

## API Reference

::: provide.foundation.logger.factories

## Related Documentation

- [Logger Core](core.md) - Core FoundationLogger implementation  
- [Logger Base](base.md) - Main logger interface
- [Configuration](config.md) - Full configuration system
- [Setup Guide](../../guide/logging/basic.md) - Basic logging usage