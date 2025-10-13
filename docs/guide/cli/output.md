# Output Formatting

Control and format CLI output using provide.foundation's console I/O functions.

## Overview

provide.foundation provides standardized console I/O functions (`pout`, `perr`, `pin`) that handle output formatting, JSON mode, color support, and stream separation. These functions ensure consistent behavior across all CLI applications.

## Output Functions

### pout() - Standard Output

Write to stdout with optional formatting:

```python
from provide.foundation import pout

# Simple output
pout("Hello, World!")

# With color and formatting
pout("Success!", color="green", bold=True)
pout("Warning", color="yellow")
pout("Error occurred", color="red")

# With prefix
pout("Processing complete", prefix="✅")
pout("Failed to connect", prefix="❌", color="red")

# Control newlines
pout("Processing...", nl=False)  # No newline
# Do work...
pout(" Done!", color="green")

# Output structured data (auto-JSON when dict/list)
results = {"status": "success", "count": 42}
pout(results)  # Automatically formatted
```

### perr() - Error Output

Write to stderr with same formatting options:

```python
from provide.foundation import perr

# Error messages go to stderr
perr("Error: File not found", color="red", bold=True)
perr("Warning: Deprecated option", color="yellow")

# With prefix
perr("Connection failed", prefix="⚠️", color="yellow")

# Structured error data
error_details = {
    "code": "E001",
    "message": "Invalid configuration",
    "file": "config.yml"
}
perr(error_details)
```

### Stream Separation

Output functions properly separate stdout and stderr:

```python
# These can be redirected independently
pout("Normal output")  # Goes to stdout
perr("Error output")   # Goes to stderr

# Shell usage:
# myapp command > output.txt 2> errors.txt
```

## Input Functions

### pin() - Standard Input

Read user input with prompts and validation:

```python
from provide.foundation import pin

# Simple input
name = pin("Enter your name: ")

# With type conversion
age = pin("Enter age: ", type=int, default=21)
ratio = pin("Ratio: ", type=float)

# Password input (hidden)
password = pin("Password: ", password=True)
confirm = pin("Confirm: ", password=True, confirmation_prompt=True)

# With color prompt
email = pin("Email: ", color="cyan", bold=True)

# With default value
host = pin("Host: ", default="localhost", show_default=True)
```

### pin_stream() - Line Streaming

Read input line by line:

```python
from provide.foundation import pin_stream, pin_lines

# Process lines as they come
for line in pin_stream():
    process_line(line)

# Read specific number of lines
headers = pin_lines(3)  # Read first 3 lines
all_input = pin_lines()  # Read until EOF
```

### Async Input

Async variants for non-blocking I/O:

```python
from provide.foundation import apin, apin_stream, apin_lines

async def get_user_input():
    # Async prompt
    name = await apin("Name: ")

    # Async stream processing
    async for line in apin_stream():
        await process_async(line)

    # Async batch reading
    lines = await apin_lines(10)
```

## JSON Output Mode

### Automatic JSON Formatting

When JSON mode is enabled, output is automatically formatted:

```python
# Via CLI flag
# myapp --json command

# In code
pout({"status": "ok", "items": [1, 2, 3]})
# Normal mode: Pretty-printed dict
# JSON mode: Valid JSON output

perr({"error": "Failed", "code": 500})
# Properly goes to stderr as JSON
```

### JSON Keys

Add structure to JSON output:

```python
# Wrap output with a key
pout(results, json_key="data")
# Output: {"data": <results>}

perr(error, json_key="error")
# Output: {"error": <error>}

# Input with JSON key
user_data = pin("Enter data: ", json_key="input")
# Returns: {"input": <user_input>}
```

## Color and Formatting

### Color Support

Colors are automatically disabled when not supported:

```python
# These colors work when stdout is a TTY
pout("Red text", color="red")
pout("Green text", color="green")
pout("Yellow text", color="yellow")
pout("Blue text", color="blue")
pout("Magenta text", color="magenta")
pout("Cyan text", color="cyan")
pout("White text", color="white")

# Combined with formatting
pout("Bold green", color="green", bold=True)
pout("Dim text", dim=True)

# Auto-disabled when piped
# myapp command | grep something  # No colors
```

### TTY Detection

Functions automatically detect TTY support:

```python
# Colors/formatting only applied when appropriate
if sys.stdout.isatty():
    # Interactive terminal - colors enabled
    pout("Colorful!", color="rainbow")
else:
    # Piped/redirected - plain text
    pout("Plain text")
```

## Context Integration

### Using Click Context

Access context for output control:

```python
import click
from provide.foundation import pout, Context

@click.command()
@click.pass_context
def command(ctx):
    # Get foundation context
    foundation_ctx = Context.get_current()

    # Output respects context settings
    pout("Output", ctx=foundation_ctx)

    # Override context
    custom_ctx = Context(json_output=True)
    pout(data, ctx=custom_ctx)  # Forces JSON
```

### Global Output Control

Control output globally via environment:

```bash
# Enable JSON output globally
export PROVIDE_JSON_OUTPUT=true

# Disable colors globally
export PROVIDE_NO_COLOR=true

# Disable emoji globally
export PROVIDE_NO_EMOJI=true
```

## Best Practices

### 1. Use Appropriate Streams

```python
# Good: Separate concerns
pout("Processing results...")  # Normal output
perr("Warning: Large file")    # Warnings/errors

# Bad: Everything to stdout
print("Results...")
print("ERROR: Failed!")  # Should use perr
```

### 2. Structured Data

```python
# Good: Structured output
results = {
    "processed": 100,
    "failed": 2,
    "duration": 45.3
}
pout(results)

# Bad: Unstructured strings
pout(f"Processed 100, failed 2, took 45.3s")
```

### 3. Consistent Formatting

```python
# Good: Consistent status indicators
pout("✅ Build successful", color="green")
pout("⚠️ Tests skipped", color="yellow")
perr("❌ Deploy failed", color="red")

# Bad: Inconsistent formatting
print("SUCCESS: Build done")
print("WARN - Tests skipped")
sys.stderr.write("ERROR!!! Deploy failed\n")
```

### 4. Interactive vs Piped

```python
# Good: Handle both modes
from provide.foundation import pout

def show_progress(items):
    for i, item in enumerate(items):
        if sys.stdout.isatty():
            # Interactive: Update in place
            pout(f"Processing {i+1}/{len(items)}...", nl=False)
        else:
            # Piped: One line per item
            pout(f"Item {i+1}: {item}")
```

## Complete Example

Here's a complete CLI with proper output handling:

```python
#!/usr/bin/env python
"""Example CLI with formatted output."""

import click
from provide.foundation import pout, perr, pin
from provide.foundation.cli import output_options, logging_options

@click.command()
@output_options
@logging_options
@click.option('--interactive', is_flag=True)
def process_data(json_output, no_color, no_emoji, interactive, **kwargs):
    """Process data with formatted output."""

    # Interactive input
    if interactive:
        name = pin("Enter dataset name: ", color="cyan")
        confirm = pin("Process now? [y/N]: ", default="n")
        if confirm.lower() != 'y':
            perr("⚠️ Cancelled by user", color="yellow")
            return

    # Status output
    pout("🚀 Starting processing...", color="blue", bold=True)

    try:
        # Simulate processing
        results = {
            "dataset": name if interactive else "default",
            "records": 1000,
            "errors": 0,
            "duration": 2.5
        }

        # Success output
        pout("✅ Processing complete!", color="green", bold=True)
        pout(results, json_key="results")

    except Exception as e:
        # Error output
        perr(f"❌ Processing failed: {e}", color="red", bold=True)
        perr({"error": str(e), "type": type(e).__name__}, json_key="error")
        raise click.ClickException(str(e))

if __name__ == "__main__":
    process_data()
```

## Related Topics

- [Arguments & Options](arguments.md) - CLI argument handling
- [Command Registration](commands.md) - Registering commands
- [Nested Commands](nested.md) - Command hierarchies