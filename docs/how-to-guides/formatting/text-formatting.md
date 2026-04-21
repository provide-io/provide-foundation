# How to Use Formatting Utilities

Foundation provides comprehensive formatting utilities for text, numbers, and data structures.

## Text Formatting

### Case Conversion

```python
from provide.foundation.formatting import (
    to_snake_case,
    to_camel_case,
    to_kebab_case
)

# Convert to snake_case
to_snake_case("HelloWorld")      # "hello_world"
to_snake_case("helloWorld")      # "hello_world"
to_snake_case("hello-world")     # "hello_world"

# Convert to camelCase
to_camel_case("hello_world")     # "helloWorld"
to_camel_case("hello-world")     # "helloWorld"

# Convert to kebab-case
to_kebab_case("hello_world")     # "hello-world"
to_kebab_case("HelloWorld")      # "hello-world"
```

### Text Manipulation

```python
from provide.foundation.formatting import (
    truncate,
    wrap_text,
    indent,
    pluralize,
    strip_ansi
)

# Truncate long text
truncate("This is a very long string", max_length=10)
# "This is..."

# Wrap text to width
wrap_text("This is a long line that needs wrapping", width=20)
# "This is a long line\nthat needs wrapping"

# Indent text
indent("Line 1\nLine 2", spaces=4)
# "    Line 1\n    Line 2"

# Pluralize words
pluralize("item", count=1)   # "item"
pluralize("item", count=2)   # "items"
pluralize("box", count=2)    # "boxes"

# Strip ANSI color codes
strip_ansi("\033[31mRed text\033[0m")
# "Red text"
```

## Number Formatting

### Size Formatting

```python
from provide.foundation.formatting import format_size

format_size(1024)              # "1.0 KB"
format_size(1024 * 1024)       # "1.0 MB"
format_size(1024 * 1024 * 1024)  # "1.0 GB"
format_size(1500)              # "1.5 KB"
```

### Duration Formatting

```python
from provide.foundation.formatting import format_duration

format_duration(1.5)           # "1.5s"
format_duration(90)            # "1m 30s"
format_duration(3661)          # "1h 1m 1s"
format_duration(0.001)         # "1ms"
```

### Number Formatting

```python
from provide.foundation.formatting import format_number, format_percentage

# Format numbers with thousands separators
format_number(1000)            # "1,000"
format_number(1000000)         # "1,000,000"

# Format percentages
format_percentage(0.855)       # "85.5%"
format_percentage(0.8555, decimals=1)  # "85.6%"
```

## Data Formatting

### Table Formatting

```python
from provide.foundation.formatting import format_table

data = [
    {"name": "Alice", "age": 30, "city": "NYC"},
    {"name": "Bob", "age": 25, "city": "SF"},
    {"name": "Charlie", "age": 35, "city": "LA"}
]

table = format_table(data)
print(table)
# ┌─────────┬─────┬──────┐
# │ name    │ age │ city │
# ├─────────┼─────┼──────┤
# │ Alice   │ 30  │ NYC  │
# │ Bob     │ 25  │ SF   │
# │ Charlie │ 35  │ LA   │
# └─────────┴─────┴──────┘
```

### Grouped Formatting

```python
from provide.foundation.formatting import format_grouped

items = ["apple", "banana", "cherry", "date", "elderberry"]
grouped = format_grouped(items, items_per_group=2)
# [["apple", "banana"], ["cherry", "date"], ["elderberry"]]
```

## Best Practices

### ✅ DO: Use Consistent Case Conversion

```python
# ✅ Good: Consistent API naming
from provide.foundation.formatting import to_snake_case

api_field = to_snake_case(user_input)  # Always snake_case for database

# ❌ Bad: Manual string manipulation
api_field = user_input.replace(" ", "_").lower()  # Inconsistent
```

### ✅ DO: Format User-Facing Numbers

```python
# ✅ Good: Readable numbers
from provide.foundation.formatting import format_number, format_size
from provide.foundation import pout

pout(f"Processed {format_number(1234567)} records")
pout(f"File size: {format_size(1024 * 1024 * 500)}")

# ❌ Bad: Raw numbers
pout(f"Processed {1234567} records")  # Hard to read
```

## Next Steps

- **[Console I/O](../console/console-io.md)**: Output formatted text
- **[Logging](../logging/basic-logging.md)**: Log formatted data

---

**Tip**: Use formatting utilities for consistent, readable output across your application.
