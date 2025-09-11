# Runtime Configuration

Dynamic configuration management and runtime updates.

## Overview

Runtime configuration allows applications to update their configuration during execution without requiring restarts. The foundation provides several mechanisms for runtime configuration management:

- **Environment Variable Updates**: Update configuration by changing environment variables
- **Configuration File Reloading**: Reload configuration from updated files
- **Context Updates**: Programmatically update context configuration

## Basic Runtime Updates

### Environment Variable Updates

```python
from provide.foundation import Context

# Initial context
ctx = Context.from_env()

# Update environment and reload
import os
os.environ['FOUNDATION_LOG_LEVEL'] = 'DEBUG'
ctx.update_from_env()
```

### Programmatic Updates

```python
# Update context programmatically
ctx.debug = True
ctx.log_level = "DEBUG"

# Apply changes to logging system
setup_telemetry()
```

### Configuration File Updates

```python
# Reload configuration from file
ctx.load_config("updated_config.yaml")
```