# FoundationLogger API

The `FoundationLogger` class provides the main logging interface for provide.foundation, built on top of structlog with emoji-enhanced visual parsing and lazy initialization.

## Classes

### FoundationLogger

Thread-safe logger with lazy setup and standardized logging interface.

```python
class FoundationLogger:
    """A structlog-based logger providing a standardized logging interface."""
    
    def __init__(self) -> None: ...
```

#### Methods

##### get_logger(name)

Get a logger instance with the given name.

```python
def get_logger(self, name: str | None = None) -> Any:
    """
    Get a logger instance with the given name.
    
    Args:
        name: Logger name (e.g., __name__ from a module)
        
    Returns:
        Configured structlog logger instance
    """
```

**Example:**
```python
from provide.foundation.logger import logger

# Get named logger
log = logger.get_logger(__name__)
log.info("Application started")

# Get default logger
log = logger.get_logger()
log.info("Using default logger")
```

##### trace(event, *args, **kwargs)

Log a trace-level message.

```python
def trace(
    self,
    event: str,
    *args: Any,
    _foundation_logger_name: str | None = None,
    **kwargs: Any,
) -> None:
    """
    Log trace-level event for detailed debugging.
    
    Args:
        event: Log message
        *args: Format arguments
        _foundation_logger_name: Optional logger name override
        **kwargs: Additional context fields
    """
```

**Example:**
```python
logger.trace("Function called", function="process_data", args=args)
logger.trace("Variable state: %s", variable_value)
```

##### debug(event, *args, **kwargs)

Log a debug-level message.

```python
def debug(self, event: str, *args: Any, **kwargs: Any) -> None:
    """Log debug-level event."""
```

##### info(event, *args, **kwargs)

Log an info-level message.

```python
def info(self, event: str, *args: Any, **kwargs: Any) -> None:
    """Log info-level event."""
```

##### warning(event, *args, **kwargs) / warn(event, *args, **kwargs)

Log a warning-level message.

```python
def warning(self, event: str, *args: Any, **kwargs: Any) -> None:
    """Log warning-level event."""
    
warn = warning  # Alias for compatibility
```

##### error(event, *args, **kwargs)

Log an error-level message.

```python
def error(self, event: str, *args: Any, **kwargs: Any) -> None:
    """Log error-level event."""
```

##### exception(event, *args, **kwargs)

Log an error-level message with exception information.

```python
def exception(self, event: str, *args: Any, **kwargs: Any) -> None:
    """Log error-level event with exception traceback."""
```

**Example:**
```python
try:
    risky_operation()
except Exception:
    logger.exception("Operation failed", operation="risky_operation")
```

##### critical(event, *args, **kwargs)

Log a critical-level message.

```python
def critical(self, event: str, *args: Any, **kwargs: Any) -> None:
    """Log critical-level event."""
```

## Global Functions

### get_logger(name)

Convenience function to get a logger instance from the global FoundationLogger.

```python
def get_logger(name: str | None = None) -> Any:
    """
    Get a logger instance with the given name.
    
    Args:
        name: Logger name (e.g., __name__ from a module)
        
    Returns:
        Configured structlog logger instance
    """
```

**Example:**
```python
from provide.foundation.logger import get_logger

log = get_logger(__name__)
log.info("Module initialized", module=__name__)
```

### setup_logging(**kwargs)

Simple logging setup for basic use cases.

```python
def setup_logging(
    level: str | int = "INFO",
    json_logs: bool = False,
    log_file: str | None = None,
    **kwargs,
) -> None:
    """
    Setup logging configuration.
    
    Args:
        level: Log level (string or int)
        json_logs: Whether to output logs as JSON
        log_file: Optional file path to write logs
        **kwargs: Additional configuration options
    """
```

**Example:**
```python
from provide.foundation.logger import setup_logging

# Basic setup
setup_logging(level="DEBUG")

# JSON logging
setup_logging(level="INFO", json_logs=True)

# File logging
setup_logging(level="INFO", log_file="/var/log/app.log")
```

## Global Instance

### logger

The global `FoundationLogger` instance used throughout the library.

```python
logger: FoundationLogger = FoundationLogger()
```

**Example:**
```python
from provide.foundation.logger import logger

logger.info("Direct usage of global logger")
logger.debug("Debug information", user_id=123)
```

## Lazy Initialization

The logger uses lazy initialization to avoid import-time side effects. Configuration is performed on first use, making it safe to import in any context.

## Thread Safety

All logging operations are thread-safe. The lazy initialization uses double-checked locking to ensure thread-safe setup.

## Related Documentation

- [Telemetry Configuration API](config.md) - Configuration objects
- [Log Processors API](processors.md) - Processing pipeline
- [Emoji System API](emoji.md) - Visual parsing system
- [Getting Started Guide](/guide/logging/basic/) - Basic usage examples