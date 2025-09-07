# Hub Components API

Component registration, discovery, and lifecycle management.

## Overview

The hub components system provides a unified way to register, discover, and manage components in provide.foundation applications. Components can be:

- **CLI commands** - Discoverable command-line interfaces
- **Services** - Background services and workers  
- **Plugins** - Extensible functionality modules
- **Middleware** - Request/response processing components
- **Utilities** - Shared utility functions and classes

## Key Features

- **Automatic Discovery** - Components are automatically found and registered
- **Lifecycle Management** - Proper initialization and cleanup
- **Dependency Resolution** - Components can depend on other components
- **Configuration Integration** - Components can be configured via settings
- **Hot Reloading** - Components can be reloaded during development

## Component Types

### Service Components
Long-running background services:
```python
from provide.foundation.hub import register_component

@register_component(type="service")
class DatabaseService:
    async def start(self):
        # Initialize database connection
        pass
    
    async def stop(self):
        # Cleanup database connection
        pass
```

### Command Components
CLI command registration:
```python
@register_component(type="command")
def migrate_database():
    """Migrate database to latest schema."""
    # Migration logic
    pass
```

### Plugin Components  
Extensible plugin system:
```python
@register_component(type="plugin")
class AuthPlugin:
    def __init__(self, config):
        self.config = config
    
    def process_request(self, request):
        # Authentication logic
        return request
```

## API Reference

::: provide.foundation.hub.components