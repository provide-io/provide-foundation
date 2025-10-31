#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Type definitions for the configuration system."""

from __future__ import annotations

from enum import Enum
from typing import Any, TypeAlias

# Basic type aliases
ConfigValue = str | int | float | bool | None | list[Any] | dict[str, Any]
ConfigDict = dict[str, ConfigValue]

# Common configuration type aliases
HeaderDict: TypeAlias = dict[str, str]
EnvDict: TypeAlias = dict[str, str]
FieldMetadata: TypeAlias = dict[str, Any]


class ConfigSource(Enum):
    """Sources for configuration values with precedence order."""

    DEFAULT = 0  # Lowest precedence
    FILE = 10
    ENV = 20
    RUNTIME = 30  # Highest precedence

    def __lt__(self, other: object) -> bool:
        """Enable comparison for precedence."""
        if not isinstance(other, ConfigSource):
            return NotImplemented
        return self.value < other.value

    def __le__(self, other: object) -> bool:
        """Enable <= comparison for precedence."""
        if not isinstance(other, ConfigSource):
            return NotImplemented
        return self.value <= other.value

    def __gt__(self, other: object) -> bool:
        """Enable > comparison for precedence."""
        if not isinstance(other, ConfigSource):
            return NotImplemented
        return self.value > other.value

    def __ge__(self, other: object) -> bool:
        """Enable >= comparison for precedence."""
        if not isinstance(other, ConfigSource):
            return NotImplemented
        return self.value >= other.value

    def __eq__(self, other: object) -> bool:
        """Enable == comparison for precedence."""
        if not isinstance(other, ConfigSource):
            return NotImplemented
        return self.value == other.value


class ConfigFormat(Enum):
    """Supported configuration file formats."""

    JSON = "json"
    YAML = "yaml"
    TOML = "toml"
    INI = "ini"
    ENV = "env"  # .env files

    @classmethod
    def from_extension(cls, filename: str) -> ConfigFormat | None:
        """Determine format from file extension."""
        ext_map = {
            ".json": cls.JSON,
            ".yaml": cls.YAML,
            ".yml": cls.YAML,
            ".toml": cls.TOML,
            ".ini": cls.INI,
            ".env": cls.ENV,
        }

        for ext, format_type in ext_map.items():
            if filename.lower().endswith(ext):
                return format_type
        return None


# 🧱🏗️🔚
