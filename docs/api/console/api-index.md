# Console API Reference

Standardized CLI input/output utilities with JSON mode support, colors, and context-aware formatting.

## Overview

The console module provides Foundation's CLI I/O system with:
- **Smart Output** - Context-aware JSON mode, colors, and formatting
- **Flexible Input** - Prompts, streaming, type conversion, and async support  
- **CLI Integration** - Click context integration with automatic detection
- **JSON Mode** - Automatic JSON handling for structured data exchange
- **Async Support** - Full async/await compatible input functions
- **Security Features** - Password input hiding and confirmation prompts

## Quick Start

```python
from provide.foundation.console import pout, perr, pin

# Basic output
pout("Hello, world!")
perr("Error occurred", color="red")

# JSON mode (when context.json_output=True)
pout({"status": "success", "data": results})

# Interactive input
name = pin("Enter your name: ")
age = pin("Age: ", type=int, default=0)
password = pin("Password: ", password=True)

# Streaming input
for line in pin_stream():
    process_line(line)
```

## Output Functions

### `pout(message, **kwargs) -> None`

Output message to stdout with formatting and JSON mode support.

**Parameters**:
- `message: Any` - Content to output (any type - will be stringified or JSON-encoded)
- `**kwargs` - Optional formatting arguments:
  - `color: str` - Color name (red, green, yellow, blue, cyan, magenta, white)
  - `bold: bool` - Bold text formatting
  - `dim: bool` - Dim text formatting
  - `nl: bool` - Add newline (default: True, also accepts `newline`)
  - `json_key: str` - Key for JSON output mode
  - `prefix: str` - Optional prefix string
  - `ctx: Context` - Override context

```python
from provide.foundation.console import pout

# Basic output
pout("Hello, world!")
pout("Processing complete")

# With formatting
pout("Success!", color="green", bold=True)
pout("Warning:", color="yellow", prefix="⚠️")
pout("Dimmed text", dim=True)

# JSON data (auto-detected)
pout({"user": "john", "status": "active"})
pout([1, 2, 3, 4, 5])

# JSON mode with specific key
pout(user_data, json_key="user_profile")

# Control newlines
pout("Loading", nl=False)  # No newline
pout("...", color="blue")  # Continues on same line
```

### `perr(message, **kwargs) -> None`

Output message to stderr with formatting and JSON mode support.

**Parameters**: Same as `pout()` but outputs to stderr

```python
from provide.foundation.console import perr

# Error messages
perr("Connection failed", color="red")
perr("Configuration error", color="red", bold=True)

# Warnings
perr("Deprecated feature used", color="yellow")
perr("High memory usage", color="yellow", prefix="⚠️")

# Debug information to stderr
perr({"debug": "trace_info", "level": "verbose"})

# Structured errors in JSON mode
perr({"error": "validation_failed", "details": error_details}, json_key="error")
```

## Input Functions

### `pin(prompt: str = "", **kwargs) -> str | Any`

Interactive input from stdin with optional prompt and type conversion.

**Parameters**:
- `prompt: str` - Prompt to display before input
- `**kwargs` - Optional formatting arguments:
  - `type: callable` - Type to convert input to (int, float, bool, etc.)
  - `default: Any` - Default value if no input provided
  - `password: bool` - Hide input for passwords (default: False)
  - `confirmation_prompt: bool` - Ask for confirmation (for passwords)
  - `hide_input: bool` - Hide the input (same as password)
  - `show_default: bool` - Show default value in prompt
  - `value_proc: callable` - Callable to process the value
  - `json_key: str` - Key for JSON output mode
  - `ctx: Context` - Override context
  - `color: str` - Color for prompt
  - `bold: bool` - Bold prompt text

**Returns**: User input as string or converted type

```python
from provide.foundation.console import pin

# Basic input
name = pin("Enter your name: ")
print(f"Hello, {name}!")

# Type conversion
age = pin("Age: ", type=int, default=0)
price = pin("Price: $", type=float)
confirm = pin("Continue? (y/n): ", type=bool)

# Default values
host = pin("Database host: ", default="localhost", show_default=True)
# Displays: Database host [localhost]: 

# Password input (hidden)
password = pin("Password: ", password=True)
new_password = pin("New password: ", password=True, confirmation_prompt=True)

# Custom validation
def validate_email(value):
    if "@" not in value:
        raise ValueError("Invalid email format")
    return value.lower()

email = pin("Email: ", value_proc=validate_email)

# Colored prompts
pin("Enter command: ", color="cyan", bold=True)
```

### `pin_stream() -> Iterator[str]`

Stream input line by line from stdin.

**Returns**: Iterator yielding lines from stdin (without trailing newline)

```python
from provide.foundation.console import pin_stream

# Process lines as they come
print("Enter lines (Ctrl+D to end):")
for line in pin_stream():
    if line.startswith("quit"):
        break
    
    processed = process_line(line)
    pout(f"Result: {processed}")

# Read configuration data
config_lines = []
pout("Enter configuration (empty line to finish):")
for line in pin_stream():
    if not line.strip():
        break
    config_lines.append(line)

config = parse_config(config_lines)
```

### `pin_lines(count: int | None = None) -> list[str]`

Read multiple lines from stdin at once.

**Parameters**:
- `count: int | None` - Number of lines to read (None for all until EOF)

**Returns**: List of input lines

```python
from provide.foundation.console import pin_lines

# Read exactly 3 lines
pout("Enter 3 favorite colors:")
colors = pin_lines(3)
pout(f"Your colors: {', '.join(colors)}")

# Read all lines until EOF
pout("Paste your data (Ctrl+D when done):")
all_lines = pin_lines()
total_chars = sum(len(line) for line in all_lines)
pout(f"Read {len(all_lines)} lines, {total_chars} characters")

# Read batch input
pout("Enter batch commands:")
commands = pin_lines(5)  # Read exactly 5 commands
for i, cmd in enumerate(commands, 1):
    pout(f"Executing command {i}: {cmd}")
    execute_command(cmd)
```

## Async Input Functions

### `async apin(prompt: str = "", **kwargs) -> str | Any`

Async version of `pin()` for non-blocking input.

**Parameters**: Same as `pin()`
**Returns**: User input as string or converted type

```python
import asyncio
from provide.foundation.console import apin, pout

async def get_user_info():
    """Collect user information asynchronously."""
    pout("User Registration")
    
    # Collect input without blocking event loop
    name = await apin("Name: ")
    age = await apin("Age: ", type=int, default=0)
    email = await apin("Email: ")
    
    # Password with confirmation
    password = await apin("Password: ", password=True, confirmation_prompt=True)
    
    return {
        "name": name,
        "age": age, 
        "email": email,
        "password_set": bool(password)
    }

# Usage in async context
async def main():
    user_data = await get_user_info()
    pout("Registration complete!", color="green")
    pout(user_data, json_key="user")

asyncio.run(main())
```

### `async apin_stream() -> AsyncIterator[str]`

Async stream input line by line from stdin.

**Returns**: Async iterator yielding lines from stdin

```python
import asyncio
from provide.foundation.console import apin_stream, pout

async def process_input_stream():
    """Process streaming input asynchronously."""
    pout("Starting stream processor...")
    
    line_count = 0
    async for line in apin_stream():
        line_count += 1
        
        # Process line asynchronously
        result = await process_line_async(line)
        pout(f"[{line_count}] {result}")
        
        if line.strip().lower() == "quit":
            break
    
    pout(f"Processed {line_count} lines")

async def chat_interface():
    """Simple async chat interface."""
    pout("Chat started. Type 'quit' to exit.")
    
    async for message in apin_stream():
        if message.strip().lower() == "quit":
            pout("Chat ended.", color="yellow")
            break
        
        # Simulate async processing
        await asyncio.sleep(0.1)
        response = await generate_response(message)
        pout(f"Bot: {response}", color="blue")

asyncio.run(chat_interface())
```

### `async apin_lines(count: int | None = None) -> list[str]`

Async version of `pin_lines()` for batch input.

**Parameters**:
- `count: int | None` - Number of lines to read (None for all until EOF)

**Returns**: List of input lines

```python
import asyncio
from provide.foundation.console import apin_lines, pout

async def batch_processor():
    """Process batch input asynchronously."""
    pout("Enter batch data (5 lines):")
    
    # Read exactly 5 lines asynchronously  
    lines = await apin_lines(5)
    
    # Process batch concurrently
    tasks = [process_item_async(line) for line in lines]
    results = await asyncio.gather(*tasks)
    
    pout("Batch processing complete:")
    for line, result in zip(lines, results):
        pout(f"{line} → {result}")

async def config_loader():
    """Load configuration asynchronously."""
    pout("Paste configuration data (Ctrl+D when done):")
    
    # Read all available lines
    config_lines = await apin_lines()
    
    # Parse asynchronously
    config = await parse_config_async(config_lines)
    pout("Configuration loaded:", color="green")
    pout(config, json_key="config")

asyncio.run(batch_processor())
```

## JSON Mode Integration

The console functions automatically detect JSON mode from the CLI context and adjust behavior accordingly.

### Automatic JSON Detection

```python
from provide.foundation.console import pout, pin
from provide.foundation.context import Context

# In regular mode
pout("Hello, world!")  # Outputs: Hello, world!
pout({"key": "value"})  # Outputs: {"key": "value"}

# In JSON mode (when context.json_output=True)
pout("Hello, world!")  # Outputs: "Hello, world!"
pout({"key": "value"})  # Outputs: {"key": "value"}

# With json_key
pout("success", json_key="status")  # Outputs: {"status": "success"}
```

### JSON Input Handling

```python
from provide.foundation.console import pin, pin_stream

# In JSON mode, pin() can parse JSON input
user_data = pin("User data: ")  # Can accept: {"name": "John", "age": 30}

# Streaming JSON input
for line in pin_stream():
    # Each line can be JSON object or plain text
    if line.startswith("{"):
        data = json.loads(line)
        process_json(data)
    else:
        process_text(line)
```

## CLI Context Integration

Console functions integrate with Click contexts and Foundation's Context system.

### Context Detection

```python
import click
from provide.foundation.console import pout
from provide.foundation.context import Context

@click.command()
@click.option('--json', 'json_output', is_flag=True)
@click.option('--color/--no-color', default=True)
@click.pass_context
def my_command(ctx, json_output, color):
    # Set up Foundation context
    ctx.obj = Context(json_output=json_output, use_color=color)
    
    # Console functions automatically detect JSON mode
    pout("Command started")  # Plain text or JSON based on --json flag
    
    data = {"processed": 100, "errors": 0}
    pout(data, json_key="results")  # Structured output
```

### Manual Context Override

```python
from provide.foundation.console import pout, perr
from provide.foundation.context import Context

# Create custom context
json_ctx = Context(json_output=True)
color_ctx = Context(use_color=False)

# Override context for specific calls
pout("Normal output")  # Uses detected context
pout("JSON output", ctx=json_ctx)  # Force JSON mode
pout("No color", color="red", ctx=color_ctx)  # Force no color
```

## Advanced Usage

### Custom Type Conversion

```python
from provide.foundation.console import pin
from datetime import datetime

def parse_date(value):
    """Parse date input in multiple formats."""
    formats = ["%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: {value}")

# Use custom parser
date = pin("Enter date (YYYY-MM-DD): ", type=parse_date)
pout(f"Parsed date: {date}")
```

### Input Validation

```python
from provide.foundation.console import pin
import re

def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValueError("Invalid email format")
    return email.lower()

def validate_port(port):
    """Validate port number."""
    port = int(port)  # This may raise ValueError
    if not (1 <= port <= 65535):
        raise ValueError("Port must be between 1 and 65535")
    return port

# Validated input with retry on error
while True:
    try:
        email = pin("Email: ", value_proc=validate_email)
        break
    except ValueError as e:
        perr(f"Error: {e}", color="red")

port = pin("Port: ", type=validate_port, default=8080)
```

### Streaming Data Processing

```python
import asyncio
from provide.foundation.console import apin_stream, pout

async def real_time_processor():
    """Process streaming data in real-time."""
    pout("Real-time processor started. Enter data:")
    
    buffer = []
    async for line in apin_stream():
        buffer.append(line)
        
        # Process buffer every 5 lines
        if len(buffer) >= 5:
            await process_batch(buffer)
            pout(f"Processed batch of {len(buffer)} items", color="green")
            buffer.clear()
        
        if line.strip().lower() == "end":
            break
    
    # Process remaining buffer
    if buffer:
        await process_batch(buffer)
        pout(f"Processed final batch of {len(buffer)} items", color="green")

async def process_batch(items):
    """Simulate async batch processing."""
    await asyncio.sleep(0.5)  # Simulate processing time
    return [item.upper() for item in items]
```

### Progress Indicators

```python
import time
from provide.foundation.console import pout

def show_progress(total, current):
    """Simple progress indicator."""
    percent = (current / total) * 100
    bar_length = 20
    filled = int(bar_length * current / total)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    pout(f"Progress: {bar} {percent:.1f}% ({current}/{total})", nl=False)
    if current < total:
        print("\r", end="")  # Carriage return to overwrite
    else:
        print()  # Final newline

# Usage
for i in range(1, 101):
    show_progress(100, i)
    time.sleep(0.1)

pout("Complete!", color="green")
```

## Error Handling

### Input Error Recovery

```python
from provide.foundation.console import pin, perr

def get_integer(prompt, min_val=None, max_val=None):
    """Get integer input with validation and retry."""
    while True:
        try:
            value = pin(prompt, type=int)
            
            if min_val is not None and value < min_val:
                perr(f"Value must be at least {min_val}", color="red")
                continue
                
            if max_val is not None and value > max_val:
                perr(f"Value must be at most {max_val}", color="red")
                continue
                
            return value
            
        except ValueError:
            perr("Please enter a valid integer", color="red")
        except KeyboardInterrupt:
            perr("\nOperation cancelled", color="yellow")
            return None

# Usage
age = get_integer("Age: ", min_val=0, max_val=150)
if age is not None:
    pout(f"Age entered: {age}")
```

### Stream Error Handling

```python
import asyncio
from provide.foundation.console import apin_stream, perr, pout

async def robust_stream_processor():
    """Stream processor with error handling."""
    try:
        async for line in apin_stream():
            try:
                # Process each line
                result = await process_line(line)
                pout(f"✓ {result}", color="green")
                
            except ValueError as e:
                perr(f"✗ Invalid data: {e}", color="red")
                continue
                
            except Exception as e:
                perr(f"✗ Processing error: {e}", color="red")
                continue
                
    except KeyboardInterrupt:
        pout("\nStream processing interrupted", color="yellow")
    except EOFError:
        pout("Stream ended", color="blue")
    except Exception as e:
        perr(f"Stream error: {e}", color="red")

async def process_line(line):
    """Process a single line (may raise exceptions)."""
    if not line.strip():
        raise ValueError("Empty line")
    
    # Simulate processing
    await asyncio.sleep(0.1)
    return line.upper()
```

## Best Practices

### 1. Use Appropriate Output Functions

```python
# ✅ Good - Use perr for errors
perr("Configuration file not found", color="red")
pout("Processing complete", color="green")

# ❌ Bad - Don't mix error output to stdout
pout("Error: file not found")  # This goes to stdout
```

### 2. Handle JSON Mode Gracefully

```python
# ✅ Good - Provide json_key for structured output
pout(results, json_key="results")
perr(error_details, json_key="error")

# ✅ Good - Let auto-detection work for objects
pout({"status": "success", "count": 42})

# ❌ Bad - Don't force string conversion in JSON mode
pout(str(results))  # Loses structure in JSON mode
```

### 3. Use Type Conversion and Validation

```python
# ✅ Good - Use type conversion and defaults
port = pin("Port: ", type=int, default=8080)
confirm = pin("Continue? ", type=bool)

# ✅ Good - Use validation functions
email = pin("Email: ", value_proc=validate_email)

# ❌ Bad - Manual conversion without error handling
port_str = pin("Port: ")
port = int(port_str)  # May raise ValueError
```

### 4. Handle Async Properly

```python
# ✅ Good - Use async functions in async contexts
async def async_workflow():
    name = await apin("Name: ")
    async for line in apin_stream():
        await process_line_async(line)

# ❌ Bad - Don't mix sync and async incorrectly
async def bad_workflow():
    name = pin("Name: ")  # Blocks event loop
    for line in pin_stream():  # Blocks event loop
        await process_line_async(line)
```

## Thread Safety

All console functions are thread-safe and can be used from multiple threads:

```python
import threading
from provide.foundation.console import pout, perr

def worker(worker_id):
    """Worker thread function."""
    for i in range(5):
        pout(f"Worker {worker_id}: Processing item {i}")
        time.sleep(0.1)
    
    pout(f"Worker {worker_id} completed", color="green")

# Safe to use from multiple threads
threads = [
    threading.Thread(target=worker, args=(i,))
    for i in range(3)
]

for t in threads:
    t.start()
for t in threads:
    t.join()

pout("All workers completed", color="green", bold=True)
```

## See Also

- [Context API](../context/index.md) - Foundation context system
- [CLI Guide](../../guide/cli/index.md) - Building CLI applications
- [Logger API](../logger/index.md) - Structured logging integration
- [Testing API](../testing/index.md) - Testing console interactions