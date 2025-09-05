# Console Utilities

Console I/O utilities for CLI applications.

## Overview

provide.foundation's console utilities (`pout`, `perr`, `pin`) provide standardized input/output handling for CLI applications. These utilities handle JSON mode, color support, stream separation, and interactive prompts seamlessly.

## Output Functions

### pout() - Standard Output

Write formatted output to stdout:

```python
from provide.foundation import pout

# Simple output
pout("Hello, World!")

# With formatting
pout("Success!", color="green", bold=True)
pout("Warning", color="yellow", dim=True)

# With prefix
pout("Task complete", prefix="✅")

# Structured data (auto-formatted)
data = {"status": "ok", "count": 42}
pout(data)

# Control newlines
pout("Processing...", nl=False)
time.sleep(1)
pout(" Done!", color="green")
```

### perr() - Error Output

Write to stderr with same interface:

```python
from provide.foundation import perr

# Error messages
perr("Error: File not found", color="red", bold=True)
perr("Warning: Deprecated", color="yellow")

# With context
perr({"error": "Invalid input", "line": 42}, json_key="error")
```

## Input Functions  

### pin() - User Input

Read input with prompts and validation:

```python
from provide.foundation import pin

# Simple prompt
name = pin("Enter name: ")

# Type conversion
age = pin("Age: ", type=int, default=25)

# Hidden input
password = pin("Password: ", password=True)

# Colored prompt
email = pin("Email: ", color="cyan", bold=True)
```

### Streaming Input

Process input line by line:

```python
from provide.foundation import pin_stream, pin_lines

# Stream lines
for line in pin_stream():
    pout(f"Processing: {line}")

# Read specific number
headers = pin_lines(3)  # First 3 lines
```

### Async Input

Non-blocking input operations:

```python
from provide.foundation import apin, apin_stream

async def get_input():
    # Async prompt
    name = await apin("Name: ")
    
    # Async streaming
    async for line in apin_stream():
        await process(line)
```

## JSON Mode

### Automatic Formatting

JSON output when enabled:

```python
# Enable via CLI: myapp --json command

# Structured output
result = {"items": [1, 2, 3], "total": 3}
pout(result)  # Outputs valid JSON

# With key wrapping
pout(data, json_key="response")
# {"response": <data>}
```

### Input in JSON Mode

Handle JSON input:

```python
# Read JSON from stdin
data = pin()  # Automatically parses JSON

# Stream JSON lines
for line in pin_stream():
    # Each line parsed as JSON
    process_json(line)
```

## Color Support

### Available Colors

```python
# Standard colors
pout("Red", color="red")
pout("Green", color="green")
pout("Yellow", color="yellow")
pout("Blue", color="blue")
pout("Magenta", color="magenta")
pout("Cyan", color="cyan")
pout("White", color="white")

# With styles
pout("Bold", bold=True)
pout("Dim", dim=True)
pout("Bold Green", color="green", bold=True)
```

### TTY Detection

Colors auto-disabled when not supported:

```python
import sys

# Automatic detection
if sys.stdout.isatty():
    pout("Colorful!", color="rainbow")
else:
    pout("Plain text")

# Force disable
pout("No color", no_color=True)
```

## Environment Variables

Control behavior via environment:

```bash
# JSON output
export PROVIDE_JSON_OUTPUT=true

# Disable colors
export PROVIDE_NO_COLOR=true  

# Disable emoji
export PROVIDE_NO_EMOJI=true
```

## Complete Examples

### Interactive CLI

```python
from provide.foundation import pout, perr, pin

def interactive_setup():
    """Interactive configuration setup."""
    pout("🔧 Configuration Setup", color="blue", bold=True)
    pout("-" * 40)
    
    # Get configuration
    host = pin("Database host: ", default="localhost")
    port = pin("Port: ", type=int, default=5432)
    username = pin("Username: ")
    password = pin("Password: ", password=True)
    
    # Confirm
    pout("\n📝 Configuration Summary:", color="cyan")
    pout(f"  Host: {host}:{port}")
    pout(f"  User: {username}")
    
    confirm = pin("\nSave configuration? [y/N]: ", default="n")
    
    if confirm.lower() == 'y':
        pout("✅ Configuration saved!", color="green")
        return {"host": host, "port": port, "username": username}
    else:
        perr("❌ Configuration cancelled", color="yellow")
        return None
```

### Data Processing Pipeline

```python
from provide.foundation import pout, perr, pin_stream

def process_pipeline():
    """Process streaming data with feedback."""
    pout("📥 Reading input stream...", color="blue")
    
    processed = 0
    errors = 0
    
    for line in pin_stream():
        try:
            # Process line
            result = transform(line)
            pout(result)
            processed += 1
            
        except ValueError as e:
            perr(f"⚠️ Skipped invalid: {e}", color="yellow")
            errors += 1
    
    # Summary
    pout("-" * 40)
    pout(f"✅ Processed: {processed}", color="green")
    if errors:
        perr(f"⚠️ Errors: {errors}", color="yellow")
```

### Progress Indicator

```python
import time
from provide.foundation import pout

def show_progress(items):
    """Show progress for batch processing."""
    total = len(items)
    
    for i, item in enumerate(items, 1):
        # Update in place
        pout(f"\rProcessing {i}/{total}...", nl=False)
        
        # Process item
        process(item)
    
    # Final status
    pout(f"\r✅ Completed {total} items", color="green")
```

## Best Practices

### 1. Stream Separation

```python
# Good: Use appropriate streams
pout("Results here")      # stdout
perr("Errors here")       # stderr

# Allows: myapp > output.txt 2> errors.txt
```

### 2. Structured Output

```python
# Good: Structured data
pout({"status": "success", "count": 10})

# Bad: Formatted strings
print(f"Status: success, Count: 10")
```

### 3. Interactive vs Batch

```python
def smart_output(data, interactive=None):
    """Adapt output to context."""
    if interactive is None:
        interactive = sys.stdout.isatty()
    
    if interactive:
        # Rich formatting for terminal
        pout("✨ Results:", color="cyan", bold=True)
        for item in data:
            pout(f"  • {item}")
    else:
        # Machine-readable for pipes
        pout(data)  # JSON or plain
```

### 4. Error Context

```python
# Good: Contextual errors
perr("Database connection failed",
     color="red",
     prefix="❌")

# Include structured context
perr({"error": "Connection timeout",
      "host": "db.example.com",
      "port": 5432},
     json_key="database_error")
```

## Related Topics

- [CLI Output](../cli/output.md) - CLI output formatting
- [Logging](../logging/basic.md) - Structured logging
- [CLI Arguments](../cli/arguments.md) - Input handling