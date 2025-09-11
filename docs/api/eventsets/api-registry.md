# Event Sets Registry

Registration and discovery system for event sets.

## Overview

The EventSetRegistry provides centralized management of event set definitions, including automatic discovery, registration, and retrieval of event enrichment configurations.

## Core Classes

### EventSetRegistry

Extends Foundation's Registry to provide specialized event set management.

```python
class EventSetRegistry(Registry):
    """Registry for event set definitions using foundation Registry."""
    
    def register_event_set(self, event_set: EventSet) -> None:
        """Register an event set definition."""
        
    def get_event_set(self, name: str) -> EventSet:
        """Get a registered event set by name."""
        
    def list_event_sets(self) -> list[EventSet]:
        """Get all registered event sets."""
        
    def has_event_set(self, name: str) -> bool:
        """Check if an event set is registered."""
```

## Registry Functions

### Core Registry Access

```python
from provide.foundation.eventsets.registry import get_registry

# Get the global registry instance
registry = get_registry()

# Register an event set
registry.register_event_set(my_event_set)

# Check what's registered
event_sets = registry.list_event_sets()
print(f"Registered: {[es.name for es in event_sets]}")
```

### Event Set Discovery

```python
from provide.foundation.eventsets.registry import discover_event_sets

# Automatically discover and register event sets
discover_event_sets()

# Discovery searches for:
# - Built-in event sets in provide.foundation.eventsets.sets
# - Plugin-provided event sets via entry points
# - Dynamically registered event sets
```

## Usage Patterns

### 1. Manual Registration

```python
from provide.foundation.eventsets.types import EventSet, EventMapping, FieldMapping
from provide.foundation.eventsets.registry import get_registry

# Create event set
api_event_set = EventSet(
    name="api",
    description="API operations",
    mappings=[
        EventMapping(
            name="status",
            visual_markers={"success": "✅", "error": "❌"}
        )
    ],
    field_mappings=[
        FieldMapping(log_key="api.status", event_set_name="status")
    ]
)

# Register it
registry = get_registry()
registry.register_event_set(api_event_set)
```

### 2. Plugin-Based Registration

```python
# In your plugin's setup.py or pyproject.toml
entry_points = {
    "provide.foundation.eventsets": [
        "my_domain = mypackage.eventsets:get_event_sets"
    ]
}

# In mypackage/eventsets.py
def get_event_sets() -> list[EventSet]:
    """Return event sets for automatic discovery."""
    return [
        EventSet(name="my_domain", ...),
        EventSet(name="my_other_domain", ...)
    ]
```

### 3. Conditional Registration

```python
from provide.foundation.eventsets.registry import get_registry

registry = get_registry()

# Only register if not already present
if not registry.has_event_set("custom_api"):
    registry.register_event_set(custom_api_event_set)

# Override existing registration
try:
    registry.register_event_set(updated_event_set)
except AlreadyExistsError:
    # Handle conflict - maybe merge or replace
    pass
```

## Discovery Mechanism

The discovery system searches multiple sources:

### 1. Built-in Event Sets

```python
# Located in: provide.foundation.eventsets.sets/
# - http.py - HTTP request/response enrichment
# - database.py - Database operation enrichment  
# - system.py - System-level event enrichment
```

### 2. Entry Point Discovery

```python
# Searches for entry points under "provide.foundation.eventsets"
# Each entry point should return list[EventSet]

import pkg_resources

for entry_point in pkg_resources.iter_entry_points("provide.foundation.eventsets"):
    event_sets = entry_point.load()()
    for event_set in event_sets:
        registry.register_event_set(event_set)
```

### 3. Runtime Registration

```python
# Direct registration at runtime
from provide.foundation.eventsets.registry import get_registry

registry = get_registry()

# Can register at any time during application lifecycle
registry.register_event_set(dynamic_event_set)
```

## Error Handling

### Registration Conflicts

```python
from provide.foundation.errors.resources import AlreadyExistsError

try:
    registry.register_event_set(event_set)
except AlreadyExistsError as e:
    # Event set name already exists
    logger.warning("Event set already registered", name=event_set.name)
```

### Missing Event Sets

```python
from provide.foundation.errors.resources import NotFoundError

try:
    event_set = registry.get_event_set("nonexistent")
except NotFoundError:
    # Event set not found
    logger.error("Event set not found", name="nonexistent")
```

## Integration Example

```python
from provide.foundation import logger, setup_telemetry
from provide.foundation.eventsets.registry import discover_event_sets
from provide.foundation.eventsets.types import EventSet, EventMapping, FieldMapping

# Setup custom event set
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
    ],
    field_mappings=[
        FieldMapping(
            log_key="payment.status",
            event_set_name="payment_status"
        )
    ]
)

# Initialize system
setup_telemetry()
discover_event_sets()

# Register custom event set
from provide.foundation.eventsets.registry import get_registry
get_registry().register_event_set(custom_event_set)

# Use enriched logging
logger.info("payment_processed",
           payment_id="pay_123",
           amount=99.99,
           status="completed")  # Will show 💰 marker
```

## API Reference

::: provide.foundation.eventsets.registry

## Related Documentation

- [Event Sets Overview](api-index.md) - System overview
- [Types Documentation](api-types.md) - Core type definitions
- [Display Utilities](api-display.md) - Visualization tools