from __future__ import annotations

import os
from pathlib import Path
from typing import Any, TypeVar

from provide.foundation.utils.environment.getters import (
    get_bool,
    get_dict,
    get_float,
    get_int,
    get_list,
    get_path,
    get_str,
    require,
)

"""Environment variable reader with prefix support.

Provides the EnvPrefix class for convenient access to environment variables
with a common prefix, useful for application-specific configuration namespacing.
"""


T = TypeVar("T")


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

    def get_list(self, name: str, default: list[str] | None = None, separator: str = ",") -> list[str]:
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
        return get_dict(self._make_name(name), default, item_separator, key_value_separator)

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
