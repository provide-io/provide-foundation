# CLI Framework

Build powerful command-line interfaces with provide.foundation's decorator-based CLI framework.

## Overview

The CLI framework in provide.foundation simplifies building command-line applications through:

- 🎯 **Decorator-Based Commands** - Define commands with simple decorators
- 🔧 **Type Hints Integration** - Automatic argument parsing from type annotations
- 📝 **Rich Help Generation** - Beautiful, auto-generated help text
- 🧪 **Built-in Testing Support** - Test your CLI apps easily
- 🎨 **Colorized Output** - Enhanced terminal output with color support

## Why Use This Framework?

Traditional CLI development requires boilerplate for argument parsing, help text, and command dispatch. Our framework eliminates this by using Python's type hints and decorators to automatically generate a complete CLI interface.

The framework integrates seamlessly with provide.foundation's logging system, giving you structured logs and beautiful console output out of the box.

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

### Type Safety

The framework leverages Python's type system:

```python
@register_command
def process(
    count: int,           # Validates integer input
    ratio: float,         # Converts to float
    verbose: bool = False # Boolean flag with default
):
    """Process data with specified parameters."""
    for i in range(count):
        result = i * ratio
        if verbose:
            logger.debug("processing", index=i, result=result)
```

Invalid types produce clear error messages:
```bash
$ python app.py process not-a-number
Error: Argument 'count' expects int, got 'not-a-number'
```

### Nested Commands

Build complex CLIs with command groups:

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

# Usage:
# $ python app.py database migrate
# $ python app.py database backup output.sql
```


## Command Registration

Commands can be registered in multiple ways:

### Direct Decoration
```python
@register_command
def simple_command():
    """Simplest form of command."""
    pass
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

## Error Handling

The framework provides comprehensive error handling:

### Validation Errors
Type mismatches and missing arguments produce helpful messages:
```python
@register_command
def strict(number: int, email: str):
    """Command with strict types."""
    # Framework validates inputs before calling function
```

## Testing CLI Commands

The framework includes testing utilities:

### Command Testing
```python
from provide.foundation.cli.utils import CliTestRunner

def test_greet_command():
    runner = CliTestRunner()
    result = runner.invoke(["greet", "Alice", "--excited"])

    assert result.exit_code == 0
    assert "Hello, Alice!" in result.output
```


## Integration with Logging

CLI commands integrate seamlessly with provide.foundation's logging:

### Automatic Context
```python
@register_command
def process(task_id: str):
    """Process a task."""
    # CLI framework automatically adds context
    with logger.bind(command="process", task_id=task_id):
        logger.info("processing_started")
        # All logs in this command include context
```

## Best Practices

### 1. Use Type Hints
Type hints provide validation and better help text:
```python
# Good: Clear types and validation
@register_command
def deploy(env: str, version: str, dry_run: bool = False):
    """Deploy application."""
    pass

# Avoid: No type hints
@register_command
def deploy(env, version, dry_run=False):
    pass
```

### 2. Write Clear Docstrings
Docstrings become help text:
```python
@register_command
def sync(source: str, dest: str, delete: bool = False):
    """Synchronize files between directories.

    Args:
        source: Source directory path
        dest: Destination directory path
        delete: Remove files not in source

    Examples:
        sync /data /backup
        sync /data /backup --delete
    """
```

### 3. Handle Errors Gracefully
Provide meaningful error messages:
```python
from provide.foundation.errors import CLIError

@register_command
def upload(file: str):
    """Upload a file."""
    if not Path(file).exists():
        logger.error("file_not_found", file=file)
        raise CLIError(f"File not found: {file}")
```


## Performance Considerations

The CLI framework is optimized for quick startup:

- Lazy imports: Commands are only imported when needed
- Minimal dependencies: Fast load time
- Efficient parsing: Optimized argument processing
- Smart caching: Reuses parsed command metadata

## Next Steps

- 📝 [Command Registration](commands.md) - Detailed command patterns
- 🔀 [Nested Commands](nested.md) - Building command hierarchies
- 🎯 [Arguments & Options](arguments.md) - Advanced argument handling
- 🎨 [Output Formatting](output.md) - Rich terminal output
- 🧪 [Testing CLI Apps](../../api/cli/utils.md) - Testing strategies
- 🏠 [Back to User Guide](../index.md)
