# Logger API Reference

The logging subsystem of provide.foundation.

## Module: `provide.foundation.logger`

The logger module provides structured logging with emoji enhancement and high performance.

## Core Classes

### `FoundationLogger`
The main logger class that provides structured logging capabilities.

```python
from provide.foundation import logger

# Basic usage
logger.info("event_occurred", user_id=123, status="success")
```

**Methods:**
- `trace(event: str, **kwargs)` - Trace level logging
- `debug(event: str, **kwargs)` - Debug level logging  
- `info(event: str, **kwargs)` - Info level logging
- `warning(event: str, **kwargs)` - Warning level logging
- `error(event: str, **kwargs)` - Error level logging
- `critical(event: str, **kwargs)` - Critical level logging
- `bind(**kwargs)` - Create child logger with additional context
- `set_level(level: str)` - Set logging level
- `get_level()` - Get current logging level

### `TelemetryConfig`
Configuration for the logging system.

```python
from provide.foundation.logger.config import TelemetryConfig

config = TelemetryConfig(
    level="INFO",
    format="json",
    no_emoji=False
)
```

**Attributes:**
- `level` - Logging level (TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `format` - Output format (json, pretty, compact, plain)
- `no_emoji` - Disable emoji in output
- `show_timestamp` - Include timestamps
- `show_location` - Include code location

## Processors

### Built-in Processors
- `TimestampProcessor` - Adds timestamp to log entries
- `EmojiProcessor` - Adds contextual emoji
- `LocationProcessor` - Adds code location info
- `ContextProcessor` - Manages context binding

### Custom Processors
Create custom processors by implementing the processor protocol:

```python
def my_processor(logger, method_name: str, event_dict: dict) -> dict:
    event_dict["custom_field"] = "value"
    return event_dict

logger.add_processor(my_processor)
```

## Configuration

### Environment Variables
- `PROVIDE_LOG_LEVEL` - Set log level
- `PROVIDE_LOG_FORMAT` - Set output format
- `PROVIDE_NO_EMOJI` - Disable emoji

### Programmatic Configuration
```python
from provide.foundation import logger

logger.set_level("DEBUG")
logger.configure(format="json", no_emoji=True)
```

## See Also

- [Base Logger](base.md) - Core logger implementation
- [Configuration](config.md) - Configuration details
- [Processors](processors.md) - Log processing pipeline
- [Emoji Matrix](emoji.md) - Emoji mapping system
- [User Guide: Logging](../../guide/logging/index.md) - Usage patterns