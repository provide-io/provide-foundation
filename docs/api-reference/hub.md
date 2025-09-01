# 📚 API Reference

## Hub API

The Foundation Hub module provides a unified system for registering, discovering, and managing components and CLI commands. It serves as a central coordination point for plugin-style architectures and CLI applications.

### Key Features

- **Component Registry**: Organize and discover components.
- **CLI Command Management**: Register functions as CLI commands with automatic `click` integration and support for nested commands.
- **Entry Point Discovery**: Automatically load plugins from installed packages.

### `Hub` Class

The `Hub` class is the main manager that coordinates all components and commands.

```python
from provide.foundation.hub import Hub

# Create a default hub instance
hub = Hub()
```

*   `hub.add_component(...)`: Programmatically register a component.
*   `hub.get_component(...)`: Retrieve a registered component class.
*   `hub.add_command(...)`: Programmatically register a command.
*   `hub.get_command(...)`: Retrieve a registered command function.
*   `hub.create_cli(...)`: Build a complete `click`-based CLI application from the registered commands.

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

Registers a function as a CLI command. The function's signature is automatically converted into a `click` command.

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

!!! tip "Nested Commands with Dot Notation"
    You can easily create nested commands (or `click` groups) by using a dot (`.`) in the command name. The Hub will automatically create the parent groups for you.

    ```python
    # This will create a `container` group with a `status` command.
    @register_command("container.status")
    def container_status():
        print("Container is running.")

    # This will create a `volumes` group inside `container`.
    @register_command("container.volumes.list")
    def container_volumes_list():
        print("Listing volumes...")
    ```

### Building a CLI Application

You can assemble all registered commands into a runnable CLI application with a single call.

```python
# create_cli.py
from provide.foundation.hub import Hub, register_command

@register_command("container.status")
def container_status():
    print("Container is running.")

@register_command
def status():
    """Check the top-level status."""
    print("All systems nominal.")

# Create the Hub and build the CLI
hub = Hub()
cli = hub.create_cli(name="my-app")

if __name__ == "__main__":
    cli()
```

Running this script will provide a fully-functional CLI with nested commands:

```bash
$ python create_cli.py --help
Usage: create_cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  container  Container commands.
  status     Check the top-level status.

$ python create_cli.py container --help
Usage: create_cli.py container [OPTIONS] COMMAND [ARGS]...

  Container commands.

Options:
  --help  Show this message and exit.

Commands:
  status
```

### Advanced Usage

For more advanced patterns, including lifecycle management with `BaseComponent`, multi-dimensional component organization, and plugin-based architectures, please refer to the original, detailed [**Foundation Hub Module Documentation**](../HUB.md).