# Logger Core Implementation

The core logger module contains the main `FoundationLogger` class implementation with lazy initialization, thread safety, and advanced configuration management.

## Overview

The core module provides the foundational logging implementation that powers provide.foundation's structured logging system. It features:

- **Lazy Setup**: Deferred initialization to avoid import-time side effects
- **Thread Safety**: Double-checked locking pattern for concurrent access
- **Emergency Fallback**: Graceful degradation when setup fails
- **Configuration Tracking**: State management for active configurations
- **Structured Logging**: Built on structlog with emoji enhancement

## Architecture

### Lazy Initialization Pattern

The logger uses a sophisticated lazy initialization system:

```python
from provide.foundation.logger import logger

# First call triggers setup
logger.info("This triggers lazy initialization")

# Subsequent calls use configured logger
logger.debug("This uses the configured logger")
```

### Thread Safety

All operations are thread-safe using proper locking:

- Setup uses double-checked locking
- Emergency fallback for setup failures  
- Global state tracking across threads

### Configuration Management

The core tracks active configurations:

```python
# Check if configured by explicit setup
if logger._is_configured_by_setup:
    print("Logger was explicitly configured")

# Access active configuration
config = logger._active_config
if config:
    print(f"Using log level: {config.log_level}")
```

## Internal State

The core logger maintains several internal state variables:

- `_is_configured_by_setup`: Tracks explicit configuration
- `_active_config`: Current `TelemetryConfig` instance
- `_active_resolved_emoji_config`: Resolved emoji configuration
- `_LAZY_SETUP_STATE`: Global setup state tracking

## Usage Examples

### Basic Logging

```python
from provide.foundation.logger.core import logger

# All standard logging levels
logger.trace("Detailed debugging info", function="process_data")
logger.debug("Debug information", user_id=123)  
logger.info("Application event", event="user_login")
logger.warning("Warning condition", threshold_exceeded=True)
logger.error("Error occurred", error="timeout")
logger.exception("Exception with traceback")  # Use in except blocks
logger.critical("Critical system failure", system="database")
```

### Configuration Checking

```python
from provide.foundation.logger.core import FoundationLogger

# Create logger instance
log = FoundationLogger()

# Check configuration status
if not log._is_configured_by_setup:
    print("Logger will use lazy initialization")

# Ensure configuration before use
log._ensure_configured()
```

### Emergency Fallback

If setup fails, the logger automatically switches to an emergency fallback mode:

```python
# This will gracefully handle setup failures
logger.info("Will work even if setup fails")
```

## Advanced Features

### Custom Configuration

```python
from provide.foundation.logger.core import FoundationLogger
from provide.foundation.logger.config import TelemetryConfig

# Create with custom config
config = TelemetryConfig(
    log_level="DEBUG",
    enable_emoji=True,
    json_logs=False
)

logger = FoundationLogger()
# Configuration will be applied on first use
```

### Structlog Integration

The core logger wraps structlog with additional functionality:

```python
# Access the underlying structlog logger
internal_logger = logger._internal_logger

# Use structlog methods directly if needed
bound_logger = internal_logger.bind(request_id="abc123")
bound_logger.info("Request processed")
```

## Error Handling

The core implementation handles various error conditions:

- **Setup Failures**: Falls back to emergency logging
- **Configuration Errors**: Uses sensible defaults
- **Thread Contention**: Handles concurrent initialization safely
- **Import Errors**: Graceful degradation when dependencies missing

## Performance Characteristics

- **First Call Overhead**: Setup cost on initial use (~10ms)
- **Subsequent Calls**: Native structlog performance (~70μs per log)
- **Thread Safety**: Minimal locking overhead after initialization
- **Memory Usage**: Lazy setup reduces import-time memory footprint

## API Reference

::: provide.foundation.logger.core

## Related Documentation

- [api-Logger Base API](api-base.md) - Public interface and exports
- [api-Logger Factories](api-factories.md) - Factory functions for logger creation
- [api-Configuration](api-config.md) - Configuration classes and options
- [Setup Guide](../../guide/logging/basic.md) - Basic usage patterns