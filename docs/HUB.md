# Foundation Hub Module Documentation

## Overview

The Foundation Hub module provides a unified system for registering, discovering, and managing components and CLI commands across the provide-io ecosystem. It serves as a central coordination point for plugin-style architectures and CLI applications.

## Key Features

- **Multi-dimensional Registry**: Organize components by type (component, resource, data_source, etc.)
- **CLI Command Management**: Register and organize CLI commands with automatic Click integration
- **Entry Point Discovery**: Automatically discover and load plugins from installed packages
- **Type-Safe Decorators**: Python 3.11+ type hints and overloads for better IDE support
- **Lifecycle Management**: Initialize and cleanup components with context manager support
- **Integration Ready**: Works seamlessly with `foundation.context`, `foundation.registry`, and `foundation.cli`

## Installation

The hub module is included with provide-foundation:

```bash
pip install provide-foundation
```

## Quick Start

### Basic Component Registration

```python
from provide.foundation.hub import register_component, Hub

@register_component("database", version="1.0.0")
class DatabaseConnection:
    """A database connection component."""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
    
    def connect(self):
        # Connection logic here
        pass

# Access the component
hub = Hub()
db_class = hub.get_component("database")
db = db_class("postgresql://localhost/mydb")
```

### Basic Command Registration

```python
from provide.foundation.hub import register_command, Hub

@register_command("greet", description="Greet someone")
def greet_command(name: str = "World", excited: bool = False):
    """Say hello to someone."""
    greeting = f"Hello, {name}!"
    if excited:
        greeting += "!!!"
    print(greeting)

# Create CLI
hub = Hub()
cli = hub.create_cli("myapp", version="1.0.0")

if __name__ == "__main__":
    cli()
```

## Component Registration

### Using the Decorator

The `@register_component` decorator supports multiple usage patterns:

```python
from provide.foundation.hub import register_component, BaseComponent

# Simple registration (uses class name)
@register_component
class SimpleComponent:
    pass

# With custom name
@register_component("custom_name")
class MyComponent:
    pass

# With full metadata
@register_component(
    "advanced_component",
    dimension="resource",
    version="2.0.0",
    author="Your Name",
    tags=["database", "postgresql"],
    description="An advanced database component"
)
class AdvancedComponent:
    pass
```

### Extending BaseComponent

For components that need lifecycle management:

```python
from provide.foundation.hub import BaseComponent, register_component

@register_component("managed_resource")
class ManagedResource(BaseComponent):
    """A resource with lifecycle management."""
    
    def _setup(self):
        """Called during initialization."""
        print("Setting up resource...")
        self.connection = self.create_connection()
    
    def _teardown(self):
        """Called during cleanup."""
        print("Cleaning up resource...")
        if self.connection:
            self.connection.close()
    
    def create_connection(self):
        # Create and return connection
        pass

# Use as context manager
with ManagedResource() as resource:
    # Resource is initialized
    pass
# Resource is cleaned up automatically
```

### Component Discovery

Discover components from Python entry points:

```python
from provide.foundation.hub import Hub

hub = Hub()

# Discover components from entry points
discovered = hub.discover_components("provide.resources")

for name, component_class in discovered.items():
    print(f"Found: {name} -> {component_class}")
```

To make your components discoverable, add entry points to your `pyproject.toml`:

```toml
[project.entry_points."provide.resources"]
my_resource = "mypackage.resources:MyResource"
another_resource = "mypackage.resources:AnotherResource"
```

## Command Registration

### Using the Decorator

The `@register_command` decorator automatically creates CLI commands:

```python
from provide.foundation.hub import register_command

# Simple command
@register_command
def status():
    """Show status."""
    print("All systems operational")

# With custom name and options
@register_command("deploy", aliases=["dp", "push"], category="deployment")
def deploy_command(
    environment: str = "staging",
    force: bool = False,
    version: str | None = None
):
    """Deploy application to environment."""
    print(f"Deploying to {environment}")
    if version:
        print(f"Version: {version}")
    if force:
        print("Force deployment enabled")

# Hidden command (not shown in help)
@register_command("secret", hidden=True)
def secret_command():
    """Secret administrative command."""
    pass
```

### Building Click Commands

The hub automatically converts registered functions to Click commands with proper options and arguments based on the function signature:

```python
from provide.foundation.hub import build_click_command

# Function parameters become Click options/arguments
@register_command("configure")
def configure(
    host: str,                    # Required argument (no default)
    port: int = 8080,            # Optional with default
    ssl: bool = False,           # Boolean flag
    config_file: str | None = None  # Optional string
):
    """Configure the application."""
    pass

# Build Click command
click_cmd = build_click_command("configure")
# Equivalent to:
# @click.command()
# @click.argument("host")
# @click.option("--port", type=int, default=8080)
# @click.option("--ssl", is_flag=True, default=False)
# @click.option("--config-file", type=str, default=None)
```

## Hub Manager

The Hub class coordinates all components and commands:

```python
from provide.foundation.hub import Hub
from provide.foundation.context import Context

# Create hub with custom context
context = Context(log_level="DEBUG", profile="development")
hub = Hub(context=context)

# Add components programmatically
hub.add_component(MyComponent, "my_component", version="1.0.0")

# Add commands programmatically
hub.add_command(my_function, "my-command", description="Do something")

# List registered items
components = hub.list_components()  # All components
commands = hub.list_commands()      # All commands

# Get specific items
component_class = hub.get_component("my_component")
command_func = hub.get_command("my-command")
```

### Creating CLI Applications

The hub can generate complete Click CLI applications:

```python
from provide.foundation.hub import Hub, register_command

# Register some commands
@register_command("init")
def init():
    """Initialize project."""
    print("Initializing...")

@register_command("build")
def build(target: str = "all"):
    """Build project."""
    print(f"Building {target}...")

@register_command("test")
def test(verbose: bool = False):
    """Run tests."""
    print("Running tests...")
    if verbose:
        print("Verbose mode enabled")

# Create CLI application
hub = Hub()
cli = hub.create_cli(
    name="myproject",
    version="1.0.0",
    help="My project CLI tool"
)

if __name__ == "__main__":
    cli()
```

This generates a CLI with:
- Automatic `--help` for all commands
- `--version` option
- Standard logging options from `foundation.cli`
- Proper error handling

### Lifecycle Management

The hub supports component lifecycle management:

```python
from provide.foundation.hub import Hub

hub = Hub()

# Initialize all components
hub.initialize()

try:
    # Use components
    pass
finally:
    # Cleanup all components
    hub.cleanup()

# Or use as context manager
with Hub() as hub:
    # Components are initialized
    pass
# Components are cleaned up
```

## Integration with Foundation Modules

### Using with foundation.context

```python
from provide.foundation.hub import Hub, register_command
from provide.foundation.context import Context
from provide.foundation.cli.decorators import pass_context

@register_command("config")
@pass_context
def config_command(ctx: Context):
    """Show configuration."""
    print(f"Log level: {ctx.log_level}")
    print(f"Profile: {ctx.profile}")
    print(f"Debug: {ctx.debug}")

hub = Hub()
cli = hub.create_cli("myapp")
```

### Using with foundation.registry

The hub uses `foundation.registry` internally, but you can provide custom registries:

```python
from provide.foundation.hub import Hub
from provide.foundation.registry import Registry

# Create custom registries
component_reg = Registry()
command_reg = Registry()

# Create hub with custom registries
hub = Hub(
    component_registry=component_reg,
    command_registry=command_reg
)
```

### Using with foundation.cli

The hub integrates with `foundation.cli` decorators and utilities:

```python
from provide.foundation.hub import register_command
from provide.foundation.cli import echo_success, echo_error
from provide.foundation.cli.decorators import error_handler

@register_command("process")
@error_handler
def process_command(file: str):
    """Process a file."""
    try:
        # Process the file
        result = process_file(file)
        echo_success(f"Processed {file}: {result}")
    except FileNotFoundError:
        echo_error(f"File not found: {file}")
        raise
```

## Advanced Usage

### Multi-Dimensional Registry

Organize components by dimension:

```python
from provide.foundation.hub import register_component, Hub

@register_component("postgres", dimension="database")
class PostgresDatabase:
    pass

@register_component("redis", dimension="cache")
class RedisCache:
    pass

@register_component("s3", dimension="storage")
class S3Storage:
    pass

hub = Hub()

# List by dimension
databases = hub.list_components(dimension="database")  # ["postgres"]
caches = hub.list_components(dimension="cache")        # ["redis"]
storage = hub.list_components(dimension="storage")     # ["s3"]
```

### Command Categories

Organize commands by category:

```python
@register_command("create", category="project")
def create_project():
    pass

@register_command("delete", category="project")
def delete_project():
    pass

@register_command("backup", category="database")
def backup_database():
    pass

@register_command("restore", category="database")
def restore_database():
    pass
```

### Plugin Architecture

Create a plugin-based architecture:

```python
# In your main application
from provide.foundation.hub import Hub

class Application:
    def __init__(self):
        self.hub = Hub()
        self.load_plugins()
    
    def load_plugins(self):
        """Load all available plugins."""
        # Discover database plugins
        self.hub.discover_components("myapp.databases")
        
        # Discover command plugins
        self.hub.discover_components("myapp.commands")
    
    def get_database(self, name: str):
        """Get a database plugin."""
        db_class = self.hub.get_component(name, dimension="database")
        if db_class:
            return db_class()
        raise ValueError(f"Unknown database: {name}")

# In a plugin package
from provide.foundation.hub import register_component

@register_component("custom_db", dimension="database")
class CustomDatabase:
    """A custom database implementation."""
    pass
```

## Testing

The hub module includes testing utilities:

```python
import pytest
from provide.foundation.hub import Hub, register_component, clear_hub

class TestMyComponents:
    def setup_method(self):
        """Clear hub before each test."""
        clear_hub()
    
    def test_component_registration(self):
        @register_component("test_component")
        class TestComponent:
            pass
        
        hub = Hub()
        component = hub.get_component("test_component")
        assert component is TestComponent
    
    def test_command_registration(self):
        from provide.foundation.hub import register_command
        
        @register_command("test")
        def test_command():
            return "test"
        
        hub = Hub()
        command = hub.get_command("test")
        assert command() == "test"
```

## Best Practices

1. **Use Type Hints**: Always use type hints for better IDE support and documentation
2. **Provide Descriptions**: Add docstrings and descriptions to components and commands
3. **Use Dimensions**: Organize components into logical dimensions
4. **Handle Lifecycle**: Extend BaseComponent for resources that need setup/teardown
5. **Test Isolation**: Use `clear_hub()` in tests to ensure isolation
6. **Version Components**: Include version information for components
7. **Document Entry Points**: Clearly document entry points for plugin discovery

## API Reference

### Decorators

- `@register_component()` - Register a component class
- `@register_command()` - Register a CLI command function

### Classes

- `Hub` - Main hub manager
- `BaseComponent` - Base class for components with lifecycle
- `ComponentInfo` - Component metadata
- `CommandInfo` - Command metadata

### Functions

- `get_hub()` - Get global hub instance
- `clear_hub()` - Clear global hub
- `discover_components()` - Discover from entry points
- `build_click_command()` - Build Click command from function

## Examples

See the `examples/hub/` directory for complete examples:
- `basic_cli.py` - Simple CLI application
- `plugin_system.py` - Plugin-based architecture
- `resource_manager.py` - Resource lifecycle management
- `multi_dimensional.py` - Multi-dimensional registry usage