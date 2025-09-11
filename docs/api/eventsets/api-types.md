# Event Sets Types

Core type definitions for the event enrichment system.

## Overview

The event sets type system provides structured definitions for event enrichment configuration, field mappings, and visual markers.

## Core Types

### EventMapping

Maps specific values to visual markers and metadata for a particular field.

```python
@define(frozen=True, slots=True)
class EventMapping:
    """Individual event enrichment mapping for a specific domain."""
    
    name: str                                          # Unique identifier
    visual_markers: dict[str, str] = field(factory=lambda: {})      # Value -> emoji/marker
    metadata_fields: dict[str, dict[str, Any]] = field(factory=lambda: {})  # Value -> metadata
    transformations: dict[str, Callable[[Any], Any]] = field(factory=lambda: {})  # Value transformers
    default_key: str = field(default="default")       # Fallback key
```

**Example:**
```python
http_status_mapping = EventMapping(
    name="http_status",
    visual_markers={
        "200": "✅",
        "404": "❓", 
        "500": "❌",
        "default": "🌐"
    },
    metadata_fields={
        "200": {"level": "info", "category": "success"},
        "500": {"level": "error", "category": "server_error"}
    }
)
```

### FieldMapping

Associates a log field with an event mapping for enrichment.

```python
@define(frozen=True, slots=True)
class FieldMapping:
    """Maps a log field to an event set for enrichment."""
    
    log_key: str                                       # Field key in log events
    description: str | None = field(default=None)     # Human-readable description
    value_type: str | None = field(default=None)      # Expected value type
    event_set_name: str | None = field(default=None)  # EventSet name to use
    default_override_key: str | None = field(default=None)  # Override default key
    default_value: Any | None = field(default=None)   # Default if field missing
```

**Example:**
```python
status_field = FieldMapping(
    log_key="http.status_code",
    description="HTTP response status code",
    value_type="int",
    event_set_name="http_status",
    default_value=200
)
```

### EventSet

Complete event enrichment domain definition.

```python
@define(frozen=True, slots=True)
class EventSet:
    """Complete event enrichment domain definition."""
    
    name: str                                          # Unique identifier
    description: str | None = field(default=None)     # Human-readable description
    mappings: list[EventMapping] = field(factory=lambda: [])    # Event mappings
    field_mappings: list[FieldMapping] = field(factory=lambda: [])  # Field associations
    priority: int = field(default=0, converter=int)   # Processing priority
```

**Example:**
```python
http_event_set = EventSet(
    name="http",
    description="HTTP request/response enrichment",
    mappings=[http_status_mapping, http_method_mapping],
    field_mappings=[status_field, method_field],
    priority=50
)
```

## Type Usage Patterns

### 1. Status Enrichment

```python
# Define status indicators
status_mapping = EventMapping(
    name="operation_status",
    visual_markers={
        "success": "✅",
        "failure": "❌",
        "pending": "🔄",
        "cancelled": "🚫"
    }
)

# Map to fields
status_field = FieldMapping(
    log_key="operation.status",
    event_set_name="operation_status"
)
```

### 2. Multi-Domain Enrichment

```python
# Database operations
db_event_set = EventSet(
    name="database",
    description="Database operation enrichment",
    mappings=[
        EventMapping(name="db_operation", visual_markers={
            "SELECT": "🔍", "INSERT": "➕", "UPDATE": "✏️", "DELETE": "🗑️"
        }),
        EventMapping(name="db_status", visual_markers={
            "success": "✅", "error": "❌", "timeout": "⏰"
        })
    ],
    field_mappings=[
        FieldMapping(log_key="db.operation", event_set_name="db_operation"),
        FieldMapping(log_key="db.status", event_set_name="db_status")
    ]
)
```

### 3. Value Transformations

```python
# Transform numeric status codes to categories
status_transformer = EventMapping(
    name="http_categories",
    visual_markers={
        "success": "✅",
        "client_error": "🚫", 
        "server_error": "❌"
    },
    transformations={
        "status_code": lambda code: (
            "success" if 200 <= code < 300
            else "client_error" if 400 <= code < 500
            else "server_error" if 500 <= code < 600
            else "unknown"
        )
    }
)
```

## API Reference

::: provide.foundation.eventsets.types

## Related Documentation

- [Event Sets Overview](api-index.md) - System overview and quick start
- [Registry API](api-registry.md) - Registration and discovery
- [Configuration Guide](../../guide/config/index.md) - Configuration patterns