# Emoji System API

Visual log parsing system that provides emoji-enhanced log messages for rapid visual scanning.

## Overview

The emoji system transforms log events into visually parseable messages using emoji prefixes. It supports Domain-Action-Status (DAS) patterns and semantic layer configurations.

## Core Emoji Mappings

### PRIMARY_EMOJI

Domain-level emoji mappings for the DAS system.

```python
PRIMARY_EMOJI: dict[str, str] = {
    "system": "⚙️",
    "server": "🛎️", 
    "client": "🙋",
    "network": "🌐",
    "security": "🔐",
    "config": "🔩",
    "database": "🗄️",
    "cache": "💾",
    "task": "🔄",
    "plugin": "🔌",
    "telemetry": "🛰️",
    "di": "💉",
    "protocol": "📡",
    "file": "📄",
    "user": "👤",
    "test": "🧪",
    "utils": "🧰",
    "core": "🌟",
    "auth": "🔑",
    "entity": "🦎",
    "report": "📈", 
    "payment": "💳",
    "default": "❓",
}
```

### SECONDARY_EMOJI

Action-level emoji mappings for the DAS system.

```python
SECONDARY_EMOJI: dict[str, str] = {
    "init": "🌱",
    "start": "🚀",
    "stop": "🛑", 
    "connect": "🔗",
    "disconnect": "💔",
    "listen": "👂",
    "send": "📤",
    "receive": "📥",
    "read": "📖",
    "write": "📝",
    "process": "⚙️",
    "validate": "🛡️",
    "execute": "▶️",
    "query": "🔍",
    "update": "🔄",
    "delete": "🗑️",
    "login": "➡️",
    "logout": "⬅️",
    "auth": "🔑",
    "error": "🔥",
    "encrypt": "🛡️",
    "decrypt": "🔓",
    "parse": "🧩",
    "transmit": "📡",
    "build": "🏗️",
    "schedule": "📅",
    "emit": "📢",
    "load": "💡",
    "observe": "🧐",
    "request": "🗣️",
    "interrupt": "🚦",
    "register": "⚙️",
    "default": "❓",
}
```

### TERTIARY_EMOJI

Status-level emoji mappings for the DAS system.

```python
TERTIARY_EMOJI: dict[str, str] = {
    "success": "✅",
    "failure": "❌",
    "error": "🔥",
    "warning": "⚠️", 
    "info": "ℹ️",
    "debug": "🐞",
    "trace": "👣",
    "attempt": "⏳",
    "retry": "🔁",
    "skip": "⏭️",
    "complete": "🏁",
    "timeout": "⏱️",
    "notfound": "❓",
    "unauthorized": "🚫",
    "invalid": "💢",
    "cached": "🎯",
    "ongoing": "🏃",
    "idle": "💤",
    "ready": "👍",
    "default": "➡️",
}
```

## Functions

### show_emoji_matrix()

Display the active emoji configuration to the console.

```python
def show_emoji_matrix() -> None:
    """
    Prints the active Foundation emoji logging contract to the console.
    If semantic layers are active, it displays their configuration.
    Otherwise, it displays the core DAS emoji mappings.
    Activated by FOUNDATION_SHOW_EMOJI_MATRIX environment variable.
    """
```

**Activation:**
```bash
export FOUNDATION_SHOW_EMOJI_MATRIX=true
python your_app.py  # Will display emoji matrix on startup
```

**Output Examples:**

Core DAS system output:
```
Foundation Telemetry: DAS Emoji Contract
======================================================================
Primary Emojis ('domain' key):
  ⚙️  -> System
  🗄️  -> Database
  🌐  -> Network
  ...

Secondary Emojis ('action' key):
  🚀  -> Start
  🔍  -> Query
  ✅  -> Success
  ...

Tertiary Emojis ('status' key):
  ✅  -> Success
  ❌  -> Failure
  ⚠️  -> Warning
  ...
```

Semantic layers output:
```
Foundation Telemetry: Active Semantic Layer Emoji Contract
======================================================================
Active Semantic Field Definitions (Order determines prefix sequence):

Field 1:
  Log Key: 'http_method'
  Desc: HTTP request method
  Type: str
  Emoji Set: 'http_methods'

Field 2:
  Log Key: 'status_code'
  Emoji Set: 'http_status'

======================================================================
Available Emoji Sets (Referenced by Semantic Field Definitions):

  Emoji Set: 'http_methods' (Default Key: 'unknown')
    📥  -> Get
    📤  -> Post
    🔄  -> Put
    🗑️  -> Delete
    
  Emoji Set: 'http_status' (Default Key: 'unknown')
    ✅  -> Success
    ⚠️  -> Warning
    ❌  -> Error
```

## Usage Examples

### Core DAS System

```python
from provide.foundation.logger import logger

# Domain-Action-Status logging
logger.info(
    "User authentication completed",
    domain="auth",
    action="login", 
    status="success"
)
# Output: [🔑][➡️][✅] User authentication completed

logger.error(
    "Database connection failed",
    domain="database",
    action="connect",
    status="failure"
)
# Output: [🗄️][🔗][❌] Database connection failed
```

### Semantic Layers

With custom semantic layers configured:

```python
logger.info(
    "API request processed",
    http_method="GET",
    response_status="success",
    endpoint="/users"
)
# Output: [📥][✅] API request processed    endpoint=/users
```

### Mixed Usage

```python
# Logger name emoji (automatic)
log = logger.get_logger("myapp.database")
log.info("Connection established")
# Output: [🗄️] Connection established

# Combined with DAS
log.info(
    "Query executed",
    domain="database",
    action="query",
    status="success",
    table="users"
)
# Output: [🗄️][🔍][✅] Query executed    table=users
```

## Environment Variables

### FOUNDATION_SHOW_EMOJI_MATRIX

Enable emoji matrix display on startup.

```bash
export FOUNDATION_SHOW_EMOJI_MATRIX=true
# or
export FOUNDATION_SHOW_EMOJI_MATRIX=1
# or  
export FOUNDATION_SHOW_EMOJI_MATRIX=yes
```

### Emoji Control

Control emoji behavior through configuration:

```bash
export FOUNDATION_DISABLE_EMOJI=true          # Disable all emoji
export FOUNDATION_DISABLE_DAS_EMOJI=true     # Disable DAS emoji only
export FOUNDATION_DISABLE_LOGGER_EMOJI=true  # Disable logger name emoji only
```

## Helper Functions

### _format_emoji_set_for_display(emoji_set)

Format emoji set for console display.

```python
def _format_emoji_set_for_display(emoji_set: CustomDasEmojiSet) -> list[str]:
    """
    Format emoji set for display in show_emoji_matrix().
    
    Args:
        emoji_set: Custom emoji set to format
        
    Returns:
        List of formatted display lines
    """
```

### _format_field_definition_for_display(field_def)

Format semantic field definition for console display.

```python
def _format_field_definition_for_display(field_def: SemanticFieldDefinition) -> str:
    """
    Format semantic field definition for display.
    
    Args:
        field_def: Field definition to format
        
    Returns:
        Formatted display string
    """
```

## Integration with Processors

The emoji system integrates with the log processors to automatically add emoji prefixes:

1. **Logger Name Processing**: Adds emoji based on logger name patterns
2. **DAS Processing**: Processes `domain`, `action`, `status` fields 
3. **Semantic Processing**: Uses custom field definitions and emoji sets
4. **Fallback**: Uses default emoji when specific mappings not found

## Performance Considerations

- Emoji processing adds minimal overhead (~microseconds per log event)
- Emoji mappings are loaded once at startup
- String concatenation is optimized for common cases
- Can be completely disabled via configuration for maximum performance

## Related Documentation

- [Semantic Layers Guide](/guide/concepts/semantic-layers/) - Advanced emoji configuration
- [Log Processors API](processors.md) - Processing pipeline
- [Performance Guide](/guide/concepts/performance/) - Optimization strategies
- [Configuration Guide](/guide/config/environment/) - Environment setup