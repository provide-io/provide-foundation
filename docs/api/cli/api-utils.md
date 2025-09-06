# CLI Utils API

Common CLI utilities for output, logging, and testing with Click integration.

## Overview

The CLI utilities module provides:

- **Formatted output** - Consistent JSON and styled text output
- **Message functions** - Success, error, warning, and info messages
- **Logging setup** - CLI-specific logging configuration
- **Context creation** - CLI context management
- **Test utilities** - CLI testing helpers

## Output Functions

### echo_json(data, err)

Output data as formatted JSON.

```python
def echo_json(data: Any, err: bool = False) -> None:
    """
    Output data as JSON.
    
    Args:
        data: Data to output as JSON
        err: Whether to output to stderr
    """
```

**Features:**
- Automatic indentation (2 spaces)
- Default string conversion for non-JSON types
- Support for stdout/stderr routing

**Usage Examples:**
```python
from provide.foundation.cli.utils import echo_json

# Basic JSON output
data = {"status": "success", "count": 42}
echo_json(data)
# Output: {
#   "status": "success", 
#   "count": 42
# }

# Error output to stderr
error_data = {"error": "Something went wrong", "code": "ERR001"}
echo_json(error_data, err=True)
```

### Message Functions

Standard message output functions with emoji and color support.

#### echo_error(message, json_output)

Output an error message.

```python
def echo_error(message: str, json_output: bool = False) -> None:
    """
    Output an error message.
    
    Args:
        message: Error message to output
        json_output: Whether to output as JSON
    """
```

#### echo_success(message, json_output)

Output a success message.

```python
def echo_success(message: str, json_output: bool = False) -> None:
    """
    Output a success message.
    
    Args:
        message: Success message to output
        json_output: Whether to output as JSON
    """
```

#### echo_warning(message, json_output)

Output a warning message.

```python
def echo_warning(message: str, json_output: bool = False) -> None:
    """
    Output a warning message.
    
    Args:
        message: Warning message to output
        json_output: Whether to output as JSON
    """
```

#### echo_info(message, json_output)

Output an informational message.

```python
def echo_info(message: str, json_output: bool = False) -> None:
    """
    Output an informational message.
    
    Args:
        message: Info message to output  
        json_output: Whether to output as JSON
    """
```

**Usage Examples:**
```python
from provide.foundation.cli.utils import echo_error, echo_success, echo_warning, echo_info

# Text output (default)
echo_success("Operation completed successfully")
# Output: ✓ Operation completed successfully

echo_error("Configuration file not found")  
# Output: ✗ Configuration file not found

echo_warning("Using default configuration")
# Output: ⚠ Using default configuration

echo_info("Processing 100 items")
# Output: ℹ Processing 100 items

# JSON output
echo_success("Deployment complete", json_output=True)
# Output: {"success": "Deployment complete"}

echo_error("Database connection failed", json_output=True)
# Output: {"error": "Database connection failed"}
```

## Logging Functions

### setup_cli_logging(ctx, log_level, log_file, json_logs)

Setup logging for CLI applications with flexible configuration.

```python
def setup_cli_logging(
    ctx: Context | None = None,
    log_level: str | None = None,
    log_file: str | Path | None = None,
    json_logs: bool = False,
) -> None:
    """
    Setup logging for CLI applications.
    
    Args:
        ctx: Optional Context to get settings from
        log_level: Override log level
        log_file: Override log file path
        json_logs: Whether to output logs as JSON
    """
```

**Features:**
- Context integration for configuration
- Parameter overrides for flexibility  
- Support for file and console logging
- JSON log format option

**Usage Examples:**
```python
from provide.foundation.cli.utils import setup_cli_logging
from provide.foundation.context import Context

# Basic setup
setup_cli_logging(log_level="DEBUG")

# With context
ctx = Context(log_level="INFO", log_file="/var/log/myapp.log")
setup_cli_logging(ctx=ctx)

# Override context settings
setup_cli_logging(
    ctx=ctx,
    log_level="DEBUG",  # Override context log level
    json_logs=True      # Override format
)

# Standalone file logging
setup_cli_logging(
    log_level="WARNING",
    log_file="errors.log",
    json_logs=True
)
```

## Context Functions

### create_cli_context(**kwargs)

Create a Context for CLI usage with environment loading and overrides.

```python
def create_cli_context(**kwargs) -> Context:
    """
    Create a Context for CLI usage.
    
    Loads from environment, then overlays any provided kwargs.
    
    Args:
        **kwargs: Override values for the context
        
    Returns:
        Configured Context instance
    """
```

**Usage Examples:**
```python
from provide.foundation.cli.utils import create_cli_context

# Load from environment
ctx = create_cli_context()

# Override specific values
ctx = create_cli_context(
    debug=True,
    log_level="DEBUG",
    json_output=True
)

# Use in CLI command
import click

@click.command()
@click.option("--debug", is_flag=True)
@click.option("--log-level", default="INFO")
def my_command(debug, log_level):
    ctx = create_cli_context(debug=debug, log_level=log_level)
    setup_cli_logging(ctx)
    
    echo_info(f"Running with debug={ctx.debug}, log_level={ctx.log_level}")
```

## Testing Classes

### CliTestRunner

Test runner for CLI commands using Click's testing facilities.

```python
class CliTestRunner:
    """Test runner for CLI commands using Click's testing facilities."""
    
    def __init__(self, mix_stderr: bool = False) -> None:
        """
        Initialize the test runner.
        
        Args:
            mix_stderr: Whether to mix stderr with stdout in output
        """
```

#### Methods

##### invoke(cli, args, input, env, catch_exceptions, **kwargs)

Invoke a CLI command for testing.

```python
def invoke(
    self,
    cli: click.Command | click.Group,
    args: list[str] | None = None,
    input: str | None = None,
    env: dict[str, str] | None = None,
    catch_exceptions: bool = True,
    **kwargs,
):
    """
    Invoke a CLI command for testing.
    
    Args:
        cli: The Click command or group to invoke
        args: Command line arguments
        input: Optional input to provide
        env: Environment variables to set
        catch_exceptions: Whether to catch exceptions
        **kwargs: Additional arguments for CliRunner.invoke
        
    Returns:
        Click Result object with exit_code, output, etc.
    """
```

##### isolated_filesystem()

Context manager for isolated filesystem testing.

```python
def isolated_filesystem(self):
    """
    Context manager for isolated filesystem.
    
    Creates a temporary directory and changes to it,
    cleaning up on exit.
    """
```

#### Usage Examples

```python
from provide.foundation.cli.utils import CliTestRunner
import click

@click.command()
@click.option("--name", default="World")
def hello(name):
    click.echo(f"Hello, {name}!")

def test_hello_command():
    runner = CliTestRunner()
    
    # Test default behavior
    result = runner.invoke(hello)
    assert result.exit_code == 0
    assert "Hello, World!" in result.output
    
    # Test with argument
    result = runner.invoke(hello, ["--name", "Alice"])
    assert result.exit_code == 0
    assert "Hello, Alice!" in result.output
    
    # Test with environment
    result = runner.invoke(hello, env={"USER": "Bob"})
    assert result.exit_code == 0

def test_with_isolated_filesystem():
    runner = CliTestRunner()
    
    with runner.isolated_filesystem():
        # Create test files
        with open("test.txt", "w") as f:
            f.write("test content")
        
        # Test command that works with files
        result = runner.invoke(my_file_command, ["test.txt"])
        assert result.exit_code == 0
```

## Testing Assertion Functions

### assert_cli_success(result, expected_output)

Assert that a CLI command succeeded.

```python
def assert_cli_success(result, expected_output: str | None = None) -> None:
    """
    Assert that a CLI command succeeded.
    
    Args:
        result: Click Result object from invoke
        expected_output: Optional expected output substring
    """
```

### assert_cli_error(result, expected_error, exit_code)

Assert that a CLI command failed.

```python
def assert_cli_error(
    result,
    expected_error: str | None = None,
    exit_code: int | None = None,
) -> None:
    """
    Assert that a CLI command failed.
    
    Args:
        result: Click Result object from invoke
        expected_error: Optional expected error substring
        exit_code: Expected exit code (default: any non-zero)
    """
```

#### Usage Examples

```python
from provide.foundation.cli.utils import (
    CliTestRunner, 
    assert_cli_success, 
    assert_cli_error
)

def test_successful_command():
    runner = CliTestRunner()
    result = runner.invoke(my_cli, ["status"])
    
    assert_cli_success(result, "System is running")

def test_failing_command():
    runner = CliTestRunner()
    result = runner.invoke(my_cli, ["invalid-command"])
    
    assert_cli_error(
        result, 
        expected_error="No such command",
        exit_code=2
    )
```

## Integration Patterns

### CLI Command with Full Setup

```python
import click
from provide.foundation.cli.utils import (
    create_cli_context,
    setup_cli_logging,
    echo_success,
    echo_error
)

@click.command()
@click.option("--debug", is_flag=True)
@click.option("--log-level", default="INFO")
@click.option("--json", "json_output", is_flag=True)
def deploy(debug, log_level, json_output):
    """Deploy the application."""
    # Setup context and logging
    ctx = create_cli_context(
        debug=debug,
        log_level=log_level,
        json_output=json_output
    )
    setup_cli_logging(ctx)
    
    try:
        # Perform deployment
        perform_deployment()
        echo_success("Deployment completed successfully", ctx.json_output)
        
    except Exception as e:
        echo_error(f"Deployment failed: {e}", ctx.json_output)
        raise click.ClickException("Deployment failed")
```

### Testing with Different Output Formats

```python
def test_output_formats():
    runner = CliTestRunner()
    
    # Test text output
    result = runner.invoke(my_cli, ["status"])
    assert_cli_success(result, "✓ System operational")
    
    # Test JSON output  
    result = runner.invoke(my_cli, ["--json", "status"])
    assert_cli_success(result)
    
    import json
    output_data = json.loads(result.output)
    assert output_data["status"] == "operational"
```

### Error Handling Patterns

```python
@click.command()
def risky_operation():
    """Perform a risky operation."""
    try:
        do_risky_thing()
        echo_success("Operation completed")
        
    except ValidationError as e:
        echo_error(f"Validation failed: {e}")
        raise click.ClickException("Invalid input")
        
    except ConnectionError as e:
        echo_error(f"Connection failed: {e}")
        raise click.ClickException("Network error")
        
    except Exception as e:
        echo_error(f"Unexpected error: {e}")
        raise click.ClickException("Internal error")
```

## Related Documentation

- [api-CLI Decorators API](api-decorators.md) - Standard CLI decorators
- [api-CLI Testing API](api-testing.md) - Testing utilities
- [Context API](../context/api-index.md) - Context management
- [CLI Guide](../../guide/cli/index.md) - Building CLI applications