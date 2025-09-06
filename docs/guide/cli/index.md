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
from provide.foundation.cli import cli, command
from provide.foundation import logger

@command
def greet(name: str, excited: bool = False):
    """Greet someone by name."""
    greeting = f"Hello, {name}{'!' if excited else '.'}"
    logger.info("greeting_sent", name=name, excited=excited)
    print(greeting)

if __name__ == "__main__":
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

Every CLI command is just a Python function decorated with `@command`. The framework:
1. Inspects the function signature to determine arguments
2. Uses type hints for validation and conversion
3. Extracts help text from docstrings
4. Handles errors gracefully with helpful messages

### Type Safety

The framework leverages Python's type system:

```python
@command
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
from provide.foundation.cli import group

@group("database")
class DatabaseCommands:
    """Database management commands."""
    
    @command
    def migrate(self, version: str = "latest"):
        """Run database migrations."""
        logger.info("migration_started", target=version)
        # Migration logic here
    
    @command
    def backup(self, output: str):
        """Create database backup."""
        logger.info("backup_started", output=output)
        # Backup logic here

# Usage:
# $ python app.py database migrate
# $ python app.py database backup output.sql
```

### Global Options

Define options that apply to all commands:

```python
@cli.option("--verbose", "-v", help="Enable verbose output")
@cli.option("--config", "-c", help="Config file path")
def setup_globals(verbose: bool = False, config: str = None):
    """Configure global settings before command execution."""
    if verbose:
        logger.set_level("DEBUG")
    if config:
        load_config(config)
```

## Command Registration

Commands can be registered in multiple ways:

### Direct Decoration
```python
@command
def simple_command():
    """Simplest form of command."""
    pass
```

### Explicit Registration
```python
def my_function():
    """Regular function."""
    pass

cli.register(my_function, name="custom-name")
```

### Auto-Discovery
```python
# Automatically find and register commands in a module
cli.discover("myapp.commands")
```

## Argument Handling

The framework supports various argument patterns:

### Positional Arguments
Required arguments derived from function parameters without defaults:

```python
@command
def copy(source: str, dest: str):
    """Copy from source to destination."""
    # source and dest are required positional args
```

### Optional Arguments
Parameters with defaults become optional flags:

```python
@command
def build(target: str, debug: bool = False, jobs: int = 4):
    """Build the target."""
    # target is required
    # --debug and --jobs are optional
```

### Variable Arguments
Support for *args and **kwargs:

```python
@command
def run(script: str, *args, **options):
    """Run a script with arguments."""
    # Can accept: run script.py arg1 arg2 --opt1=val1 --opt2=val2
```

## Output Formatting

The CLI framework includes rich output formatting:

### Tables
```python
from provide.foundation.cli import Table

@command
def list_users():
    """List all users."""
    table = Table(["ID", "Name", "Email"])
    table.add_row(["1", "Alice", "alice@example.com"])
    table.add_row(["2", "Bob", "bob@example.com"])
    table.render()
```

### Progress Bars
```python
from provide.foundation.cli import progress_bar

@command
def process_files(directory: str):
    """Process all files in directory."""
    files = Path(directory).glob("*")
    for file in progress_bar(files, desc="Processing"):
        process_file(file)
```

### Colored Output
```python
from provide.foundation.cli import style

@command
def status():
    """Show system status."""
    print(style("✓ System OK", fg="green", bold=True))
    print(style("⚠ Warning: High memory", fg="yellow"))
    print(style("✗ Error: Service down", fg="red"))
```

## Error Handling

The framework provides comprehensive error handling:

### Validation Errors
Type mismatches and missing arguments produce helpful messages:
```python
@command
def strict(number: int, email: str):
    """Command with strict types."""
    # Framework validates inputs before calling function
```

### Custom Validation
Add custom validators:
```python
from provide.foundation.cli import validate

@command
@validate("port", lambda p: 1 <= p <= 65535, "Port must be 1-65535")
def serve(port: int = 8080):
    """Start server on specified port."""
    pass
```

### Exception Handling
Graceful error handling with logging:
```python
@command
def risky():
    """Command that might fail."""
    try:
        dangerous_operation()
    except SpecificError as e:
        logger.error("operation_failed", error=str(e))
        raise cli.Exit(1, "Operation failed: see logs")
```

## Testing CLI Commands

The framework includes testing utilities:

### Command Testing
```python
from provide.foundation.cli.testing import CliRunner

def test_greet_command():
    runner = CliRunner()
    result = runner.invoke(greet, ["Alice", "--excited"])
    
    assert result.exit_code == 0
    assert "Hello, Alice!" in result.output
```

### Isolated Testing
```python
def test_with_isolation():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Commands run in temporary directory
        result = runner.invoke(create_file, ["test.txt"])
        assert Path("test.txt").exists()
    # Temporary directory cleaned up
```

### Input Simulation
```python
def test_interactive():
    runner = CliRunner()
    result = runner.invoke(confirm_action, input="yes\n")
    assert "Confirmed" in result.output
```

## Configuration

Configure the CLI framework behavior:

```python
from provide.foundation.cli import CliConfig

cli.configure(
    CliConfig(
        # Help text settings
        show_default_values=True,
        max_help_width=80,
        
        # Error handling
        show_traceback=False,  # Only in debug mode
        exit_on_error=True,
        
        # Output formatting
        use_colors=True,
        timestamp_format="%H:%M:%S",
        
        # Command discovery
        auto_discover_commands=True,
        command_packages=["myapp.commands"],
    )
)
```

## Integration with Logging

CLI commands integrate seamlessly with provide.foundation's logging:

### Automatic Context
```python
@command
def process(task_id: str):
    """Process a task."""
    # CLI framework automatically adds context
    with logger.bind(command="process", task_id=task_id):
        logger.info("processing_started")
        # All logs in this command include context
```

### Log Level Control
```python
@cli.option("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
def set_log_level(log_level: str = "INFO"):
    """Set logging verbosity."""
    logger.set_level(log_level)
```

## Best Practices

### 1. Use Type Hints
Type hints provide validation and better help text:
```python
# Good: Clear types and validation
@command
def deploy(env: str, version: str, dry_run: bool = False):
    """Deploy application."""
    pass

# Avoid: No type hints
@command
def deploy(env, version, dry_run=False):
    pass
```

### 2. Write Clear Docstrings
Docstrings become help text:
```python
@command
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
@command
def upload(file: str):
    """Upload a file."""
    if not Path(file).exists():
        logger.error("file_not_found", file=file)
        raise cli.Exit(1, f"File not found: {file}")
```

### 4. Use Progress Indicators
For long-running operations:
```python
@command
def analyze(directory: str):
    """Analyze all files."""
    files = list(Path(directory).rglob("*"))
    
    with progress_bar(files) as pb:
        for file in pb:
            pb.set_description(f"Analyzing {file.name}")
            analyze_file(file)
```

### 5. Provide Confirmation
For destructive operations:
```python
@command
def delete_all(confirm: bool = False):
    """Delete all data."""
    if not confirm:
        if not cli.confirm("Delete all data?"):
            raise cli.Exit(0, "Cancelled")
    
    perform_deletion()
```

## Advanced Features

### Plugins
Extend CLI with plugins:
```python
cli.load_plugin("myapp.plugins.admin")  # Loads additional commands
```

### Command Aliases
```python
@command(aliases=["rm", "del"])
def remove(path: str):
    """Remove a file or directory."""
```

### Context Processors
```python
@cli.processor
def inject_user(ctx):
    """Add current user to context."""
    ctx.user = get_current_user()
```

### Custom Types
```python
from provide.foundation.cli import ClickType

class PortType(ClickType):
    def convert(self, value, param, ctx):
        port = int(value)
        if not 1 <= port <= 65535:
            self.fail(f"{value} is not a valid port")
        return port

@command
def serve(port: PortType = 8080):
    """Start server."""
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
- 🧪 [Testing CLI Apps](../../api/cli/api-testing.md) - Testing strategies
- 🏠 [Back to User Guide](../index.md)
