# Console

::: provide.foundation.console

## Overview

The console module provides standardized CLI input/output functions for consistent user interaction across applications. It offers both synchronous and asynchronous variants with support for JSON mode, colored output, streaming, and integration with the foundation's Context system.

## Key Features

- **Standardized Output**: `pout()` for stdout, `perr()` for stderr
- **Interactive Input**: `pin()` with type conversion and validation
- **Stream Processing**: Line-by-line input streaming
- **Async Support**: Full async/await compatibility
- **JSON Mode**: Automatic JSON formatting for data interchange
- **Color Support**: Terminal color and styling support
- **Context Integration**: Automatic detection of output preferences

## Quick Start

```python
from provide.foundation import pout, perr, pin

# Basic output
pout("✅ Operation successful")
perr("❌ Error occurred") 

# Interactive input
name = pin("Enter your name: ")
age = pin("Enter age: ", type=int, default=0)

# Styled output
pout("Success!", color="green", bold=True)
perr("Warning", color="yellow")

# JSON mode (when context.json_output = True)
pout({"status": "success", "data": results})
```

## API Reference

### Output Functions

#### `pout(message, **kwargs)`

Output message to stdout with optional formatting.

**Parameters:**
- `message` (Any): Content to output (will be stringified or JSON-encoded)
- `**kwargs`: Formatting options:
  - `color` (str): Color name (red, green, yellow, blue, cyan, magenta, white)
  - `bold` (bool): Bold text styling
  - `dim` (bool): Dim text styling  
  - `nl`/`newline` (bool): Add newline (default: True)
  - `json_key` (str): Key for JSON output mode
  - `prefix` (str): Optional prefix string
  - `ctx` (Context): Override context for formatting decisions

**Examples:**
```python
from provide.foundation import pout

# Basic output
pout("Hello world")

# Styled output  
pout("Success!", color="green", bold=True)
pout("Info", color="blue", dim=True)

# With prefix
pout("Task completed", prefix="[INFO]")

# JSON mode output
pout({"status": "ok", "count": 42})
pout(results, json_key="results")

# No newline
pout("Loading", nl=False)
pout("...", nl=False)
pout(" Done!")
```

#### `perr(message, **kwargs)`

Output message to stderr with optional formatting.

**Parameters:**
- `message` (Any): Content to output (will be stringified or JSON-encoded) 
- `**kwargs`: Same formatting options as `pout()`

**Examples:**
```python
from provide.foundation import perr

# Error messages
perr("File not found!")
perr("Invalid input", color="red", bold=True)

# Warnings
perr("Deprecated API", color="yellow")

# Structured error data
perr({"error": "ValidationError", "field": "email", "message": "Invalid format"})

# With error prefix
perr("Connection failed", prefix="[ERROR]")
```

### Input Functions

#### `pin(prompt="", **kwargs)`

Interactive input from stdin with optional prompt and type conversion.

**Parameters:**
- `prompt` (str): Prompt to display before input
- `**kwargs`: Input options:
  - `type`: Type converter (int, float, bool, etc.)
  - `default`: Default value if no input provided
  - `password`/`hide_input` (bool): Hide input for passwords
  - `confirmation_prompt` (bool): Ask for confirmation (passwords)
  - `show_default` (bool): Show default value in prompt
  - `value_proc` (callable): Custom value processor
  - `json_key` (str): Key for JSON mode
  - `color` (str): Prompt color
  - `bold` (bool): Bold prompt text
  - `ctx` (Context): Override context

**Returns:**
- User input as string or converted type

**Examples:**
```python
from provide.foundation import pin

# Basic input
name = pin("Enter your name: ")
print(f"Hello, {name}!")

# Type conversion
age = pin("Enter age: ", type=int, default=0)
price = pin("Enter price: $", type=float)

# Boolean input (accepts yes/no, true/false, 1/0)
debug = pin("Enable debug mode? ", type=bool, default=False)

# Password input (hidden)
password = pin("Password: ", password=True)
password = pin("New password: ", password=True, confirmation_prompt=True)

# With defaults shown
config_file = pin("Config file: ", default="config.json", show_default=True)

# Styled prompts
username = pin("Username: ", color="cyan", bold=True)

# Custom validation
def validate_email(email):
    if "@" not in email:
        raise ValueError("Invalid email format")
    return email.lower()

email = pin("Email: ", value_proc=validate_email)
```

#### `pin_lines(count=None)`

Read multiple lines from stdin.

**Parameters:**
- `count` (int, optional): Number of lines to read (None for all until EOF)

**Returns:**
- `list[str]`: List of input lines

**Examples:**
```python
from provide.foundation import pin_lines

# Read exactly 3 lines
lines = pin_lines(3)
print(f"Got {len(lines)} lines")

# Read all input until EOF
all_lines = pin_lines()
content = "\n".join(all_lines)

# Read poem input
pout("Enter your poem (Ctrl+D to finish):")
poem_lines = pin_lines()
poem = "\n".join(poem_lines)
```

#### `pin_stream()`

Stream input line by line from stdin.

**Returns:**
- `Iterator[str]`: Iterator yielding lines from stdin

**Examples:**
```python
from provide.foundation import pin_stream

# Process lines as they arrive
pout("Enter commands (Ctrl+D to finish):")
for line in pin_stream():
    if line.strip() == "quit":
        break
    pout(f"Processing: {line}")

# Log processing with streaming
pout("Paste log data:")
for line_num, line in enumerate(pin_stream(), 1):
    if "ERROR" in line:
        perr(f"Line {line_num}: {line}")
    else:
        pout(f"Line {line_num}: OK")
```

### Async Input Functions

#### `apin(prompt="", **kwargs)`

Async version of `pin()` for non-blocking input.

**Parameters:**
- Same as `pin()`

**Returns:**
- `str | Any`: User input as string or converted type

**Examples:**
```python
from provide.foundation import apin
import asyncio

async def get_user_info():
    name = await apin("Name: ")
    age = await apin("Age: ", type=int)
    email = await apin("Email: ")
    
    return {"name": name, "age": age, "email": email}

# Run async
user_info = asyncio.run(get_user_info())
```

#### `apin_lines(count=None)`

Async version of `pin_lines()`.

**Parameters:**
- `count` (int, optional): Number of lines to read

**Returns:**
- `list[str]`: List of input lines

#### `apin_stream()`

Async stream input line by line from stdin.

**Returns:**
- `AsyncIterator[str]`: Async iterator yielding lines

**Examples:**
```python
from provide.foundation import apin_stream, pout
import asyncio

async def process_stream():
    pout("Starting stream processor...")
    line_count = 0
    
    async for line in apin_stream():
        line_count += 1
        
        # Simulate async processing
        await asyncio.sleep(0.1)
        pout(f"Processed line {line_count}: {len(line)} chars")
        
        if line.strip() == "stop":
            break
    
    pout(f"Finished processing {line_count} lines")

# Run async stream processing
asyncio.run(process_stream())
```

## JSON Mode

When the Context has `json_output=True`, console functions automatically switch to JSON mode:

**Output Functions:**
```python
from provide.foundation import pout, perr, Context

# Enable JSON mode
ctx = Context(json_output=True)

# Regular output becomes JSON
pout("Hello")  # {"message": "Hello"}
pout({"key": "value"})  # {"key": "value"}

# With json_key
pout(data, json_key="results")  # {"results": data}

# Error output
perr("Failed", json_key="error")  # {"error": "Failed"}
```

**Input Functions:**
```python
# JSON input mode
name = pin("Name: ")  # Reads JSON from stdin
# Input: "John Doe" -> Returns: "John Doe"
# Input: {"first": "John", "last": "Doe"} -> Returns: {"first": "John", "last": "Doe"}

# With json_key
result = pin("Data: ", json_key="input")  # {"input": <data>}
```

## Color and Styling

### Supported Colors

- `red`, `green`, `yellow`, `blue`, `cyan`, `magenta`, `white`, `black`
- `bright_red`, `bright_green`, `bright_yellow`, `bright_blue`, `bright_cyan`, `bright_magenta`, `bright_white`

### Styling Options

- `bold=True`: Bold text
- `dim=True`: Dim/faded text  
- `underline=True`: Underlined text (terminal dependent)

**Examples:**
```python
from provide.foundation import pout, perr

# Success messages
pout("✅ Success", color="green", bold=True)

# Warning messages  
pout("⚠️ Warning", color="yellow")

# Error messages
perr("❌ Error", color="red", bold=True)

# Info messages
pout("ℹ️ Info", color="blue", dim=True)

# Bright colors
pout("Attention!", color="bright_red", bold=True)
```

## Context Integration

Console functions automatically integrate with the foundation's Context system:

```python
from provide.foundation import Context, pout, perr, pin

# Create context with preferences
ctx = Context(
    json_output=True,
    no_color=True,
    profile="production"
)

# Functions respect context settings
pout("Message")  # Outputs as JSON
pin("Input: ")   # Reads JSON format

# Override context per call
pout("Colored!", color="red", ctx=Context(no_color=False))
```

## Streaming and Batch Processing

### File Processing Example

```python
from provide.foundation import pin_stream, pout, perr
import json

def process_json_stream():
    """Process JSON objects from stdin line by line."""
    pout("Send JSON objects, one per line:")
    
    processed = 0
    errors = 0
    
    for line in pin_stream():
        try:
            data = json.loads(line)
            # Process data
            result = process_data(data)
            pout(result, json_key="result")
            processed += 1
        except json.JSONDecodeError as e:
            perr(f"Invalid JSON: {e}", json_key="error")
            errors += 1
        except Exception as e:
            perr(f"Processing error: {e}", json_key="error")
            errors += 1
    
    pout(f"Processed: {processed}, Errors: {errors}", json_key="summary")

# Usage: cat data.jsonl | python script.py
process_json_stream()
```

### Async Pipeline Example

```python
from provide.foundation import apin_stream, pout
import asyncio
import aiohttp

async def url_checker():
    """Check URLs from stdin asynchronously."""
    pout("Enter URLs to check:")
    
    async with aiohttp.ClientSession() as session:
        async for url in apin_stream():
            if not url.strip():
                continue
                
            try:
                async with session.get(url) as response:
                    status = response.status
                    pout({
                        "url": url,
                        "status": status,
                        "ok": status == 200
                    })
            except Exception as e:
                pout({
                    "url": url,
                    "error": str(e),
                    "ok": False
                })

# Run async URL checker
asyncio.run(url_checker())
```

## Form Input Patterns

### Simple Form

```python
from provide.foundation import pin, pout

def collect_user_info():
    pout("User Registration", color="cyan", bold=True)
    pout("=" * 20)
    
    name = pin("Full Name: ")
    email = pin("Email: ")
    age = pin("Age: ", type=int, default=0)
    newsletter = pin("Subscribe to newsletter? [y/n]: ", type=bool)
    
    # Confirmation
    pout("\nPlease confirm:")
    pout(f"Name: {name}")
    pout(f"Email: {email}")
    pout(f"Age: {age}")
    pout(f"Newsletter: {'Yes' if newsletter else 'No'}")
    
    confirm = pin("Is this correct? [y/n]: ", type=bool)
    
    if confirm:
        return {
            "name": name,
            "email": email, 
            "age": age,
            "newsletter": newsletter
        }
    else:
        pout("Registration cancelled.")
        return None

user_data = collect_user_info()
```

### Password Management

```python
from provide.foundation import pin, pout, perr

def change_password():
    # Current password
    current = pin("Current password: ", password=True)
    
    # New password with confirmation
    new_password = pin(
        "New password: ", 
        password=True, 
        confirmation_prompt=True
    )
    
    # Validate
    if len(new_password) < 8:
        perr("Password must be at least 8 characters", color="red")
        return False
    
    pout("Password changed successfully!", color="green")
    return True

change_password()
```

## Error Handling

Console functions handle errors gracefully:

```python
from provide.foundation import pin, pout, perr

def safe_numeric_input():
    while True:
        try:
            # This will keep prompting until valid input
            value = pin("Enter a number: ", type=float)
            break
        except (ValueError, TypeError) as e:
            perr(f"Invalid input: {e}", color="red")
    
    pout(f"You entered: {value}")
    return value

# Custom validation
def validated_input():
    def validate_positive(value):
        if value <= 0:
            raise ValueError("Must be positive")
        return value
    
    try:
        num = pin(
            "Enter positive number: ",
            type=float,
            value_proc=validate_positive
        )
        pout(f"Valid input: {num}")
    except ValueError as e:
        perr(f"Validation failed: {e}")

safe_numeric_input()
validated_input()
```

## Best Practices

### 1. Use Consistent Output Patterns

```python
# Good: Consistent success/error patterns
def process_file(filename):
    try:
        # Process file
        pout(f"✅ Processed {filename}", color="green")
        return True
    except Exception as e:
        perr(f"❌ Failed to process {filename}: {e}", color="red")
        return False
```

### 2. Provide Clear User Feedback

```python
# Good: Clear, helpful prompts
email = pin(
    "Email address (format: user@example.com): ",
    value_proc=validate_email,
    color="cyan"
)

# Good: Show progress for long operations
pout("Processing files...")
for i, file in enumerate(files):
    pout(f"[{i+1}/{len(files)}] {file.name}", prefix="📄")
```

### 3. Handle JSON Mode Gracefully

```python
# Good: Works in both interactive and JSON modes
def output_results(results):
    if isinstance(results, dict):
        pout(results)  # JSON mode: direct output, Interactive: formatted
    else:
        pout({"results": results})  # Always structured
```

### 4. Use Streaming for Large Data

```python
# Good: Stream processing for memory efficiency
def process_large_dataset():
    pout("Send data line by line:")
    
    for line in pin_stream():
        # Process immediately, don't accumulate
        result = process_line(line)
        pout(result)
```

## Thread Safety

Console functions are thread-safe for concurrent use:

```python
import threading
from provide.foundation import pout, perr

def worker(worker_id):
    pout(f"Worker {worker_id} starting", color="blue")
    # Do work
    pout(f"Worker {worker_id} finished", color="green")

# Safe to use from multiple threads
threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
```

## Integration Examples

### CLI Application

```python
from provide.foundation import Context, pout, perr, pin
import click

@click.command()
@click.option('--json', is_flag=True, help='JSON output mode')
@click.option('--no-color', is_flag=True, help='Disable colors')
@click.pass_context
def myapp(ctx, json, no_color):
    # Setup context
    app_ctx = Context(json_output=json, no_color=no_color)
    ctx.obj = app_ctx
    
    # Now console functions respect these settings
    pout("Welcome to MyApp!", color="green", bold=True)
    
    name = pin("Enter your name: ")
    pout(f"Hello, {name}!")

if __name__ == '__main__':
    myapp()
```

### Data Processing Pipeline

```python
from provide.foundation import pin_stream, pout, perr
import json
import sys

def data_transformer():
    """Transform JSON data from stdin to stdout."""
    
    for line_num, line in enumerate(pin_stream(), 1):
        try:
            # Parse input
            data = json.loads(line)
            
            # Transform data
            transformed = transform_data(data)
            
            # Output result
            pout(transformed)
            
        except json.JSONDecodeError:
            perr(f"Line {line_num}: Invalid JSON", file=sys.stderr)
        except Exception as e:
            perr(f"Line {line_num}: Transform error: {e}", file=sys.stderr)

# Usage in pipeline: cat input.jsonl | python transformer.py > output.jsonl
data_transformer()
```

## See Also

- [Context Module](../context/api-index.md) - For configuration and context management
- [CLI Guide](../../guide/cli/index.md) - Building CLI applications  
- [Logger Module](../logger/api-index.md) - For structured logging
- [Process Module](../process/api-index.md) - For external command execution
