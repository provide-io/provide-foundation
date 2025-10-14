# CLI Arguments & Options

Learn how to handle command-line arguments and options in provide.foundation CLI applications.

## Overview

provide.foundation provides a comprehensive set of decorators and utilities for handling CLI arguments, built on top of Click. These decorators ensure consistency across all CLI tools while reducing boilerplate code.

## Standard Option Groups

### Logging Options

The `@logging_options` decorator adds standard logging controls to any command:

```python
from provide.foundation.cli import logging_options
import click

@click.command()
@logging_options
def my_command(log_level, log_file, log_format):
    """Your command with logging support."""
    # Logging is automatically configured based on these options
    pass
```

This adds:
- `--log-level/-l` - Set logging verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `--log-file` - Write logs to a file
- `--log-format` - Choose output format (json, text, key_value)

All options respect environment variables:
- `PROVIDE_LOG_LEVEL`
- `PROVIDE_LOG_FILE`
- `PROVIDE_LOG_FORMAT`

### Configuration Options

The `@config_options` decorator adds configuration file support:

```python
from provide.foundation.cli import config_options

@click.command()
@config_options
def my_command(config, profile):
    """Command with configuration file support."""
    if config:
        # Load configuration from file
        pass
```

This adds:
- `--config/-c` - Path to configuration file
- `--profile/-p` - Configuration profile to use

Environment variables:
- `PROVIDE_CONFIG_FILE`
- `PROVIDE_PROFILE`

### Output Options

The `@output_options` decorator controls output formatting:

```python
from provide.foundation.cli import output_options

@click.command()
@output_options
def my_command(json_output, no_color, no_emoji):
    """Command with output formatting options."""
    if json_output:
        # Output as JSON
        pass
```

This adds:
- `--json` - Output in JSON format
- `--no-color` - Disable colored output
- `--no-emoji` - Disable emoji in output

Environment variables:
- `PROVIDE_JSON_OUTPUT`
- `PROVIDE_NO_COLOR`
- `PROVIDE_NO_EMOJI`

## Debug Options

For development and troubleshooting:

```python
from provide.foundation.cli import debug_options

@click.command()
@debug_options
def my_command(debug, trace, verbose, quiet):
    """Command with debug options."""
    if debug:
        # Enable debug mode
        pass
```

This adds:
- `--debug/-d` - Enable debug mode
- `--trace` - Enable trace-level logging
- `--verbose/-v` - Increase verbosity (can be repeated)
- `--quiet/-q` - Suppress non-essential output

## Complete Example

Here's a complete CLI command using multiple option groups:

```python
import click
from provide.foundation.cli import (
    logging_options,
    config_options,
    output_options,
    debug_options
)
from provide.foundation import logger

@click.command()
@logging_options
@config_options
@output_options
@debug_options
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', help='Output file path')
def process_file(
    # From decorators
    log_level, log_file, log_format,
    config, profile,
    json_output, no_color, no_emoji,
    debug, trace, verbose, quiet,
    # Custom arguments
    input_file, output
):
    """Process a file with full CLI support."""

    # Logging is automatically configured
    logger.info("Processing file", file=input_file)

    if config:
        logger.info("Loading config", config=config, profile=profile)

    # Your processing logic here
    result = {"status": "success", "file": input_file}

    if json_output:
        import json
        print(json.dumps(result))
    else:
        print(f"✅ Processed {input_file}")
```

## Type Conversion

Click automatically handles type conversion for common types:

```python
@click.command()
@click.option('--count', type=int, default=1)
@click.option('--ratio', type=float, default=0.5)
@click.option('--active', type=bool, is_flag=True)
@click.option('--file', type=click.Path(exists=True))
@click.option('--choice', type=click.Choice(['a', 'b', 'c']))
def command(count, ratio, active, file, choice):
    """Command with typed arguments."""
    pass
```

## Validation

Arguments can be validated using Click's built-in validators:

```python
@click.command()
@click.option(
    '--port',
    type=click.IntRange(1, 65535),
    default=8080,
    help='Port number'
)
@click.option(
    '--email',
    callback=lambda ctx, param, value: validate_email(value),
    help='Email address'
)
def command(port, email):
    """Command with validation."""
    pass
```

## Context Access

Access the Click context and foundation Context:

```python
from provide.foundation import Context

@click.command()
@click.pass_context
def command(ctx):
    """Command with context access."""
    # Click context
    click_ctx = ctx

    # Foundation context (if initialized)
    foundation_ctx = Context.get_current()

    # Access parent command's parameters
    if ctx.parent:
        parent_params = ctx.parent.params
```

## Environment Variables

All options can be configured via environment variables:

```python
@click.command()
@click.option(
    '--api-key',
    envvar='API_KEY',  # Single env var
    required=True,
    help='API key for authentication'
)
@click.option(
    '--endpoint',
    envvar=['ENDPOINT_URL', 'API_ENDPOINT'],  # Multiple env vars (first found wins)
    default='https://api.example.com',
    help='API endpoint'
)
def command(api_key, endpoint):
    """Command with environment variable support."""
    pass
```

## Best Practices

1. **Use Standard Decorators**: Prefer the provided decorators for consistency
2. **Environment Variables**: Always provide envvar support for configuration
3. **Help Text**: Write clear, concise help text for all options
4. **Defaults**: Provide sensible defaults where possible
5. **Validation**: Validate inputs early using Click's validators
6. **Type Hints**: Use type hints for better IDE support

## Related Topics

- [Command Registration](commands.md) - How to register and organize commands
- [Nested Commands](nested.md) - Building command hierarchies
- [Output Formatting](output.md) - Formatting and styling output