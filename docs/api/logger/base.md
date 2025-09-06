# Logger Base API

The logger base module provides the main logging interface for provide.foundation, with thread-safe initialization and standardized logging methods.

## Overview

The base logger module exports the core logging components:

- **FoundationLogger**: Main logging class with lazy initialization
- **logger**: Global logger instance for direct use
- **get_logger()**: Factory function for creating named loggers  
- **setup_logging()**: Simple logging configuration function

## Usage Patterns

### Direct Logger Usage

```python
from provide.foundation.logger import logger

# Direct logging with the global instance
logger.info("Application started", version="1.0.0")
logger.debug("Processing request", request_id=12345)
logger.error("Operation failed", error="Connection timeout")
```

### Named Logger Creation

```python
from provide.foundation.logger import get_logger

# Create module-specific logger
log = get_logger(__name__)
log.info("Module initialized", module=__name__)

# Create domain-specific logger
db_log = get_logger("database")
db_log.debug("Query executed", query="SELECT * FROM users", duration_ms=45)
```

### Simple Setup

```python
from provide.foundation.logger import setup_logging

# Basic setup for development
setup_logging(level="DEBUG")

# Production setup with JSON output
setup_logging(level="INFO", json_logs=True, log_file="/var/log/app.log")
```

## Key Features

- **Lazy Initialization**: Logger setup occurs on first use to avoid import-time side effects
- **Thread Safety**: All operations use proper locking for concurrent access
- **Emoji Enhancement**: Visual log parsing with contextual emojis
- **Structured Output**: Built on structlog for consistent structured logging
- **Flexible Configuration**: Support for various output formats and destinations

## API Reference

::: provide.foundation.logger.base