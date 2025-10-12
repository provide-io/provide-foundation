# CLI Framework

Build powerful command-line interfaces with provide.foundation's decorator-based CLI framework.

## Overview

The CLI framework in provide.foundation simplifies building command-line applications through:

- 🎯 **Decorator-Based Commands** - Define commands with simple decorators
- 🔧 **Type Hints Integration** - Automatic argument parsing from type annotations
- 📝 **Rich Help Generation** - Beautiful, auto-generated help text
- 🧪 **Built-in Testing Support** - Test your CLI apps easily
- 🎨 **Colorized Output** - Enhanced terminal output with color support

## Quick Start

Here's a minimal CLI application:

```python
from provide.foundation.hub import register_command, Hub
from provide.foundation import logger

@register_command
def greet(name: str, excited: bool = False):
    """Greet someone by name."""
    greeting = f"Hello, {name}{'!' if excited else '.'}"
    logger.info("greeting_sent", name=name, excited=excited)
    print(greeting)

if __name__ == "__main__":
    hub = Hub()
    cli = hub.create_cli()
    cli()
```

This creates a CLI with:
- Automatic argument parsing from the function signature
- Help text from the docstring
- Type validation
- Structured logging

Run it:
```bash
$ python app.py greet Alice --excited
Hello, Alice!
# Logs: ✅ greeting_sent name=Alice excited=True

$ python app.py greet --help
Usage: app.py greet <name> [--excited]

Greet someone by name.

Arguments:
  name        Person to greet
  --excited   Add excitement (default: False)
```

## Core Concepts

### Commands as Functions

Every CLI command is just a Python function decorated with `@register_command`. The framework:
1. Inspects the function signature to determine arguments
2. Uses type hints for validation and conversion
3. Extracts help text from docstrings
4. Handles errors gracefully with helpful messages

### Nested Commands

Build complex CLIs with command groups by using a dot (`.`) in the command name:

```python
from provide.foundation.hub import register_command

@register_command("database.migrate")
def migrate(version: str = "latest"):
    """Run database migrations."""
    logger.info("migration_started", target=version)
    # Migration logic here

@register_command("database.backup")
def backup(output: str):
    """Create database backup."""
    logger.info("backup_started", output=output)
    # Backup logic here
```

## Argument Handling

The framework supports various argument patterns:

### Positional Arguments
Required arguments derived from function parameters without defaults:

```python
@register_command
def copy(source: str, dest: str):
    """Copy from source to destination."""
    # source and dest are required positional args
```

### Optional Arguments
Parameters with defaults become optional flags:

```python
@register_command
def build(target: str, debug: bool = False, jobs: int = 4):
    """Build the target."""
    # target is required
    # --debug and --jobs are optional
```

## Output Formatting

The CLI framework includes rich output formatting:

### Colored Output
```python
from provide.foundation.console.output import pout, perr

@register_command
def status():
    """Show system status."""
    pout("✓ System OK", fg="green", bold=True)
    perr("⚠ Warning: High memory", fg="yellow")
```

## Next Steps

- 📝 [Command Registration](commands.md) - Detailed command patterns
- 🔀 [Nested Commands](nested.md) - Building command hierarchies
- 🎯 [Arguments & Options](arguments.md) - Advanced argument handling
- 🎨 [Output Formatting](output.md) - Rich terminal output
- 🧪 [Testing CLI Apps](../../api/cli/utils.md) - Testing strategies
- 🏠 [Back to User Guide](../index.md)