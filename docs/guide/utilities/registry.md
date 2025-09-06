# Registry System

Plugin and component registry for extensible applications.

## Overview

provide.foundation's registry system provides a powerful plugin architecture with automatic discovery, dependency management, and namespace isolation. It enables building extensible applications with modular components.

## Basic Registration

### Registering Components

Register components in the global registry:

```python
from provide.foundation.hub.registry import Registry

# Create a registry instance
registry = Registry()

# Register a component
registry.register(
    name="my_processor",
    value=DataProcessor(),
    dimension="processor",
    metadata={"version": "1.0.0", "author": "me"}
)

# Register with aliases
registry.register(
    name="csv_reader",
    value=CSVReader(),
    dimension="reader",
    aliases=["csv", "comma_separated"]
)
```

### Retrieving Components

Access registered components:

```python
# Get by exact name
processor = registry.get("my_processor", dimension="processor")

# Get by alias
reader = registry.get("csv", dimension="reader")

# Get with default
parser = registry.get(
    "json_parser",
    dimension="parser",
    default=DefaultParser()
)

# Check existence
if registry.has("my_processor", dimension="processor"):
    processor = registry.get("my_processor", dimension="processor")
```

## Dimensions

### Using Dimensions

Organize components by type:

```python
# Register in different dimensions
registry.register("json", JsonHandler(), dimension="serializer")
registry.register("json", JsonValidator(), dimension="validator")
registry.register("json", JsonSchema(), dimension="schema")

# Retrieve from specific dimension
serializer = registry.get("json", dimension="serializer")
validator = registry.get("json", dimension="validator")

# List all in dimension
serializers = registry.list_dimension("serializer")
for name, component in serializers:
    print(f"Serializer: {name}")
```

### Common Dimensions

Standard dimensions for organization:

```python
# Commands
registry.register("deploy", deploy_cmd, dimension="command")

# Plugins
registry.register("auth", AuthPlugin(), dimension="plugin")

# Handlers
registry.register("http", HttpHandler(), dimension="handler")

# Services
registry.register("database", DatabaseService(), dimension="service")

# Processors
registry.register("image", ImageProcessor(), dimension="processor")
```

## Plugin System

### Creating Plugins

Build a plugin system:

```python
from provide.foundation.registry import Registry
from abc import ABC, abstractmethod

class Plugin(ABC):
    """Base plugin interface."""
    
    @abstractmethod
    def initialize(self):
        """Initialize the plugin."""
        pass
    
    @abstractmethod
    def execute(self, *args, **kwargs):
        """Execute plugin functionality."""
        pass

class DataPlugin(Plugin):
    """Data processing plugin."""
    
    def __init__(self, name: str):
        self.name = name
    
    def initialize(self):
        logger.info(f"Initializing {self.name}")
    
    def execute(self, data):
        # Process data
        return transformed_data

# Register plugins
registry = Registry(name="plugins")
registry.register(
    "csv_processor",
    DataPlugin("CSV Processor"),
    dimension="plugin",
    metadata={"formats": ["csv", "tsv"]}
)
```

### Plugin Discovery

Auto-discover and load plugins:

```python
import importlib
import pkgutil
from pathlib import Path

def discover_plugins(package_path: Path):
    """Discover and register plugins from a package."""
    registry = Registry.get_default()
    
    # Find plugin modules
    for finder, name, ispkg in pkgutil.iter_modules([str(package_path)]):
        if name.startswith("plugin_"):
            # Import module
            module = importlib.import_module(f"plugins.{name}")
            
            # Register if it has register function
            if hasattr(module, "register"):
                plugin = module.register()
                registry.register(
                    name=plugin.name,
                    value=plugin,
                    dimension="plugin",
                    metadata=plugin.metadata
                )
                logger.info(f"Registered plugin: {plugin.name}")

# Discover all plugins
discover_plugins(Path("plugins"))

# Use discovered plugins
for name, plugin in registry.list_dimension("plugin"):
    plugin.initialize()
```

## Dependency Management

### Dependencies Between Components

Handle component dependencies:

```python
class DependencyRegistry(Registry):
    """Registry with dependency resolution."""
    
    def register_with_deps(self, name, value, dependencies=None, **kwargs):
        """Register with dependency tracking."""
        deps = dependencies or []
        
        # Check dependencies exist
        for dep in deps:
            if not self.has(dep, dimension=kwargs.get("dimension")):
                raise ValueError(f"Missing dependency: {dep}")
        
        # Register with dependency metadata
        kwargs["metadata"] = kwargs.get("metadata", {})
        kwargs["metadata"]["dependencies"] = deps
        
        self.register(name, value, **kwargs)
    
    def get_with_deps(self, name, dimension=None):
        """Get component with all dependencies."""
        component = self.get(name, dimension=dimension)
        metadata = self.get_metadata(name, dimension=dimension)
        
        deps = {}
        for dep_name in metadata.get("dependencies", []):
            deps[dep_name] = self.get(dep_name, dimension=dimension)
        
        return component, deps

# Use dependency registry
registry = DependencyRegistry()

# Register with dependencies
registry.register_with_deps(
    "app",
    Application(),
    dependencies=["database", "cache"],
    dimension="service"
)

# Get with dependencies resolved
app, deps = registry.get_with_deps("app", dimension="service")
db = deps["database"]
cache = deps["cache"]
```

## Pattern Examples

### Command Registry

Build a CLI with registered commands:

```python
from provide.foundation.registry import Registry
from provide.foundation.hub import HubManager

class CommandRegistry:
    """Registry for CLI commands."""
    
    def __init__(self):
        self.registry = Registry(name="commands")
    
    def command(self, name, **metadata):
        """Decorator to register commands."""
        def decorator(func):
            self.registry.register(
                name=name,
                value=func,
                dimension="command",
                metadata=metadata
            )
            return func
        return decorator
    
    def get_all_commands(self):
        """Get all registered commands."""
        return self.registry.list_dimension("command")

# Create command registry
cmd_registry = CommandRegistry()

# Register commands
@cmd_registry.command("deploy", aliases=["d"])
def deploy_command():
    """Deploy the application."""
    print("Deploying...")

@cmd_registry.command("test", aliases=["t"])
def test_command():
    """Run tests."""
    print("Testing...")

# Build CLI from registry
def build_cli():
    manager = HubManager(name="myapp")
    
    for name, func in cmd_registry.get_all_commands():
        metadata = cmd_registry.registry.get_metadata(name, "command")
        manager.register_command(
            name=name,
            func=func,
            aliases=metadata.get("aliases", [])
        )
    
    return manager.create_cli()
```

### Service Locator

Implement service locator pattern:

```python
from provide.foundation.registry import Registry

class ServiceLocator:
    """Central service registry."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.registry = Registry(name="services")
        return cls._instance
    
    def register_service(self, interface, implementation, **config):
        """Register service implementation."""
        self.registry.register(
            name=interface.__name__,
            value=implementation,
            dimension="service",
            metadata={"config": config, "interface": interface}
        )
    
    def get_service(self, interface):
        """Get service by interface."""
        name = interface.__name__
        service = self.registry.get(name, dimension="service")
        
        if service is None:
            raise ValueError(f"No service registered for {name}")
        
        return service
    
    def configure_services(self):
        """Configure all registered services."""
        for name, service in self.registry.list_dimension("service"):
            metadata = self.registry.get_metadata(name, "service")
            config = metadata.get("config", {})
            
            if hasattr(service, "configure"):
                service.configure(**config)

# Use service locator
locator = ServiceLocator()

# Register services
locator.register_service(
    IDatabase,
    PostgresDatabase(),
    host="localhost",
    port=5432
)

locator.register_service(
    ICache,
    RedisCache(),
    host="localhost",
    port=6379
)

# Get services anywhere
db = locator.get_service(IDatabase)
cache = locator.get_service(ICache)
```

### Extension Points

Create extension points:

```python
from provide.foundation.registry import Registry

class ExtensionPoint:
    """Defines an extension point."""
    
    def __init__(self, name: str, interface: type):
        self.name = name
        self.interface = interface
        self.registry = Registry(name=f"ext_{name}")
    
    def register(self, extension):
        """Register an extension."""
        if not isinstance(extension, self.interface):
            raise TypeError(f"Extension must implement {self.interface}")
        
        self.registry.register(
            name=extension.__class__.__name__,
            value=extension,
            dimension="extension"
        )
    
    def get_extensions(self):
        """Get all registered extensions."""
        return [
            ext for _, ext in 
            self.registry.list_dimension("extension")
        ]
    
    def execute_all(self, *args, **kwargs):
        """Execute all extensions."""
        results = []
        for extension in self.get_extensions():
            try:
                result = extension.execute(*args, **kwargs)
                results.append(result)
            except Exception as e:
                logger.error(f"Extension failed: {e}")
        return results

# Define extension points
class IValidator:
    def validate(self, data): pass

validation_point = ExtensionPoint("validation", IValidator)

# Register extensions
class EmailValidator(IValidator):
    def validate(self, data):
        return "@" in data.get("email", "")

validation_point.register(EmailValidator())

# Use extensions
def process_data(data):
    # Run all validators
    results = validation_point.execute_all(data)
    
    if all(results):
        print("Validation passed")
    else:
        print("Validation failed")
```

## Best Practices

### 1. Use Dimensions

```python
# Good: Organized by dimension
registry.register("json", JsonParser(), dimension="parser")
registry.register("json", JsonWriter(), dimension="writer")

# Bad: Flat namespace
registry.register("json_parser", JsonParser())
registry.register("json_writer", JsonWriter())
```

### 2. Include Metadata

```python
# Good: Rich metadata
registry.register(
    "my_plugin",
    plugin,
    dimension="plugin",
    metadata={
        "version": "1.0.0",
        "author": "developer",
        "dependencies": ["core"],
        "description": "Does something useful"
    }
)

# Bad: No metadata
registry.register("my_plugin", plugin)
```

### 3. Handle Missing Components

```python
# Good: Graceful handling
component = registry.get(
    "optional_component",
    dimension="feature",
    default=FallbackComponent()
)

# Bad: Assume existence
component = registry.get("optional_component")  # May be None
```

### 4. Validate on Registration

```python
# Good: Validate during registration
def register_handler(name, handler):
    if not callable(handler):
        raise TypeError("Handler must be callable")
    
    registry.register(
        name,
        handler,
        dimension="handler"
    )

# Bad: No validation
registry.register(name, handler)  # May not be valid
```

## Related Topics

- [Command Registration](../cli/commands.md) - CLI commands
- [Advanced Usage](../advanced/index.md) - Advanced patterns
- [Hub System](../../api/hub/index.md) - Hub system API