# Event Sets API

Event enrichment system for structured logging with contextual field enhancement and visual parsing.

## Overview

The Event Sets system provides event-driven enrichment for structured logging, replacing the previous emoji system with a more flexible and powerful approach. Event sets allow you to:

- **Enrich log events** with contextual metadata and visual markers
- **Map field values** to visual indicators for rapid log scanning
- **Define domain-specific** enrichment rules for different technologies
- **Transform field values** during log processing

## Core Components

- [Types](api-types.md) - Core type definitions (EventSet, EventMapping, FieldMapping)
- [Registry](api-registry.md) - Event set registration and discovery system
- [Display](api-display.md) - Utilities for visualizing event configurations

## Quick Start

### Using Built-in Event Sets

```python
from provide.foundation import logger
from provide.foundation.eventsets import show_event_matrix

# Use structured logging - event sets enhance automatically
logger.info("user_login", user_id="usr_123", method="oauth", status="success")
logger.error("database_query", table="users", operation="SELECT", error="timeout")

# Display current event set configuration
show_event_matrix()
```

### Creating Custom Event Sets

```python
from provide.foundation.eventsets.types import EventSet, EventMapping, FieldMapping

# Define visual markers for different states
status_mapping = EventMapping(
    name="api_status",
    visual_markers={
        "success": "✅",
        "error": "❌", 
        "pending": "🔄",
        "timeout": "⏰"
    }
)

# Define field mappings
field_mappings = [
    FieldMapping(
        log_key="api.status",
        description="API call status",
        event_set_name="api_status"
    )
]

# Create event set
api_event_set = EventSet(
    name="api",
    description="API operation enrichment",
    mappings=[status_mapping],
    field_mappings=field_mappings,
    priority=100
)

# Register the event set
from provide.foundation.eventsets.registry import get_registry
registry = get_registry()
registry.register_event_set(api_event_set)
```

## Architecture

Event sets work through a pipeline:

1. **Registration** - Event sets are registered with the registry
2. **Discovery** - System automatically discovers available event sets
3. **Resolution** - Field mappings are resolved to enrichment rules
4. **Processing** - Log events are enriched during processing
5. **Output** - Enhanced events are formatted with visual markers

## Integration with Logging

Event sets integrate seamlessly with the Foundation logging system:

```python
from provide.foundation import logger, setup_telemetry

# Setup with event enrichment enabled
setup_telemetry()

# Log with structured fields - enrichment happens automatically
logger.info("payment_processed", 
           amount=100.50, 
           currency="USD", 
           status="success",
           gateway="stripe")
```

## API Reference

::: provide.foundation.eventsets

## Related Documentation

- [Structured Logging Guide](../../guide/logging/index.md) - Core logging concepts
- [Configuration Guide](../../guide/config/index.md) - System configuration
- [Testing Guide](../../guide/testing.md) - Testing event enrichment