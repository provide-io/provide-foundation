# Log Processors API

Structlog processors for Foundation Telemetry log processing pipeline.

## Overview

The processors module provides the core log processing pipeline that transforms raw log events into formatted output. It handles level filtering, emoji prefixes, timestamps, and output formatting.

## Core Functions

### _build_core_processors_list(config, resolved_emoji_config)

Build the core processor pipeline for log processing.

```python
def _build_core_processors_list(
    config: TelemetryConfig, 
    resolved_emoji_config: "ResolvedEmojiConfig"
) -> list[StructlogProcessor]:
    """
    Build core processors list for structlog configuration.
    
    Args:
        config: Telemetry configuration
        resolved_emoji_config: Resolved emoji set configuration
        
    Returns:
        List of processor functions in execution order
    """
```

**Processors included:**
1. `structlog.contextvars.merge_contextvars` - Context variable merging
2. `add_log_level_custom` - Custom log level handling
3. `filter_by_level_custom` - Level-based filtering
4. `structlog.processors.StackInfoRenderer()` - Stack trace rendering
5. `structlog.dev.set_exc_info` - Exception info handling
6. Timestamp processors (configurable)
7. Service name processor (if configured)
8. Emoji processors (if enabled)

### _config_create_service_name_processor(service_name)

Create processor to add service name to log events.

```python
def _config_create_service_name_processor(
    service_name: str | None,
) -> StructlogProcessor:
    """
    Create processor that adds service_name to log events.
    
    Args:
        service_name: Service name to add, or None to skip
        
    Returns:
        Processor function
    """
```

**Example:**
```python
# Adds service_name field to all log events
processor = _config_create_service_name_processor("myapp")
```

### _config_create_timestamp_processors(omit_timestamp)

Create timestamp-related processors.

```python
def _config_create_timestamp_processors(
    omit_timestamp: bool,
) -> list[StructlogProcessor]:
    """
    Create timestamp processors based on configuration.
    
    Args:
        omit_timestamp: Whether to omit timestamps from output
        
    Returns:
        List of timestamp-related processors
    """
```

**Behavior:**
- Always adds `TimeStamper` with format `"%Y-%m-%d %H:%M:%S.%f"`
- If `omit_timestamp=True`, adds processor to remove timestamp from final output

### _config_create_emoji_processors(logging_config, resolved_emoji_config)

Create emoji prefix processors for visual log parsing.

```python
def _config_create_emoji_processors(
    logging_config: LoggingConfig, 
    resolved_emoji_config: "ResolvedEmojiConfig"
) -> list[StructlogProcessor]:
    """
    Create emoji processors based on configuration.
    
    Args:
        logging_config: Logging configuration
        resolved_emoji_config: Emoji set configuration
        
    Returns:
        List of emoji processors
    """
```

**Features:**
- Logger name emoji prefixes (if `logger_name_emoji_prefix_enabled`)
- Domain-Action-Status emoji prefixes (if `das_emoji_prefix_enabled`)
- Supports both DAS system and emoji sets
- Automatically selects appropriate emoji based on log context

## Formatter Functions

### _config_create_json_formatter_processors()

Create JSON output formatter processors.

```python
def _config_create_json_formatter_processors() -> list[StructlogProcessor]:
    """
    Create processors for JSON output formatting.
    
    Returns:
        List of JSON formatting processors
    """
```

**Output format:**
```json
{
  "timestamp": "2024-01-01 12:00:00.123456",
  "level": "INFO",
  "event": "[🚀] Application started",
  "service_name": "myapp",
  "module": "myapp.main"
}
```

### _config_create_keyvalue_formatter_processors(output_stream)

Create key-value console formatter processors.

```python
def _config_create_keyvalue_formatter_processors(
    output_stream: TextIO,
) -> list[StructlogProcessor]:
    """
    Create processors for key-value console formatting.
    
    Args:
        output_stream: Output stream for color detection
        
    Returns:
        List of key-value formatting processors
    """
```

**Features:**
- Automatic color detection based on TTY capability
- Clean key-value output format
- Exception formatting with plain tracebacks

**Output format:**
```
2024-01-01 12:00:00.123 [INFO    ] [🚀] Application started    service_name=myapp module=myapp.main
```

### _build_formatter_processors_list(logging_config, output_stream)

Build formatter processor list based on configuration.

```python
def _build_formatter_processors_list(
    logging_config: LoggingConfig, 
    output_stream: TextIO
) -> list[StructlogProcessor]:
    """
    Build formatter processors based on console_formatter setting.
    
    Args:
        logging_config: Logging configuration
        output_stream: Output stream for formatter
        
    Returns:
        List of formatter processors
    """
```

**Supported formats:**
- `"json"`: JSON output using `_config_create_json_formatter_processors()`
- `"key_value"`: Key-value output using `_config_create_keyvalue_formatter_processors()`

## Level Processing

### Level Mapping

The module defines log level to numeric mappings:

```python
_LEVEL_TO_NUMERIC: dict[LogLevelStr, int] = {
    "CRITICAL": 50,  # stdlib_logging.CRITICAL
    "ERROR": 40,     # stdlib_logging.ERROR
    "WARNING": 30,   # stdlib_logging.WARNING
    "INFO": 20,      # stdlib_logging.INFO
    "DEBUG": 10,     # stdlib_logging.DEBUG
    "TRACE": 5,      # Custom TRACE level
    "NOTSET": 0,     # stdlib_logging.NOTSET
}
```

## Emoji Processing

The emoji processors support two modes:

### Core DAS System

Processes `domain`, `action`, and `status` fields:

```python
logger.info(
    "Operation completed",
    domain="database",
    action="query", 
    status="success"
)
# Output: [🗄️][🔍][✅] Operation completed
```

### Emoji Set System

Uses custom Contextual field definitions and emoji sets:

```python
# With custom emoji sets
logger.info(
    "Request processed",
    http_method="GET",
    response_status="success"
)
# Output: [📥][✅] Request processed
```

## Usage Examples

### Basic Processor Setup

```python
from provide.foundation.logger.processors import (
    _build_core_processors_list,
    _build_formatter_processors_list
)

# Build processor pipeline
core_processors = _build_core_processors_list(config, resolved_emoji_config)
formatter_processors = _build_formatter_processors_list(config.logging, sys.stdout)

# Combine for structlog
all_processors = core_processors + formatter_processors
```

### Custom Processor Integration

```python
def custom_processor(logger, method_name, event_dict):
    """Add custom processing logic."""
    event_dict["custom_field"] = "custom_value"
    return event_dict

# Insert into pipeline
processors = _build_core_processors_list(config, resolved_emoji_config)
processors.append(custom_processor)  # Add custom processor
processors.extend(_build_formatter_processors_list(config.logging, sys.stdout))
```

## Related Documentation

- [FoundationLogger API](base.md) - Main logger interface
- [Emoji System API](emoji.md) - Visual parsing system
- [Custom Processors Guide](/guide/logging/advanced/) - Creating custom processors
- [Emoji Sets Guide](/guide/concepts/emoji-sets/) - Advanced emoji system