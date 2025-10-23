# Argument Parsing

Learn how to handle command-line arguments, options, and flags in your CLI applications.

## Overview

Foundation's CLI framework (built on Click) provides powerful argument parsing with automatic type conversion and validation.

## Basic Arguments

```python
from provide.foundation.hub import register_command

@register_command("greet")
def greet(name: str):
    """Greet a user by name."""
    print(f"Hello, {name}!")

# Usage: python app.py greet Alice
# Output: Hello, Alice!
```

## Optional Arguments with Defaults

```python
@register_command("greet")
def greet(name: str, greeting: str = "Hello"):
    """Greet a user with a custom greeting."""
    print(f"{greeting}, {name}!")

# Usage: python app.py greet Alice
# Output: Hello, Alice!

# Usage: python app.py greet Alice --greeting "Hi"
# Output: Hi, Alice!
```

## Type Conversion

Foundation automatically converts argument types:

```python
@register_command("process")
def process(count: int, rate: float, enabled: bool = True):
    """Process with typed arguments."""
    print(f"Count: {count} (type: {type(count).__name__})")
    print(f"Rate: {rate} (type: {type(rate).__name__})")
    print(f"Enabled: {enabled} (type: {type(enabled).__name__})")

# Usage: python app.py process 42 3.14 --enabled
```

## Lists and Multiple Values

```python
from typing import list

@register_command("batch")
def batch(files: list[str]):
    """Process multiple files."""
    for file in files:
        print(f"Processing: {file}")

# Usage: python app.py batch file1.txt file2.txt file3.txt
```

## Choice Arguments

```python
from typing import Literal

@register_command("deploy")
def deploy(environment: Literal["dev", "staging", "prod"]):
    """Deploy to a specific environment."""
    print(f"Deploying to {environment}")

# Usage: python app.py deploy prod
# Invalid: python app.py deploy invalid
# Error: Invalid value for 'environment': 'invalid' is not one of 'dev', 'staging', 'prod'
```

## File Path Arguments

```python
from pathlib import Path

@register_command("read")
def read(file: Path):
    """Read and display file contents."""
    if not file.exists():
        raise FileNotFoundError(f"File not found: {file}")

    content = file.read_text()
    print(content)

# Usage: python app.py read config.yaml
```

## Variadic Arguments

```python
@register_command("sum")
def sum_numbers(*numbers: int):
    """Sum any number of integers."""
    total = sum(numbers)
    print(f"Total: {total}")

# Usage: python app.py sum 1 2 3 4 5
# Output: Total: 15
```

## Argument Validation

```python
@register_command("process")
def process(workers: int):
    """Process with worker validation."""
    if workers < 1:
        raise ValueError("Workers must be at least 1")
    if workers > 100:
        raise ValueError("Workers cannot exceed 100")

    print(f"Processing with {workers} workers")
```

## Next Steps

- **[Building Commands](commands.md)** - Command structure
- **[Interactive Prompts](prompts.md)** - User input
- **[API Reference: CLI](../../reference/provide/foundation/cli/index.md)** - Complete CLI API

---

**See also:** [examples/cli/01_cli_application.py](https://github.com/provide-io/provide-foundation/blob/main/examples/cli/01_cli_application.py)
