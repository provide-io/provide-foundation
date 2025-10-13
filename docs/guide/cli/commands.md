# Command Registration

Learn how to register and organize CLI commands using provide.foundation's hub system.

## Related API Reference

For detailed API documentation, see:
- [CLI Decorators API](../../api/cli/api-decorators.md) - Command registration decorators
- [CLI Utils API](../../api/cli/api-utils.md) - CLI utility functions
- [Hub Commands API](../../api/hub/api-commands.md) - Command management
- [Hub Registry API](../../api/hub/api-registry.md) - Component registry

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

# Command will be available as: myapp hello
```

### Custom Name

Specify a custom command name:

```python
@register_command("greet")
def say_hello():
    """Greet the user."""
    print("Greetings!")

# Command will be available as: myapp greet
```

### With Arguments

Commands can have arguments and options via Click:

```python
import click
from provide.foundation.hub import register_command

@register_command
@click.argument('name')
@click.option('--greeting', default='Hello')
def greet(name, greeting):
    """Greet someone by name."""
    print(f"{greeting}, {name}!")

# Usage: myapp greet Alice --greeting Hi
```

## Command Metadata

### Aliases

Provide alternative names for commands:

```python
@register_command("status", aliases=["s", "st"])
def show_status():
    """Show application status."""
    print("Status: Running")

# All these work:
# myapp status
# myapp s
# myapp st
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

# Commands are grouped in help output by category
```

### Hidden Commands

Hide commands from help output (still accessible):

```python
@register_command(hidden=True)
def debug_info():
    """Internal debug command."""
    print("Debug information...")

# Won't appear in: myapp --help
# But still works: myapp debug-info
```

## Nested Commands

### Using Dot Notation

Create nested command groups using dots:

```python
@register_command("db.migrate")
def db_migrate():
    """Run database migrations."""
    print("Running migrations...")

@register_command("db.seed")
def db_seed():
    """Seed the database."""
    print("Seeding database...")

@register_command("db.backup.create")
def db_backup_create():
    """Create a database backup."""
    print("Creating backup...")

# Creates this structure:
# myapp db migrate
# myapp db seed
# myapp db backup create
```

### Explicit Groups

Define groups with custom descriptions:

```python
@register_command("db", group=True, description="Database management commands")
def database_group():
    """Database operations."""
    pass

@register_command("db.migrate")
def migrate():
    """Run migrations."""
    pass

# The group description appears in help output
```

## Command Registry

### Default Registry

Commands are automatically registered in the global registry:

```python
from provide.foundation.hub import get_command_registry

# Get the default registry
registry = get_command_registry()

# List all registered commands
for name, info in registry.list_commands():
    print(f"{name}: {info.description}")
```

### Custom Registry

Use a custom registry for isolated command sets:

```python
from provide.foundation.registry import Registry
from provide.foundation.hub import register_command

# Create custom registry
my_registry = Registry(name="custom_commands")

@register_command(registry=my_registry)
def custom_command():
    """A command in a custom registry."""
    pass
```

## Building the CLI

### Automatic CLI Creation

Use the hub manager to build a Click CLI:

```python
from provide.foundation.hub import HubManager

def create_cli():
    """Create the CLI application."""
    manager = HubManager(
        name="myapp",
        description="My Application CLI"
    )

    # Auto-discover and register all commands
    cli = manager.create_cli()
    return cli

if __name__ == "__main__":
    cli = create_cli()
    cli()
```

### With Configuration

Configure the CLI with options:

```python
from provide.foundation.hub import HubManager
from provide.foundation.cli import logging_options

def create_cli():
    manager = HubManager(
        name="myapp",
        add_help_option=True,
        add_version_option="1.0.0"
    )

    # Add global options to all commands
    manager.add_global_decorator(logging_options)

    return manager.create_cli()
```

## Advanced Patterns

### Command Replacement

Replace existing commands:

```python
# Original command
@register_command("deploy")
def deploy_v1():
    """Deploy version 1."""
    pass

# Replace it
@register_command("deploy", replace=True)
def deploy_v2():
    """Deploy version 2 (improved)."""
    pass
```

### Dynamic Registration

Register commands programmatically:

```python
from provide.foundation.hub import get_command_registry

def create_dynamic_command(name: str):
    def command():
        print(f"Dynamic command: {name}")

    # Register dynamically
    registry = get_command_registry()
    registry.register(
        name=f"dynamic.{name}",
        func=command,
        description=f"Dynamic {name} command"
    )

# Create commands at runtime
for i in range(3):
    create_dynamic_command(f"cmd{i}")
```

### Plugin Commands

Load commands from plugins:

```python
from provide.foundation.hub import get_command_registry
import importlib

def load_plugin_commands(plugin_name: str):
    """Load commands from a plugin module."""
    try:
        module = importlib.import_module(f"plugins.{plugin_name}")
        # Plugin registers its commands on import
        print(f"Loaded plugin: {plugin_name}")
    except ImportError:
        print(f"Plugin not found: {plugin_name}")

# In plugin file (plugins/extra.py):
from provide.foundation.hub import register_command

@register_command("plugin.hello")
def plugin_hello():
    """Hello from plugin."""
    print("Plugin says hello!")
```

## Best Practices

1. **Use Dot Notation**: Organize related commands with dots (e.g., `db.migrate`)
2. **Provide Descriptions**: Always include docstrings for help text
3. **Group Related Commands**: Use categories or nested groups
4. **Add Aliases**: Provide short aliases for frequently used commands
5. **Hide Internal Commands**: Mark debug/internal commands as hidden
6. **Use Type Hints**: Add type hints for better IDE support

## Complete Example

Here's a complete CLI application:

```python
#!/usr/bin/env python
"""Example CLI application."""

import click
from provide.foundation.hub import register_command, HubManager
from provide.foundation.cli import logging_options, output_options
from provide.foundation import logger

# Database commands
@register_command("db.migrate")
@click.option('--dry-run', is_flag=True, help='Show what would be migrated')
def db_migrate(dry_run):
    """Run database migrations."""
    if dry_run:
        logger.info("Would run migrations (dry run)")
    else:
        logger.info("Running migrations...")
        # Migration logic here

@register_command("db.seed")
@click.option('--count', type=int, default=10, help='Number of records')
def db_seed(count):
    """Seed the database with test data."""
    logger.info(f"Seeding {count} records...")
    # Seeding logic here

# API commands
@register_command("api.serve", aliases=["serve"])
@click.option('--port', type=int, default=8000)
@click.option('--host', default='127.0.0.1')
def api_serve(port, host):
    """Start the API server."""
    logger.info(f"Starting server on {host}:{port}")
    # Server logic here

# Utility commands
@register_command("version", aliases=["v"])
def show_version():
    """Show application version."""
    print("MyApp v1.0.0")

def main():
    """Main entry point."""
    manager = HubManager(
        name="myapp",
        description="My Application CLI"
    )

    # Add global options
    manager.add_global_decorator(logging_options)
    manager.add_global_decorator(output_options)

    # Create and run CLI
    cli = manager.create_cli()
    cli()

if __name__ == "__main__":
    main()
```

## Related Topics

- [Arguments & Options](arguments.md) - Handling command arguments
- [Nested Commands](nested.md) - Building command hierarchies
- [Output Formatting](output.md) - Formatting command output