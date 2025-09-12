"""
Configuration field converters for parsing environment variables.

These converters are used with the field() decorator to automatically
parse and validate environment variable values into the correct types.
"""

import json
from typing import Any

# Use string type annotations to avoid circular imports during runtime
# Type checking imports are only available during static analysis
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from provide.foundation.logger.types import LogLevelStr, ConsoleFormatterStr
else:
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


def parse_log_level(value: str) -> "LogLevelStr":
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
        raise ValueError(f"Invalid log level '{value}'. Valid options: {', '.join(_VALID_LOG_LEVEL_TUPLE)}")
    return level


def parse_console_formatter(value: str) -> "ConsoleFormatterStr":
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


# TODO: Add back error handling decorator once circular imports are fully resolved
def parse_module_levels(value: str | dict[str, str]) -> dict[str, "LogLevelStr"]:
    """
    Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}
        
        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}
        
        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}
        
        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.
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

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}
        
        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}
        
        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.
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
            # Skip entries that don't have exactly 3 parts (logger:rate:capacity)
            continue

        logger, rate_str, capacity_str = parts
        logger = logger.strip()

        if logger:
            try:
                rate = float(rate_str.strip())
                capacity = float(capacity_str.strip())
                result[logger] = (rate, capacity)
            except (ValueError, TypeError):
                # Skip entries where rate or capacity cannot be parsed as floats
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
        raise ValueError(f"Invalid foundation log output '{value}'. Valid options: {', '.join(valid_options)}")


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
    Parse boolean from string with lenient/forgiving interpretation.

    This is the **lenient** boolean parser - designed for user-facing configuration
    where we want to be forgiving of various inputs. Any unrecognized string 
    defaults to False rather than raising an error.

    **Use Cases:**
    - Environment variables set by end users
    - Feature flags that should default to "off" if misconfigured  
    - Optional telemetry settings where failure should not break the system

    **Recognized True Values:** true, yes, 1, on (case-insensitive)
    **Recognized False Values:** false, no, 0, off (case-insensitive) 
    **Default Behavior:** Any other string → False (no error)

    Args:
        value: Boolean string representation or actual bool

    Returns:
        Boolean value (defaults to False for unrecognized strings)

    Examples:
        >>> parse_bool_extended("yes")  # True
        >>> parse_bool_extended("FALSE")  # False  
        >>> parse_bool_extended("invalid")  # False (no error)
        >>> parse_bool_extended(True)  # True
    """
    # If already a bool, return as-is
    if isinstance(value, bool):
        return value

    # Convert to string and parse
    value_lower = str(value).lower().strip()
    # Only return True for explicit true values, everything else is False
    return value_lower in ("true", "yes", "1", "on")


def parse_bool_strict(value: str | bool) -> bool:
    """
    Parse boolean from string with strict validation and clear error messages.

    This is the **strict** boolean parser - designed for internal APIs and critical
    configuration where invalid values should cause immediate failure with helpful
    error messages.

    **Use Cases:**
    - Internal API parameters where precision matters
    - Critical system configurations where misconfiguration is dangerous
    - Programmatic configuration where clear validation errors help developers

    **Recognized True Values:** true, yes, 1, on (case-insensitive)
    **Recognized False Values:** false, no, 0, off (case-insensitive)
    **Error Behavior:** Raises ValueError with helpful message for invalid values

    Args:
        value: Boolean string representation or actual bool

    Returns:
        Boolean value (never defaults - raises on invalid input)

    Raises:
        TypeError: If value is not a string or bool
        ValueError: If string value cannot be parsed as boolean

    Examples:
        >>> parse_bool_strict("yes")  # True
        >>> parse_bool_strict("FALSE")  # False
        >>> parse_bool_strict("invalid")  # ValueError with helpful message
        >>> parse_bool_strict(42)  # TypeError
    """
    # Check type first for clear error messages
    if not isinstance(value, (str, bool)):
        raise TypeError(
            f"Boolean field requires str or bool, got {type(value).__name__}. "
            f"Received value: {value!r}"
        )

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
        raise ValueError(
            f"Invalid boolean value '{value}'. "
            f"Valid options: true/false, yes/no, 1/0, on/off (case-insensitive). "
            f"Use parse_bool_extended() for lenient parsing that defaults to False."
        )


# TODO: Add back error handling decorator once circular imports are fully resolved
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
        raise ValueError(f"Invalid float value '{value}': {e}") from e

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
        raise ValueError(f"Invalid JSON: {e}") from e


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
        raise ValueError(f"Invalid JSON: {e}") from e


def parse_headers(value: str) -> dict[str, str]:
    """
    Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}
        
        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}
        
        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}
        
        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.
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
        raise ValueError(f"Sample rate {value} for {attribute.name} must be between 0.0 and 1.0")


def validate_port(instance: Any, attribute: Any, value: int) -> None:
    """Validate that a port number is valid."""
    if not 1 <= value <= 65535:
        raise ValueError(f"Port {value} for {attribute.name} must be between 1 and 65535")


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
