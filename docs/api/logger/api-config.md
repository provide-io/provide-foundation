# Logger Configuration

Configuration classes for the provide.foundation logging system, providing structured configuration for telemetry and logging behavior.

## Overview

The logger configuration system provides two main configuration classes:

- **TelemetryConfig**: High-level configuration for the entire telemetry system
- **LoggingConfig**: Specific logging configuration (output formats, levels, etc.)

These classes use the `attrs` library for immutable, type-safe configuration with validation and sensible defaults.

## Key Features

- **Immutable Configuration**: Thread-safe configuration objects using `attrs` frozen classes
- **Type Safety**: Full type annotations with modern Python typing
- **Validation**: Built-in validation for configuration values
- **Environment Integration**: Automatic loading from environment variables
- **Sensible Defaults**: Production-ready defaults for all settings

## Basic Usage

### TelemetryConfig

```python
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

# Basic configuration with defaults
config = TelemetryConfig()

# Custom configuration
config = TelemetryConfig(
    service_name="my-application",
    globally_disabled=False,
    logging=LoggingConfig(
        default_level="INFO",
        console_formatter="key_value"
    )
)

# Environment-based configuration
config = TelemetryConfig.from_env()
```

### LoggingConfig

```python
from provide.foundation.logger.config import LoggingConfig
from pathlib import Path

# Basic logging configuration
logging_config = LoggingConfig(
    default_level="INFO",
    console_formatter="key_value"
)

# Advanced logging configuration
logging_config = LoggingConfig(
    default_level="DEBUG",
    console_formatter="json",
    log_file=Path("/var/log/app.log"),
    enable_colors=True,
    show_timestamp=True
)

# Use with TelemetryConfig
telemetry_config = TelemetryConfig(logging=logging_config)
```

## Configuration Options

### TelemetryConfig Options

- **profile**: Environment profile (development, staging, production)
- **debug**: Enable debug mode with verbose output
- **service_name**: Name of the service for structured logging
- **service_version**: Version of the service
- **logging**: LoggingConfig instance for logging-specific settings
- **enable_emoji**: Enable emoji enhancement for visual log parsing

### LoggingConfig Options

- **default_level**: Default log level for all loggers
- **console_formatter**: Console output format (key_value, json, minimal)
- **log_file**: Optional file path for log output
- **enable_colors**: Enable colored console output
- **show_timestamp**: Include timestamps in log output
- **json_indent**: Indentation for JSON formatted logs

## Environment Variables

Configuration can be loaded from environment variables:

```bash
# TelemetryConfig environment variables
export FOUNDATION_PROFILE=production
export FOUNDATION_DEBUG=false
export FOUNDATION_SERVICE_NAME=my-app
export FOUNDATION_SERVICE_VERSION=1.2.3
export FOUNDATION_ENABLE_EMOJI=true

# LoggingConfig environment variables  
export FOUNDATION_LOG_LEVEL=INFO
export FOUNDATION_LOG_FORMAT=json
export FOUNDATION_LOG_FILE=/var/log/app.log
export FOUNDATION_ENABLE_COLORS=false
```

```python
from provide.foundation.logger.config import TelemetryConfig

# Load from environment
config = TelemetryConfig.from_env()
```

## Configuration Validation

Configuration classes include built-in validation:

```python
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

# Invalid log level raises validation error
try:
    config = LoggingConfig(default_level="INVALID")
except ValueError as e:
    print(f"Validation error: {e}")

# Invalid profile raises validation error
try:
    config = TelemetryConfig(profile="invalid_profile")  
except ValueError as e:
    print(f"Validation error: {e}")
```

## Integration Examples

### Simple Application Setup

```python
from provide.foundation.logger.config import TelemetryConfig
from provide.foundation.setup import setup_telemetry

# Environment-based configuration
config = TelemetryConfig.from_env()
setup_telemetry(config)

# Now use logging throughout application
from provide.foundation.logger import get_logger
log = get_logger(__name__)
log.info("Application started", config=config.profile)
```

### Custom Service Configuration

```python
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
from pathlib import Path

# Service-specific logging
logging_config = LoggingConfig(
    default_level="INFO",
    console_formatter="json",
    log_file=Path("/var/log/microservice.json"),
    enable_colors=False  # Disable colors for log aggregation
)

# Service telemetry
telemetry_config = TelemetryConfig(
    profile="production",
    service_name="user-authentication-service",
    service_version="2.1.0",
    logging=logging_config,
    enable_emoji=False  # Disable emojis for production
)

# Apply configuration
from provide.foundation.setup import setup_telemetry
setup_telemetry(telemetry_config)
```

### Development vs Production

```python
import os
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

# Environment-aware configuration
is_development = os.getenv("ENVIRONMENT", "development") == "development"

if is_development:
    config = TelemetryConfig(
        profile="development",
        debug=True,
        logging=LoggingConfig(
            default_level="DEBUG",
            console_formatter="key_value",
            enable_colors=True
        )
    )
else:
    config = TelemetryConfig(
        profile="production", 
        debug=False,
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",
            log_file=Path("/var/log/production.json"),
            enable_colors=False
        )
    )
```

## Configuration Sources Priority

Configuration is resolved in this order (higher priority overrides lower):

1. **Explicit parameters** - Direct constructor arguments
2. **Environment variables** - `from_env()` method
3. **Default values** - Built-in defaults in the class definition

## Thread Safety

All configuration objects are immutable (`frozen=True` in attrs), making them thread-safe for concurrent access across multiple threads.

## API Reference

::: provide.foundation.logger.config

## Related Documentation

- [Logger Base](base.md) - Main logger interface that uses these configurations
- [Logger Core](core.md) - Core implementation that applies configuration
- [Setup Functions](../../api/setup.md) - Functions that use configuration
- [Configuration Guide](../../guide/config/index.md) - Detailed configuration guide