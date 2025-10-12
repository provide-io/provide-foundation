# Command Registration

Learn how to register and organize CLI commands using provide.foundation's hub system.

## Overview

The command registration system provides a declarative way to build CLI applications with automatic command discovery, nested groups, and metadata management. Commands are registered using the `@register_command` decorator.

## Basic Registration

### Simple Command

The simplest way to register a command:

```python
from provide.foundation.hub import register_command

@register_command
def hello():
    """Say hello."""
    print("Hello, World!")
```

### Custom Name

Specify a custom command name:

```python
@register_command("greet")
def say_hello():
    """Greet the user."""
    print("Greetings!")
```

### With Arguments

Commands can have arguments and options, which are automatically generated from the function's type hints:

```python
from provide.foundation.hub import register_command

@register_command
def greet(name: str, excited: bool = False):
    """Greet someone by name."""
    greeting = f"Hello, {name}{'!' if excited else '.'}"
    print(greeting)
```

## Command Metadata

### Aliases

Provide alternative names for commands:

```python
@register_command("status", aliases=["s", "st"])
def show_status():
    """Show application status."""
    print("Status: Running")
```

### Categories

Organize commands into logical categories:

```python
@register_command(category="database")
def migrate():
    """Run database migrations."""
    pass

@register_command(category="database")
def seed():
    """Seed the database."""
    pass
```

### Hidden Commands

Hide commands from help output (still accessible):

```python
@register_command(hidden=True)
def debug_info():
    """Internal debug command."""
    print("Debug information...")
```

## Nested Commands

Create nested command groups by using dots in the command name:

```python
@register_command("db.migrate")
def db_migrate():
    """Run database migrations."""
    print("Running migrations...")

@register_command("db.seed")
def db_seed():
    """Seed the database."""
    print("Seeding database...")
```

## Command Registry

Commands are automatically registered in the global command registry. You can access the registry to list all registered commands:

```python
from provide.foundation.hub.registry import get_command_registry

registry = get_command_registry()

for name, info in registry.list_all().items():
    print(f"{name}: {info.instance.description}")
```

## Building the CLI

Use the `Hub` class to build a Click CLI:

```python
from provide.foundation.hub import Hub

def create_cli():
    """Create the CLI application."""
    hub = Hub()
    cli = hub.create_cli()
    return cli

if __name__ == "__main__":
    cli = create_cli()
    cli()
```