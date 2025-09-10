"""
Configuration field converters for parsing environment variables.

These converters are used with the field() decorator to automatically
parse and validate environment variable values into the correct types.
"""

import json
from typing import Any

from provide.foundation.errors.decorators import with_error_handling

# Type definitions to avoid circular imports
LogLevelStr = str
ConsoleFormatterStr = str

_VALID_LOG_LEVEL_TUPLE = (
    "TRACE",
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
)

_VALID_FORMATTER_TUPLE = (
    "key_value",
    "json",
)


def parse_log_level(value: str) -> LogLevelStr:
    """
    Parse and validate log level string.
    
    Args:
        value: Log level string (case-insensitive)
        
    Returns:
        Valid log level string in uppercase
        
    Raises:
        ValueError: If the log level is invalid
    """
    level = value.upper()
    if level not in _VALID_LOG_LEVEL_TUPLE:
        raise ValueError(
            f"Invalid log level '{value}'. Valid options: {', '.join(_VALID_LOG_LEVEL_TUPLE)}"
        )
    return level



def parse_console_formatter(value: str) -> ConsoleFormatterStr:
    """
    Parse and validate console formatter string.
    
    Args:
        value: Formatter string (case-insensitive)
        
    Returns:
        Valid formatter string in lowercase
        
    Raises:
        ValueError: If the formatter is invalid
    """
    formatter = value.lower()
    if formatter not in _VALID_FORMATTER_TUPLE:
        raise ValueError(
            f"Invalid console formatter '{value}'. Valid options: {', '.join(_VALID_FORMATTER_TUPLE)}"
        )
    return formatter


@with_error_handling(
    fallback={},
    suppress=(ValueError, KeyError),
    context_provider=lambda: {"function": "parse_module_levels", "module": "config.converters"}
)
def parse_module_levels(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """
    Parse module-specific log levels from string format.
    
    Format: "module1:LEVEL,module2:LEVEL"
    Example: "auth.service:DEBUG,database:ERROR"
    
    Args:
        value: Comma-separated module:level pairs or dict
        
    Returns:
        Dictionary mapping module names to log levels
    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result
    
    if not value or not value.strip():
        return {}
    
    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue
            
        if ":" not in pair:
            # Skip invalid entries silently
            continue
            
        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()
        
        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue
    
    return result


def parse_rate_limits(value: str) -> dict[str, tuple[float, float]]:
    """
    Parse per-logger rate limits from string format.
    
    Format: "logger1:rate:capacity,logger2:rate:capacity"
    Example: "api:10.0:100.0,worker:5.0:50.0"
    
    Args:
        value: Comma-separated logger:rate:capacity triplets
        
    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples
    """
    if not value or not value.strip():
        return {}
    
    result = {}
    for item in value.split(","):
        item = item.strip()
        if not item:
            continue
            
        parts = item.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue
            
        logger, rate_str, capacity_str = parts
        logger = logger.strip()
        
        if logger:
            try:
                rate = float(rate_str.strip())
                capacity = float(capacity_str.strip())
                result[logger] = (rate, capacity)
            except (ValueError, TypeError):
                # Skip invalid numbers silently
                continue
    
    return result


def parse_foundation_log_output(value: str) -> str:
    """
    Parse and validate foundation log output destination.
    
    Args:
        value: Output destination string
        
    Returns:
        Valid output destination (stderr, stdout, main)
        
    Raises:
        ValueError: If the value is invalid
    """
    if not value:
        return "stderr"
        
    normalized = value.lower().strip()
    valid_options = ("stderr", "stdout", "main")
    
    if normalized in valid_options:
        return normalized
    else:
        raise ValueError(
            f"Invalid foundation log output '{value}'. Valid options: {', '.join(valid_options)}"
        )


def parse_comma_list(value: str) -> list[str]:
    """
    Parse comma-separated list of strings.
    
    Args:
        value: Comma-separated string
        
    Returns:
        List of trimmed non-empty strings
    """
    if not value or not value.strip():
        return []
    
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_bool_extended(value: str | bool) -> bool:
    """
    Parse boolean from string with extended format support.
    
    Recognizes: true/false, yes/no, 1/0, on/off (case-insensitive)
    
    Args:
        value: Boolean string representation or bool
        
    Returns:
        Boolean value
    """
    # If already a bool, return as-is
    if isinstance(value, bool):
        return value
    
    # Convert to string and parse
    value_lower = str(value).lower().strip()
    return value_lower in ("true", "yes", "1", "on")


def parse_bool_strict(value: str | bool) -> bool:
    """
    Parse boolean from string with strict validation.
    
    Recognizes: true/false, yes/no, 1/0, on/off (case-insensitive)
    
    Args:
        value: Boolean string representation or bool
        
    Returns:
        Boolean value
        
    Raises:
        TypeError: If value is not a string or bool
        ValueError: If the value cannot be parsed as boolean
    """
    # Check type first
    if not isinstance(value, (str, bool)):
        raise TypeError(f"Boolean field requires str or bool, got {type(value).__name__}")
    
    # If already a bool, return as-is
    if isinstance(value, bool):
        return value
    
    # Convert to string and parse
    value_lower = value.lower().strip()
    
    if value_lower in ("true", "yes", "1", "on"):
        return True
    elif value_lower in ("false", "no", "0", "off"):
        return False
    else:
        raise ValueError(f"Invalid boolean value '{value}'. Valid options: true/false, yes/no, 1/0, on/off")


@with_error_handling(
    fallback=0.0,
    context_provider=lambda: {"module": "config.converters"}
)
def parse_float_with_validation(
    value: str, min_val: float | None = None, max_val: float | None = None
) -> float:
    """
    Parse float with optional range validation.
    
    Args:
        value: String representation of float
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)
        
    Returns:
        Parsed float value
        
    Raises:
        ValueError: If value is not a valid float or out of range
    """
    try:
        result = float(value)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid float value '{value}': {e}")
    
    if min_val is not None and result < min_val:
        raise ValueError(f"Value {result} is below minimum {min_val}")
    
    if max_val is not None and result > max_val:
        raise ValueError(f"Value {result} is above maximum {max_val}")
    
    return result


def parse_sample_rate(value: str) -> float:
    """
    Parse sampling rate (0.0 to 1.0).
    
    Args:
        value: String representation of sampling rate
        
    Returns:
        Float between 0.0 and 1.0
        
    Raises:
        ValueError: If value is not valid or out of range
    """
    return parse_float_with_validation(value, min_val=0.0, max_val=1.0)


def parse_json_dict(value: str) -> dict[str, Any]:
    """
    Parse JSON string into dictionary.
    
    Args:
        value: JSON string
        
    Returns:
        Parsed dictionary
        
    Raises:
        ValueError: If JSON is invalid
    """
    if not value or not value.strip():
        return {}
    
    try:
        result = json.loads(value)
        if not isinstance(result, dict):
            raise ValueError(f"Expected JSON object, got {type(result).__name__}")
        return result
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")


def parse_json_list(value: str) -> list[Any]:
    """
    Parse JSON string into list.
    
    Args:
        value: JSON string
        
    Returns:
        Parsed list
        
    Raises:
        ValueError: If JSON is invalid
    """
    if not value or not value.strip():
        return []
    
    try:
        result = json.loads(value)
        if not isinstance(result, list):
            raise ValueError(f"Expected JSON array, got {type(result).__name__}")
        return result
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")


def parse_headers(value: str) -> dict[str, str]:
    """
    Parse HTTP headers from string format.
    
    Format: "key1=value1,key2=value2"
    Example: "Authorization=Bearer token,Content-Type=application/json"
    
    Args:
        value: Comma-separated key=value pairs
        
    Returns:
        Dictionary of headers
    """
    if not value or not value.strip():
        return {}
    
    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue
            
        if "=" not in pair:
            # Skip invalid entries
            continue
            
        key, val = pair.split("=", 1)
        key = key.strip()
        val = val.strip()
        
        if key:
            result[key] = val
    
    return result


# Validators (used with validator parameter in field())

def validate_log_level(instance: Any, attribute: Any, value: str) -> None:
    """Validate that a log level is valid."""
    if value not in _VALID_LOG_LEVEL_TUPLE:
        raise ValueError(
            f"Invalid log level '{value}' for {attribute.name}. "
            f"Valid options: {', '.join(_VALID_LOG_LEVEL_TUPLE)}"
        )


def validate_sample_rate(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a sample rate is between 0.0 and 1.0."""
    if not 0.0 <= value <= 1.0:
        raise ValueError(
            f"Sample rate {value} for {attribute.name} must be between 0.0 and 1.0"
        )


def validate_port(instance: Any, attribute: Any, value: int) -> None:
    """Validate that a port number is valid."""
    if not 1 <= value <= 65535:
        raise ValueError(
            f"Port {value} for {attribute.name} must be between 1 and 65535"
        )


def validate_positive(instance: Any, attribute: Any, value: float | int) -> None:
    """Validate that a value is positive."""
    if value <= 0:
        raise ValueError(f"Value {value} for {attribute.name} must be positive")


def validate_non_negative(instance: Any, attribute: Any, value: float | int) -> None:
    """Validate that a value is non-negative."""
    if value < 0:
        raise ValueError(f"Value {value} for {attribute.name} must be non-negative")


def validate_overflow_policy(instance: Any, attribute: Any, value: str) -> None:
    """Validate rate limit overflow policy."""
    valid_policies = ("drop_oldest", "drop_newest", "block")
    if value not in valid_policies:
        raise ValueError(
            f"Invalid overflow policy '{value}' for {attribute.name}. "
            f"Valid options: {', '.join(valid_policies)}"
        )



__all__ = [
    # Parsers/Converters
    "parse_log_level",
    "parse_console_formatter", 
    "parse_module_levels",
    "parse_rate_limits",
    "parse_comma_list",
    "parse_bool_extended",
    "parse_float_with_validation",
    "parse_sample_rate",
    "parse_json_dict",
    "parse_json_list",
    "parse_headers",
    # Validators
    "validate_log_level",
    "validate_sample_rate",
    "validate_port",
    "validate_positive",
    "validate_non_negative",
    "validate_overflow_policy",
]