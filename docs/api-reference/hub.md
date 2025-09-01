# 📚 API Reference

## Hub API

The Foundation Hub module provides a unified system for registering, discovering, and managing components and CLI commands. It serves as a central coordination point for plugin-style architectures and CLI applications.

### Key Features

- **Component Registry**: Organize and discover components (e.g., resources, data sources).
- **CLI Command Management**: Register functions as CLI commands with automatic `click` integration.
- **Entry Point Discovery**: Automatically load plugins from installed packages.
- **Lifecycle Management**: Support for `setup` and `teardown` logic in components.

### `Hub` Class

The `Hub` class is the main manager that coordinates all components and commands.

```python
from provide.foundation.hub import Hub

# Create a default hub instance
hub = Hub()
```

#### Component Management

*   `hub.add_component(component_class, name, ...)`: Programmatically register a component.
*   `hub.get_component(name)`: Retrieve a registered component class by name.
*   `hub.list_components()`: List the names of all registered components.
*   `hub.discover_components(entry_point_group)`: Discover and load components from `setuptools` entry points.

#### Command Management

*   `hub.add_command(func, name, ...)`: Programmatically register a function as a command.
*   `hub.get_command(name)`: Retrieve a registered command function.
*   `hub.list_commands()`: List the names of all registered commands.
*   `hub.create_cli(name, ...)`: Build a complete `click`-based CLI application from the registered commands.

### Decorators

The most common way to register components and commands is via decorators.

#### `@register_component`

Registers a class as a component in the Hub.

```python
from provide.foundation.hub import register_component

@register_component("database.postgres", version="1.0.0")
class PostgresConnection:
    """A component for connecting to PostgreSQL."""
    def connect(self):
        pass
```

#### `@register_command`

Registers a function as a CLI command. The function's signature (parameters, type hints, and docstring) is automatically converted into a `click` command with arguments, options, and help text.

```python
from provide.foundation.hub import register_command

@register_command("greet", description="A command to greet someone.")
def greet_command(name: str = "World", excited: bool = False):
    """This docstring becomes the command's help text."""
    greeting = f"Hello, {name}!"
    if excited:
        greeting += "!!!"
    print(greeting)
```

### Building a CLI Application

You can assemble all registered commands into a runnable CLI application with a single call.

```python
# create_cli.py
from provide.foundation.hub import Hub, register_command

# Register one or more commands...
@register_command
def status():
    """Check the status of the application."""
    print("All systems nominal.")

# Create the Hub and build the CLI
hub = Hub()
cli = hub.create_cli(
    name="my-app",
    version="1.0.0",
    help="A sample application CLI."
)

if __name__ == "__main__":
    cli()
```

Running this script will provide a fully-functional CLI:

```bash
$ python create_cli.py --help
Usage: create_cli.py [OPTIONS] COMMAND [ARGS]...

  A sample application CLI.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  status  Check the status of the application.

$ python create_cli.py status
All systems nominal.
```

### Advanced Usage

For more advanced patterns, including lifecycle management with `BaseComponent`, multi-dimensional component organization, and plugin-based architectures, please refer to the original, detailed [**Foundation Hub Module Documentation**](../HUB.md).
