# Console I/O Guide

The provide.foundation library provides a complete I/O trinity for console operations: `pout()`, `perr()`, and `pin()`. These functions provide consistent, context-aware I/O handling with support for JSON mode, colors, and streaming.

## The I/O Trinity

### Output Functions

#### pout() - Standard Output
```python
from provide.foundation import pout

# Basic output
pout("Hello, world!")

# Colored output
pout("Success!", color="green", bold=True)

# JSON mode (automatic when ctx.json_output is True)
pout({"status": "complete", "count": 42})
```

#### perr() - Error Output
```python
from provide.foundation import perr

# Basic error output (goes to stderr)
perr("Error occurred")

# Styled error
perr("Warning!", color="yellow")

# JSON error output
perr({"error": "Failed to connect"}, json_key="error")
```

### Input Functions

#### pin() - Standard Input
```python
from provide.foundation import pin

# Basic input
name = pin("Enter your name: ")

# Type conversion
age = pin("Enter age: ", type=int, default=0)

# Password input (hidden)
password = pin("Password: ", password=True)

# With validation
email = pin("Email: ", 
    value_proc=lambda x: x if '@' in x else None)
```

## Streaming Input

### Synchronous Streaming
```python
from provide.foundation.console import pin_stream, pin_lines

# Stream line by line
for line in pin_stream():
    process(line)
    if line == "STOP":
        break

# Read specific number of lines
lines = pin_lines(5)  # Read 5 lines
all_lines = pin_lines()  # Read until EOF
```

### Asynchronous Streaming
```python
from provide.foundation.console import apin, apin_stream, apin_lines
import asyncio

async def process_input():
    # Async single input
    name = await apin("Name: ")
    
    # Async streaming
    async for line in apin_stream():
        await process_line(line)
        if line == "QUIT":
            break
    
    # Read multiple lines asynchronously
    lines = await apin_lines(10)
```

## JSON Mode Integration

All I/O functions respect the Context's JSON mode setting:

```python
from provide.foundation import Context, pout, perr, pin

ctx = Context()
ctx.json_output = True

# In JSON mode, input/output is structured
pout({"message": "Starting"}, ctx=ctx)
user_data = pin("Data: ", ctx=ctx)  # Expects JSON input
perr({"error": "Failed"}, ctx=ctx)
```

When JSON mode is active:
- `pout()` and `perr()` output JSON-formatted data
- `pin()` attempts to parse input as JSON
- Streaming functions handle JSON arrays/objects

## Real-World Examples

### Interactive CLI Tool
```python
from provide.foundation import pout, perr, pin

def interactive_menu():
    pout("=== Main Menu ===", color="cyan", bold=True)
    pout("1. Process data")
    pout("2. View status")
    pout("3. Exit")
    
    choice = pin("Select option: ", type=int)
    
    if choice == 1:
        filename = pin("Enter filename: ")
        if not filename:
            perr("No filename provided", color="red")
            return
        process_file(filename)
    elif choice == 2:
        show_status()
    elif choice == 3:
        pout("Goodbye!", color="green")
        exit(0)
    else:
        perr(f"Invalid choice: {choice}", color="yellow")
```

### Stream Processing Pipeline
```python
from provide.foundation.console import pin_stream, pout, perr

def process_pipeline():
    pout("Starting pipeline processor", color="green")
    pout("Enter data (one item per line, 'END' to finish):")
    
    results = []
    for line in pin_stream():
        if line == "END":
            break
        
        try:
            # Process each line
            result = transform(line)
            results.append(result)
            pout(f"✓ Processed: {line}", color="green", dim=True)
        except Exception as e:
            perr(f"✗ Failed: {line} - {e}", color="red")
    
    pout(f"Processed {len(results)} items successfully", bold=True)
    return results
```

### Async Data Ingestion
```python
import asyncio
from provide.foundation.console import apin_stream, pout, perr

async def ingest_data():
    pout("📥 Starting async data ingestion", color="blue")
    
    batch = []
    batch_size = 100
    
    async for line in apin_stream():
        batch.append(line)
        
        if len(batch) >= batch_size:
            # Process batch asynchronously
            await process_batch(batch)
            pout(f"✓ Processed batch of {len(batch)}", dim=True)
            batch = []
    
    # Process remaining items
    if batch:
        await process_batch(batch)
    
    pout("✅ Ingestion complete", color="green", bold=True)

# Run the async function
asyncio.run(ingest_data())
```

### CI/CD Integration
```python
from provide.foundation import Context, pout, pin

# In CI environments, use JSON mode for structured output
ctx = Context()
ctx.json_output = os.getenv("CI") == "true"

if ctx.json_output:
    # Structured output for CI tools
    pout({"step": "build", "status": "starting"}, ctx=ctx)
    config = pin("", ctx=ctx)  # Read JSON config from stdin
    pout({"step": "build", "status": "complete", "config": config}, ctx=ctx)
else:
    # Human-readable output for local development
    pout("🔨 Building project...", color="blue")
    config_file = pin("Config file (or press Enter for default): ")
    pout("✅ Build complete", color="green")
```

## Best Practices

1. **Use the appropriate function**: `pout()` for normal output, `perr()` for errors/warnings
2. **Handle JSON mode**: Always consider that your code might run in JSON mode
3. **Add color judiciously**: Use color to enhance readability, not distract
4. **Stream for large inputs**: Use streaming functions for potentially large input
5. **Go async when needed**: Use async variants for I/O-heavy operations
6. **Validate input**: Use `type` and `value_proc` parameters for input validation

## Advanced Features

### Context Override
```python
# Override context for specific operations
test_ctx = Context()
test_ctx.json_output = True

pout("Normal output")
pout({"json": "output"}, ctx=test_ctx)  # Forces JSON mode
```

### Custom Input Processing
```python
# Custom value processor
def validate_email(value):
    import re
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
        return value
    raise click.BadParameter("Invalid email address")

email = pin("Email: ", value_proc=validate_email)
```

### Streaming with Filtering
```python
# Process only non-empty lines
for line in pin_stream():
    if line.strip():  # Skip empty lines
        process(line)
```

## Error Handling

Always handle potential errors in I/O operations:

```python
from provide.foundation import pout, perr, pin

try:
    data = pin("Enter JSON data: ", type=json.loads)
    pout(f"Received: {data}")
except Exception as e:
    perr(f"Invalid input: {e}", color="red")
```

## Summary

The provide.foundation console I/O functions provide a complete, consistent interface for all console operations:

- **pout()**: Standard output with formatting and JSON support
- **perr()**: Error output to stderr with same features
- **pin()**: Flexible input with type conversion and validation
- **Streaming**: Both sync and async streaming for efficient I/O
- **JSON Mode**: Automatic structured I/O for CI/automation

This trinity of functions ensures your CLI tools have professional, consistent I/O handling across all scenarios.