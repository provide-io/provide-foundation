# Interactive Prompts

Learn how to create interactive CLI applications with user prompts and confirmations.

## Overview

Foundation provides utilities for interactive user input, confirmations, and selections through the console module.

## Basic Input

```python
from provide.foundation.console.input import prompt

name = prompt("Enter your name: ")
print(f"Hello, {name}!")
```

## Input with Default

```python
name = prompt("Enter your name: ", default="User")
# If user presses Enter without typing, returns "User"
```

## Yes/No Confirmation

```python
from provide.foundation.console.input import confirm

if confirm("Do you want to continue?"):
    print("Continuing...")
else:
    print("Cancelled")

# With default
if confirm("Delete file?", default=False):
    delete_file()
```

## Password Input

```python
from provide.foundation.console.input import prompt_password

password = prompt_password("Enter password: ")
# Input is hidden while typing
```

## Input Validation

```python
def validate_email(value: str) -> str:
    """Validate email format."""
    if "@" not in value:
        raise ValueError("Invalid email address")
    return value

email = prompt(
    "Enter email: ",
    validator=validate_email
)
```

## Numeric Input

```python
age = prompt("Enter your age: ", type=int)
# Automatically converts to int and re-prompts on invalid input

price = prompt("Enter price: ", type=float)
```

## Choice Selection

```python
from provide.foundation.console.input import select

environment = select(
    "Select environment:",
    choices=["development", "staging", "production"]
)

print(f"Selected: {environment}")
```

## Multi-Line Input

```python
from provide.foundation.console.input import prompt_multiline

description = prompt_multiline(
    "Enter description (Ctrl+D to finish):\n"
)
```

## Interactive Confirmation Workflow

```python
from provide.foundation import pout, perr
from provide.foundation.console.input import confirm, prompt

def interactive_deploy():
    """Interactive deployment workflow."""

    # Get environment
    env = prompt(
        "Environment (dev/prod): ",
        validator=lambda v: v if v in ["dev", "prod"] else None
    )

    # Get version
    version = prompt("Version tag: ")

    # Show summary
    pout("\nDeployment Summary:", bold=True)
    pout(f"  Environment: {env}")
    pout(f"  Version: {version}")
    pout("")

    # Confirm
    if not confirm(f"Deploy version {version} to {env}?", default=False):
        perr("Deployment cancelled", color="yellow")
        return

    # Execute deployment
    pout("Deploying...", color="cyan")
    # ... deployment logic ...
    pout("✅ Deployment successful!", color="green")
```

## Input with Retry

```python
def get_valid_port():
    """Prompt for port until valid."""
    while True:
        try:
            port = prompt("Enter port (1024-65535): ", type=int)
            if 1024 <= port <= 65535:
                return port
            perr("Port must be between 1024 and 65535")
        except ValueError:
            perr("Invalid port number")

port = get_valid_port()
```

## Styled Prompts

```python
from provide.foundation.console.output import pout

pout("🚀 Welcome to the setup wizard!", color="cyan", bold=True)
pout("")

name = prompt("📝 Project name: ")
desc = prompt("📄 Description: ")
version = prompt("🔢 Version: ", default="1.0.0")
```

## Next Steps

- **[Building Commands](commands.md)** - Command structure
- **[Argument Parsing](arguments.md)** - Handle arguments
- **[API Reference: Console](../../reference/provide/foundation/console/index.md)** - Complete console API

---

**See also:** [examples/cli/](https://github.com/provide-io/provide-foundation/tree/main/examples/cli)
