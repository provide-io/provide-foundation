"""Environment variable utilities with type coercion and prefix support.

Provides utilities for safely reading and parsing environment variables with
automatic type detection, prefix-based namespacing, and default value handling.
"""

import os
from pathlib import Path
from typing import Any, TypeVar, get_origin

from provide.foundation.errors.config import ValidationError
from provide.foundation.utils.parsing import parse_bool, parse_dict, parse_list


def _get_logger():
    """Get logger instance lazily to avoid circular imports."""
    from provide.foundation.logger import get_logger

    return get_logger(__name__)


T = TypeVar("T")


def get_bool(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value or default

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False
    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return parse_bool(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid boolean value for {name}: {value}",
            field=name,
            value=value,
            rule="boolean",
        ) from e


def get_int(name: str, default: int | None = None) -> int | None:
    """Get integer environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Integer value or default

    Raises:
        ValidationError: If value cannot be parsed as integer
    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid integer value for {name}: {value}",
            field=name,
            value=value,
            rule="integer",
        ) from e


def get_float(name: str, default: float | None = None) -> float | None:
    """Get float environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Float value or default

    Raises:
        ValidationError: If value cannot be parsed as float
    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return float(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid float value for {name}: {value}",
            field=name,
            value=value,
            rule="float",
        ) from e


def get_str(name: str, default: str | None = None) -> str | None:
    """Get string environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        String value or default
    """
    return os.environ.get(name, default)


def get_path(name: str, default: Path | str | None = None) -> Path | None:
    """Get path environment variable.

    Args:
        name: Environment variable name
        default: Default path if not set

    Returns:
        Path object or None
    """
    value = os.environ.get(name)
    if value is None:
        if default is None:
            return None
        return Path(default) if not isinstance(default, Path) else default

    # Expand user and environment variables
    expanded = os.path.expanduser(os.path.expandvars(value))
    return Path(expanded)


def get_list(
    name: str, default: list[str] | None = None, separator: str = ","
) -> list[str]:
    """Get list from environment variable.

    Args:
        name: Environment variable name
        default: Default list if not set
        separator: String separator (default: comma)

    Returns:
        List of strings

    Examples:
        >>> os.environ['ITEMS'] = 'a,b,c'
        >>> get_list('ITEMS')
        ['a', 'b', 'c']
    """
    value = os.environ.get(name)
    if value is None:
        return default or []

    # Use existing parse_list which handles empty strings and stripping
    items = parse_list(value, separator=separator, strip=True)
    # Filter empty strings (parse_list doesn't do this by default)
    return [item for item in items if item]


def get_dict(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}
    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def require(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set
    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=name,
            rule="required",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        # Simple type
        if type_hint is bool:
            return get_bool(name)
        elif type_hint is int:
            return get_int(name)
        elif type_hint is float:
            return get_float(name)
        elif type_hint is str:
            return get_str(name)
        elif type_hint is Path:
            return get_path(name)
    elif origin is list:
        return get_list(name)
    elif origin is dict:
        return get_dict(name)

    # Fallback to string
    return os.environ[name]


class EnvPrefix:
    """Environment variable reader with prefix support.

    Provides convenient access to environment variables with a common prefix,
    useful for application-specific configuration namespacing.

    Examples:
        >>> app_env = EnvPrefix('MYAPP')
        >>> app_env.get_bool('DEBUG')  # Reads MYAPP_DEBUG
        >>> app_env['database_url']  # Reads MYAPP_DATABASE_URL
    """

    def __init__(self, prefix: str, separator: str = "_") -> None:
        """Initialize with prefix.

        Args:
            prefix: Prefix for all environment variables
            separator: Separator between prefix and variable name
        """
        self.prefix = prefix.upper()
        self.separator = separator

    def _make_name(self, name: str) -> str:
        """Create full environment variable name."""
        # Convert to uppercase and replace common separators
        name = name.upper().replace("-", "_").replace(".", "_")
        return f"{self.prefix}{self.separator}{name}"

    def get_bool(self, name: str, default: bool | None = None) -> bool | None:
        """Get boolean with prefix."""
        return get_bool(self._make_name(name), default)

    def get_int(self, name: str, default: int | None = None) -> int | None:
        """Get integer with prefix."""
        return get_int(self._make_name(name), default)

    def get_float(self, name: str, default: float | None = None) -> float | None:
        """Get float with prefix."""
        return get_float(self._make_name(name), default)

    def get_str(self, name: str, default: str | None = None) -> str | None:
        """Get string with prefix."""
        return get_str(self._make_name(name), default)

    def get_path(self, name: str, default: Path | str | None = None) -> Path | None:
        """Get path with prefix."""
        return get_path(self._make_name(name), default)

    def get_list(
        self, name: str, default: list[str] | None = None, separator: str = ","
    ) -> list[str]:
        """Get list with prefix."""
        return get_list(self._make_name(name), default, separator)

    def get_dict(
        self,
        name: str,
        default: dict[str, str] | None = None,
        item_separator: str = ",",
        key_value_separator: str = "=",
    ) -> dict[str, str]:
        """Get dictionary with prefix."""
        return get_dict(
            self._make_name(name), default, item_separator, key_value_separator
        )

    def require(self, name: str, type_hint: type[T] | None = None) -> Any:
        """Require variable with prefix."""
        return require(self._make_name(name), type_hint)

    def __getitem__(self, name: str) -> str | None:
        """Get environment variable using subscript notation."""
        return self.get_str(name)

    def __contains__(self, name: str) -> bool:
        """Check if environment variable exists."""
        return self._make_name(name) in os.environ

    def all_with_prefix(self) -> dict[str, str]:
        """Get all environment variables with this prefix.

        Returns:
            Dictionary of variable names (without prefix) to values
        """
        result = {}
        prefix_with_sep = f"{self.prefix}{self.separator}"

        for key, value in os.environ.items():
            if key.startswith(prefix_with_sep):
                # Remove prefix and add to result
                var_name = key[len(prefix_with_sep) :]
                result[var_name] = value

        return result


def parse_duration(value: str) -> int:
    """Parse duration string to seconds.

    Supports formats like: 30s, 5m, 2h, 1d, 1h30m, etc.

    Args:
        value: Duration string

    Returns:
        Duration in seconds

    Examples:
        >>> parse_duration('30s')
        30
        >>> parse_duration('1h30m')
        5400
        >>> parse_duration('2d')
        172800
    """
    import re

    if value.isdigit():
        return int(value)

    total_seconds = 0

    # Pattern for duration components
    pattern = r"(\d+)([dhms])"
    matches = re.findall(pattern, value.lower())

    if not matches:
        raise ValidationError(
            f"Invalid duration format: {value}", value=value, rule="duration"
        )

    units = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,
    }

    for amount, unit in matches:
        if unit in units:
            total_seconds += int(amount) * units[unit]
        else:
            raise ValidationError(
                f"Unknown duration unit: {unit}", value=value, rule="duration_unit"
            )

    return total_seconds


def parse_size(value: str) -> int:
    """Parse size string to bytes.

    Supports formats like: 1024, 1KB, 10MB, 1.5GB, etc.

    Args:
        value: Size string

    Returns:
        Size in bytes

    Examples:
        >>> parse_size('1024')
        1024
        >>> parse_size('10MB')
        10485760
        >>> parse_size('1.5GB')
        1610612736
    """
    import re

    if value.isdigit():
        return int(value)

    # Pattern for size with unit
    pattern = r"^(\d+(?:\.\d+)?)\s*([KMGT]?B?)$"
    match = re.match(pattern, value.upper())

    if not match:
        raise ValidationError(f"Invalid size format: {value}", value=value, rule="size")

    amount = float(match.group(1))
    unit = match.group(2) or "B"

    units = {
        "B": 1,
        "KB": 1024,
        "K": 1024,
        "MB": 1024**2,
        "M": 1024**2,
        "GB": 1024**3,
        "G": 1024**3,
        "TB": 1024**4,
        "T": 1024**4,
    }

    if unit not in units:
        raise ValidationError(
            f"Unknown size unit: {unit}", value=value, rule="size_unit"
        )

    return int(amount * units[unit])


__all__ = [
    "EnvPrefix",
    "get_bool",
    "get_dict",
    "get_float",
    "get_int",
    "get_list",
    "get_path",
    "get_str",
    "parse_duration",
    "parse_size",
    "require",
]
