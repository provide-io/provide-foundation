# Hub Manager API

Component management and lifecycle operations.

## Overview

The hub manager coordinates component lifecycles, manages dependencies, and provides centralized control over all registered components.

## Key Responsibilities

- **Component Registration** - Register and catalog components
- **Lifecycle Management** - Start, stop, and restart components  
- **Dependency Resolution** - Manage component dependencies
- **Configuration Management** - Apply configuration to components
- **Health Monitoring** - Monitor component health and status

## Usage Example

```python
from provide.foundation.hub import HubManager

manager = HubManager()

# Register components
manager.register(DatabaseService())
manager.register(AuthPlugin())

# Start all components
await manager.start_all()

# Stop specific component
await manager.stop('database')
```

## API Reference

::: provide.foundation.hub.manager