# Registry API

The `provide.foundation.Registry` class provides a thread-safe, multi-dimensional registry for storing and retrieving objects.

## Overview

The Registry is a flexible storage system that:
- Organizes items by dimensions (categories)
- Supports aliases for items
- Provides thread-safe operations
- Stores metadata with items
- Allows iteration and querying

## Quick Start

```python
from provide.foundation import Registry

# Create a registry
reg = Registry()

# Register items in different dimensions
reg.register("postgres", PostgresDriver, dimension="database")
reg.register("mysql", MySQLDriver, dimension="database")
reg.register("json", JSONFormatter, dimension="formatter")

# Retrieve items
postgres = reg.get("postgres", dimension="database")
formatter = reg.get("json")  # Searches all dimensions

# Use aliases
reg.register("pg", PostgresDriver, dimension="database", aliases=["postgresql"])
assert reg.get("postgresql") == PostgresDriver
```

## Core Methods

### `register(name, value, **kwargs)`

Register an item in the registry.

**Parameters:**
- `name: str` - Unique name within the dimension
- `value: Any` - The item to register
- `dimension: str = "default"` - Category for organization
- `metadata: dict[str, Any] | None` - Optional metadata
- `aliases: list[str] | None` - Alternative names
- `replace: bool = False` - Allow replacing existing items

**Returns:** `RegistryEntry` object

**Raises:** `AlreadyExistsError` if name exists and `replace=False`

**Example:**
```python
# Simple registration
reg.register("redis", RedisCache, dimension="cache")

# With metadata
reg.register(
    "s3",
    S3Storage,
    dimension="storage",
    metadata={"region": "us-west-2", "version": "2.0"}
)

# With aliases
reg.register(
    "postgresql",
    PostgresDB,
    dimension="database",
    aliases=["pg", "postgres"]
)

# Replace existing
reg.register("redis", NewRedisCache, dimension="cache", replace=True)
```

### `get(name, dimension=None)`

Retrieve an item from the registry.

**Parameters:**
- `name: str` - Name or alias of the item
- `dimension: str | None` - Specific dimension to search

**Returns:** The registered value or `None` if not found

**Example:**
```python
# Get from specific dimension
cache = reg.get("redis", dimension="cache")

# Search all dimensions
item = reg.get("postgres")

# Get by alias
db = reg.get("pg")  # Returns PostgresDB if "pg" is an alias
```

### `get_entry(name, dimension=None)`

Get the full registry entry with metadata.

**Parameters:** Same as `get()`

**Returns:** `RegistryEntry` object or `None`

**Example:**
```python
entry = reg.get_entry("s3")
if entry:
    print(f"Name: {entry.name}")
    print(f"Dimension: {entry.dimension}")
    print(f"Metadata: {entry.metadata}")
    storage_class = entry.value
```

### `list_dimension(dimension)`

List all items in a dimension.

**Parameters:**
- `dimension: str` - Dimension to list

**Returns:** `list[str]` of item names

**Example:**
```python
databases = reg.list_dimension("database")
# ["postgres", "mysql", "sqlite"]
```

### `list_all()`

List all dimensions and their items.

**Returns:** `dict[str, list[str]]`

**Example:**
```python
all_items = reg.list_all()
# {
#     "database": ["postgres", "mysql"],
#     "cache": ["redis", "memcached"],
#     "storage": ["s3", "gcs"]
# }
```

### `remove(name, dimension=None)`

Remove an item from the registry.

**Parameters:**
- `name: str` - Item name
- `dimension: str | None` - Specific dimension

**Returns:** `bool` - True if removed, False if not found

**Example:**
```python
# Remove from specific dimension
removed = reg.remove("redis", dimension="cache")

# Remove first match from any dimension
removed = reg.remove("postgres")
```

### `clear(dimension=None)`

Clear the registry or a specific dimension.

**Parameters:**
- `dimension: str | None` - Dimension to clear, or None for all

**Example:**
```python
# Clear specific dimension
reg.clear(dimension="cache")

# Clear entire registry
reg.clear()
```

## Special Methods

### `__contains__`

Check if an item exists.

```python
# Check by name
if "postgres" in reg:
    print("Postgres is registered")

# Check by dimension and name
if ("database", "mysql") in reg:
    print("MySQL is in database dimension")
```

### `__iter__`

Iterate over all entries.

```python
for entry in reg:
    print(f"{entry.dimension}/{entry.name}: {entry.value}")
```

### `__len__`

Get total number of items.

```python
count = len(reg)
print(f"Registry contains {count} items")
```

## Thread Safety

All registry operations are thread-safe:

```python
import threading

reg = Registry()

def register_items(thread_id):
    for i in range(100):
        reg.register(f"item_{thread_id}_{i}", f"value_{i}")

# Safe concurrent registration
threads = [
    threading.Thread(target=register_items, args=(i,))
    for i in range(10)
]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

## Use Cases

### Plugin System

```python
class PluginRegistry:
    def __init__(self):
        self.reg = Registry()
    
    def register_plugin(self, name, plugin_class, **metadata):
        self.reg.register(
            name,
            plugin_class,
            dimension="plugin",
            metadata=metadata
        )
    
    def get_plugin(self, name):
        return self.reg.get(name, dimension="plugin")
    
    def list_plugins(self):
        return self.reg.list_dimension("plugin")
```

### Command Registry

```python
from provide.foundation import Registry

command_registry = Registry()

def register_command(name, func, aliases=None):
    command_registry.register(
        name,
        func,
        dimension="command",
        aliases=aliases,
        metadata={"help": func.__doc__}
    )

@register_command("deploy", aliases=["d", "dep"])
def deploy_command():
    """Deploy the application"""
    pass

# Execute command
cmd = command_registry.get("d")  # Works with alias
if cmd:
    cmd()
```

### Service Locator

```python
class ServiceLocator:
    def __init__(self):
        self.services = Registry()
    
    def register(self, interface, implementation, singleton=False):
        instance = implementation() if singleton else implementation
        self.services.register(
            interface.__name__,
            instance,
            dimension="service",
            metadata={"singleton": singleton}
        )
    
    def get(self, interface):
        entry = self.services.get_entry(interface.__name__)
        if entry and not entry.metadata.get("singleton"):
            return entry.value()  # Create new instance
        return entry.value if entry else None
```

## Best Practices

1. **Use dimensions for organization**:
   ```python
   reg.register("json", JSONHandler, dimension="serializer")
   reg.register("json", JSONValidator, dimension="validator")
   ```

2. **Store metadata for configuration**:
   ```python
   reg.register(
       "api_v2",
       APIHandlerV2,
       metadata={"version": "2.0", "deprecated": False}
   )
   ```

3. **Use aliases for convenience**:
   ```python
   reg.register(
       "postgresql",
       PostgresDriver,
       aliases=["pg", "postgres", "psql"]
   )
   ```

4. **Check existence before registration**:
   ```python
   if "myitem" not in reg:
       reg.register("myitem", MyClass)
   ```

5. **Handle missing items gracefully**:
   ```python
   handler = reg.get("handler") or DefaultHandler
   ```

## See Also

- [Hub](hub.md) - Higher-level component management
- [CLI Framework](cli.md) - Command registration system