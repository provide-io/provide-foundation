# Utils

::: provide.foundation.utils

## Overview

The utils module provides a comprehensive collection of utility functions for common programming tasks including environment variable handling, string formatting, data parsing, timing operations, and text processing. These utilities are designed to be reusable across applications and provide consistent, well-tested functionality.

## Key Features

- **Environment Utilities**: Type-safe environment variable parsing
- **String Formatting**: Human-readable formatting for sizes, durations, numbers
- **Text Processing**: Case conversion, wrapping, truncation, and table formatting  
- **Data Parsing**: Intelligent parsing of strings to appropriate types
- **Timing Utilities**: Performance measurement and logging
- **Type Safety**: Full type annotations and validation

## Quick Start

```python
from provide.foundation.utils import (
    get_str, get_int, get_bool,          # Environment parsing
    format_size, format_duration,        # Formatting
    to_snake_case, pluralize,           # Text processing
    parse_bool, auto_parse,             # Data parsing
    timed_block                         # Performance timing
)

# Environment variable parsing
database_url = get_str("DATABASE_URL", "sqlite:///default.db")
max_connections = get_int("MAX_CONNECTIONS", 10)
debug_mode = get_bool("DEBUG", False)

# String formatting
print(format_size(1536))           # "1.5 KB"
print(format_duration(125.5))      # "2m 5.5s"

# Text processing
print(to_snake_case("CamelCase"))  # "camel_case"
print(pluralize("item", 5))        # "items"

# Performance timing
with timed_block(logger, "data_processing") as ctx:
    # Your code here
    ctx["records_processed"] = 1000
```

## API Reference

The utilities are organized into several categories:

- **[api-Environment Utilities](api-environment.md)**: Type-safe environment variable parsing
- **[api-String Formatting](api-formatting.md)**: Human-readable formatting functions
- **[api-Timing Utilities](api-timing.md)**: Performance measurement and logging tools

Each section provides detailed documentation with examples and usage patterns.