"""
Environment variable configuration utilities.
"""
import os
from typing import Any, Callable, TypeVar

from attrs import fields

from provide.foundation.config.base import BaseConfig, field
from provide.foundation.config.types import ConfigDict, ConfigSource

T = TypeVar("T")


def get_env(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True
) -> str | None:
    """
    Get environment variable value with optional file-based secret support.
    
    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets
        
    Returns:
        Environment variable value or default
        
    Raises:
        ValueError: If required and not found
    """
    value = os.environ.get(var_name)
    
    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{var_name}' not found")
        return default
    
    # Handle file-based secrets
    if secret_file and value.startswith("file://"):
        file_path = value[7:]  # Remove "file://" prefix
        try:
            with open(file_path, "r") as f:
                value = f.read().strip()
        except Exception as e:
            raise ValueError(f"Failed to read secret from file '{file_path}': {e}")
    
    return value


def parse_bool(value: str | bool) -> bool:
    """
    Parse boolean from string.
    
    Args:
        value: String or boolean value
        
    Returns:
        Boolean value
    """
    if isinstance(value, bool):
        return value
    
    if isinstance(value, str):
        value_lower = value.lower().strip()
        
        if value_lower in ("true", "1", "yes", "on", "enabled"):
            return True
        elif value_lower in ("false", "0", "no", "off", "disabled", ""):
            return False
    
    raise ValueError(f"Cannot parse boolean from: {value}")


def parse_list(
    value: str | list[str],
    separator: str = ",",
    strip: bool = True
) -> list[str]:
    """
    Parse list from string.
    
    Args:
        value: String or list value
        separator: List separator
        strip: Whether to strip whitespace from items
        
    Returns:
        List of strings
    """
    if isinstance(value, list):
        return value
    
    if not value:
        return []
    
    items = value.split(separator)
    
    if strip:
        items = [item.strip() for item in items]
        items = [item for item in items if item]  # Remove empty strings
    
    return items


def parse_dict(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_value_separator: str = "="
) -> dict[str, str]:
    """
    Parse dictionary from string.
    
    Args:
        value: String or dictionary value
        item_separator: Separator between items
        key_value_separator: Separator between key and value
        
    Returns:
        Dictionary
    """
    if isinstance(value, dict):
        return value
    
    if not value:
        return {}
    
    result = {}
    items = value.split(item_separator)
    
    for item in items:
        item = item.strip()
        if not item:
            continue
        
        if key_value_separator not in item:
            raise ValueError(f"Invalid key-value pair: {item}")
        
        key, val = item.split(key_value_separator, 1)
        result[key.strip()] = val.strip()
    
    return result


def env_field(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs
) -> Any:
    """
    Create a field that can be loaded from environment variables.
    
    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments
        
    Returns:
        Field descriptor
    """
    metadata = kwargs.pop("metadata", {})
    
    if env_var:
        metadata["env_var"] = env_var
    if env_prefix:
        metadata["env_prefix"] = env_prefix
    if parser:
        metadata["env_parser"] = parser
    
    return field(metadata=metadata, **kwargs)


class EnvConfig(BaseConfig):
    """
    Configuration that can be loaded from environment variables.
    """
    
    @classmethod
    def from_env(
        cls: type[T],
        prefix: str = "",
        delimiter: str = "_",
        case_sensitive: bool = False
    ) -> T:
        """
        Load configuration from environment variables.
        
        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name
            case_sensitive: Whether variable names are case-sensitive
            
        Returns:
            Configuration instance
        """
        data = {}
        
        for attr in fields(cls):
            # Determine environment variable name
            env_var = attr.metadata.get("env_var")
            
            if not env_var:
                # Build from prefix and field name
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper() if not case_sensitive else attr.name
                
                if field_prefix:
                    env_var = f"{field_prefix}{delimiter}{field_name}"
                else:
                    env_var = field_name
            
            # Get value from environment
            value = os.environ.get(env_var)
            
            if value is not None:
                # Apply parser if specified
                parser = attr.metadata.get("env_parser")
                
                if parser:
                    try:
                        value = parser(value)
                    except Exception as e:
                        raise ValueError(f"Failed to parse {env_var}: {e}")
                else:
                    # Try to infer parser from type
                    value = cls._auto_parse(attr, value)
                
                data[attr.name] = value
        
        return cls.from_dict(data, source=ConfigSource.ENV)
    
    @classmethod
    def _auto_parse(cls, attr: Any, value: str) -> Any:
        """
        Automatically parse value based on field type.
        
        Args:
            attr: Field attribute
            value: String value to parse
            
        Returns:
            Parsed value
        """
        # Get type hint if available
        if hasattr(attr, "type"):
            field_type = attr.type
            
            # Handle basic types
            if field_type == bool:
                return parse_bool(value)
            elif field_type == int:
                return int(value)
            elif field_type == float:
                return float(value)
            elif field_type == str:
                return value
            
            # Handle generic types
            origin = getattr(field_type, "__origin__", None)
            
            if origin == list:
                return parse_list(value)
            elif origin == dict:
                return parse_dict(value)
        
        # Default to string
        return value
    
    def to_env_dict(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
        """
        Convert configuration to environment variable dictionary.
        
        Args:
            prefix: Prefix for all environment variables
            delimiter: Delimiter between prefix and field name
            
        Returns:
            Dictionary of environment variables
        """
        env_dict = {}
        
        for attr in fields(self.__class__):
            value = getattr(self, attr.name)
            
            # Skip None values
            if value is None:
                continue
            
            # Determine environment variable name
            env_var = attr.metadata.get("env_var")
            
            if not env_var:
                field_prefix = attr.metadata.get("env_prefix", prefix)
                field_name = attr.name.upper()
                
                if field_prefix:
                    env_var = f"{field_prefix}{delimiter}{field_name}"
                else:
                    env_var = field_name
            
            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ",".join(str(item) for item in value)
            elif isinstance(value, dict):
                str_value = ",".join(f"{k}={v}" for k, v in value.items())
            else:
                str_value = str(value)
            
            env_dict[env_var] = str_value
        
        return env_dict