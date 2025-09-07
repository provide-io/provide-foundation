# ConfigManager API

Centralized configuration manager for handling multiple configurations with lifecycle management, validation, and runtime updates.

## Class Overview

### ConfigManager

The main configuration management class that coordinates multiple configuration objects.

```python
class ConfigManager:
    """
    Centralized configuration manager.
    
    Manages multiple configuration objects and provides a unified interface.
    """
    
    def __init__(self) -> None: ...
```

## Methods

### register(name, config, schema, loader, defaults)

Register a configuration with optional schema, loader, and defaults.

```python
async def register(
    self,
    name: str,
    config: BaseConfig | None = None,
    schema: ConfigSchema | None = None,
    loader: ConfigLoader | None = None,
    defaults: ConfigDict | None = None,
) -> None:
    """
    Register a configuration.
    
    Args:
        name: Configuration name
        config: Configuration instance
        schema: Configuration schema
        loader: Configuration loader
        defaults: Default configuration values
    """
```

**Example:**
```python
from provide.foundation.config.manager import ConfigManager
from provide.foundation.config.loader import FileConfigLoader

manager = ConfigManager()

# Register with all components
await manager.register(
    name="database",
    config=db_config,
    schema=db_schema,
    loader=FileConfigLoader("db.yaml"),
    defaults={"timeout": 30}
)
```

### unregister(name)

Remove a configuration from the manager.

```python
def unregister(self, name: str) -> None:
    """
    Unregister a configuration.
    
    Args:
        name: Configuration name
    """
```

### get(name)

Retrieve a configuration by name.

```python
async def get(self, name: str) -> BaseConfig | None:
    """
    Get a configuration by name.
    
    Args:
        name: Configuration name
        
    Returns:
        Configuration instance or None
    """
```

**Example:**
```python
db_config = await manager.get("database")
if db_config:
    print(f"Database host: {db_config.host}")
```

### set(name, config)

Store a configuration instance.

```python
async def set(self, name: str, config: BaseConfig) -> None:
    """
    Set a configuration.
    
    Args:
        name: Configuration name
        config: Configuration instance
    """
```

### load(name, config_class, loader)

Load a configuration using a registered or provided loader.

```python
async def load(
    self, name: str, config_class: type[T], loader: ConfigLoader | None = None
) -> T:
    """
    Load a configuration.
    
    Args:
        name: Configuration name
        config_class: Configuration class
        loader: Optional loader (uses registered if None)
        
    Returns:
        Configuration instance
    """
```

**Features:**
- Applies registered defaults
- Validates against registered schema
- Stores the loaded configuration
- Handles loader resolution

**Example:**
```python
# Load using registered loader
config = await manager.load("app", AppConfig)

# Load with explicit loader
file_loader = FileConfigLoader("config.json")
config = await manager.load("app", AppConfig, loader=file_loader)
```

### reload(name)

Reload a configuration from its registered loader.

```python
async def reload(self, name: str) -> BaseConfig:
    """
    Reload a configuration.
    
    Args:
        name: Configuration name
        
    Returns:
        Reloaded configuration instance
    """
```

**Example:**
```python
# Reload configuration after file changes
config = await manager.reload("app")
```

### update(name, updates, source)

Update a configuration with new values.

```python
async def update(
    self,
    name: str,
    updates: ConfigDict,
    source: ConfigSource = ConfigSource.RUNTIME,
) -> None:
    """
    Update a configuration.
    
    Args:
        name: Configuration name
        updates: Configuration updates
        source: Source of updates
    """
```

**Example:**
```python
# Runtime configuration update
await manager.update("app", {
    "debug": True,
    "log_level": "DEBUG"
}, source=ConfigSource.RUNTIME)
```

### reset(name)

Reset a configuration to its defaults.

```python
async def reset(self, name: str) -> None:
    """
    Reset a configuration to defaults.
    
    Args:
        name: Configuration name
    """
```

### list_configs()

List all registered configuration names.

```python
def list_configs(self) -> list[str]:
    """
    List all registered configurations.
    
    Returns:
        List of configuration names
    """
```

### export(name, include_sensitive)

Export a configuration as a dictionary.

```python
async def export(self, name: str, include_sensitive: bool = False) -> ConfigDict:
    """
    Export a configuration as dictionary.
    
    Args:
        name: Configuration name
        include_sensitive: Whether to include sensitive fields
        
    Returns:
        Configuration dictionary
    """
```

### export_all(include_sensitive)

Export all configurations.

```python
async def export_all(
    self, include_sensitive: bool = False
) -> dict[str, ConfigDict]:
    """
    Export all configurations.
    
    Args:
        include_sensitive: Whether to include sensitive fields
        
    Returns:
        Dictionary of all configurations
    """
```

## Global Manager Functions

The module provides convenience functions for working with a global manager instance:

### get_config(name)

Get a configuration from the global manager.

```python
async def get_config(name: str) -> BaseConfig | None:
    """
    Get a configuration from the global manager.
    
    Args:
        name: Configuration name
        
    Returns:
        Configuration instance or None
    """
```

### set_config(name, config)

Set a configuration in the global manager.

```python
async def set_config(name: str, config: BaseConfig) -> None:
    """
    Set a configuration in the global manager.
    
    Args:
        name: Configuration name
        config: Configuration instance
    """
```

### register_config(name, config, schema, loader, defaults)

Register a configuration with the global manager.

```python
async def register_config(
    name: str,
    config: BaseConfig | None = None,
    schema: ConfigSchema | None = None,
    loader: ConfigLoader | None = None,
    defaults: ConfigDict | None = None,
) -> None:
    """
    Register a configuration with the global manager.
    """
```

### load_config(name, config_class, loader)

Load a configuration using the global manager.

```python
async def load_config(
    name: str, config_class: type[T], loader: ConfigLoader | None = None
) -> T:
    """
    Load a configuration using the global manager.
    """
```

## Usage Examples

### Application Setup

```python
from provide.foundation.config.manager import ConfigManager
from provide.foundation.config.loader import FileConfigLoader, RuntimeConfigLoader
from provide.foundation.config.schema import ConfigSchema, SchemaField

# Create manager
manager = ConfigManager()

# Register application configuration
await manager.register(
    name="app",
    loader=FileConfigLoader("app.yaml"),
    schema=ConfigSchema([
        SchemaField("name", str, required=True),
        SchemaField("port", int, min_value=1000, max_value=9999),
    ]),
    defaults={"port": 8000, "debug": False}
)

# Load configuration
app_config = await manager.load("app", AppConfig)
```

### Configuration Hot Reload

```python
import asyncio

async def watch_config():
    """Watch for configuration changes and reload."""
    while True:
        try:
            # Check if config file changed (implementation specific)
            if config_file_changed():
                new_config = await manager.reload("app")
                print(f"Configuration reloaded: {new_config}")
        except Exception as e:
            print(f"Failed to reload config: {e}")
        
        await asyncio.sleep(10)  # Check every 10 seconds

# Start watching in background
asyncio.create_task(watch_config())
```

### Multi-Environment Setup

```python
# Development environment
dev_loader = MultiSourceLoader(
    FileConfigLoader("config/base.yaml"),
    FileConfigLoader("config/dev.yaml"),
    RuntimeConfigLoader(prefix="DEV"),
)

# Production environment
prod_loader = MultiSourceLoader(
    FileConfigLoader("config/base.yaml"),
    FileConfigLoader("config/prod.yaml"),
    RuntimeConfigLoader(prefix="PROD"),
)

# Register based on environment
environment = os.getenv("ENVIRONMENT", "dev")
loader = dev_loader if environment == "dev" else prod_loader

await manager.register("app", loader=loader)
config = await manager.load("app", AppConfig)
```

### Runtime Configuration Updates

```python
# Update configuration dynamically
async def update_debug_mode(enabled: bool):
    await manager.update("app", {"debug": enabled}, ConfigSource.RUNTIME)
    
    # Get updated config
    config = await manager.get("app")
    print(f"Debug mode: {config.debug}")

# Enable debug mode
await update_debug_mode(True)
```

### Configuration Validation

```python
try:
    config = await manager.load("app", AppConfig)
except ValidationError as e:
    print(f"Configuration validation failed: {e}")
    print(f"Field: {e.field_name}, Value: {e.field_value}")
    
    # Reset to defaults and try again
    await manager.reset("app")
    config = await manager.get("app")
```

## Error Handling

The ConfigManager raises specific exceptions:

```python
from provide.foundation.errors.config import ConfigurationError

try:
    config = await manager.get("nonexistent")
except ValueError as e:
    print(f"Configuration not found: {e}")

try:
    await manager.load("app", AppConfig)
except ConfigurationError as e:
    print(f"Load failed: {e.message}")
    print(f"Error code: {e.code}")
```

## Thread Safety

The ConfigManager is designed for concurrent access. All async operations are safe to call from multiple tasks simultaneously.

## Related Documentation

- [api-Configuration Base API](api-base.md) - BaseConfig and field definitions
- [api-Configuration Loaders API](api-loader.md) - Loading from various sources
- [api-Configuration Schema API](api-schema.md) - Validation and schema definition
- [Runtime Configuration Guide](../../guide/config/runtime/index.md) - Dynamic configuration updates