# Configuration System API

Async-first configuration management system with support for multiple sources, validation, and runtime updates.

## Overview

The provide.foundation configuration system provides:

- **Async-first design** - All operations support async/await
- **Multiple sources** - Environment variables, files (JSON/YAML/TOML/INI/ENV), dictionaries
- **Schema validation** - Type checking and custom validators
- **Runtime updates** - Dynamic configuration changes with source tracking
- **Immutable configs** - Thread-safe configuration objects using attrs
- **Source precedence** - Clear precedence rules for merging multiple sources

## Core Concepts

### Configuration Classes

All configuration classes inherit from `BaseConfig` and use attrs for structure:

```python
from provide.foundation.config.base import BaseConfig, field

@define(frozen=True)
class DatabaseConfig(BaseConfig):
    host: str = field(default="localhost", description="Database host")
    port: int = field(default=5432, description="Database port")
    username: str = field(sensitive=True, description="Database user")
    password: str = field(sensitive=True, description="Database password")
```

### Configuration Sources

Sources are loaded in order of precedence (higher values override lower):

1. `ConfigSource.DEFAULT` (0) - Default values
2. `ConfigSource.FILE` (10) - Configuration files
3. `ConfigSource.ENV` (20) - Environment variables
4. `ConfigSource.RUNTIME` (30) - Runtime updates

### Async Operations

All configuration operations are async to support:
- Async file I/O with aiofiles
- Async validation (database connections, API checks)
- Async secret loading from external systems

## Quick Start

### Basic Usage

```python
from provide.foundation.config import BaseConfig, field

@define(frozen=True)
class AppConfig(BaseConfig):
    name: str = field(default="myapp")
    debug: bool = field(default=False)
    port: int = field(default=8000)

# Create from dictionary
config = AppConfig.from_dict({"name": "myapp", "debug": True})

# Validate
await config.validate()

# Export
data = await config.to_dict()
```

### Environment Configuration

```python
from provide.foundation.config.env import RuntimeConfig, env_field

@define(frozen=True)
class DatabaseConfig(RuntimeConfig):
    host: str = env_field(env_var="DB_HOST", default="localhost")
    port: int = env_field(default=5432)
    password: str = env_field(sensitive=True)

# Load from environment
config = DatabaseConfig.from_env(prefix="DATABASE")
```

### File Configuration

```python
from provide.foundation.config.loader import FileConfigLoader

loader = FileConfigLoader("config.yaml")
config = await loader.load(AppConfig)
```

### Configuration Manager

```python
from provide.foundation.config.manager import ConfigManager

manager = ConfigManager()
await manager.register("app", config=app_config)

# Retrieve
app_config = await manager.get("app")
```

## API Modules

### [api-BaseConfig](api-base.md)
Core configuration base class with field definitions, validation, and serialization.

### [api-ConfigManager](api-manager.md)
Centralized configuration registry with lifecycle management and runtime updates.

### [api-Environment Config](api-env.md)
Environment variable loading with async secret support and type coercion.

### [api-Config Loaders](api-loader.md)
File and multi-source configuration loading with format detection.

### [api-Config Schema](api-schema.md)
Schema definition and validation with async validators and type checking.

## Usage Patterns

### Multi-source Configuration

```python
from provide.foundation.config.loader import (
    FileConfigLoader, 
    RuntimeConfigLoader,
    MultiSourceLoader
)

# Load from multiple sources with precedence
loader = MultiSourceLoader(
    FileConfigLoader("config.yaml"),      # Base configuration
    FileConfigLoader("local.yaml"),      # Local overrides
    RuntimeConfigLoader(prefix="MYAPP"),     # Environment overrides
)

config = await loader.load(AppConfig)
```

### Schema Validation

```python
from provide.foundation.config.schema import ConfigSchema, SchemaField

schema = ConfigSchema([
    SchemaField("host", type=str, required=True),
    SchemaField("port", type=int, min_value=1, max_value=65535),
    SchemaField("url", validator=validate_url),
])

await schema.validate(config_data)
```

### Runtime Updates

```python
# Update configuration at runtime
await config.update({"debug": True}, source=ConfigSource.RUNTIME)

# Track source of each field
source = config.get_source("debug")  # ConfigSource.RUNTIME
```

### Sensitive Data Handling

```python
# Fields marked as sensitive are excluded from standard serialization
config_dict = await config.to_dict(include_sensitive=False)

# File-based secrets
# Environment: DATABASE_PASSWORD=file:///run/secrets/db_password
config = DatabaseConfig.from_env()  # Automatically reads from file
```

## Error Handling

The configuration system provides specific error types:

```python
from provide.foundation.errors.config import (
    ConfigurationError,
    ValidationError,
    NotFoundError
)

try:
    config = await loader.load(AppConfig)
    await config.validate()
except ConfigurationError as e:
    print(f"Configuration error: {e.message}")
    print(f"Error code: {e.code}")
    print(f"Context: {e.context}")
```

## Thread Safety

Configuration objects are immutable (frozen) and thread-safe. The ConfigManager uses appropriate locking for concurrent access.

## Performance Considerations

- Configuration loading is typically done at startup
- Validation can be cached for unchanged configurations
- Use `include_sensitive=False` for logging/debugging to avoid exposing secrets
- File I/O is async and can be parallelized for multiple sources

## Related Documentation

- [Environment Configuration Guide](../../guide/config/environment.md) - Environment setup
- [Configuration Files Guide](../../guide/config/files.md) - File formats and locations
- [Runtime Configuration Guide](../../guide/config/runtime.md) - Dynamic updates
- [Configuration Best Practices](../../guide/config/best-practices.md) - Recommended patterns