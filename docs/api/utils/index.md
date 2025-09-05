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

### Environment Utilities

#### `get_str(key, default="", prefix=None)`

Get string value from environment variable.

**Parameters:**
- `key` (str): Environment variable name
- `default` (str): Default value if not found (default: "")
- `prefix` (str, optional): Variable prefix to prepend

**Returns:**
- `str`: Environment variable value or default

**Example:**
```python
from provide.foundation.utils import get_str

# Basic usage
api_key = get_str("API_KEY", "default-key")
host = get_str("HOST", "localhost")

# With prefix
db_host = get_str("HOST", "localhost", prefix="DB")  # Looks for DB_HOST
```

#### `get_int(key, default=0, prefix=None)`

Get integer value from environment variable.

**Parameters:**
- `key` (str): Environment variable name
- `default` (int): Default value if not found or invalid (default: 0)
- `prefix` (str, optional): Variable prefix to prepend

**Returns:**
- `int`: Parsed integer value or default

**Example:**
```python
from provide.foundation.utils import get_int

port = get_int("PORT", 8000)
workers = get_int("WORKERS", 4)
timeout = get_int("TIMEOUT", 30, prefix="API")  # API_TIMEOUT
```

#### `get_float(key, default=0.0, prefix=None)`

Get float value from environment variable.

**Parameters:**
- `key` (str): Environment variable name
- `default` (float): Default value if not found or invalid
- `prefix` (str, optional): Variable prefix to prepend

**Returns:**
- `float`: Parsed float value or default

#### `get_bool(key, default=False, prefix=None)`

Get boolean value from environment variable.

**Parameters:**
- `key` (str): Environment variable name
- `default` (bool): Default value if not found
- `prefix` (str, optional): Variable prefix to prepend

**Returns:**
- `bool`: Parsed boolean value or default

**Supported Values:**
- **True**: `true`, `True`, `1`, `yes`, `Yes`, `on`, `On`
- **False**: `false`, `False`, `0`, `no`, `No`, `off`, `Off`

**Example:**
```python
from provide.foundation.utils import get_bool

debug = get_bool("DEBUG", False)
ssl_enabled = get_bool("SSL_ENABLED", True)
auto_reload = get_bool("RELOAD", False, prefix="DEV")  # DEV_RELOAD
```

#### `get_list(key, default=None, separator=",", prefix=None)`

Get list value from environment variable.

**Parameters:**
- `key` (str): Environment variable name
- `default` (list, optional): Default value if not found
- `separator` (str): List item separator (default: ",")
- `prefix` (str, optional): Variable prefix to prepend

**Returns:**
- `list[str]`: Parsed list or default

**Example:**
```python
from provide.foundation.utils import get_list

# Basic usage
allowed_hosts = get_list("ALLOWED_HOSTS", ["localhost"])
# ALLOWED_HOSTS=example.com,api.example.com -> ["example.com", "api.example.com"]

# Custom separator
features = get_list("FEATURES", [], separator="|")
# FEATURES=auth|logging|metrics -> ["auth", "logging", "metrics"]
```

#### `get_dict(key, default=None, item_sep=",", kv_sep="=", prefix=None)`

Get dictionary value from environment variable.

**Parameters:**
- `key` (str): Environment variable name  
- `default` (dict, optional): Default value if not found
- `item_sep` (str): Item separator (default: ",")
- `kv_sep` (str): Key-value separator (default: "=")
- `prefix` (str, optional): Variable prefix to prepend

**Returns:**
- `dict[str, str]`: Parsed dictionary or default

**Example:**
```python
from provide.foundation.utils import get_dict

# Basic usage
db_config = get_dict("DB_CONFIG", {})
# DB_CONFIG=host=localhost,port=5432,name=mydb
# -> {"host": "localhost", "port": "5432", "name": "mydb"}

# Custom separators  
headers = get_dict("HTTP_HEADERS", {}, item_sep="|", kv_sep=":")
# HTTP_HEADERS=Content-Type:application/json|Authorization:Bearer token
```

#### `get_path(key, default=None, prefix=None)`

Get Path object from environment variable.

**Parameters:**
- `key` (str): Environment variable name
- `default` (Path, optional): Default Path if not found  
- `prefix` (str, optional): Variable prefix to prepend

**Returns:**
- `Path | None`: Path object or default

**Example:**
```python
from provide.foundation.utils import get_path

config_dir = get_path("CONFIG_DIR", Path("config"))
log_file = get_path("LOG_FILE", Path("app.log"))
```

#### `require(key, prefix=None)`

Require environment variable to be set.

**Parameters:**
- `key` (str): Environment variable name
- `prefix` (str, optional): Variable prefix to prepend

**Returns:**
- `str`: Environment variable value

**Raises:**
- `ValueError`: If environment variable is not set

**Example:**
```python
from provide.foundation.utils import require

# These will raise ValueError if not set
database_url = require("DATABASE_URL")
secret_key = require("SECRET_KEY")
api_token = require("TOKEN", prefix="API")  # API_TOKEN
```

#### `parse_duration(duration_str)`

Parse duration string to seconds.

**Parameters:**
- `duration_str` (str): Duration string (e.g., "1h30m", "45s", "2d")

**Returns:**
- `float`: Duration in seconds

**Supported Units:**
- `s`, `sec`, `second`, `seconds`: Seconds
- `m`, `min`, `minute`, `minutes`: Minutes
- `h`, `hr`, `hour`, `hours`: Hours
- `d`, `day`, `days`: Days
- `w`, `week`, `weeks`: Weeks

**Example:**
```python
from provide.foundation.utils import parse_duration

timeout = parse_duration("30s")      # 30.0
delay = parse_duration("1h30m")      # 5400.0
cache_ttl = parse_duration("2d")     # 172800.0
```

#### `parse_size(size_str)`

Parse size string to bytes.

**Parameters:**
- `size_str` (str): Size string (e.g., "1GB", "512MB", "1.5KB")

**Returns:**
- `int`: Size in bytes

**Supported Units:**
- `B`, `byte`, `bytes`: Bytes
- `K`, `KB`, `KiB`: Kilobytes
- `M`, `MB`, `MiB`: Megabytes  
- `G`, `GB`, `GiB`: Gigabytes
- `T`, `TB`, `TiB`: Terabytes

**Example:**
```python
from provide.foundation.utils import parse_size

max_file_size = parse_size("10MB")     # 10485760
cache_size = parse_size("1.5GB")       # 1610612736
buffer_size = parse_size("64KB")       # 65536
```

#### `EnvPrefix` Class

Environment variable prefix manager for consistent naming.

**Example:**
```python
from provide.foundation.utils import EnvPrefix, get_str

# Create prefix manager
db_env = EnvPrefix("DATABASE")

# Use with get_* functions
host = db_env.get_str("HOST", "localhost")      # DATABASE_HOST
port = db_env.get_int("PORT", 5432)             # DATABASE_PORT
ssl = db_env.get_bool("SSL", False)             # DATABASE_SSL

# Manual prefix usage
url = get_str("URL", prefix="DATABASE")         # DATABASE_URL
```

### String Formatting

#### `format_size(size_bytes, precision=1)`

Format bytes as human-readable size.

**Parameters:**
- `size_bytes` (int | float): Size in bytes
- `precision` (int): Decimal places (default: 1)

**Returns:**
- `str`: Human-readable size

**Example:**
```python
from provide.foundation.utils import format_size

print(format_size(1024))         # "1.0 KB"
print(format_size(1536))         # "1.5 KB"
print(format_size(1073741824))   # "1.0 GB"
print(format_size(0))            # "0 B"
print(format_size(1024, 2))      # "1.00 KB"
```

#### `format_duration(seconds, precision=1)`

Format seconds as human-readable duration.

**Parameters:**
- `seconds` (float): Duration in seconds
- `precision` (int): Decimal places (default: 1)

**Returns:**
- `str`: Human-readable duration

**Example:**
```python
from provide.foundation.utils import format_duration

print(format_duration(90))       # "1m 30s"  
print(format_duration(3661))     # "1h 1m 1s"
print(format_duration(125.5))    # "2m 5.5s"
print(format_duration(0.5))      # "0.5s"
```

#### `format_number(number, precision=None)`

Format number with appropriate precision and thousands separators.

**Parameters:**
- `number` (int | float): Number to format
- `precision` (int, optional): Decimal places (auto if None)

**Returns:**
- `str`: Formatted number

**Example:**
```python
from provide.foundation.utils import format_number

print(format_number(1234567))        # "1,234,567"
print(format_number(1234.5678))      # "1,234.57"  
print(format_number(1234.5678, 3))   # "1,234.568"
```

#### `format_percentage(value, total, precision=1)`

Format percentage from value and total.

**Parameters:**
- `value` (float): Current value
- `total` (float): Total value  
- `precision` (int): Decimal places (default: 1)

**Returns:**
- `str`: Formatted percentage

**Example:**
```python
from provide.foundation.utils import format_percentage

print(format_percentage(25, 100))    # "25.0%"
print(format_percentage(1, 3))       # "33.3%"
print(format_percentage(2, 3, 2))    # "66.67%"
```

#### `format_table(data, headers=None, align=None)`

Format data as ASCII table.

**Parameters:**
- `data` (list[list]): Table data rows
- `headers` (list[str], optional): Column headers
- `align` (list[str], optional): Column alignment ('left', 'center', 'right')

**Returns:**
- `str`: Formatted table

**Example:**
```python
from provide.foundation.utils import format_table

data = [
    ["Alice", 25, "Engineer"],
    ["Bob", 30, "Manager"],
    ["Charlie", 35, "Designer"]
]

headers = ["Name", "Age", "Role"]
table = format_table(data, headers=headers)
print(table)
# +---------+-----+----------+
# | Name    | Age | Role     |
# +---------+-----+----------+
# | Alice   | 25  | Engineer |
# | Bob     | 30  | Manager  |
# | Charlie | 35  | Designer |
# +---------+-----+----------+
```

### Text Processing

#### `to_snake_case(text)`

Convert text to snake_case.

**Parameters:**
- `text` (str): Text to convert

**Returns:**
- `str`: snake_case text

**Example:**
```python
from provide.foundation.utils import to_snake_case

print(to_snake_case("CamelCase"))        # "camel_case"
print(to_snake_case("kebab-case"))       # "kebab_case" 
print(to_snake_case("Mixed_Format"))     # "mixed_format"
```

#### `to_camel_case(text)`

Convert text to camelCase.

**Parameters:**
- `text` (str): Text to convert

**Returns:**
- `str`: camelCase text

**Example:**
```python
from provide.foundation.utils import to_camel_case

print(to_camel_case("snake_case"))       # "snakeCase"
print(to_camel_case("kebab-case"))       # "kebabCase"
print(to_camel_case("normal text"))      # "normalText"
```

#### `to_kebab_case(text)`

Convert text to kebab-case.

**Parameters:**
- `text` (str): Text to convert

**Returns:**
- `str`: kebab-case text

**Example:**
```python
from provide.foundation.utils import to_kebab_case

print(to_kebab_case("CamelCase"))        # "camel-case"
print(to_kebab_case("snake_case"))       # "snake-case"
print(to_kebab_case("Normal Text"))      # "normal-text"
```

#### `pluralize(word, count)`

Pluralize word based on count.

**Parameters:**
- `word` (str): Word to potentially pluralize
- `count` (int): Count to determine singular/plural

**Returns:**
- `str`: Singular or plural form

**Example:**
```python
from provide.foundation.utils import pluralize

print(pluralize("item", 1))      # "item"
print(pluralize("item", 0))      # "items"  
print(pluralize("item", 5))      # "items"
print(pluralize("child", 2))     # "children"
```

#### `truncate(text, length, suffix="...")`

Truncate text to specified length.

**Parameters:**
- `text` (str): Text to truncate
- `length` (int): Maximum length
- `suffix` (str): Truncation suffix (default: "...")

**Returns:**
- `str`: Truncated text

**Example:**
```python
from provide.foundation.utils import truncate

print(truncate("Long text here", 8))           # "Long ..."
print(truncate("Short", 10))                   # "Short"
print(truncate("Text", 8, suffix=">>"))        # "Text"
```

#### `wrap_text(text, width=80, indent=0)`

Wrap text to specified width.

**Parameters:**
- `text` (str): Text to wrap
- `width` (int): Line width (default: 80)
- `indent` (int): Indentation spaces (default: 0)

**Returns:**
- `str`: Wrapped text

#### `indent(text, spaces=4, first_line=True)`

Indent text lines.

**Parameters:**
- `text` (str): Text to indent
- `spaces` (int): Number of spaces to indent (default: 4)
- `first_line` (bool): Indent first line (default: True)

**Returns:**
- `str`: Indented text

#### `strip_ansi(text)`

Remove ANSI escape codes from text.

**Parameters:**
- `text` (str): Text containing ANSI codes

**Returns:**
- `str`: Text without ANSI codes

**Example:**
```python
from provide.foundation.utils import strip_ansi

colored_text = "\033[31mRed text\033[0m"
plain_text = strip_ansi(colored_text)  # "Red text"
```

### Data Parsing

#### `parse_bool(value, strict=False)`

Parse value as boolean.

**Parameters:**
- `value` (Any): Value to parse
- `strict` (bool): Strict parsing mode (default: False)

**Returns:**
- `bool`: Parsed boolean value

**True Values:** `true`, `True`, `1`, `yes`, `Yes`, `on`, `On`
**False Values:** `false`, `False`, `0`, `no`, `No`, `off`, `Off`

**Example:**
```python
from provide.foundation.utils import parse_bool

print(parse_bool("true"))     # True
print(parse_bool("1"))        # True
print(parse_bool("yes"))      # True
print(parse_bool("false"))    # False
print(parse_bool("0"))        # False
```

#### `parse_list(value, separator=",", item_type=str)`

Parse value as list.

**Parameters:**
- `value` (str): String to parse
- `separator` (str): Item separator (default: ",")
- `item_type` (type): Type to convert items to (default: str)

**Returns:**
- `list`: Parsed list

**Example:**
```python
from provide.foundation.utils import parse_list

items = parse_list("a,b,c")              # ["a", "b", "c"]
numbers = parse_list("1,2,3", item_type=int)  # [1, 2, 3]
```

#### `parse_dict(value, item_sep=",", kv_sep="=")`

Parse value as dictionary.

**Parameters:**
- `value` (str): String to parse
- `item_sep` (str): Item separator (default: ",")
- `kv_sep` (str): Key-value separator (default: "=")

**Returns:**
- `dict[str, str]`: Parsed dictionary

#### `parse_typed_value(value, target_type)`

Parse value to specific type.

**Parameters:**
- `value` (str): String to parse
- `target_type` (type): Target type

**Returns:**
- Parsed value of target_type

#### `auto_parse(value)`

Automatically parse value to appropriate type.

**Parameters:**
- `value` (str): String to parse

**Returns:**
- `Any`: Value parsed to most appropriate type (int, float, bool, str)

**Example:**
```python
from provide.foundation.utils import auto_parse

print(auto_parse("42"))        # 42 (int)
print(auto_parse("3.14"))      # 3.14 (float)  
print(auto_parse("true"))      # True (bool)
print(auto_parse("hello"))     # "hello" (str)
```

### Timing Utilities

#### `timed_block(logger_instance, event_name, layer_keys=None, initial_kvs=None, **extra_kvs)`

Context manager for timing and logging code blocks.

**Parameters:**
- `logger_instance` (FoundationLogger): Logger to use
- `event_name` (str): Name of the operation being timed
- `layer_keys` (dict, optional): Emoji set keys
- `initial_kvs` (dict, optional): Initial key-value pairs
- `**extra_kvs`: Additional key-value pairs

**Yields:**
- `dict[str, Any]`: Mutable context dictionary

**Example:**
```python
from provide.foundation import logger
from provide.foundation.utils import timed_block

# Basic timing
with timed_block(logger, "data_processing") as ctx:
    # Your code here
    data = process_data()
    ctx["records_processed"] = len(data)

# With initial context
with timed_block(logger, "database_query", 
                 initial_kvs={"table": "users"}) as ctx:
    result = db.query("SELECT * FROM users")
    ctx["rows_returned"] = len(result)

# Error handling (automatically logged)
with timed_block(logger, "risky_operation") as ctx:
    ctx["attempt"] = 1
    # If this raises an exception, it's automatically logged with timing
    risky_function()
```

**Logging Behavior:**
- **Start**: Logs at DEBUG level when entering
- **Success**: Logs at INFO level with duration on completion
- **Error**: Logs at ERROR level with duration and exception info

## Complete Examples

### Environment Configuration Manager

```python
from provide.foundation.utils import (
    get_str, get_int, get_bool, get_list, require, EnvPrefix
)
from pathlib import Path

class DatabaseConfig:
    def __init__(self):
        # Use environment prefix for consistency
        env = EnvPrefix("DATABASE")
        
        # Required values
        self.url = require("URL", prefix="DATABASE")
        
        # Optional with defaults
        self.host = env.get_str("HOST", "localhost")
        self.port = env.get_int("PORT", 5432)
        self.name = env.get_str("NAME", "myapp")
        self.ssl = env.get_bool("SSL", False)
        
        # Connection pool settings
        self.min_connections = env.get_int("MIN_CONNECTIONS", 1)
        self.max_connections = env.get_int("MAX_CONNECTIONS", 10)
        
        # Advanced options
        self.allowed_schemas = env.get_list("ALLOWED_SCHEMAS", ["public"])
        self.connection_params = env.get_dict("CONNECTION_PARAMS", {})

class AppConfig:
    def __init__(self):
        self.debug = get_bool("DEBUG", False)
        self.secret_key = require("SECRET_KEY")
        self.allowed_hosts = get_list("ALLOWED_HOSTS", ["localhost"])
        
        # File paths
        self.log_dir = get_path("LOG_DIR", Path("logs"))
        self.static_dir = get_path("STATIC_DIR", Path("static"))
        
        # Feature flags
        self.features = get_list("ENABLED_FEATURES", [])
        
        # Performance settings
        self.cache_ttl = parse_duration(get_str("CACHE_TTL", "1h"))
        self.max_upload_size = parse_size(get_str("MAX_UPLOAD", "10MB"))
        
        self.database = DatabaseConfig()

# Usage
config = AppConfig()
```

### String Processing Pipeline

```python
from provide.foundation.utils import (
    format_size, format_duration, format_percentage,
    to_snake_case, pluralize, truncate, strip_ansi
)

def generate_report(stats):
    """Generate formatted report from statistics."""
    
    # Format numbers and sizes
    total_files = stats["files_processed"]
    total_size = format_size(stats["total_bytes"])
    avg_time = format_duration(stats["average_time"])
    
    # Calculate success rate
    success_rate = format_percentage(
        stats["successful_files"], 
        total_files
    )
    
    # Format file names consistently
    processed_files = [
        to_snake_case(filename) 
        for filename in stats["processed_files"]
    ]
    
    # Truncate long file names for display
    display_files = [
        truncate(filename, 50)
        for filename in processed_files
    ]
    
    report = f"""
Processing Report
=================

Files {pluralize("file", total_files)}: {total_files}
Total Size: {total_size}  
Success Rate: {success_rate}
Average Time: {avg_time}

Processed Files:
{chr(10).join(f"  - {file}" for file in display_files)}
"""
    
    return report.strip()

# Usage with stats
stats = {
    "files_processed": 1523,
    "total_bytes": 2547483648,
    "successful_files": 1498,
    "average_time": 0.245,
    "processed_files": ["CamelCaseFile.txt", "another-file.pdf"]
}

print(generate_report(stats))
```

### Performance Monitoring

```python
from provide.foundation import logger
from provide.foundation.utils import timed_block
import asyncio

class PerformanceMonitor:
    def __init__(self):
        self.logger = logger
        
    def time_function(self, name: str, **context):
        """Decorator for timing functions."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                with timed_block(self.logger, name, initial_kvs=context) as ctx:
                    ctx["function"] = func.__name__
                    result = func(*args, **kwargs)
                    
                    # Add result metadata if available
                    if hasattr(result, '__len__'):
                        ctx["result_size"] = len(result)
                    
                    return result
            return wrapper
        return decorator
    
    async def time_async_operation(self, name: str, coro, **context):
        """Time async operations."""
        with timed_block(self.logger, name, initial_kvs=context) as ctx:
            ctx["operation_type"] = "async"
            result = await coro
            
            if hasattr(result, '__len__'):
                ctx["result_size"] = len(result)
                
            return result

# Usage
monitor = PerformanceMonitor()

@monitor.time_function("data_processing", source="api")  
def process_api_data(data):
    # Simulate processing
    return [item.upper() for item in data]

# Async usage
async def fetch_data():
    await asyncio.sleep(0.1)  # Simulate async work
    return ["item1", "item2", "item3"]

async def main():
    # Time the async operation
    result = await monitor.time_async_operation(
        "fetch_data",
        fetch_data(),
        endpoint="/api/data"
    )
    
    # Time the sync processing
    processed = process_api_data(result)

asyncio.run(main())
```

### Data Validation and Parsing

```python
from provide.foundation.utils import (
    parse_bool, parse_list, auto_parse, parse_typed_value
)

class ConfigValidator:
    def __init__(self):
        self.errors = []
    
    def validate_and_parse(self, raw_config: dict[str, str]) -> dict[str, Any]:
        """Validate and parse configuration from string values."""
        config = {}
        
        # Define expected types and defaults
        schema = {
            "debug": (bool, False),
            "port": (int, 8000),
            "host": (str, "localhost"),
            "workers": (int, 1),
            "allowed_ips": (list, []),
            "timeout": (float, 30.0),
            "features": (list, []),
            "ssl_enabled": (bool, False),
        }
        
        for key, (expected_type, default) in schema.items():
            raw_value = raw_config.get(key)
            
            if raw_value is None:
                config[key] = default
                continue
            
            try:
                if expected_type == bool:
                    config[key] = parse_bool(raw_value)
                elif expected_type == list:
                    config[key] = parse_list(raw_value)
                else:
                    config[key] = parse_typed_value(raw_value, expected_type)
            except (ValueError, TypeError) as e:
                self.errors.append(f"Invalid {key}: {e}")
                config[key] = default
        
        return config
    
    def smart_parse_config(self, raw_config: dict[str, str]) -> dict[str, Any]:
        """Parse configuration with automatic type detection."""
        config = {}
        
        for key, value in raw_config.items():
            try:
                # Try automatic parsing first
                config[key] = auto_parse(value)
            except:
                # Fall back to string
                config[key] = value
                
        return config

# Usage
validator = ConfigValidator()

# Raw config from environment or file
raw_config = {
    "debug": "true",
    "port": "8080", 
    "workers": "4",
    "allowed_ips": "127.0.0.1,192.168.1.0/24",
    "timeout": "45.5",
    "ssl_enabled": "yes"
}

# Validated parsing
config = validator.validate_and_parse(raw_config)
if validator.errors:
    print("Validation errors:", validator.errors)

# Smart parsing
smart_config = validator.smart_parse_config(raw_config)
```

## Best Practices

### 1. Use Type-Safe Environment Parsing

```python
# Good: Type-safe with defaults
port = get_int("PORT", 8000)
debug = get_bool("DEBUG", False)

# Bad: Manual parsing with potential errors
port = int(os.environ.get("PORT", "8000"))  # Crashes on invalid input
```

### 2. Consistent Naming with Prefixes

```python
# Good: Consistent prefix usage
db_env = EnvPrefix("DATABASE")
host = db_env.get_str("HOST", "localhost")      # DATABASE_HOST
port = db_env.get_int("PORT", 5432)             # DATABASE_PORT

# Good: Manual prefix for single use
secret = get_str("SECRET", prefix="API")        # API_SECRET
```

### 3. Use Timing for Performance Insights

```python
# Good: Comprehensive timing with context
with timed_block(logger, "data_export", 
                 initial_kvs={"format": "csv"}) as ctx:
    data = fetch_data()
    ctx["records"] = len(data)
    export_to_csv(data)
```

### 4. Format Output Consistently

```python
# Good: Consistent formatting
def show_progress(current, total, start_time):
    elapsed = time.time() - start_time
    percent = format_percentage(current, total)
    duration = format_duration(elapsed)
    
    print(f"Progress: {percent} ({current}/{total}) - {duration}")
```

## Thread Safety

All utility functions are thread-safe:
- Environment parsing functions are read-only
- Formatting functions are stateless  
- `timed_block` uses thread-local context variables

## Performance Considerations

- **Environment Access**: Results are not cached; consider caching frequently accessed values
- **String Formatting**: Format functions are optimized but create new strings
- **Timing Operations**: `timed_block` has minimal overhead (<1μs)

## Module Organization

- [Platform](platform.md) - OS detection and platform utilities
- [Process](process.md) - Process execution and command running
- [Console](console.md) - Console I/O and user interaction
- [Registry](registry.md) - Object registry and service location

## See Also

- [Environment Configuration Guide](../../guide/config/environment.md) - Environment variable patterns
- [Console Module](console.md) - For user interaction and output
- [Logger Module](../logger/index.md) - For structured logging integration
- [Context Module](../context/index.md) - For configuration management
