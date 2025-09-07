# CLI Decorators API

Standard CLI decorators for consistent option handling, error management, and context integration.

## Overview

The CLI decorators module provides reusable decorators for Click commands that add:

- **Standard options** - Logging, configuration, and output options
- **Error handling** - Consistent error formatting and exit codes
- **Context integration** - Automatic Context creation and management
- **Option grouping** - Logical grouping of related options

## Standard Option Decorators

### logging_options

Add standard logging options to a Click command.

```python
def logging_options(f: F) -> F:
    """
    Add standard logging options to a Click command.
    
    Adds:
    - --log-level/-l: Set logging verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - --log-file: Write logs to file
    - --log-format: Choose log output format (json, text, key_value)
    """
```

**Added Options:**
- `--log-level/-l` - Log level choice (envvar: `PROVIDE_LOG_LEVEL`)
- `--log-file` - Log file path (envvar: `PROVIDE_LOG_FILE`)
- `--log-format` - Log format choice (envvar: `PROVIDE_LOG_FORMAT`)

**Usage Example:**
```python
import click
from provide.foundation.cli.decorators import logging_options

@click.command()
@logging_options
def my_command(log_level, log_file, log_format):
    """Example command with logging options."""
    print(f"Log level: {log_level}")
    print(f"Log file: {log_file}")
    print(f"Log format: {log_format}")

# Usage:
# my-command --log-level DEBUG --log-file app.log --log-format json
```

### config_options

Add configuration file options to a Click command.

```python
def config_options(f: F) -> F:
    """
    Add configuration file options to a Click command.
    
    Adds:
    - --config/-c: Path to configuration file
    - --profile/-p: Configuration profile to use
    """
```

**Added Options:**
- `--config/-c` - Configuration file path (envvar: `PROVIDE_CONFIG_FILE`)
- `--profile/-p` - Configuration profile (envvar: `PROVIDE_PROFILE`)

**Usage Example:**
```python
@click.command()
@config_options
def deploy(config, profile):
    """Deploy with configuration."""
    print(f"Using config: {config}")
    print(f"Profile: {profile}")

# Usage:
# deploy --config production.yaml --profile west-coast
```

### output_options

Add output formatting options to a Click command.

```python
def output_options(f: F) -> F:
    """
    Add output formatting options to a Click command.
    
    Adds:
    - --json: Output in JSON format
    - --no-color: Disable colored output
    - --no-emoji: Disable emoji in output
    """
```

**Added Options:**
- `--json` - JSON output (envvar: `PROVIDE_JSON_OUTPUT`)
- `--no-color` - Disable colors (envvar: `PROVIDE_NO_COLOR`)
- `--no-emoji` - Disable emoji (envvar: `PROVIDE_NO_EMOJI`)

**Usage Example:**
```python
@click.command()
@output_options
def status(json_output, no_color, no_emoji):
    """Show system status."""
    if json_output:
        click.echo('{"status": "running"}')
    else:
        emoji = "" if no_emoji else "✓ "
        color = None if no_color else "green"
        click.secho(f"{emoji}System running", fg=color)

# Usage:
# status --json
# status --no-color --no-emoji
```

## Composite Decorators

### flexible_options

Apply flexible CLI options that can be used at any command level.

```python
def flexible_options(f: F) -> F:
    """
    Apply flexible CLI options that can be used at any command level.
    
    Combines logging_options and config_options for consistent
    control at both group and command levels.
    """
```

**Usage Example:**
```python
@click.group()
@flexible_options
def cli(log_level, log_file, log_format, config, profile):
    """Main CLI group."""
    pass

@cli.command()
@flexible_options  # Can be used at command level too
def subcommand(log_level, log_file, log_format, config, profile):
    """Subcommand with same options."""
    pass
```

### standard_options

Apply all standard CLI options.

```python
def standard_options(f: F) -> F:
    """
    Apply all standard CLI options.
    
    Combines logging_options, config_options, and output_options.
    
    Note: Consider using flexible_options for better granular control.
    This decorator is maintained for backward compatibility.
    """
```

**Usage Example:**
```python
@click.command()
@standard_options
def comprehensive_command(**kwargs):
    """Command with all standard options."""
    # Access all standard options:
    # log_level, log_file, log_format, config, profile, 
    # json_output, no_color, no_emoji
    pass
```

## Error Handling Decorators

### error_handler

Decorator to handle errors consistently in CLI commands.

```python
def error_handler(f: F) -> F:
    """
    Decorator to handle errors consistently in CLI commands.
    
    Catches exceptions and formats them appropriately based on
    debug mode and output format.
    """
```

**Features:**
- Handles Click exceptions appropriately
- Keyboard interrupt handling (SIGINT)
- Debug mode support (shows full traceback)
- JSON error output when requested
- Proper exit codes

**Usage Example:**
```python
@click.command()
@error_handler
def risky_command(debug=False, json_output=False):
    """Command that might fail."""
    if some_condition:
        raise ValueError("Something went wrong")
    
    click.echo("Success!")

# Normal error (non-debug):
# Error: Something went wrong
# Exit code: 1

# Debug mode:
# Full traceback displayed
# Exit code: 1

# JSON mode:
# {"error": "Something went wrong", "type": "ValueError"}
# Exit code: 1
```

## Context Integration Decorators

### pass_context

Decorator to pass the foundation Context to a command.

```python
def pass_context(f: F) -> F:
    """
    Decorator to pass the foundation Context to a command.
    
    Creates or retrieves a Context from Click's context object
    and passes it as the first argument to the decorated function.
    """
```

**Features:**
- Automatic Context creation from Click context
- Context updates from command options
- Parameter cleanup (removes processed options from kwargs)
- Integration with existing Click context objects

**Usage Example:**
```python
from provide.foundation.context import Context

@click.command()
@standard_options
@pass_context
def my_command(ctx: Context, additional_arg):
    """Command that receives Foundation Context."""
    print(f"Log level: {ctx.log_level}")
    print(f"JSON output: {ctx.json_output}")
    print(f"Profile: {ctx.profile}")
    
    # Use context for logging setup
    if ctx.log_file:
        setup_logging(log_file=ctx.log_file)

# The context is automatically populated from command options
```

**Context Updates:**
The decorator automatically updates the Context with:
- `log_level` from `--log-level`
- `log_file` from `--log-file`
- `log_format` from `--log-format`
- `json_output` from `--json`
- `no_color` from `--no-color`
- `no_emoji` from `--no-emoji`
- `profile` from `--profile`
- Config loading from `--config`

## Utility Decorators

### version_option(version, prog_name)

Add a --version option to display version information.

```python
def version_option(version: str | None = None, prog_name: str | None = None):
    """
    Add a --version option to display version information.
    
    Args:
        version: Version string to display
        prog_name: Program name to display
    """
```

**Usage Example:**
```python
@click.command()
@version_option("1.2.3", "myapp")
def cli():
    """My application."""
    pass

# Usage:
# myapp --version
# Output: myapp version 1.2.3
```

## Usage Patterns

### Basic CLI Application

```python
import click
from provide.foundation.cli.decorators import standard_options, pass_context, error_handler
from provide.foundation.context import Context

@click.group()
@standard_options
@pass_context
def cli(ctx: Context):
    """My application CLI."""
    # Context is automatically configured from options
    setup_cli_logging(ctx)

@cli.command()
@error_handler
@pass_context  
def deploy(ctx: Context):
    """Deploy the application."""
    try:
        if ctx.debug:
            click.echo("Debug mode enabled")
        
        # Deployment logic
        perform_deployment()
        
        if ctx.json_output:
            click.echo('{"status": "deployed"}')
        else:
            click.secho("✓ Deployment successful", fg="green")
            
    except DeploymentError as e:
        # error_handler will format this appropriately
        raise click.ClickException(f"Deployment failed: {e}")
```

## Constants

### LOG_LEVELS

Valid log level choices used by logging_options.

```python
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
```

## Related Documentation

- [api-CLI Utils API](utils.md) - CLI utilities and helpers  
- [api-CLI Testing API](testing.md) - Testing utilities
- [Context API](../context/api-index.md) - Context management
- [Click Documentation](https://click.palletsprojects.com/) - Click framework reference
