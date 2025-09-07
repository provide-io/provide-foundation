# String Formatting

Human-readable formatting functions for common data types including sizes, durations, numbers, and text processing.

## Size Formatting

### `format_size(bytes, binary=True, precision=1)`

Format byte count as human-readable size.

**Parameters:**
- `bytes` (int): Number of bytes
- `binary` (bool): Use binary (1024) vs decimal (1000) units (default: True)
- `precision` (int): Decimal places to show (default: 1)

**Returns:**
- `str`: Formatted size string

**Example:**
```python
from provide.foundation.utils import format_size

print(format_size(1024))        # "1.0 KB"
print(format_size(1536))        # "1.5 KB" 
print(format_size(1024, False)) # "1.0 kB" (decimal)
print(format_size(1048576, precision=2))  # "1.00 MB"
```

## Duration Formatting

### `format_duration(seconds, precision=1)`

Format duration in seconds as human-readable string.

**Parameters:**
- `seconds` (float): Duration in seconds
- `precision` (int): Decimal places for seconds (default: 1)

**Returns:**
- `str`: Formatted duration string

**Example:**
```python
from provide.foundation.utils import format_duration

print(format_duration(65))      # "1m 5.0s"
print(format_duration(125.5))   # "2m 5.5s"
print(format_duration(3665))    # "1h 1m 5.0s"
print(format_duration(0.123))   # "123.0ms"
```

## Number Formatting

### `format_number(number, precision=None, thousands_sep=",")`

Format number with thousands separators.

**Parameters:**
- `number` (int|float): Number to format
- `precision` (int, optional): Decimal places for floats
- `thousands_sep` (str): Thousands separator (default: ",")

**Returns:**
- `str`: Formatted number string

**Example:**
```python
from provide.foundation.utils import format_number

print(format_number(1234567))           # "1,234,567"
print(format_number(1234.5678, 2))      # "1,234.57"
print(format_number(1234567, thousands_sep="_"))  # "1_234_567"
```

## Text Processing

### `to_snake_case(text)`

Convert text to snake_case.

**Parameters:**
- `text` (str): Input text

**Returns:**
- `str`: snake_case version

**Example:**
```python
from provide.foundation.utils import to_snake_case

print(to_snake_case("CamelCase"))      # "camel_case"
print(to_snake_case("kebab-case"))     # "kebab_case"
print(to_snake_case("Title Case"))     # "title_case"
```

### `to_camel_case(text)`

Convert text to camelCase.

**Parameters:**
- `text` (str): Input text

**Returns:**
- `str`: camelCase version

**Example:**
```python
from provide.foundation.utils import to_camel_case

print(to_camel_case("snake_case"))     # "snakeCase"
print(to_camel_case("kebab-case"))     # "kebabCase"
print(to_camel_case("Title Case"))     # "titleCase"
```

### `to_pascal_case(text)`

Convert text to PascalCase.

**Parameters:**
- `text` (str): Input text

**Returns:**
- `str`: PascalCase version

**Example:**
```python
from provide.foundation.utils import to_pascal_case

print(to_pascal_case("snake_case"))    # "SnakeCase"
print(to_pascal_case("kebab-case"))    # "KebabCase"
print(to_pascal_case("title case"))    # "TitleCase"
```

### `pluralize(word, count, plural=None)`

Pluralize word based on count.

**Parameters:**
- `word` (str): Singular word
- `count` (int): Count to check
- `plural` (str, optional): Custom plural form

**Returns:**
- `str`: Singular or plural form based on count

**Example:**
```python
from provide.foundation.utils import pluralize

print(pluralize("item", 1))        # "item"
print(pluralize("item", 5))        # "items"
print(pluralize("child", 3, "children"))  # "children"
```

### `truncate(text, max_length, suffix="...")`

Truncate text to maximum length.

**Parameters:**
- `text` (str): Input text
- `max_length` (int): Maximum length including suffix
- `suffix` (str): Suffix to append (default: "...")

**Returns:**
- `str`: Truncated text

**Example:**
```python
from provide.foundation.utils import truncate

print(truncate("Very long text here", 10))  # "Very lo..."
print(truncate("Short", 10))                # "Short"
print(truncate("Long text", 8, ">>"))       # "Long t>>"
```

### `wrap_text(text, width=80, indent="", subsequent_indent="")`

Wrap text to specified width.

**Parameters:**
- `text` (str): Input text
- `width` (int): Line width (default: 80)
- `indent` (str): First line indent
- `subsequent_indent` (str): Subsequent lines indent

**Returns:**
- `list[str]`: List of wrapped lines

**Example:**
```python
from provide.foundation.utils import wrap_text

long_text = "This is a very long line that needs to be wrapped"
lines = wrap_text(long_text, width=20)
for line in lines:
    print(line)
```

## Table Formatting

### `format_table(data, headers=None, align=None)`

Format data as an ASCII table.

**Parameters:**
- `data` (list[list]): Table data
- `headers` (list, optional): Column headers
- `align` (list, optional): Column alignments ('left', 'center', 'right')

**Returns:**
- `str`: Formatted table string

**Example:**
```python
from provide.foundation.utils import format_table

data = [
    ["Alice", 25, "Engineer"],
    ["Bob", 30, "Designer"],
    ["Charlie", 35, "Manager"]
]
headers = ["Name", "Age", "Role"]

table = format_table(data, headers=headers, align=['left', 'center', 'right'])
print(table)
```