# Hub System API

Centralized component and command management system for building extensible applications with plugin-like architecture.

## Overview

The Hub system provides:

- **Component Registration** - Decorator-based component registration with metadata
- **Command Management** - Automatic CLI generation from registered functions  
- **Plugin Discovery** - Entry point-based plugin discovery
- **Registry Pattern** - Centralized registration and retrieval system
- **Lifecycle Management** - Component initialization and cleanup

## Core Concepts

### Components vs Commands

- **Components** - Classes that provide functionality (services, resources, utilities)
- **Commands** - Functions that can be exposed as CLI commands

### Registration Dimensions

The Hub uses registry dimensions to organize different types of registrations:
- `"component"` - General components and services
- `"command"` - CLI commands and functions
- Custom dimensions for specialized use cases

### Discovery Mechanisms

1. **Direct Registration** - Hub-based registration using `hub.add_component()` and `@register_command`
2. **Entry Point Discovery** - Automatic discovery from installed packages
3. **Programmatic Registration** - Runtime registration via Hub methods

## Quick Start

### Basic Component Registration

```python
from provide.foundation.hub import Hub

class DatabaseService:
    """Database connection service."""
    
    def __init__(self, name: str):
        self.name = name
        self.connection = None
        
    def __enter__(self):
        self.connection = create_connection()
        return self
        
    def __exit__(self, *args):
        self.connection.close()

    def query(self, sql: str):
        return self.connection.execute(sql)

# Register and use the component
hub = Hub()
hub.add_component(DatabaseService, name="database", version="1.0.0")

db_class = hub.get_component("database")
with db_class("mydb") as db:
    results = db.query("SELECT * FROM users")
```

### Command Registration

```python
from provide.foundation.hub.commands import register_command

@register_command("init")
def initialize_project(name: str, template: str = "basic"):
    """Initialize a new project."""
    print(f"Creating project '{name}' with template '{template}'")

@register_command("deploy")  
def deploy_application(environment: str, dry_run: bool = False):
    """Deploy application to environment."""
    action = "would deploy" if dry_run else "deploying"
    print(f"{action.title()} to {environment}")
```

### Hub Integration

```python
from provide.foundation.hub.manager import Hub

# Create hub
hub = Hub()

# Add components and commands
hub.add_component(DatabaseService, "db")
hub.add_command(initialize_project, "init")
hub.add_command(deploy_application, "deploy")

# Create CLI
cli = hub.create_cli("myapp", version="1.0.0")

# Run CLI
if __name__ == "__main__":
    cli()
```

## API Modules

### [Hub Manager](manager.md)
Central coordination class for components and commands with lifecycle management.

### [Components](components.md)
Component registration system with decorator support and plugin discovery.

### [Registry](registry.md)  
Core registry pattern implementation for storing and retrieving registered items.

### [Commands](commands.md)
Command registration and Click CLI integration with automatic parameter detection.

## Usage Patterns

### Plugin Architecture

```python
# Define plugin interface
class PluginInterface:
    def process(self, data):
        raise NotImplementedError

# Define plugins
class JsonProcessor(PluginInterface):
    def process(self, data):
        return json.dumps(data)

class XmlProcessor(PluginInterface):
    def process(self, data):
        return dicttoxml(data)

# Register and use plugins
hub = Hub()
hub.add_component(JsonProcessor, name="json_plugin", dimension="plugin")
hub.add_component(XmlProcessor, name="xml_plugin", dimension="plugin")

# Or discover from entry points
plugins = hub.discover_components("myapp.plugins", dimension="plugin")

for name, plugin_class in plugins.items():
    plugin = plugin_class()
    result = plugin.process({"key": "value"})
    print(f"{name}: {result}")
```

### Service Container

```python
from provide.foundation.hub.manager import get_hub

# Define services
class LoggerService:
    def get_logger(self, name: str):
        return logging.getLogger(name)

class ConfigService:
    def get(self, key: str, default=None):
        return os.getenv(key, default)

# Register services
hub = get_hub()
hub.add_component(LoggerService, name="logger_service")
hub.add_component(ConfigService, name="config_service")

# Use as service container
hub = get_hub()

# Get services
logger_service = hub.get_component("logger_service")
config_service = hub.get_component("config_service")

# Use services
logger = logger_service().get_logger(__name__)
debug_mode = config_service().get("DEBUG", False)
```

### CLI Application with Nested Commands

```python
@register_command("database.migrate")
def database_migrate(revision: str = "head"):
    """Run database migrations."""
    print(f"Migrating to {revision}")

@register_command("database.seed")
def database_seed(fixture: str = "basic"):
    """Seed database with test data.""" 
    print(f"Seeding with {fixture} fixture")

@register_command("server.start")
def server_start(port: int = 8000, debug: bool = False):
    """Start development server."""
    mode = "debug" if debug else "production"
    print(f"Starting server on port {port} in {mode} mode")

@register_command("server.stop")
def server_stop():
    """Stop development server."""
    print("Stopping server")

# Creates nested command structure:
# myapp database migrate [--revision]
# myapp database seed [--fixture]  
# myapp server start [--port] [--debug]
# myapp server stop

hub = Hub()
cli = hub.create_cli("myapp")

if __name__ == "__main__":
    cli()
```

### Entry Point Discovery

**setup.py or pyproject.toml:**
```toml
[project.entry-points."myapp.components"]
redis_service = "myapp_redis:RedisService"
postgres_service = "myapp_postgres:PostgresService"

[project.entry-points."myapp.commands"]
backup = "myapp_backup:backup_command"
restore = "myapp_backup:restore_command"
```

**Application code:**
```python
hub = Hub()

# Discover and register components
components = hub.discover_components("myapp.components")
commands = hub.discover_components("myapp.commands", dimension="command")

print(f"Discovered {len(components)} components")
print(f"Discovered {len(commands)} commands")

# Create CLI with all discovered commands
cli = hub.create_cli("myapp")
```

### Advanced Component Lifecycle

```python
class AdvancedService:
    """Service with complex lifecycle."""
    
    def __init__(self, name: str, **config):
        self.name = name
        self.config = config
        self.connections = []
        self.background_tasks = []
    
    def __enter__(self):
        # Initialize connections
        self.db = create_db_connection(self.config.get("database_url"))
        self.redis = create_redis_connection(self.config.get("redis_url"))
        
        # Start background tasks
        self.background_tasks.append(start_metrics_collector())
        return self
        
    def __exit__(self, *args):
        # Stop background tasks
        for task in self.background_tasks:
            task.stop()
            
        # Close connections
        if hasattr(self, "db"):
            self.db.close()
        if hasattr(self, "redis"):
            self.redis.close()

# Register and use with hub
hub = Hub()
hub.add_component(AdvancedService, name="advanced_service")

service_class = hub.get_component("advanced_service")
with service_class("myservice", 
                  database_url="postgresql://localhost/app",
                  redis_url="redis://localhost:6379") as service:
    # Service is initialized here
    service.do_work()
    # Service is cleaned up automatically
```

## Error Handling

Hub operations can raise several types of exceptions:

```python
from provide.foundation.errors.resources import AlreadyExistsError
from provide.foundation.errors.config import ValidationError

try:
    hub.add_component(MyService, "existing_name")
except AlreadyExistsError as e:
    print(f"Component already exists: {e.message}")

try:
    hub.add_command(invalid_function, "bad_command")
except ValidationError as e:
    print(f"Invalid command: {e.message}")
    print(f"Context: {e.context}")
```

## Thread Safety

The Hub system is designed for concurrent access:

- Registry operations are thread-safe
- Component lifecycle methods should be idempotent
- Global hub instance uses double-checked locking

## Performance Considerations

- Component registration is typically done at startup
- Plugin discovery can be expensive - consider caching results
- CLI creation builds command structure once - reuse the CLI object
- Component initialization is lazy by default

## Testing

```python
from provide.foundation.hub.manager import Hub, clear_hub

def test_component_registration():
    # Use local hub for testing
    hub = Hub()
    
    class TestService:
        def get_value(self):
            return "test"
    
    # Register and test component
    hub.add_component(TestService, name="test_service")
    service_class = hub.get_component("test_service")
    service_class = hub.get_component("test")
    assert service_class == TestService
    
    # Test instantiation
    service = service_class()
    assert service.get_value() == "test"

def test_command_cli():
    from provide.foundation.cli.testing import isolated_cli_runner
    
    hub = Hub()
    
    @register_command("greet")
    def greet_command(name: str = "World"):
        print(f"Hello, {name}!")
    
    hub.add_command(greet_command, "greet")
    cli = hub.create_cli("test-cli")
    
    with isolated_cli_runner() as runner:
        result = runner.invoke(cli, ["greet", "--name", "Alice"])
        assert result.exit_code == 0
        assert "Hello, Alice!" in result.output

def teardown():
    # Clear global state between tests
    clear_hub()
```

## Related Documentation

- [Components API](components.md) - Component registration patterns
- [CLI Framework Guide](../../guide/cli/index.md) - CLI development with Hub  
- [Advanced Usage Guide](../../guide/advanced/index.md) - Plugin patterns
- [Registry Utils Guide](../../guide/utilities/registry.md) - Registry system patterns