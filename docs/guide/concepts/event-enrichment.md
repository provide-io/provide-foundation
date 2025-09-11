# Event Enrichment

Event enrichment provides contextual enhancement of log messages through visual markers and metadata attachment.

## Overview

The event enrichment system allows you to:

- **Add visual markers** to log messages for rapid scanning
- **Attach metadata** based on field values
- **Transform values** during log processing
- **Define domain-specific** enrichment rules

## Core Concepts

### Event Sets

Event sets are collections of enrichment rules for specific domains:

```python
from provide.foundation.eventsets.types import EventSet, EventMapping

http_event_set = EventSet(
    name="http",
    description="HTTP request/response enrichment",
    mappings=[
        EventMapping(
            name="status_code",
            visual_markers={
                "200": "✅",
                "404": "❓", 
                "500": "❌"
            }
        )
    ]
)
```

### Event Mappings

Event mappings define how specific field values are enriched:

```python
from provide.foundation.eventsets.types import EventMapping, FieldMapping

# Visual markers for different states
status_mapping = EventMapping(
    name="operation_status",
    visual_markers={
        "success": "✅",
        "error": "❌",
        "pending": "🔄"
    }
)

# Field association
field_mapping = FieldMapping(
    log_key="operation.status",
    event_set_name="operation_status"
)
```

## How It Works

1. **Registration**: Event sets are registered with the system
2. **Field Matching**: Log fields are matched to enrichment rules
3. **Enhancement**: Visual markers and metadata are added
4. **Output**: Enriched logs are formatted for display

## Usage Examples

### Basic Usage

```python
from provide.foundation import logger

# Standard logging - enrichment happens automatically
logger.info("user_login", user_id="usr_123", status="success")
# Output: ✅ user_login user_id=usr_123 status=success
```

### Display Configuration

```python
from provide.foundation.eventsets import show_event_matrix

# Show current enrichment configuration
show_event_matrix()
```

### Custom Enrichment

```python
from provide.foundation.eventsets.types import EventSet, EventMapping
from provide.foundation.eventsets.registry import get_registry

# Create custom event set
custom_event_set = EventSet(
    name="payment",
    description="Payment processing events",
    mappings=[
        EventMapping(
            name="payment_status",
            visual_markers={
                "completed": "💰",
                "failed": "💸",
                "pending": "⏳"
            }
        )
    ]
)

# Register for use
registry = get_registry()
registry.register_event_set(custom_event_set)
```

## Benefits

- **Rapid Log Scanning**: Visual markers provide immediate context
- **Domain Recognition**: Quickly identify log sources and types
- **Consistent Enhancement**: Standardized enrichment across applications
- **Reduced Cognitive Load**: Less text parsing needed for log analysis

## Related Documentation

- [Event Sets API](../../api/eventsets/api-index.md) - Complete API reference
- [Structured Logging](structured-logging.md) - Core logging concepts
- [Performance](performance.md) - Performance considerations