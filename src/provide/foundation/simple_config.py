#
# provide/foundation/config.py
#
"""
Unified configuration management for provide.foundation applications.
"""

import os
import tomllib
from pathlib import Path
from typing import Any, Self, TypeVar

import attrs

from provide.foundation.errors import FoundationError

T = TypeVar("T", bound="BaseConfig")


class ConfigError(FoundationError):
    """Configuration-related errors."""
    pass


@attrs.define
class BaseConfig:
    """Base configuration class with common loading patterns."""

    @classmethod
    def from_env(cls: type[Self], prefix: str = "") -> Self:
        """Create configuration from environment variables."""
        config_dict: dict[str, Any] = {}
        
        # Get all fields for this class
        field_dict = attrs.fields_dict(cls)
        
        for field_name, field in field_dict.items():
            # Convert field_name to UPPER_CASE env var name
            env_name = f"{prefix}_{field_name.upper()}" if prefix else field_name.upper()
            value = os.environ.get(env_name)
            
            if value is not None:
                # Type conversion based on field type annotation
                field_type = field.type
                
                # Handle common type conversions
                if field_type == Path or field_type == Path | None:
                    config_dict[field_name] = Path(value)
                elif field_type == int or field_type == int | None:
                    try:
                        config_dict[field_name] = int(value)
                    except ValueError as e:
                        raise ConfigError(f"Invalid integer value for {env_name}: {value}") from e
                elif field_type == bool or field_type == bool | None:
                    config_dict[field_name] = value.lower() in ("true", "1", "yes", "on")
                elif field_type == float or field_type == float | None:
                    try:
                        config_dict[field_name] = float(value)
                    except ValueError as e:
                        raise ConfigError(f"Invalid float value for {env_name}: {value}") from e
                else:
                    config_dict[field_name] = value
        
        return cls(**config_dict)

    @classmethod
    def from_toml_file(cls: type[Self], file_path: Path | str) -> Self:
        """Create configuration from TOML file."""
        path = Path(file_path)
        
        if not path.exists():
            raise ConfigError(f"Configuration file not found: {path}")
        
        try:
            with open(path, "rb") as f:
                data = tomllib.load(f)
            
            # Handle nested configuration by looking for class name or using root
            class_name = cls.__name__.lower().replace("config", "")
            config_data = data.get(class_name, data)
            
            return cls.from_dict(config_data)
        except tomllib.TOMLDecodeError as e:
            raise ConfigError(f"Invalid TOML file {path}: {e}") from e
        except Exception as e:
            raise ConfigError(f"Error loading configuration from {path}: {e}") from e

    @classmethod
    def from_dict(cls: type[Self], data: dict[str, Any]) -> Self:
        """Create configuration from dictionary with type conversion."""
        config_dict: dict[str, Any] = {}
        field_dict = attrs.fields_dict(cls)
        
        for key, value in data.items():
            if key in field_dict:
                field = field_dict[key]
                field_type = field.type
                
                # Type conversion
                if field_type == Path or field_type == Path | None:
                    config_dict[key] = Path(value) if value is not None else None
                elif isinstance(value, str) and (field_type == int or field_type == int | None):
                    try:
                        config_dict[key] = int(value)
                    except ValueError as e:
                        raise ConfigError(f"Invalid integer value for {key}: {value}") from e
                elif isinstance(value, str) and (field_type == float or field_type == float | None):
                    try:
                        config_dict[key] = float(value)
                    except ValueError as e:
                        raise ConfigError(f"Invalid float value for {key}: {value}") from e
                else:
                    config_dict[key] = value
        
        return cls(**config_dict)

    def merge(self, other: Self) -> Self:
        """Merge with another configuration, with other taking precedence."""
        if not isinstance(other, self.__class__):
            raise ConfigError(f"Cannot merge {type(other)} with {type(self)}")
        
        # Get all non-None values from other
        other_dict = attrs.asdict(other)
        self_dict = attrs.asdict(self)
        
        # Merge, with other taking precedence for non-None values
        merged_dict = self_dict.copy()
        for key, value in other_dict.items():
            if value is not None:
                merged_dict[key] = value
        
        return self.__class__(**merged_dict)

    def to_env_dict(self, prefix: str = "") -> dict[str, str]:
        """Convert configuration to environment variable dictionary."""
        env_dict: dict[str, str] = {}
        
        for field in attrs.fields(self.__class__):
            value = getattr(self, field.name)
            if value is not None:
                env_name = f"{prefix}_{field.name.upper()}" if prefix else field.name.upper()
                if isinstance(value, Path):
                    env_dict[env_name] = str(value)
                elif isinstance(value, bool):
                    env_dict[env_name] = "true" if value else "false"
                else:
                    env_dict[env_name] = str(value)
        
        return env_dict


# Configuration loading utilities

def load_config_with_precedence(
    config_class: type[T],
    *,
    env_prefix: str = "",
    config_files: list[Path | str] | None = None,
    explicit_config: dict[str, Any] | None = None
) -> T:
    """
    Load configuration with precedence:
    1. Explicit config (highest priority)
    2. Environment variables
    3. Configuration files (in order, last wins)
    4. Class defaults (lowest priority)
    """
    # Start with defaults
    config = config_class()
    
    # Load from files (in order)
    if config_files:
        for file_path in config_files:
            path = Path(file_path)
            if path.exists():
                file_config = config_class.from_toml_file(path)
                config = config.merge(file_config)
    
    # Load from environment
    env_config = config_class.from_env(env_prefix)
    config = config.merge(env_config)
    
    # Apply explicit config
    if explicit_config:
        explicit_config_obj = config_class.from_dict(explicit_config)
        config = config.merge(explicit_config_obj)
    
    return config


# 🏗️⚙️🪄