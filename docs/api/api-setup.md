# Setup API

Foundation setup and initialization utilities.

## Overview

The setup module provides utilities for initializing and configuring provide.foundation in applications. It handles:

- **Application bootstrapping**: One-line setup for common configurations
- **Logger initialization**: Automatic logging setup with sensible defaults
- **Configuration loading**: Environment-based configuration discovery
- **Plugin registration**: Automatic discovery and registration of plugins
- **Development utilities**: Enhanced setup for development environments

## Key Functions

### `setup_foundation()`

Primary setup function that initializes provide.foundation with comprehensive defaults:

```python
from provide.foundation import setup_foundation

# Basic setup with defaults
setup_foundation()

# Custom configuration
setup_foundation(
    log_level="DEBUG",
    config_file="app.yaml",
    enable_tracing=True
)
```

### `setup_logging()`

Dedicated logging setup with fine-grained control:

```python
from provide.foundation.setup import setup_logging

# Quick setup
setup_logging(level="INFO")

# Advanced configuration
setup_logging(
    level="DEBUG",
    format="json",
    file="/var/log/app.log",
    enable_colors=True
)
```

### `auto_discover_config()`

Automatic configuration file discovery and loading:

```python
from provide.foundation.setup import auto_discover_config

# Discovers config files in standard locations
config = auto_discover_config()

# Custom search paths
config = auto_discover_config(
    search_paths=["/etc/myapp", "~/.config/myapp"],
    formats=["yaml", "toml", "json"]
)
```

## Setup Patterns

### Quick Start Setup

```python
#!/usr/bin/env python3
from provide.foundation import setup_foundation, logger

# One-line setup
setup_foundation()

# Your application code
logger.info("Application started")
```

### Production Setup

```python
from provide.foundation.setup import setup_foundation

# Production-ready configuration
setup_foundation(
    log_level="INFO",
    log_format="json",
    enable_metrics=True,
    enable_tracing=True,
    config_env_prefix="MYAPP"
)
```

### Development Setup

```python
from provide.foundation.setup import setup_foundation

# Development-friendly configuration
setup_foundation(
    log_level="DEBUG",
    log_format="pretty",
    enable_colors=True,
    reload_on_change=True
)
```

### Testing Setup

```python
from provide.foundation.setup import setup_foundation

# Minimal setup for tests
setup_foundation(
    log_level="WARNING",
    log_format="compact",
    disable_telemetry=True
)
```

## Configuration Options

### Environment Variables

Setup functions respect standard environment variables:

- `PROVIDE_LOG_LEVEL`: Default log level
- `PROVIDE_LOG_FORMAT`: Output format (json, pretty, compact)
- `PROVIDE_CONFIG_FILE`: Configuration file path
- `PROVIDE_DISABLE_COLORS`: Disable colored output
- `PROVIDE_ENABLE_TRACING`: Enable distributed tracing

### Configuration Files

Supported configuration file formats and locations:

- **YAML**: `app.yaml`, `config.yaml`, `.provide.yaml`
- **TOML**: `app.toml`, `pyproject.toml` (tool.provide section)
- **JSON**: `app.json`, `config.json`, `package.json` (provide section)

Standard search locations:
- Current directory
- `./config/`
- `~/.config/appname/`
- `/etc/appname/`

## API Reference

::: provide.foundation.setup