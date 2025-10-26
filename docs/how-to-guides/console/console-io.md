# How to Use Console I/O

Foundation provides a suite of console I/O utilities for building robust CLI applications with proper separation between logging and user-facing output.

## Overview

The console module provides three main categories of functions:

- **Output**: `pout()` and `perr()` for user-facing messages
- **Input**: `pin()` and variants for user input
- **Async I/O**: Async versions of all I/O functions

## User-Facing Output

### pout() - Standard Output

Use `pout()` for success messages and general user output:

```python
from provide.foundation import pout

# Simple message
pout("Operation completed successfully")

# With color
pout("✅ File saved", color="green")

# With bold formatting
pout("Important Notice", bold=True, color="yellow")

# With dim text
pout("(additional details)", dim=True)

# Disable newline
pout("Processing... ", nl=False)
pout("Done!", color="green")
```

**Available parameters:**
- `message`: Content to output (any type)
- `color`: Color name (red, green, yellow, blue, cyan, magenta, white)
- `bold`: Bold text (default: False)
- `dim`: Dim/faded text (default: False)
- `nl` or `newline`: Add newline (default: True)
- `prefix`: Optional prefix string
- `json_key`: Key for JSON output mode
- `ctx`: Override context

### perr() - Error Output

Use `perr()` for error messages and warnings (writes to stderr):

```python
from provide.foundation import perr

# Error message
perr("❌ Operation failed", color="red")

# Warning message
perr("⚠️  Configuration file not found", color="yellow")

# Critical error
perr("CRITICAL: System failure detected", color="red", bold=True)
```

### Separation of Concerns

**Best Practice:** Keep logging and user output separate:

```python
from provide.foundation import logger, pout, perr

def process_file(filename: str):
    # Log for operators/debugging
    logger.info("file_processing_started", filename=filename)

    # Show to user
    pout(f"Processing {filename}...", color="cyan")

    try:
        result = do_work(filename)

        # Log result
        logger.info("file_processed", filename=filename, records=len(result))

        # Show to user
        pout(f"✅ Processed {len(result)} records", color="green")

    except Exception as e:
        # Log error with context
        logger.error("file_processing_failed", filename=filename, error=str(e))

        # Show to user
        perr(f"❌ Failed to process {filename}: {e}", color="red")
        raise
```

## User Input

### pin() - Basic Input

Get user input with optional type conversion and validation:

```python
from provide.foundation import pin

# Simple string input
name = pin("Enter your name: ")

# Integer input with type conversion
age = pin("Enter your age: ", type=int)

# With default value
city = pin("Enter city: ", default="San Francisco")

# Boolean input
confirmed = pin("Proceed? (y/n): ", type=bool)
```

### Password Input

Hide sensitive input:

```python
from provide.foundation import pin

# Hidden input
password = pin("Enter password: ", password=True)

# With confirmation
password = pin(
    "Enter password: ",
    password=True,
    confirmation_prompt=True
)
```

### Input with Validation

```python
from provide.foundation import pin

def validate_email(value):
    """Validate email format."""
    if "@" not in value:
        raise ValueError("Invalid email address")
    return value.lower()

email = pin(
    "Enter email: ",
    value_proc=validate_email
)
```

### pin_stream() - Stream Input

Read multiple lines from stdin:

```python
from provide.foundation import pin_stream

pout("Enter text (Ctrl+D to finish):")

for line in pin_stream():
    process_line(line)
```

### pin_lines() - Read Multiple Lines

```python
from provide.foundation import pin_lines

# Read exactly 3 lines
lines = pin_lines(count=3)

# Read until EOF
all_lines = pin_lines()
```

## Async I/O

All console I/O functions have async equivalents:

```python
from provide.foundation.console import apin, apin_lines, apin_stream
import asyncio

async def get_user_info():
    # Async input
    name = await apin("Enter name: ")
    age = await apin("Enter age: ", type=int)

    # Async multi-line input
    lines = await apin_lines(count=3)

    # Async streaming
    async for line in apin_stream():
        await process_line(line)

asyncio.run(get_user_info())
```

## JSON Output Mode

Foundation automatically detects JSON mode for machine-readable output:

```python
from provide.foundation import pout

# Automatically outputs JSON when in JSON mode
pout({"status": "success", "records": 42}, json_key="result")

# In JSON mode outputs:
# {"result": {"status": "success", "records": 42}}

# In normal mode outputs:
# {'status': 'success', 'records': 42}
```

**Enable JSON mode:**
```python
from provide.foundation.context import CLIContext
from provide.foundation import pout

ctx = CLIContext(json_output=True)
pout("Success", json_key="message", ctx=ctx)
# {"message": "Success"}
```

## Color Support

Foundation automatically detects color support:

### Environment Variables

```bash
# Force color output
export FORCE_COLOR=1

# Disable color output
export NO_COLOR=1
```

### Manual Control

```python
from provide.foundation.context import CLIContext
from provide.foundation import pout

# Disable colors
ctx = CLIContext(no_color=True)
pout("No colors", color="red", ctx=ctx)  # Plain text
```

## Best Practices

### ✅ DO: Use pout/perr for User Output

```python
# ✅ Good: User-facing output via pout/perr
from provide.foundation import pout, perr, logger

pout("✅ Deployment successful", color="green")
logger.info("deployment_completed", duration_ms=1234)

# ❌ Bad: Using print() or logger for user output
print("Deployment successful")  # Wrong: bypasses Foundation's I/O
logger.info("Deployment successful")  # Wrong: logging is not for users
```

### ✅ DO: Use Colors Consistently

```python
# ✅ Good: Consistent color scheme
pout("✅ Success", color="green")
perr("❌ Error", color="red")
perr("⚠️  Warning", color="yellow")
pout("ℹ️  Info", color="cyan")

# ❌ Bad: Inconsistent colors
pout("✅ Success", color="red")  # Confusing
perr("Error", color="green")  # Very confusing
```

### ✅ DO: Add Emojis for Visual Clarity

```python
# ✅ Good: Clear visual indicators
pout("✅ File saved successfully", color="green")
perr("❌ Connection failed", color="red")
perr("⚠️  Deprecated feature", color="yellow")
pout("📁 Opening file...", color="cyan")
pout("🔄 Syncing data...", color="blue")
```

### ❌ DON'T: Mix Output Methods

```python
# ❌ Bad: Mixing print() with pout()
pout("Starting process...")
print("Step 1 complete")  # Inconsistent
pout("Process complete")

# ✅ Good: Consistent use of pout()
pout("Starting process...")
pout("Step 1 complete")
pout("Process complete", color="green")
```

## Common Patterns

### Progress Indicator

```python
from provide.foundation import pout
import time

pout("Processing files: ", nl=False)
for i in range(5):
    pout(".", nl=False)
    time.sleep(0.5)
pout(" Done!", color="green")
```

### Interactive Confirmation

```python
from provide.foundation import pin, pout, perr

def confirm_action(message: str) -> bool:
    """Ask user to confirm an action."""
    response = pin(f"{message} (y/n): ").lower()
    return response in ("y", "yes")

if confirm_action("Delete all files?"):
    pout("✅ Confirmed, proceeding...", color="yellow")
else:
    perr("❌ Cancelled", color="red")
```

### Multi-Step Input

```python
from provide.foundation import pin, pout

pout("📝 User Registration", bold=True)
pout()  # Empty line

name = pin("Name: ")
email = pin("Email: ")
age = pin("Age: ", type=int)
password = pin("Password: ", password=True)

pout()
pout(f"✅ User {name} registered successfully!", color="green")
```

### Error Handling with Retry

```python
from provide.foundation import pin, perr

def get_valid_number(prompt: str, max_attempts: int = 3) -> int:
    """Get valid integer input with retry."""
    for attempt in range(max_attempts):
        try:
            return pin(prompt, type=int)
        except ValueError:
            perr(f"❌ Invalid number. {max_attempts - attempt - 1} attempts remaining.", color="red")

    raise ValueError("Max attempts exceeded")

age = get_valid_number("Enter your age: ")
```

## Integration with Click

Foundation's console I/O works seamlessly with Click:

```python
import click
from provide.foundation import pout, perr, pin

@click.command()
@click.option("--name", prompt="Your name", help="User name")
@click.option("--confirm", is_flag=True, help="Skip confirmation")
def greet(name: str, confirm: bool):
    """Greet the user."""
    if not confirm:
        if not pin(f"Greet {name}? (y/n): ").lower().startswith("y"):
            perr("Cancelled", color="red")
            return

    pout(f"Hello, {name}!", color="green", bold=True)
```

## Next Steps

- **[CLI Commands](../cli/commands.md)**: Build CLI applications
- **[Logging](../logging/basic-logging.md)**: Use logging for debugging
- **[Architecture](../../explanation/architecture.md)**: Understand Foundation's design

---

**Tip**: Always use `pout()`/`perr()` for user-facing output and `logger` for system logging.
