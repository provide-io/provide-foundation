# Output Formatting

Control and format CLI output using provide.foundation's console I/O functions.

## Overview

`provide.foundation` provides standardized console I/O functions (`pout`, `perr`, `pin`) that handle output formatting, JSON mode, color support, and stream separation. These functions ensure consistent behavior across all CLI applications.

## Output Functions

### pout() - Standard Output

Write to stdout with optional formatting:

```python
from provide.foundation.console.output import pout

# Simple output
pout("Hello, World!")

# With color and formatting
pout("Success!", fg="green", bold=True)
pout("Warning", fg="yellow")
pout("Error occurred", fg="red")

# Control newlines
pout("Processing...", nl=False)  # No newline
# Do work...
pout(" Done!", fg="green")
```

### perr() - Error Output

Write to stderr with the same formatting options:

```python
from provide.foundation.console.output import perr

# Error messages go to stderr
perr("Error: File not found", fg="red", bold=True)
perr("Warning: Deprecated option", fg="yellow")
```

## Input Functions

### pin() - Standard Input

Read user input with prompts and validation:

```python
from provide.foundation.console.input import pin

# Simple input
name = pin("Enter your name: ")

# With type conversion
age = pin("Enter age: ", type=int, default=21)
ratio = pin("Ratio: ", type=float)

# Password input (hidden)
password = pin("Password: ", hide_input=True)
```

## JSON Output Mode

When JSON mode is enabled, `pout` and `perr` will automatically format dictionaries and lists as JSON.

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

## Color and Formatting

Colors are automatically disabled when not supported (e.g., when piping output to another command).

```python
# These colors work when stdout is a TTY
pout("Red text", fg="red")
pout("Green text", fg="green")
pout("Yellow text", fg="yellow")
pout("Blue text", fg="blue")
pout("Magenta text", fg="magenta")
pout("Cyan text", fg="cyan")
pout("White text", fg="white")

# Combined with formatting
pout("Bold green", fg="green", bold=True)
pout("Dim text", dim=True)
```

## Related Topics

- [Arguments & Options](arguments.md) - CLI argument handling
- [Command Registration](commands.md) - Registering commands
- [Nested Commands](nested.md) - Command hierarchies