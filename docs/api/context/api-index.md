# Context API

Unified context for configuration and CLI state management, providing a single point of configuration for applications and services.

## Overview

The `Context` class serves as a unified configuration and state management system that combines:

- **Configuration Management**: Load settings from files, environment variables, and programmatic sources
- **CLI State**: Runtime state for command-line interfaces and tools
- **Environment Profiles**: Support for development, staging, and production profiles
- **Type Safety**: Full type validation and conversion with attrs
- **File Format Support**: TOML, YAML, JSON, and INI configuration files

## Key Features

- **Multiple Sources**: Environment variables, configuration files, and direct assignment
- **Profile-based Configuration**: Different settings for different environments
- **Automatic Type Conversion**: Safe conversion of string values to appropriate types
- **Validation**: Built-in validation for configuration values
- **Runtime Updates**: Mutable configuration that can be updated at runtime
- **Telemetry Integration**: Direct integration with TelemetryConfig for logging

## Basic Usage

### Creating a Context

```python
from provide.foundation import Context

# Default context with standard settings
ctx = Context()

# Custom context with specific configuration
ctx = Context(
    log_level="DEBUG",
    profile="development", 
    debug=True,
    json_output=False
)

# Environment-based context
ctx = Context.from_env()
```

### Loading Configuration Files

```python
from provide.foundation import Context

# Load from TOML file
ctx = Context()
ctx.load_config("config.toml")

# Load from YAML file
ctx.load_config("config.yaml")

# Load from JSON file
ctx.load_config("config.json")

# Load from multiple files (later files override earlier ones)
ctx.load_config_files([
    "defaults.toml",
    "environment.yaml", 
    "local.json"
])
```

### Environment Variable Integration

```python
from provide.foundation import Context

# Load configuration from environment variables
ctx = Context.from_env()

# Environment variable format:
# FOUNDATION_LOG_LEVEL=DEBUG
# FOUNDATION_PROFILE=production
# FOUNDATION_DEBUG=true
# FOUNDATION_JSON_OUTPUT=false
```

## Configuration Options

### Core Settings

- **log_level**: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **profile**: Environment profile name (development, staging, production, etc.)
- **debug**: Enable debug mode with verbose output
- **json_output**: Format output as JSON instead of human-readable format

### File and Path Settings

- **config_file**: Path to primary configuration file
- **data_dir**: Directory for application data storage
- **cache_dir**: Directory for cache files
- **log_dir**: Directory for log files

### Service Configuration

- **service_name**: Name identifier for the service
- **service_version**: Version of the service
- **base_url**: Base URL for API services

## File Configuration Examples

### TOML Configuration

```toml
# config.toml
log_level = "INFO"
profile = "production"
debug = false
json_output = true

service_name = "my-application"
service_version = "1.0.0"
base_url = "https://api.example.com"

[paths]
data_dir = "/var/lib/myapp"
cache_dir = "/var/cache/myapp"
log_dir = "/var/log/myapp"
```

### YAML Configuration

```yaml
# config.yaml
log_level: DEBUG
profile: development
debug: true
json_output: false

service_name: my-development-app
service_version: 1.0.0-dev

paths:
  data_dir: ./data
  cache_dir: ./cache
  log_dir: ./logs
```

### JSON Configuration

```json
{
  "log_level": "INFO",
  "profile": "staging",
  "debug": false,
  "json_output": true,
  "service_name": "my-staging-app",
  "service_version": "1.0.0-rc1",
  "base_url": "https://staging-api.example.com"
}
```

## Environment Variables

The Context class supports automatic loading from environment variables with the `FOUNDATION_` prefix:

```bash
export FOUNDATION_LOG_LEVEL=DEBUG
export FOUNDATION_PROFILE=development
export FOUNDATION_DEBUG=true
export FOUNDATION_JSON_OUTPUT=false
export FOUNDATION_SERVICE_NAME=my-app
export FOUNDATION_SERVICE_VERSION=1.0.0
```

## Profile-Based Configuration

Use profiles to manage different environment configurations:

```python
from provide.foundation import Context

# Development profile
dev_ctx = Context(
    profile="development",
    log_level="DEBUG",
    debug=True,
    data_dir=Path("./dev-data")
)

# Production profile
prod_ctx = Context(
    profile="production", 
    log_level="INFO",
    debug=False,
    data_dir=Path("/var/lib/myapp")
)

# Load profile-specific config files
ctx = Context(profile="staging")
ctx.load_config(f"config-{ctx.profile}.toml")
```

## Integration with Telemetry

The Context class integrates directly with the telemetry system:

```python
from provide.foundation import Context, setup_telemetry

# Create context
ctx = Context.from_env()

# Convert to telemetry configuration
telemetry_config = ctx.to_telemetry_config()

# Setup telemetry with context
setup_telemetry(telemetry_config)

# Use logging with context-derived configuration
from provide.foundation import get_logger
log = get_logger(__name__)
log.info("Application started", profile=ctx.profile)
```

## Runtime Configuration Updates

The Context is mutable and supports runtime updates:

```python
from provide.foundation import Context

ctx = Context()

# Update configuration at runtime
ctx.log_level = "DEBUG"
ctx.debug = True

# Load additional configuration
ctx.load_config("runtime-config.toml")

# Apply changes to telemetry system
telemetry_config = ctx.to_telemetry_config()
setup_telemetry(telemetry_config)
```

## Validation and Error Handling

The Context class includes validation for all configuration values:

```python
from provide.foundation import Context

try:
    ctx = Context(log_level="INVALID_LEVEL")
except ValueError as e:
    print(f"Invalid log level: {e}")

try:
    ctx = Context()
    ctx.load_config("nonexistent.toml")
except FileNotFoundError as e:
    print(f"Config file not found: {e}")
```

## Advanced Usage Examples

### Multi-Environment Setup

```python
import os
from provide.foundation import Context

# Determine environment from system
environment = os.getenv("ENVIRONMENT", "development")

# Create context for environment
ctx = Context(profile=environment)

# Load base configuration
ctx.load_config("config.toml")

# Load environment-specific overrides
env_config = f"config-{environment}.toml"
if Path(env_config).exists():
    ctx.load_config(env_config)

# Apply local developer overrides
if Path("config-local.toml").exists():
    ctx.load_config("config-local.toml")
```

### CLI Application Integration

```python
import argparse
from provide.foundation import Context

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--profile", default="default")
    parser.add_argument("--config", type=Path)
    args = parser.parse_args()
    
    # Create context from environment
    ctx = Context.from_env()
    
    # Override with CLI arguments
    if args.debug:
        ctx.debug = True
        ctx.log_level = "DEBUG"
    
    if args.profile:
        ctx.profile = args.profile
        
    if args.config:
        ctx.load_config(args.config)
    
    # Setup telemetry with context
    setup_telemetry(ctx.to_telemetry_config())
    
    # Application logic here
    from provide.foundation import get_logger
    log = get_logger(__name__)
    log.info("CLI application started", profile=ctx.profile)

if __name__ == "__main__":
    main()
```

## Performance Characteristics

- **Creation**: Lightweight object creation (~100μs)
- **File Loading**: I/O bound, depends on file size and format
- **Environment Loading**: Fast environment variable parsing (~1ms)
- **Validation**: Minimal overhead with attrs validators
- **Memory Usage**: Small footprint with slots optimization

## API Reference

::: provide.foundation.context.core.Context

## Related Documentation

- [Configuration Guide](../../guide/config/index.md) - Detailed configuration patterns
- [Logger Configuration](../logger/config.md) - Telemetry configuration integration
- [Setup Functions](../setup.md) - Setup functions that use Context
- [CLI Framework](../cli/api-index.md) - CLI integration patterns