# How to Register CLI Commands

`provide.foundation` simplifies CLI development by allowing you to register Python functions as commands using decorators.

## Basic Command Registration

Use the `@register_command` decorator to expose a function as a CLI command.

```python
# From: examples/cli/01_cli_application.py
from provide.foundation.hub import register_command
from provide.foundation.cli import echo_success

@register_command("init")
def init_command(name: str = "myproject", template: str = "default"):
    """Initialize a new project."""
    echo_success(f"Initializing project '{name}' with template '{template}'")
```

**Key Points:**
- Function name becomes the command handler
- Function parameters become CLI arguments/options
- Docstring becomes the help text
- Type hints enable automatic type conversion

## Argument Types and Defaults

Foundation automatically converts CLI arguments based on type hints:

```python
@register_command("deploy")
def deploy_command(
    environment: str,              # Required string argument
    version: str = "latest",       # Optional with default
    force: bool = False,           # Boolean flag (--force)
    replicas: int = 3,             # Integer option
    timeout: float = 30.0,         # Float option
):
    """Deploy application to environment."""
    echo_info(f"Deploying {version} to {environment}")
    echo_info(f"Replicas: {replicas}, Timeout: {timeout}s")
    if force:
        echo_warning("Force deployment enabled")
```

**Usage:**
```bash
# Required argument
./mycli deploy production

# With options
./mycli deploy production --version v2.0 --replicas 5

# Boolean flags
./mycli deploy production --force
```

## Nested Commands

Organize commands into groups using dot notation:

```python
@register_command("db.migrate")
def migrate_database():
    """Run database migrations."""
    echo_info("Running migrations...")

@register_command("db.seed")
def seed_database(dataset: str = "default"):
    """Seed database with test data."""
    echo_info(f"Seeding database with {dataset} dataset...")

@register_command("db.status")
def database_status():
    """Show database connection status."""
    echo_info("Database status: Connected")
```

**Usage:**
```bash
./mycli db migrate
./mycli db seed --dataset production
./mycli db status
```

**Output:**
```
Usage: mycli [OPTIONS] COMMAND [ARGS]...

Commands:
  db      Database management commands
    migrate  Run database migrations
    seed     Seed database with test data
    status   Show database connection status
```

## Command Metadata

Add metadata like aliases, categories, and tags:

```python
@register_command("status", aliases=["st", "info"], category="info")
def status_command(verbose: bool = False):
    """Show system status."""
    echo_info("System Status")
    echo_info("=" * 40)
    # ... status implementation ...
```

**Features:**
- **aliases:** Alternative command names (`st`, `info`)
- **category:** Group commands in help output
- **tags:** Metadata for filtering/searching

## User-Facing Output

Use Foundation's console output functions for clean user feedback:

```python
from provide.foundation.cli import pout, perr, echo_success, echo_error, echo_warning, echo_info

@register_command("process")
def process_command(file: str, validate: bool = True):
    """Process a data file."""

    # Info messages (cyan)
    echo_info(f"Processing {file}...")

    # Warnings (yellow)
    if not validate:
        echo_warning("Validation disabled - proceed with caution")

    try:
        # ... processing logic ...

        # Success messages (green)
        echo_success(f"Successfully processed {file}")
        pout(f"✅ Output saved to output/{file}", color="green")

    except Exception as e:
        # Error messages (red)
        echo_error(f"Failed to process {file}: {e}")
        perr(f"❌ Processing failed", color="red")
        raise
```

## Validation and Error Handling

Add validation logic and provide clear error messages:

```python
from provide.foundation.errors import ValidationError

@register_command("backup")
def backup_command(source: str, destination: str, compress: bool = False):
    """Backup files from source to destination."""

    # Validate inputs
    if not os.path.exists(source):
        echo_error(f"Source directory not found: {source}")
        raise ValidationError(f"Invalid source: {source}")

    if os.path.exists(destination):
        echo_warning(f"Destination exists: {destination}")
        if not click.confirm("Overwrite?"):
            echo_info("Backup cancelled")
            return

    # Perform backup
    try:
        echo_info(f"Backing up {source} → {destination}")
        # ... backup logic ...
        echo_success("Backup completed")

    except Exception as e:
        echo_error(f"Backup failed: {e}")
        raise
```

## Complex Argument Types

Handle lists, paths, and custom types:

```python
from pathlib import Path

@register_command("batch-process")
def batch_process_command(
    files: str,                    # Comma-separated list
    output_dir: str = "./output",  # Path
    formats: str = "json,csv",     # Multiple formats
):
    """Process multiple files in batch."""

    # Parse comma-separated files
    file_list = [f.strip() for f in files.split(",")]

    # Convert to Path
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Parse formats
    format_list = [f.strip() for f in formats.split(",")]

    echo_info(f"Processing {len(file_list)} files")
    echo_info(f"Output formats: {', '.join(format_list)}")

    for file in file_list:
        echo_info(f"Processing {file}...")
        # ... process file ...
```

**Usage:**
```bash
./mycli batch-process --files "data1.txt,data2.txt,data3.txt" --formats "json,xml"
```

## Interactive Prompts

Use Click's built-in prompt functions for interactive input:

```python
import click

@register_command("configure")
def configure_command():
    """Interactive configuration wizard."""

    echo_info("Configuration Wizard")
    echo_info("=" * 40)

    # Text prompts
    api_key = click.prompt("API Key", hide_input=True)
    region = click.prompt("Region", default="us-east-1")

    # Number prompts
    timeout = click.prompt("Timeout (seconds)", type=int, default=30)

    # Confirmation
    if click.confirm("Enable debug mode?"):
        debug = True
        echo_warning("Debug mode enabled")
    else:
        debug = False

    # Choice prompts
    environment = click.prompt(
        "Environment",
        type=click.Choice(["development", "staging", "production"]),
        default="development"
    )

    echo_success("Configuration saved")
```

## Creating the CLI Application

Once commands are registered, create the CLI application:

```python
from provide.foundation import get_hub

def main():
    """Main CLI entry point."""

    # Get the hub instance
    hub = get_hub()

    # Create CLI from registered commands
    cli = hub.create_cli(
        name="mycli",
        version="1.0.0",
        help="My CLI Application"
    )

    # Run the CLI
    cli()

if __name__ == "__main__":
    main()
```

**Alternative - With Context:**
```python
from provide.foundation.context import CLIContext
from provide.foundation.hub import Hub

def main():
    """Main CLI entry point with custom context."""

    # Create context with settings
    context = CLIContext(
        log_level="INFO",
        profile="production",
        debug=False,
        no_emoji=False,
    )

    # Create hub with context
    hub = Hub(context=context)

    # Create CLI
    cli = hub.create_cli(
        name="mycli",
        version="1.0.0",
        help="My CLI Application"
    )

    # Run
    cli()

if __name__ == "__main__":
    main()
```

## Testing CLI Commands

Test commands without invoking the full CLI:

```python
import pytest
from click.testing import CliRunner
from provide.foundation import get_hub

def test_status_command():
    """Test the status command."""
    hub = get_hub()
    cli = hub.create_cli(name="test-cli")

    runner = CliRunner()
    result = runner.invoke(cli, ["status"])

    assert result.exit_code == 0
    assert "System Status" in result.output

def test_deploy_command_with_args():
    """Test deploy command with arguments."""
    hub = get_hub()
    cli = hub.create_cli(name="test-cli")

    runner = CliRunner()
    result = runner.invoke(cli, ["deploy", "production", "--force"])

    assert result.exit_code == 0
    assert "production" in result.output
```

## Progress Indicators

Show progress for long-running operations:

```python
import click
from provide.foundation.cli import echo_info

@register_command("install")
def install_command(packages: str):
    """Install packages."""

    package_list = [p.strip() for p in packages.split(",")]

    echo_info(f"Installing {len(package_list)} packages...")

    with click.progressbar(package_list, label="Installing") as bar:
        for package in bar:
            # Simulate installation
            time.sleep(0.5)

    echo_success(f"Installed {len(package_list)} packages")
```

## Best Practices

### ✅ DO: Use Clear Command Names

```python
# ✅ Good: Descriptive command names
@register_command("database.migrate")
@register_command("user.create")

# ❌ Bad: Vague names
@register_command("do-stuff")
@register_command("run")
```

### ✅ DO: Provide Good Help Text

```python
# ✅ Good: Clear docstring and parameter descriptions
@register_command("backup")
def backup_command(source: str, destination: str, compress: bool = False):
    """Backup files from source to destination.

    Creates a backup of all files in the source directory and saves
    them to the destination. Optionally compresses the backup.
    """
    pass

# ❌ Bad: No help text
@register_command("backup")
def backup_command(source: str, destination: str, compress: bool = False):
    pass
```

### ✅ DO: Validate Inputs Early

```python
# ✅ Good: Validate before processing
@register_command("process")
def process_command(file: str):
    """Process a file."""
    if not os.path.exists(file):
        echo_error(f"File not found: {file}")
        raise click.Abort()
    # ... continue processing ...
```

### ✅ DO: Use Structured Logging Internally

```python
# ✅ Good: Use logger for internal logging, echo for user output
from provide.foundation import logger

@register_command("deploy")
def deploy_command(env: str):
    """Deploy application."""
    # Internal logging (for operators/debugging)
    logger.info("deployment_started", environment=env)

    # User output (for CLI users)
    echo_info(f"Deploying to {env}...")

    # ... deploy logic ...

    logger.info("deployment_completed", environment=env)
    echo_success("Deployment complete")
```

### ❌ DON'T: Mix Logging and User Output

```python
# ❌ Bad: Using logger for user feedback
@register_command("status")
def status_command():
    logger.info("System is running")  # User won't see this clearly

# ✅ Good: Use echo functions for users
@register_command("status")
def status_command():
    echo_success("System is running")
```

## Common Patterns

### Pattern: Configuration Command

```python
@register_command("config.show")
def show_config():
    """Show current configuration."""
    from provide.foundation.config import get_config

    config = get_config()
    echo_info("Current Configuration:")
    echo_info("=" * 40)
    for key, value in config.items():
        echo_info(f"{key}: {value}")
```

### Pattern: Version Command

```python
@register_command("version")
def version_command():
    """Show version information."""
    from provide.foundation import __version__

    echo_info(f"mycli version {__version__}")
    echo_info("Foundation version: ...")
```

### Pattern: Dry-Run Mode

```python
@register_command("cleanup")
def cleanup_command(path: str, dry_run: bool = False):
    """Clean up old files."""

    if dry_run:
        echo_warning("DRY RUN MODE - No files will be deleted")

    files_to_delete = find_old_files(path)

    echo_info(f"Found {len(files_to_delete)} files to delete")

    if dry_run:
        for file in files_to_delete:
            echo_info(f"Would delete: {file}")
    else:
        for file in files_to_delete:
            echo_info(f"Deleting: {file}")
            os.remove(file)
        echo_success(f"Deleted {len(files_to_delete)} files")
```

## Next Steps

### Building CLI Features
- **[Argument Parsing](arguments.md)**: Advanced argument handling patterns
- **[Interactive Prompts](prompts.md)**: Building interactive CLIs
- **[First Application](../../getting-started/first-app.md)**: Complete CLI tutorial

### Testing & Production
- **[Testing CLI Commands](../testing/cli-tests.md)**: Write tests for your CLI applications
- **[Production Deployment](../production/deployment.md)**: Deploy CLI tools to production

### Related Guides
- **[Basic Logging](../logging/basic-logging.md)**: Add structured logging to commands
- **[Configuration](../configuration/env-variables.md)**: Configure CLI tools via environment
- **[Error Handling](../resilience/retry.md)**: Add resilience to CLI operations

---

**See Also:** Check `examples/cli/01_cli_application.py` for a comprehensive example.
