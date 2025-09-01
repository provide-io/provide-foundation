"""
Type definitions for the configuration system.
"""
from enum import Enum
from typing import Any, Dict, List, Optional, Union

# Basic type aliases
ConfigValue = Union[str, int, float, bool, None, List[Any], Dict[str, Any]]
ConfigDict = Dict[str, ConfigValue]


class ConfigSource(Enum):
    """Sources for configuration values with precedence order."""
    
    DEFAULT = 0  # Lowest precedence
    FILE = 10
    ENV = 20
    RUNTIME = 30  # Highest precedence
    
    def __lt__(self, other):
        """Enable comparison for precedence."""
        if not isinstance(other, ConfigSource):
            return NotImplemented
        return self.value < other.value


class ConfigFormat(Enum):
    """Supported configuration file formats."""
    
    JSON = "json"
    YAML = "yaml"
    TOML = "toml"
    INI = "ini"
    ENV = "env"  # .env files
    
    @classmethod
    def from_extension(cls, filename: str) -> Optional["ConfigFormat"]:
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