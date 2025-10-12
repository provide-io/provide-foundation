# CLI Arguments & Options

Learn how to handle command-line arguments and options in provide.foundation CLI applications.

## Overview

`provide.foundation` automatically generates CLI arguments and options from the type hints in your function signatures. This means you don't need to use any `click` decorators for basic argument handling.

## Positional Arguments

Function parameters without default values are treated as required positional arguments.

```python
from provide.foundation.hub import register_command

@register_command
def copy(source: str, dest: str):
    """Copy from source to destination."""
    # source and dest are required positional args
    print(f"Copying from {source} to {dest}")
```

## Optional Arguments

Function parameters with default values are treated as optional arguments (flags).

```python
from provide.foundation.hub import register_command

@register_command
def build(target: str, debug: bool = False, jobs: int = 4):
    """Build the target."""
    # target is a required positional argument
    # --debug and --jobs are optional flags
    print(f"Building {target} with debug={debug} and jobs={jobs}")
```

## Type Conversion

`provide.foundation` uses the type hints in your function signature to automatically convert and validate arguments.

```python
from provide.foundation.hub import register_command

@register_command
def process(
    count: int,
    ratio: float,
    verbose: bool = False
):
    """Process data with specified parameters."""
    for i in range(count):
        result = i * ratio
        if verbose:
            print(f"Processing item {i} with result {result}")
```

If you provide an invalid type, the CLI will automatically generate an error message:

```bash
$ python app.py process not-a-number 0.5
Error: Invalid value for 'count': 'not-a-number' is not a valid integer.
```

## Standard Options

`provide.foundation` provides a set of standard decorators for adding common options to your commands.

### Logging Options

The `@logging_options` decorator adds standard logging controls to any command:

```python
from provide.foundation.cli.decorators import logging_options
from provide.foundation.hub import register_command

@register_command
@logging_options
def my_command(log_level, log_file, log_format):
    """Your command with logging support."""
    # Logging is automatically configured based on these options
    pass
```

### Configuration Options

The `@config_options` decorator adds configuration file support:

```python
from provide.foundation.cli.decorators import config_options
from provide.foundation.hub import register_command

@register_command
@config_options
def my_command(config, profile):
    """Command with configuration file support."""
    if config:
        # Load configuration from file
        pass
```

### Output Options

The `@output_options` decorator controls output formatting:

```python
from provide.foundation.cli.decorators import output_options
from provide.foundation.hub import register_command

@register_command
@output_options
def my_command(json_output, no_color, no_emoji):
    """Command with output formatting options."""
    if json_output:
        # Output as JSON
        pass
```

## Related Topics

- [Command Registration](commands.md) - How to register and organize commands
- [Nested Commands](nested.md) - Building command hierarchies
- [Output Formatting](output.md) - Formatting and styling output