# Configuration Field Converters

This document provides comprehensive documentation for the Foundation configuration field converters, including usage patterns, best practices, and examples.

## Overview

Foundation provides a robust set of field converters and validators to parse and validate environment variables and configuration values. These converters handle the common task of converting string values (from environment variables, config files, CLI args, etc.) into proper Python types with validation and helpful error messages.

## Converter Categories

### 1. Strict vs Lenient Parsers

Foundation provides two philosophies for parsing:

#### Strict Parsers
- **Use Case**: Internal APIs, critical configuration where precision matters
- **Behavior**: Raise detailed errors for invalid values
- **Examples**: `parse_bool_strict()`, `parse_log_level()`, `parse_float_with_validation()`

#### Lenient Parsers  
- **Use Case**: User-facing configuration, optional settings
- **Behavior**: Skip invalid values silently or use sensible defaults
- **Examples**: `parse_bool_extended()`, `parse_module_levels()`, `parse_rate_limits()`

## Parser Functions

### Boolean Parsing

#### `parse_bool_extended(value: str | bool) -> bool`
**Lenient boolean parser** - forgiving of user input, defaults to `False` for unrecognized values.

```python
from provide.foundation.config.converters import parse_bool_extended

# Recognized True values: "true", "yes", "1", "on" (case-insensitive)
parse_bool_extended("yes")      # True
parse_bool_extended("TRUE")     # True
parse_bool_extended("1")        # True

# Recognized False values: "false", "no", "0", "off" (case-insensitive)
parse_bool_extended("no")       # False
parse_bool_extended("0")        # False

# Default behavior - unknown values default to False
parse_bool_extended("maybe")    # False (no error)
parse_bool_extended("")         # False
```

#### `parse_bool_strict(value: str | bool) -> bool`
**Strict boolean parser** - precise validation with helpful error messages.

```python
from provide.foundation.config.converters import parse_bool_strict

# Same recognition as extended, but strict validation
parse_bool_strict("yes")        # True
parse_bool_strict("false")      # False

# Type checking
parse_bool_strict(True)         # True (bool input preserved)

# Strict error handling
parse_bool_strict("maybe")      # ValueError: Invalid boolean 'maybe'. Valid options: true, false, yes, no, 1, 0, on, off
parse_bool_strict(42)           # TypeError: Boolean field requires str or bool, got int
```

**When to use:**
- `parse_bool_extended()`: Feature flags, optional telemetry settings, user preferences
- `parse_bool_strict()`: Critical system configuration, internal API parameters

### Log Level Parsing

#### `parse_log_level(value: str) -> LogLevelStr`
Strict parser for log levels with case normalization.

```python
from provide.foundation.config.converters import parse_log_level

parse_log_level("debug")        # "DEBUG"  
parse_log_level("INFO")         # "INFO"
parse_log_level("Warning")      # "WARNING"

parse_log_level("invalid")      # ValueError: Invalid log_level 'invalid'. Valid options: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
```

#### `parse_module_levels(value: str | dict[str, str]) -> dict[str, LogLevelStr]`
Parse module-specific log level overrides with lenient error handling.

```python
from provide.foundation.config.converters import parse_module_levels

# String format parsing
parse_module_levels("auth:DEBUG,database:ERROR")
# Result: {"auth": "DEBUG", "database": "ERROR"}

# Dict input (levels are normalized)
parse_module_levels({"web": "warning", "api": "INFO"})
# Result: {"web": "WARNING", "api": "INFO"}

# Lenient - invalid entries are skipped
parse_module_levels("auth:DEBUG,invalid:BADLEVEL,db:ERROR")  
# Result: {"auth": "DEBUG", "db": "ERROR"}
```

### Numeric Parsing

#### `parse_float_with_validation(value: str, min_val: float = None, max_val: float = None) -> float`
Parse floats with optional range validation.

```python
from provide.foundation.config.converters import parse_float_with_validation

parse_float_with_validation("3.14")                    # 3.14
parse_float_with_validation("5.0", min_val=0.0, max_val=10.0)  # 5.0

parse_float_with_validation("abc")                     # ValueError: Invalid float 'abc'. Expected: float
parse_float_with_validation("-1.0", min_val=0.0)      # ValueError: Value -1.0 for float must be >= 0.0
```

#### `parse_sample_rate(value: str) -> float`  
Specialized parser for sampling rates (0.0 to 1.0).

```python
from provide.foundation.config.converters import parse_sample_rate

parse_sample_rate("0.5")        # 0.5
parse_sample_rate("1.0")        # 1.0

parse_sample_rate("1.5")        # ValueError: Value 1.5 for float must be <= 1.0
```

### String Parsing  

#### `parse_comma_list(value: str) -> list[str]`
Parse comma-separated lists with whitespace trimming.

```python
from provide.foundation.config.converters import parse_comma_list

parse_comma_list("a,b,c")           # ["a", "b", "c"]  
parse_comma_list(" a , b , c ")     # ["a", "b", "c"]
parse_comma_list("")                # []
```

#### Complex String Parsers

##### `parse_headers(value: str) -> dict[str, str]`
Parse HTTP headers from key=value pairs.

```python  
from provide.foundation.config.converters import parse_headers

parse_headers("Authorization=Bearer token,Content-Type=application/json")
# Result: {"Authorization": "Bearer token", "Content-Type": "application/json"}

# Lenient - invalid pairs are skipped
parse_headers("valid=ok,invalid-no-equals,another=good")
# Result: {"valid": "ok", "another": "good"}
```

##### `parse_rate_limits(value: str) -> dict[str, tuple[float, float]]`
Parse per-logger rate limits in logger:rate:capacity format.

```python
from provide.foundation.config.converters import parse_rate_limits

parse_rate_limits("api:10.0:100.0,worker:5.0:50.0") 
# Result: {"api": (10.0, 100.0), "worker": (5.0, 50.0)}

# Lenient - invalid entries are skipped
parse_rate_limits("api:10:100,invalid:format,worker:5:50")
# Result: {"api": (10.0, 100.0), "worker": (5.0, 50.0)}
```

### JSON Parsing

#### `parse_json_dict(value: str) -> dict[str, Any]`
#### `parse_json_list(value: str) -> list[Any]`
Strict JSON parsers with type validation.

```python
from provide.foundation.config.converters import parse_json_dict, parse_json_list

parse_json_dict('{"key": "value", "number": 42}')
# Result: {"key": "value", "number": 42}

parse_json_list('["a", "b", "c"]')  
# Result: ["a", "b", "c"]

# Type validation
parse_json_dict('["not", "a", "dict"]')     # ValueError: Invalid json_dict 'list'. Expected: JSON object
parse_json_list('{"not": "a list"}')        # ValueError: Invalid json_list 'dict'. Expected: JSON array
```

## Validator Functions

Validators are used with attrs `validator` parameter to validate field values after conversion.

### Usage Pattern

```python
from attrs import define
from provide.foundation.config.base import field
from provide.foundation.config.converters import parse_sample_rate, validate_sample_rate

@define
class MyConfig:
    sample_rate: float = field(
        default=0.1,
        env_var="SAMPLE_RATE", 
        converter=parse_sample_rate,
        validator=validate_sample_rate,
        description="Sampling rate (0.0 to 1.0)"
    )
```

### Available Validators

#### `validate_log_level(instance, attribute, value: str)`
#### `validate_sample_rate(instance, attribute, value: float)` 
#### `validate_port(instance, attribute, value: int)`
#### `validate_positive(instance, attribute, value: float | int)`
#### `validate_non_negative(instance, attribute, value: float | int)`
#### `validate_overflow_policy(instance, attribute, value: str)`

## Best Practices

### 1. Choose the Right Parser Philosophy

```python
# ✅ Good: Strict for critical configuration
class DatabaseConfig:
    connection_timeout: float = field(
        converter=lambda x: parse_float_with_validation(x, min_val=0.1),
        validator=validate_positive
    )

# ✅ Good: Lenient for user preferences  
class UserPreferences:
    notifications_enabled: bool = field(
        converter=parse_bool_extended,  # Defaults to False for invalid input
        default=True
    )
```

### 2. Use Validators for Additional Constraints

```python
from provide.foundation.config.converters import validate_port

@define  
class ServerConfig:
    port: int = field(
        converter=int,
        validator=validate_port,  # Ensures 1 <= port <= 65535
    )
```

### 3. Provide Clear Field Documentation

```python
@define
class TelemetryConfig:
    sample_rate: float = field(
        converter=parse_sample_rate,
        validator=validate_sample_rate,
        description="Trace sampling rate (0.0=none, 1.0=all). Higher values increase overhead."
    )
```

### 4. Handle Complex Configuration Gracefully

```python
@define
class LoggingConfig:
    # Use lenient parsing for optional advanced features
    module_levels: dict[str, LogLevelStr] = field(
        factory=dict,
        env_var="LOG_MODULE_LEVELS", 
        converter=parse_module_levels,  # Skips invalid entries
        description="Per-module log levels: 'auth:DEBUG,api:INFO'"
    )
    
    # Use strict parsing for critical settings
    default_level: LogLevelStr = field(
        default="INFO",
        env_var="LOG_LEVEL",
        converter=parse_log_level,  # Strict validation
        validator=validate_log_level,
        description="Default log level for all modules"
    )
```

## Error Handling

### Standardized Error Messages

All converters use standardized error message formats:

- **Parser errors**: `"Invalid {field_name} '{value}'. Valid options: {options}"`
- **Validation errors**: `"Value {value} for {field_name} {constraint}"`
- **Type errors**: `"Boolean field requires str or bool, got {type}. Received value: {value}"`

### Error Examples

```python
# Parser error
parse_log_level("INVALID")
# ValueError: Invalid log_level 'INVALID'. Valid options: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL

# Validation error  
validate_sample_rate(None, attr_with_name('rate'), 1.5)
# ValueError: Value 1.5 for rate must be between 0.0 and 1.0

# Type error
parse_bool_strict(42)
# TypeError: Boolean field requires str or bool, got int. Received value: 42
```

## Migration Guide

### From Manual Parsing

```python  
# ❌ Before: Manual parsing with inconsistent error handling
def parse_bool_env(value: str) -> bool:
    if value.lower() in ("true", "1", "yes"):
        return True
    elif value.lower() in ("false", "0", "no"):  
        return False
    else:
        raise ValueError(f"Bad boolean: {value}")

# ✅ After: Use Foundation converters
from provide.foundation.config.converters import parse_bool_strict

# Automatic handling of case, whitespace, comprehensive value recognition
enabled = parse_bool_strict(env_value)
```

### From Basic Type Conversion

```python
# ❌ Before: Basic conversion without validation  
sample_rate = float(os.environ.get("SAMPLE_RATE", "0.1"))

# ✅ After: Validated parsing with clear errors
from provide.foundation.config.converters import parse_sample_rate
sample_rate = parse_sample_rate(os.environ.get("SAMPLE_RATE", "0.1"))
```

## Testing Converters

Foundation provides comprehensive test coverage. When creating custom converters, follow these patterns:

```python
import pytest
from provide.foundation.config.converters import parse_bool_strict

def test_my_custom_converter_valid():
    """Test valid inputs."""
    assert parse_bool_strict("true") is True
    assert parse_bool_strict("false") is False

def test_my_custom_converter_invalid():
    """Test error handling."""
    with pytest.raises(ValueError, match="Invalid boolean"):
        parse_bool_strict("maybe")
        
    with pytest.raises(TypeError, match="Boolean field requires"):
        parse_bool_strict(42)
```

## Performance Considerations

- **Lenient parsers** are optimized for partial success scenarios
- **Strict parsers** fail fast with detailed error context
- **Validators** add minimal overhead and are applied after conversion
- **String parsing** functions use efficient regex-free algorithms where possible

## Conclusion

Foundation's configuration converters provide a robust, tested foundation for handling configuration parsing with consistent error handling and validation. Choose the appropriate converter philosophy (strict vs lenient) based on your use case, and leverage the comprehensive validation functions to ensure configuration integrity.