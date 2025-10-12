# Registry System

Plugin and component registry for extensible applications.

## Overview

`provide.foundation`'s registry system provides a powerful plugin architecture with automatic discovery, dependency management, and namespace isolation. It enables building extensible applications with modular components.

## Basic Registration

### Registering Components

Register components in a registry:

```python
from provide.foundation.hub.registry import Registry

# Create a registry instance
registry = Registry()

# Register a component
registry.register(
    "my_processor",
    instance=DataProcessor(),
    dimension="processor",
    metadata={"version": "1.0.0", "author": "me"}
)
```

### Retrieving Components

Access registered components:

```python
# Get by exact name
processor = registry.get("my_processor", dimension="processor")

# Check existence
if "my_processor" in registry:
    processor = registry.get("my_processor", dimension="processor")
```

## Dimensions

### Using Dimensions

Organize components by type:

```python
# Register in different dimensions
registry.register("json", JsonHandler(), dimension="serializer")
registry.register("json", JsonValidator(), dimension="validator")

# Retrieve from specific dimension
serializer = registry.get("json", dimension="serializer")
validator = registry.get("json", dimension="validator")

# List all in dimension
serializers = registry.list_dimension("serializer")
for name, component in serializers:
    print(f"Serializer: {name}")
```

## Related Topics

- [Command Registration](../cli/commands.md) - CLI commands
- [Hub System](../../api/reference/provide/foundation/hub/index.md) - Hub system API