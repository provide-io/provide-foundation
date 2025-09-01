# Configuration API

The `provide.foundation.config` module provides a flexible configuration system with environment variable support, file loading, and type-safe config classes.

## Overview

The configuration system provides:
- Environment variable parsing with type conversion
- Multi-source configuration (env vars, files, defaults)
- Type-safe configuration with attrs classes
- YAML, JSON, and TOML file support
- Validation and error handling
- Source tracking for debugging

## Quick Start

```python
from provide.foundation import setup_telemetry
from provide.foundation.logger.config import TelemetryConfig

# Simple setup with defaults
setup_telemetry(service_name="my-app")

# Load from environment variables
config = TelemetryConfig.from_env()
setup_telemetry(config)

# Custom configuration
from provide.foundation.logger.config import LoggingConfig

config = TelemetryConfig(
    service_name="my-app",
    logging=LoggingConfig(
        level="DEBUG",
        format="json",
        use_colors=False
    )
)
setup_telemetry(config)
```

## Core Components

### TelemetryConfig

The main configuration class for the telemetry system:

```python
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

# Create with defaults
config = TelemetryConfig()

# Specify all options
config = TelemetryConfig(
    service_name="production-api",
    logging=LoggingConfig(
        level="INFO",
        format="json",
        use_colors=False,
        show_timestamp=True,
        show_caller=False,
        emoji_mode="none"
    ),
    globally_disabled=False
)

# Access configuration values
print(config.service_name)
print(config.logging.level)
print(config.logging.format)
```

### LoggingConfig

Configuration specific to logging behavior:

```python
from provide.foundation.logger.config import LoggingConfig

# Create logging config
log_config = LoggingConfig(
    level="DEBUG",              # Log level: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="console",           # Output format: console, json
    use_colors=True,           # Enable colored output
    show_timestamp=True,        # Include timestamps
    show_caller=True,          # Show caller information
    emoji_mode="emoji",        # Emoji mode: emoji, text, none
    semantic_layers=["http", "database"],  # Enable semantic layers
    output_stream=None         # Custom output stream (for testing)
)

# Use in TelemetryConfig
config = TelemetryConfig(
    service_name="my-service",
    logging=log_config
)
```

## Environment Variables

### Loading from Environment

Configure the telemetry system using environment variables:

```bash
# Core settings
export TELEMETRY_SERVICE_NAME="production-api"
export TELEMETRY_GLOBALLY_DISABLED="false"

# Logging settings
export TELEMETRY_LOG_LEVEL="INFO"
export TELEMETRY_LOG_FORMAT="json"
export TELEMETRY_USE_COLORS="false"
export TELEMETRY_SHOW_TIMESTAMP="true"
export TELEMETRY_SHOW_CALLER="false"
export TELEMETRY_EMOJI_MODE="none"

# Semantic layers (comma-separated)
export TELEMETRY_SEMANTIC_LAYERS="http,database,llm"
```

Load the configuration:

```python
from provide.foundation.logger.config import TelemetryConfig

# Load all settings from environment
config = TelemetryConfig.from_env()

# The from_env method:
# 1. Reads TELEMETRY_* environment variables
# 2. Converts types automatically (bool, int, list)
# 3. Falls back to defaults for missing values
# 4. Validates configuration
```

### Environment Variable Mapping

| Environment Variable | Config Field | Type | Default |
|---------------------|--------------|------|---------|
| `TELEMETRY_SERVICE_NAME` | `service_name` | str | "provide-telemetry" |
| `TELEMETRY_LOG_LEVEL` | `logging.level` | str | "INFO" |
| `TELEMETRY_LOG_FORMAT` | `logging.format` | str | "console" |
| `TELEMETRY_USE_COLORS` | `logging.use_colors` | bool | True |
| `TELEMETRY_SHOW_TIMESTAMP` | `logging.show_timestamp` | bool | True |
| `TELEMETRY_SHOW_CALLER` | `logging.show_caller` | bool | False |
| `TELEMETRY_EMOJI_MODE` | `logging.emoji_mode` | str | "emoji" |
| `TELEMETRY_SEMANTIC_LAYERS` | `logging.semantic_layers` | list | [] |
| `TELEMETRY_GLOBALLY_DISABLED` | `globally_disabled` | bool | False |

## Configuration Files

### Loading from YAML

```python
from provide.foundation.config import load_config

# config.yaml
"""
service_name: my-service
logging:
  level: DEBUG
  format: json
  use_colors: false
  semantic_layers:
    - http
    - database
"""

# Load configuration
config = load_config("config.yaml", config_class=TelemetryConfig)
setup_telemetry(config)
```

### Loading from JSON

```python
# config.json
"""
{
  "service_name": "my-service",
  "logging": {
    "level": "INFO",
    "format": "console",
    "emoji_mode": "text"
  }
}
"""

config = load_config("config.json", config_class=TelemetryConfig)
```

### Loading from TOML

```python
# config.toml
"""
service_name = "my-service"

[logging]
level = "DEBUG"
format = "json"
use_colors = false
semantic_layers = ["http", "llm"]
"""

config = load_config("config.toml", config_class=TelemetryConfig)
```

## Custom Configuration Classes

Create your own configuration classes:

```python
import attrs
from provide.foundation.config import BaseConfig

@attrs.define
class DatabaseConfig(BaseConfig):
    """Database configuration."""
    host: str = "localhost"
    port: int = 5432
    database: str = "myapp"
    username: str = "user"
    password: str = attrs.field(default="", repr=False)  # Hide in repr
    pool_size: int = 10
    
@attrs.define
class AppConfig(BaseConfig):
    """Application configuration."""
    service_name: str = "my-app"
    debug: bool = False
    database: DatabaseConfig = attrs.field(factory=DatabaseConfig)
    telemetry: TelemetryConfig = attrs.field(factory=TelemetryConfig)

# Load from environment
app_config = AppConfig.from_env(prefix="APP")

# Load from file
app_config = load_config("app.yaml", config_class=AppConfig)

# Access nested configuration
print(app_config.database.host)
print(app_config.telemetry.service_name)
```

## Configuration Precedence

Configuration values are loaded with the following precedence (highest to lowest):

1. **Explicit values** - Passed directly to constructors
2. **Environment variables** - Set via `TELEMETRY_*` vars
3. **Configuration files** - YAML/JSON/TOML files
4. **Defaults** - Built-in default values

```python
# Example showing precedence
import os

# Set environment variable
os.environ["TELEMETRY_LOG_LEVEL"] = "WARNING"

# Load from file (has level: INFO)
config = load_config("config.yaml")
# Result: level = "INFO" (file overrides defaults)

# Load from environment
config = TelemetryConfig.from_env()
# Result: level = "WARNING" (env overrides file)

# Explicit value
config = TelemetryConfig(logging=LoggingConfig(level="DEBUG"))
# Result: level = "DEBUG" (explicit overrides all)
```

## Validation

Configuration is validated automatically:

```python
from provide.foundation.logger.config import LoggingConfig

# Invalid log level
try:
    config = LoggingConfig(level="INVALID")
except ValueError as e:
    print(f"Validation error: {e}")

# Invalid format
try:
    config = LoggingConfig(format="invalid")
except ValueError as e:
    print(f"Invalid format: {e}")

# Custom validation in your config classes
@attrs.define
class MyConfig(BaseConfig):
    port: int = attrs.field(validator=attrs.validators.instance_of(int))
    
    @port.validator
    def _validate_port(self, attribute, value):
        if not 1 <= value <= 65535:
            raise ValueError(f"Port must be between 1 and 65535, got {value}")
```

## Dynamic Configuration

Update configuration at runtime:

```python
from provide.foundation import setup_telemetry, plog

# Initial setup
setup_telemetry(service_name="my-app", log_level="INFO")

# Log at INFO level
plog.info("This is visible")
plog.debug("This is not visible")

# Reconfigure with DEBUG level
setup_telemetry(service_name="my-app", log_level="DEBUG")

# Now debug is visible
plog.debug("Now this is visible")

# Disable telemetry globally
setup_telemetry(globally_disabled=True)
plog.info("This will not be logged")
```

## Testing with Configuration

### Mock Configuration

```python
import pytest
from provide.foundation.logger.config import TelemetryConfig

@pytest.fixture
def test_config():
    """Test configuration fixture."""
    return TelemetryConfig(
        service_name="test-service",
        logging=LoggingConfig(
            level="DEBUG",
            format="json",
            output_stream=io.StringIO()  # Capture output
        )
    )

def test_with_config(test_config):
    setup_telemetry(test_config)
    # Your test code
```

### Environment Variable Testing

```python
import os
import pytest

def test_env_config(monkeypatch):
    # Set environment variables for test
    monkeypatch.setenv("TELEMETRY_SERVICE_NAME", "test")
    monkeypatch.setenv("TELEMETRY_LOG_LEVEL", "DEBUG")
    
    config = TelemetryConfig.from_env()
    assert config.service_name == "test"
    assert config.logging.level == "DEBUG"
```

## Configuration Patterns

### Development vs Production

```python
import os

def get_config():
    """Get environment-specific configuration."""
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return TelemetryConfig(
            service_name="production-api",
            logging=LoggingConfig(
                level="INFO",
                format="json",
                use_colors=False,
                emoji_mode="none"
            )
        )
    else:
        return TelemetryConfig(
            service_name=f"{env}-api",
            logging=LoggingConfig(
                level="DEBUG",
                format="console",
                use_colors=True,
                emoji_mode="emoji"
            )
        )

# Apply configuration
config = get_config()
setup_telemetry(config)
```

### Multi-Environment Support

```python
# config/base.yaml
service_name: my-service
logging:
  show_timestamp: true
  show_caller: false

# config/dev.yaml
logging:
  level: DEBUG
  format: console
  use_colors: true

# config/prod.yaml
logging:
  level: INFO
  format: json
  use_colors: false

# Load environment-specific config
env = os.getenv("ENVIRONMENT", "dev")
base_config = load_config("config/base.yaml")
env_config = load_config(f"config/{env}.yaml")

# Merge configurations
final_config = base_config.merge(env_config)
setup_telemetry(final_config)
```

## Best Practices

1. **Use environment variables for deployment**:
   ```python
   # Production deployment
   config = TelemetryConfig.from_env()
   ```

2. **Validate early**:
   ```python
   # Validate at startup
   try:
       config = TelemetryConfig.from_env()
   except Exception as e:
       print(f"Configuration error: {e}")
       sys.exit(1)
   ```

3. **Hide sensitive values**:
   ```python
   @attrs.define
   class Config(BaseConfig):
       api_key: str = attrs.field(repr=False)  # Hidden in logs
   ```

4. **Provide sensible defaults**:
   ```python
   @attrs.define
   class Config(BaseConfig):
       timeout: int = 30  # Sensible default
       retries: int = 3
   ```

5. **Document configuration options**:
   ```python
   @attrs.define
   class Config(BaseConfig):
       """Application configuration.
       
       Attributes:
           cache_ttl: Cache time-to-live in seconds
           max_connections: Maximum database connections
       """
       cache_ttl: int = 300
       max_connections: int = 10
   ```

## API Reference

### Classes

- `TelemetryConfig` - Main telemetry configuration
- `LoggingConfig` - Logging-specific configuration
- `BaseConfig` - Base class for custom configs

### Functions

- `setup_telemetry(config)` - Apply telemetry configuration
- `load_config(path, config_class)` - Load config from file
- `TelemetryConfig.from_env()` - Load from environment

### Environment Variables

All environment variables use the `TELEMETRY_` prefix and map to configuration fields.

## See Also

- [Logger](logger.md) - Logging system documentation
- [Environment Variables](../guides/environment-variables.md) - Environment configuration guide
- [Best Practices](../guides/best-practices.md) - Configuration best practices