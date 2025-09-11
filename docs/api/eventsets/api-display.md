# Event Sets Display

Utilities for visualizing and debugging event set configurations.

## Overview

The display module provides tools for inspecting the current event set configuration, debugging enrichment rules, and understanding how events are processed.

## Core Functions

### show_event_matrix()

Display the complete event set configuration to the console.

```python
from provide.foundation.eventsets import show_event_matrix

# Display current configuration
show_event_matrix()
```

**Output Example:**
```
Foundation Event Sets: Active Configuration
======================================================================

Registered Event Sets (3):
  ✓ http (priority: 50) - HTTP request/response enrichment
  ✓ database (priority: 40) - Database operation enrichment  
  ✓ system (priority: 30) - System-level events

Field Mappings (8):
  http.status_code → http_status (✅❌❓)
  http.method → http_method (🔍📝🗑️)
  db.operation → db_operation (🔍➕✏️🗑️)
  db.status → db_status (✅❌⏰)
  
Active Enrichment Rules:
  - HTTP status codes: 200→✅, 404→❓, 500→❌
  - Database operations: SELECT→🔍, INSERT→➕, UPDATE→✏️
  - System events: start→🚀, stop→🛑, error→❌
```

## Usage Patterns

### 1. Configuration Debugging

```python
from provide.foundation import setup_telemetry
from provide.foundation.eventsets import show_event_matrix
from provide.foundation.eventsets.registry import discover_event_sets

# Setup and discover event sets
setup_telemetry()
discover_event_sets()

# Show what's configured
show_event_matrix()
```

### 2. Development and Testing

```python
from provide.foundation.eventsets.types import EventSet, EventMapping
from provide.foundation.eventsets.registry import get_registry
from provide.foundation.eventsets import show_event_matrix

# Register test event set
test_event_set = EventSet(
    name="test",
    description="Test enrichment",
    mappings=[
        EventMapping(
            name="test_status", 
            visual_markers={"pass": "✅", "fail": "❌"}
        )
    ]
)

registry = get_registry()
registry.register_event_set(test_event_set)

# Verify registration
show_event_matrix()
```

### 3. Production Monitoring

```python
import logging
from provide.foundation.eventsets import show_event_matrix

# Log current configuration for debugging
if logging.getLogger().isEnabledFor(logging.DEBUG):
    show_event_matrix()
```

## Advanced Display Options

### Custom Display Formatting

The display system can be extended for custom output formats:

```python
from provide.foundation.eventsets.registry import get_registry
from provide.foundation.eventsets.resolver import get_resolver

def show_event_sets_json():
    """Display event sets in JSON format."""
    import json
    
    registry = get_registry()
    event_sets = registry.list_event_sets()
    
    config = {
        "event_sets": [
            {
                "name": es.name,
                "description": es.description,
                "priority": es.priority,
                "mappings": len(es.mappings),
                "field_mappings": len(es.field_mappings)
            }
            for es in event_sets
        ]
    }
    
    print(json.dumps(config, indent=2))

show_event_sets_json()
```

### Selective Display

```python
from provide.foundation.eventsets.registry import get_registry

def show_event_set_details(name: str):
    """Show details for a specific event set."""
    registry = get_registry()
    
    try:
        event_set = registry.get_event_set(name)
        print(f"Event Set: {event_set.name}")
        print(f"Description: {event_set.description}")
        print(f"Priority: {event_set.priority}")
        print(f"Mappings: {len(event_set.mappings)}")
        print(f"Field Mappings: {len(event_set.field_mappings)}")
        
        for mapping in event_set.mappings:
            print(f"  - {mapping.name}: {list(mapping.visual_markers.keys())}")
            
    except NotFoundError:
        print(f"Event set '{name}' not found")

show_event_set_details("http")
```

## Integration with Logging

The display utilities integrate with the Foundation logging system:

```python
from provide.foundation import logger
from provide.foundation.eventsets import show_event_matrix

# Log configuration state
logger.info("event_set_configuration_loaded")

# Display can be called from CLI commands
@register_command("show-events")
def show_events_command():
    """Display current event set configuration."""
    show_event_matrix()
```

## Troubleshooting

### Common Issues

1. **No Event Sets Displayed**
   ```python
   from provide.foundation.eventsets.registry import discover_event_sets
   
   # Ensure discovery has run
   discover_event_sets()
   show_event_matrix()
   ```

2. **Missing Field Mappings**
   ```python
   # Check if field mappings are properly associated
   from provide.foundation.eventsets.resolver import get_resolver
   
   resolver = get_resolver()
   resolver.resolve()  # Force resolution
   show_event_matrix()
   ```

3. **Custom Event Sets Not Showing**
   ```python
   from provide.foundation.eventsets.registry import get_registry
   
   registry = get_registry()
   print(f"Registered sets: {[es.name for es in registry.list_event_sets()]}")
   ```

## Performance Considerations

The display functions are designed for development and debugging:

- **Development**: Use freely for configuration verification
- **Production**: Consider gating behind debug flags
- **CI/CD**: Useful for validating event set registration

```python
import os
from provide.foundation.eventsets import show_event_matrix

# Only show in development
if os.getenv("ENVIRONMENT") == "development":
    show_event_matrix()
```

## API Reference

::: provide.foundation.eventsets.display

## Related Documentation

- [Event Sets Overview](api-index.md) - System overview and concepts
- [Registry API](api-registry.md) - Registration and discovery
- [Types Documentation](api-types.md) - Core type definitions