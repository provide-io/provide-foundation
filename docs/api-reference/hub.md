# Hub API

The `provide.foundation.hub` module provides a centralized component management system for registering and discovering commands, services, and other components.

## Overview

The Hub is a singleton pattern that provides:
- Global component registry
- Command registration and discovery
- Service location
- Plugin management
- Thread-safe operations
- Component metadata storage

## Quick Start

```python
from provide.foundation.hub import get_hub

# Get the global hub instance
hub = get_hub()

# Register a command
@hub.register_command("deploy")
def deploy_command():
    """Deploy the application."""
    print("Deploying...")

# Register a service
hub.register_service("database", DatabaseService)

# Get registered components
command = hub.get_command("deploy")
service = hub.get_service("database")
```

## Core Components

### The Global Hub

The Hub is accessed through the `get_hub()` function which returns the singleton instance:

```python
from provide.foundation.hub import get_hub

hub = get_hub()

# The hub is a singleton - always returns the same instance
hub2 = get_hub()
assert hub is hub2
```

### Command Registration

Register CLI commands for discovery and execution:

```python
from provide.foundation.hub import get_hub

hub = get_hub()

# Register a simple command
@hub.register_command("hello")
def hello_command(name="World"):
    """Say hello."""
    print(f"Hello, {name}!")

# Register with metadata
hub.register_command(
    "deploy",
    deploy_function,
    metadata={
        "category": "deployment",
        "requires_auth": True,
        "description": "Deploy to production"
    }
)

# Register with aliases
hub.register_command(
    "remove",
    remove_function,
    aliases=["rm", "delete", "del"]
)
```

### Service Registration

Register services for dependency injection:

```python
from provide.foundation.hub import get_hub

hub = get_hub()

# Register a service class
class DatabaseService:
    def connect(self):
        return "Connected to database"

hub.register_service("database", DatabaseService)

# Register a singleton instance
db_instance = DatabaseService()
hub.register_service("db_singleton", db_instance, singleton=True)

# Register with factory function
def create_cache():
    return CacheService(ttl=300)

hub.register_service("cache", create_cache, factory=True)
```

### Component Discovery

Find and retrieve registered components:

```python
# Get a specific command
deploy_cmd = hub.get_command("deploy")
if deploy_cmd:
    deploy_cmd()

# List all commands
commands = hub.list_commands()
for name in commands:
    print(f"Command: {name}")

# Get command with metadata
entry = hub.get_command_entry("deploy")
if entry:
    print(f"Command: {entry.name}")
    print(f"Category: {entry.metadata.get('category')}")
    print(f"Auth required: {entry.metadata.get('requires_auth')}")

# Get services
db = hub.get_service("database")
if db:
    connection = db.connect()
```

## Component Organization

### Using Namespaces

Organize components with namespaces:

```python
hub = get_hub()

# Register namespaced commands
hub.register_command("db.migrate", migrate_command)
hub.register_command("db.backup", backup_command)
hub.register_command("db.restore", restore_command)

# Register namespaced services
hub.register_service("cache.redis", RedisCache)
hub.register_service("cache.memcached", MemcachedCache)
hub.register_service("cache.local", LocalCache)

# List by namespace
db_commands = hub.list_namespace("db")
cache_services = hub.list_namespace("cache")
```

### Categories and Tags

Use metadata for categorization:

```python
# Register with categories
hub.register_command(
    "deploy",
    deploy_function,
    metadata={"category": "deployment", "tags": ["production", "critical"]}
)

hub.register_command(
    "test",
    test_function,
    metadata={"category": "testing", "tags": ["ci", "quality"]}
)

# Find by category
deployment_cmds = hub.find_by_metadata("category", "deployment")
testing_cmds = hub.find_by_metadata("category", "testing")

# Find by tags
critical_cmds = hub.find_by_tag("critical")
ci_cmds = hub.find_by_tag("ci")
```

## Plugin System

Build a plugin system using the Hub:

```python
from provide.foundation.hub import get_hub
import importlib
import pkgutil

class PluginSystem:
    def __init__(self):
        self.hub = get_hub()
    
    def load_plugins(self, package):
        """Load all plugins from a package."""
        # Import the package
        pkg = importlib.import_module(package)
        
        # Walk through all modules
        for importer, modname, ispkg in pkgutil.iter_modules(pkg.__path__):
            full_modname = f"{package}.{modname}"
            module = importlib.import_module(full_modname)
            
            # Look for plugin registration
            if hasattr(module, "register_plugin"):
                module.register_plugin(self.hub)
    
    def get_plugin(self, name):
        """Get a loaded plugin."""
        return self.hub.get_service(f"plugin.{name}")

# Example plugin module (my_plugins/example.py)
def register_plugin(hub):
    """Register this plugin with the hub."""
    hub.register_service(
        "plugin.example",
        ExamplePlugin,
        metadata={"version": "1.0.0", "author": "dev@example.com"}
    )

class ExamplePlugin:
    def execute(self):
        return "Plugin executed!"

# Use the plugin system
plugins = PluginSystem()
plugins.load_plugins("my_plugins")

example = plugins.get_plugin("example")
if example:
    result = example.execute()
```

## Dependency Injection

Use the Hub for dependency injection:

```python
from provide.foundation.hub import get_hub

hub = get_hub()

# Register dependencies
hub.register_service("config", ConfigService)
hub.register_service("database", DatabaseService)
hub.register_service("cache", CacheService)

class Application:
    def __init__(self):
        self.hub = get_hub()
        self.config = self.hub.get_service("config")
        self.db = self.hub.get_service("database")
        self.cache = self.hub.get_service("cache")
    
    def run(self):
        # Use injected services
        settings = self.config.load()
        self.db.connect(settings.db_url)
        self.cache.initialize(settings.cache_ttl)

# Alternative: decorator-based injection
def inject_services(*service_names):
    def decorator(cls):
        original_init = cls.__init__
        
        def new_init(self, *args, **kwargs):
            hub = get_hub()
            for name in service_names:
                setattr(self, name, hub.get_service(name))
            original_init(self, *args, **kwargs)
        
        cls.__init__ = new_init
        return cls
    return decorator

@inject_services("config", "database", "cache")
class MyService:
    def process(self):
        # self.config, self.database, self.cache are injected
        data = self.database.query("SELECT * FROM users")
        self.cache.set("users", data)
```

## Thread Safety

All Hub operations are thread-safe:

```python
import threading
from provide.foundation.hub import get_hub

hub = get_hub()

def register_in_thread(thread_id):
    for i in range(100):
        hub.register_command(
            f"cmd_{thread_id}_{i}",
            lambda: print(f"Command from thread {thread_id}")
        )

# Safe concurrent registration
threads = []
for i in range(10):
    t = threading.Thread(target=register_in_thread, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# All 1000 commands registered safely
print(f"Total commands: {len(hub.list_commands())}")
```

## Testing with Hub

### Isolated Hub for Testing

```python
import pytest
from provide.foundation.hub import Hub

@pytest.fixture
def test_hub():
    """Create an isolated hub for testing."""
    return Hub()

def test_command_registration(test_hub):
    @test_hub.register_command("test")
    def test_command():
        return "test"
    
    cmd = test_hub.get_command("test")
    assert cmd() == "test"

def test_service_registration(test_hub):
    class TestService:
        def get_data(self):
            return "data"
    
    test_hub.register_service("test_service", TestService)
    service = test_hub.get_service("test_service")
    assert service.get_data() == "data"
```

### Mocking Hub Components

```python
from unittest.mock import Mock, patch

def test_with_mock_hub():
    mock_hub = Mock()
    mock_service = Mock()
    mock_service.process.return_value = "processed"
    
    mock_hub.get_service.return_value = mock_service
    
    with patch('provide.foundation.hub.get_hub', return_value=mock_hub):
        hub = get_hub()
        service = hub.get_service("processor")
        result = service.process()
        
        assert result == "processed"
        mock_hub.get_service.assert_called_with("processor")
```

## Advanced Patterns

### Service Locator Pattern

```python
from provide.foundation.hub import get_hub

class ServiceLocator:
    """Service locator using the Hub."""
    
    def __init__(self):
        self.hub = get_hub()
        self._cache = {}
    
    def get(self, service_type):
        """Get or create a service instance."""
        if service_type not in self._cache:
            service_class = self.hub.get_service(service_type)
            if service_class:
                self._cache[service_type] = service_class()
        return self._cache.get(service_type)
    
    def register(self, service_type, service_class):
        """Register a service type."""
        self.hub.register_service(service_type, service_class)
        # Clear cache for this type
        self._cache.pop(service_type, None)

# Usage
locator = ServiceLocator()
locator.register("email", EmailService)
locator.register("sms", SMSService)

email = locator.get("email")
email.send("user@example.com", "Hello!")
```

### Event System

```python
from provide.foundation.hub import get_hub

class EventBus:
    """Event bus using the Hub."""
    
    def __init__(self):
        self.hub = get_hub()
    
    def on(self, event_name, handler):
        """Register an event handler."""
        handlers = self.hub.get_service(f"event.{event_name}") or []
        handlers.append(handler)
        self.hub.register_service(f"event.{event_name}", handlers, replace=True)
    
    def emit(self, event_name, *args, **kwargs):
        """Emit an event to all handlers."""
        handlers = self.hub.get_service(f"event.{event_name}") or []
        for handler in handlers:
            handler(*args, **kwargs)

# Usage
bus = EventBus()

# Register handlers
bus.on("user.login", lambda user: print(f"User {user} logged in"))
bus.on("user.login", lambda user: log_login(user))
bus.on("user.logout", lambda user: print(f"User {user} logged out"))

# Emit events
bus.emit("user.login", "alice@example.com")
bus.emit("user.logout", "bob@example.com")
```

## Best Practices

1. **Use descriptive names**:
   ```python
   # Good
   hub.register_command("database.migrate")
   hub.register_service("cache.redis")
   
   # Less clear
   hub.register_command("dbm")
   hub.register_service("cr")
   ```

2. **Include metadata**:
   ```python
   hub.register_command(
       "deploy",
       deploy_function,
       metadata={
           "description": "Deploy to production",
           "requires": ["auth", "vpn"],
           "risk": "high"
       }
   )
   ```

3. **Handle missing components gracefully**:
   ```python
   service = hub.get_service("optional_service")
   if service:
       service.process()
   else:
       # Use fallback or skip
       print("Optional service not available")
   ```

4. **Use namespaces for organization**:
   ```python
   # Organize related components
   hub.register_command("user.create", create_user)
   hub.register_command("user.delete", delete_user)
   hub.register_command("user.list", list_users)
   ```

5. **Clean up in tests**:
   ```python
   def test_with_hub():
       hub = Hub()  # Isolated hub
       # Test code
       # No cleanup needed - hub is garbage collected
   ```

## API Reference

### Functions

- `get_hub()` - Get the global Hub singleton instance

### Hub Methods

- `register_command(name, func, **kwargs)` - Register a command
- `register_service(name, service, **kwargs)` - Register a service
- `get_command(name)` - Get a registered command
- `get_service(name)` - Get a registered service
- `list_commands()` - List all command names
- `list_services()` - List all service names
- `remove_command(name)` - Remove a command
- `remove_service(name)` - Remove a service
- `clear()` - Clear all registrations

## See Also

- [CLI Framework](cli.md) - Command-line interface system
- [Registry](registry.md) - Lower-level registry implementation
- [Configuration](config.md) - Configuration management