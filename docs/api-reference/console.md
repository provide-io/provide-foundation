# Console Output API

The `provide.foundation.console` module provides standardized console output functions for CLI applications.

## Overview

The console module provides:
- Structured output to stdout and stderr
- JSON output mode support
- Color and formatting control
- Testing support with output capture

## Core Functions

### `pout(message, **kwargs)`

Output a message to stdout.

**Parameters:**
- `message` - The message to output (required first argument)
- `ctx: Context` - Click context (auto-detected if not provided)
- `nl: bool = True` - Add newline after message
- `color: bool | None` - Enable/disable colors (auto-detected)
- `prefix: str | None` - Optional prefix for the message
- `json_key: str | None` - Key for JSON output mode
- `capture_output: bool = False` - Capture output for testing

**Example:**
```python
from provide.foundation.console import pout

# Simple output
pout("Operation completed successfully")

# Without newline
pout("Processing...", nl=False)

# With prefix
pout("File created", prefix="✅")

# JSON mode support
pout({"status": "success"}, json_key="result")
```

### `perr(message, **kwargs)`

Output an error message to stderr.

**Parameters:** Same as `pout`

**Example:**
```python
from provide.foundation.console import perr

# Simple error
perr("Failed to connect to database")

# With prefix
perr("Invalid configuration", prefix="❌")

# Captured for testing
output = perr("Test error", capture_output=True)
assert "Test error" in output
```

### `plog`

Alias for the foundation logger, providing structured logging.

**Example:**
```python
from provide.foundation import plog

# Use like the standard logger
plog.info("Starting application", version="1.0.0")
plog.error("Connection failed", host="localhost", port=5432)
plog.debug("Processing item", item_id=123, status="pending")
```

## JSON Output Mode

The console functions automatically detect JSON output mode from the Click context:

```python
import click
from provide.foundation.console import pout

@click.command()
@click.option('--json', 'output_json', is_flag=True)
@click.pass_context
def my_command(ctx, output_json):
    ctx.obj = ctx.obj or {}
    ctx.obj['output_json'] = output_json
    
    # This will output JSON if --json flag is set
    pout("Command executed", json_key="status")
    pout({"items": [1, 2, 3]}, json_key="data")
```

When JSON mode is active:
```json
{
  "status": "Command executed",
  "data": {"items": [1, 2, 3]}
}
```

## Color Support

Colors are automatically detected based on:
1. TTY detection (is output going to a terminal?)
2. Click context color settings
3. Manual override via `color` parameter

```python
# Force colors on
pout("Colored output", color=True)

# Force colors off
pout("Plain output", color=False)

# Auto-detect (default)
pout("Smart output")
```

## Testing Support

### Output Capture

Use `capture_output=True` to capture output for testing:

```python
def test_my_function():
    output = pout("Test message", capture_output=True)
    assert output == "Test message\n"
    
    error = perr("Error message", capture_output=True)
    assert "Error message" in error
```

### Mock Context

Create a mock context for testing:

```python
from unittest.mock import MagicMock

def test_with_json_mode():
    ctx = MagicMock()
    ctx.obj = {'output_json': True}
    
    output = pout("Test", ctx=ctx, capture_output=True)
    assert '"Test"' in output  # JSON formatted
```

## Integration with Click

The console functions integrate seamlessly with Click commands:

```python
import click
from provide.foundation.console import pout, perr

@click.command()
@click.option('--verbose', is_flag=True)
@click.pass_context
def deploy(ctx, verbose):
    pout("Starting deployment...")
    
    try:
        # Deployment logic
        if verbose:
            pout("Connecting to server...", prefix="→")
        
        # Simulate work
        pout("Deployment successful", prefix="✅")
    except Exception as e:
        perr(f"Deployment failed: {e}", prefix="❌")
        ctx.exit(1)
```

## Best Practices

### 1. Use Appropriate Output Streams

```python
# User-facing output goes to stdout
pout("Processing complete")

# Errors and warnings go to stderr
perr("Warning: Low disk space")
```

### 2. Support JSON Mode

```python
@click.command()
@click.option('--json', 'output_json', is_flag=True)
@click.pass_context
def status(ctx, output_json):
    ctx.obj = {'output_json': output_json}
    
    data = {"status": "running", "uptime": 3600}
    
    if output_json:
        pout(data, json_key="service")
    else:
        pout(f"Status: {data['status']}")
        pout(f"Uptime: {data['uptime']}s")
```

### 3. Use Prefixes for Visual Clarity

```python
pout("Creating user", prefix="➕")
pout("Updating permissions", prefix="🔧")
pout("Sending notification", prefix="📧")
perr("Failed to save", prefix="❌")
```

### 4. Structured Logging for Complex Operations

```python
from provide.foundation import plog

def process_batch(items):
    plog.info("Starting batch processing", count=len(items))
    
    for i, item in enumerate(items):
        try:
            process_item(item)
            plog.debug("Processed item", index=i, item_id=item.id)
        except Exception as e:
            plog.error("Failed to process item", 
                      index=i, 
                      item_id=item.id, 
                      error=str(e))
    
    plog.info("Batch processing complete")
```

### 5. Test Your Output

```python
def test_command_output():
    # Test normal output
    output = pout("Success", capture_output=True)
    assert output == "Success\n"
    
    # Test error output
    error = perr("Failed", capture_output=True)
    assert error == "Failed\n"
    
    # Test JSON mode
    ctx = MagicMock()
    ctx.obj = {'output_json': True}
    json_out = pout("Test", ctx=ctx, capture_output=True)
    assert json.loads(json_out) == "Test"
```

## Migration from print()

Replace print statements with console functions:

```python
# Before
print("Starting process...")
print("ERROR: Failed to connect", file=sys.stderr)

# After
pout("Starting process...")
perr("Failed to connect", prefix="ERROR:")
```

## See Also

- [Logger](logger.md) - For structured logging with `plog`
- [CLI Framework](cli.md) - For building CLI applications
- [Error Handling](errors.md) - For error context and formatting