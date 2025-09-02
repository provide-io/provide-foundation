# CLI Framework API

The `provide.foundation.cli` module provides decorators and utilities for building command-line interfaces with Click.

## Overview

The CLI framework provides:
- Command registration with decorators
- Nested command support with dot notation
- Automatic command discovery
- Integration with the Hub for component management
- Context management for CLI applications

## Quick Start

```python
from provide.foundation.cli import register_command, create_command_group

# Register simple commands
@register_command("hello")
def hello_command(name: str = "World"):
    """Say hello to someone."""
    print(f"Hello, {name}!")

# Register nested commands using dot notation
@register_command("db.migrate")
def db_migrate():
    """Run database migrations."""
    print("Running migrations...")

@register_command("db.seed")
def db_seed():
    """Seed the database."""
    print("Seeding database...")

# Create the CLI application
cli = create_command_group("myapp")

if __name__ == "__main__":
    cli()
```

## Command Registration

### `@register_command(name, **kwargs)`

Decorator to register a command with the Hub.

**Parameters:**
- `name: str` - Command name (supports dot notation for nesting)
- `aliases: list[str] | None` - Alternative names for the command
- `hidden: bool = False` - Hide from help output
- `deprecated: bool = False` - Mark as deprecated
- `group: bool = False` - Register as a command group
- `description: str | None` - Override the function's docstring
- `category: str | None` - Category for organization
- `priority: int = 0` - Sort priority in help

**Example:**
```python
# Simple command
@register_command("start")
def start_server(port: int = 8000):
    """Start the development server."""
    print(f"Starting server on port {port}")

# Command with aliases
@register_command("remove", aliases=["rm", "delete", "del"])
def remove_item(item_id: str):
    """Remove an item by ID."""
    print(f"Removing item {item_id}")

# Nested command with dot notation
@register_command("config.get")
def get_config(key: str):
    """Get a configuration value."""
    print(f"Config {key} = ...")

# Hidden command
@register_command("debug", hidden=True)
def debug_info():
    """Show debug information."""
    print("Debug mode active")

# Command group
@register_command("admin", group=True, description="Admin commands")
def admin_group():
    """Admin command group."""
    pass

@register_command("admin.users")
def list_users():
    """List all users."""
    print("Users: ...")
```

## Creating CLI Applications

### `create_command_group(name, **kwargs)`

Create a Click command group from registered commands.

**Parameters:**
- `name: str` - Name of the CLI application
- `description: str | None` - Description for --help
- `version: str | None` - Version string
- `context_settings: dict | None` - Click context settings

**Returns:** Click `Group` object

**Example:**
```python
# Basic CLI
cli = create_command_group("myapp")

# With configuration
cli = create_command_group(
    "myapp",
    description="My Application CLI",
    version="1.0.0",
    context_settings={
        "help_option_names": ["-h", "--help"],
        "max_content_width": 120,
    }
)

# Run the CLI
if __name__ == "__main__":
    cli()
```

## Context Management

### Using Click Context

Access Click context in commands:

```python
import click
from provide.foundation.cli import register_command

@register_command("status")
@click.pass_context
def status_command(ctx):
    """Show application status."""
    # Access context object
    verbose = ctx.obj.get("verbose", False)
    
    if verbose:
        print("Detailed status information...")
    else:
        print("Status: OK")
```

### Global Options

Add global options to your CLI:

```python
@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.option("--config", "-c", help="Config file path")
@click.pass_context
def cli(ctx, verbose, config):
    """My application CLI."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["config"] = config

# Commands can access global options
@register_command("process")
@click.pass_context
def process(ctx):
    if ctx.obj["verbose"]:
        print("Processing with verbose output...")
```

## Nested Commands with Dot Notation

The CLI framework supports hierarchical commands using dot notation:

```python
# Define nested structure with dots
@register_command("project.create")
def create_project(name: str):
    """Create a new project."""
    print(f"Creating project: {name}")

@register_command("project.list")
def list_projects():
    """List all projects."""
    print("Projects: ...")

@register_command("project.config.get")
def get_project_config(key: str):
    """Get project configuration."""
    print(f"Config {key} = ...")

@register_command("project.config.set")
def set_project_config(key: str, value: str):
    """Set project configuration."""
    print(f"Setting {key} = {value}")
```

This creates a hierarchy:
```
myapp
└── project
    ├── create
    ├── list
    └── config
        ├── get
        └── set
```

## Command Discovery

### Automatic Discovery

Commands can be auto-discovered from modules:

```python
from provide.foundation.cli import discover_commands

# Discover all commands in a package
discover_commands("myapp.commands")

# Create CLI with discovered commands
cli = create_command_group("myapp")
```

### Manual Registration

Register commands programmatically:

```python
from provide.foundation.hub import get_hub

hub = get_hub()

# Register a function as a command
def my_function():
    """Do something."""
    pass

hub.register_command("do-something", my_function)

# Register with metadata
hub.register_command(
    "advanced",
    my_function,
    metadata={"category": "tools", "priority": 10}
)
```

## Advanced Features

### Command Categories

Organize commands by category:

```python
@register_command("build", category="development")
def build():
    """Build the project."""
    pass

@register_command("test", category="development")
def test():
    """Run tests."""
    pass

@register_command("deploy", category="operations")
def deploy():
    """Deploy to production."""
    pass
```

### Command Priorities

Control command order in help:

```python
@register_command("important", priority=10)
def important_command():
    """This appears first in help."""
    pass

@register_command("normal", priority=0)
def normal_command():
    """This appears in normal order."""
    pass

@register_command("low", priority=-10)
def low_priority():
    """This appears last in help."""
    pass
```

### Dynamic Commands

Generate commands dynamically:

```python
def create_environment_command(env_name):
    @register_command(f"deploy.{env_name}")
    def deploy_to_env():
        f"""Deploy to {env_name} environment."""
        print(f"Deploying to {env_name}...")
    return deploy_to_env

# Create commands for each environment
for env in ["dev", "staging", "prod"]:
    create_environment_command(env)
```

## Integration with Foundation

### Using Console Output

```python
from provide.foundation.cli import register_command
from provide.foundation.console import pout, perr

@register_command("process")
def process_data(input_file: str):
    """Process data from input file."""
    pout(f"Processing {input_file}...")
    
    try:
        # Process the file
        result = process_file(input_file)
        pout(f"Processed {result['count']} records", prefix="✅")
    except Exception as e:
        perr(f"Failed to process: {e}", prefix="❌")
        raise click.Abort()
```

### Using Logger

```python
from provide.foundation import plog
from provide.foundation.cli import register_command

@register_command("sync")
def sync_data():
    """Synchronize data with remote."""
    plog.info("Starting data sync")
    
    try:
        # Sync logic
        plog.debug("Fetching remote data")
        items = fetch_remote()
        
        plog.info("Processing items", count=len(items))
        for item in items:
            process_item(item)
        
        plog.info("Sync completed successfully")
    except Exception as e:
        plog.error("Sync failed", error=str(e))
        raise
```

## Testing CLI Commands

### Unit Testing Commands

```python
from click.testing import CliRunner
from provide.foundation.cli import create_command_group

def test_hello_command():
    runner = CliRunner()
    cli = create_command_group("test")
    
    result = runner.invoke(cli, ["hello", "--name", "Alice"])
    assert result.exit_code == 0
    assert "Hello, Alice!" in result.output

def test_nested_command():
    runner = CliRunner()
    cli = create_command_group("test")
    
    result = runner.invoke(cli, ["db", "migrate"])
    assert result.exit_code == 0
    assert "Running migrations" in result.output
```

### Testing with Context

```python
def test_command_with_context():
    runner = CliRunner()
    cli = create_command_group("test")
    
    # Test with verbose flag
    result = runner.invoke(cli, ["--verbose", "status"])
    assert "Detailed status" in result.output
    
    # Test without verbose
    result = runner.invoke(cli, ["status"])
    assert "Status: OK" in result.output
```

## Best Practices

1. **Use descriptive names**:
   ```python
   # Good
   @register_command("database.migrate")
   @register_command("cache.clear")
   
   # Less clear
   @register_command("dbm")
   @register_command("cc")
   ```

2. **Provide helpful docstrings**:
   ```python
   @register_command("backup")
   def backup(destination: str, incremental: bool = False):
       """Create a backup of the application data.
       
       Args:
           destination: Path to backup location
           incremental: Only backup changed files
       """
   ```

3. **Use type hints for arguments**:
   ```python
   @register_command("create-user")
   def create_user(
       username: str,
       email: str,
       admin: bool = False,
       groups: list[str] = None
   ):
       """Create a new user account."""
   ```

4. **Handle errors gracefully**:
   ```python
   @register_command("import")
   def import_data(file: str):
       """Import data from file."""
       if not Path(file).exists():
           perr(f"File not found: {file}")
           raise click.Abort()
       
       try:
           process_import(file)
           pout("Import successful", prefix="✅")
       except Exception as e:
           perr(f"Import failed: {e}")
           raise click.Exit(1)
   ```

5. **Use command groups for organization**:
   ```python
   @register_command("db", group=True)
   def database_group():
       """Database management commands."""
       pass
   
   @register_command("db.migrate")
   def migrate():
       """Run migrations."""
   
   @register_command("db.backup")
   def backup():
       """Backup database."""
   ```

## See Also

- [Console Output](console.md) - For CLI output functions
- [Registry](registry.md) - Understanding command storage
- [Hub](hub.md) - Component management system