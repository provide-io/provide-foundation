"""
Base configuration classes and utilities.
"""
import copy
from typing import Any, Callable, Dict, Optional, Type, TypeVar, get_type_hints

from attrs import NOTHING, Attribute, Factory, define, field as attrs_field, fields

from provide.foundation.config.types import ConfigDict, ConfigSource, ConfigValue

T = TypeVar("T")


class ConfigError(Exception):
    """Base exception for configuration errors."""
    pass


class ConfigValidationError(ConfigError):
    """Raised when configuration validation fails."""
    
    def __init__(self, field_name: str, value: Any, message: str):
        self.field_name = field_name
        self.value = value
        super().__init__(f"Validation error for field '{field_name}': {message}")


def field(
    *,
    default: Any = NOTHING,
    factory: Optional[Callable[[], Any]] = None,
    validator: Optional[Callable[[Any, Attribute, Any], None]] = None,
    converter: Optional[Callable[[Any], Any]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    description: Optional[str] = None,
    env_var: Optional[str] = None,
    env_prefix: Optional[str] = None,
    sensitive: bool = False,
    **kwargs
) -> Any:
    """
    Enhanced attrs field with configuration-specific metadata.
    
    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments
    """
    config_metadata = metadata or {}
    
    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive
    
    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=Factory(factory) if not isinstance(factory, Factory) else factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs
        )
    else:
        return attrs_field(
            default=default,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs
        )


@define
class BaseConfig:
    """
    Base configuration class with common functionality.
    
    All configuration classes should inherit from this.
    """
    
    def __attrs_post_init__(self):
        """Post-initialization hook for subclasses."""
        self._source_map: Dict[str, ConfigSource] = {}
        self._original_values: Dict[str, Any] = {}
        self.validate()
    
    def validate(self) -> None:
        """
        Validate the configuration.
        
        Override this method to add custom validation logic.
        """
        pass
    
    def to_dict(self, include_sensitive: bool = False) -> ConfigDict:
        """
        Convert configuration to dictionary.
        
        Args:
            include_sensitive: Whether to include sensitive fields
            
        Returns:
            Dictionary representation of the configuration
        """
        result = {}
        
        for attr in fields(self.__class__):
            value = getattr(self, attr.name)
            
            # Skip sensitive fields if requested
            if not include_sensitive and attr.metadata.get("sensitive", False):
                continue
            
            # Convert nested configs recursively
            if isinstance(value, BaseConfig):
                value = value.to_dict(include_sensitive)
            elif isinstance(value, dict):
                value = self._convert_dict_values(value, include_sensitive)
            elif isinstance(value, list):
                value = self._convert_list_values(value, include_sensitive)
            
            result[attr.name] = value
        
        return result
    
    def _convert_dict_values(self, d: Dict, include_sensitive: bool) -> Dict:
        """Convert dictionary values recursively."""
        result = {}
        for key, value in d.items():
            if isinstance(value, BaseConfig):
                value = value.to_dict(include_sensitive)
            elif isinstance(value, dict):
                value = self._convert_dict_values(value, include_sensitive)
            elif isinstance(value, list):
                value = self._convert_list_values(value, include_sensitive)
            result[key] = value
        return result
    
    def _convert_list_values(self, lst: list, include_sensitive: bool) -> list:
        """Convert list values recursively."""
        result = []
        for value in lst:
            if isinstance(value, BaseConfig):
                value = value.to_dict(include_sensitive)
            elif isinstance(value, dict):
                value = self._convert_dict_values(value, include_sensitive)
            elif isinstance(value, list):
                value = self._convert_list_values(value, include_sensitive)
            result.append(value)
        return result
    
    @classmethod
    def from_dict(cls: Type[T], data: ConfigDict, source: ConfigSource = ConfigSource.RUNTIME) -> T:
        """
        Create configuration from dictionary.
        
        Args:
            data: Configuration data
            source: Source of the configuration
            
        Returns:
            Configuration instance
        """
        # Filter data to only include fields defined in the class
        field_names = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in field_names}
        
        # Create instance
        instance = cls(**filtered_data)
        
        # Track sources
        for key in filtered_data:
            instance._source_map[key] = source
            instance._original_values[key] = filtered_data[key]
        
        return instance
    
    def update(self, updates: ConfigDict, source: ConfigSource = ConfigSource.RUNTIME) -> None:
        """
        Update configuration with new values.
        
        Args:
            updates: Dictionary of updates
            source: Source of the updates
        """
        for key, value in updates.items():
            if hasattr(self, key):
                # Only update if new source has higher precedence
                current_source = self._source_map.get(key, ConfigSource.DEFAULT)
                if source >= current_source:
                    setattr(self, key, value)
                    self._source_map[key] = source
                    self._original_values[key] = value
    
    def get_source(self, field_name: str) -> Optional[ConfigSource]:
        """
        Get the source of a configuration field.
        
        Args:
            field_name: Name of the field
            
        Returns:
            Source of the field value or None
        """
        return self._source_map.get(field_name)
    
    def reset_to_defaults(self) -> None:
        """Reset all fields to their default values."""
        for attr in fields(self.__class__):
            if attr.default != NOTHING:
                setattr(self, attr.name, attr.default)
            elif attr.factory != NOTHING:
                setattr(self, attr.name, attr.factory())
        
        self._source_map.clear()
        self._original_values.clear()
    
    def clone(self: T) -> T:
        """Create a deep copy of the configuration."""
        return copy.deepcopy(self)
    
    def diff(self, other: "BaseConfig") -> Dict[str, tuple[Any, Any]]:
        """
        Compare with another configuration.
        
        Args:
            other: Configuration to compare with
            
        Returns:
            Dictionary of differences (field_name: (self_value, other_value))
        """
        if not isinstance(other, self.__class__):
            raise TypeError(f"Cannot compare {self.__class__.__name__} with {other.__class__.__name__}")
        
        differences = {}
        
        for attr in fields(self.__class__):
            self_value = getattr(self, attr.name)
            other_value = getattr(other, attr.name)
            
            if self_value != other_value:
                differences[attr.name] = (self_value, other_value)
        
        return differences
    
    def __repr__(self) -> str:
        """String representation hiding sensitive fields."""
        parts = []
        for attr in fields(self.__class__):
            value = getattr(self, attr.name)
            
            # Hide sensitive values
            if attr.metadata.get("sensitive", False):
                value = "***SENSITIVE***"
            
            parts.append(f"{attr.name}={value!r}")
        
        return f"{self.__class__.__name__}({', '.join(parts)})"