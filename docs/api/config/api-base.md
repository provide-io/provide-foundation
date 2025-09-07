# Base Configuration API

Base classes and interfaces for the configuration system.

## Overview

The base configuration module provides the foundational classes and interfaces for provide.foundation's configuration system. It includes:

- **Config**: Base configuration class with validation and serialization
- **ConfigLoader**: Abstract base for configuration loaders
- **ConfigError**: Base exception class for configuration-related errors
- **Validation utilities**: Schema validation and type checking

## Key Components

### Config Class

The base `Config` class provides:
- Automatic validation of configuration data
- Serialization to/from various formats (JSON, YAML, TOML)
- Environment variable integration
- Type-safe attribute access
- Immutable configuration objects

### ConfigLoader Interface

Abstract base class for implementing custom configuration loaders:
- Standardized loading interface
- Built-in caching and reload mechanisms
- Error handling and validation
- Plugin architecture support

### Validation System

Comprehensive validation system for configuration data:
- Schema-based validation
- Type checking and coercion
- Custom validator functions
- Detailed error reporting with context

## Usage Patterns

### Basic Configuration Class

```python
from provide.foundation.config.base import Config

class DatabaseConfig(Config):
    host: str = "localhost"
    port: int = 5432
    database: str
    username: str
    password: str
    
    def __post_init__(self):
        # Custom validation logic
        if not self.database:
            raise ValueError("Database name is required")
```

### Custom Loader Implementation

```python
from provide.foundation.config.base import ConfigLoader

class YAMLConfigLoader(ConfigLoader):
    def load(self, source: str) -> dict:
        with open(source, 'r') as f:
            return yaml.safe_load(f)
    
    def supports_format(self, format: str) -> bool:
        return format.lower() in ['yaml', 'yml']
```

## API Reference

::: provide.foundation.config.base