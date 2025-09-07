"""
Base configuration classes and utilities.
"""

from __future__ import annotations

from collections.abc import Callable
import copy
from typing import Any, TypeVar

from attrs import NOTHING, Attribute, define, field as attrs_field, fields

from provide.foundation.config.types import ConfigDict, ConfigSource

T = TypeVar("T", bound="BaseConfig")


def field(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute, Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
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
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    else:
        return attrs_field(
            default=default,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )


@define(slots=True, repr=False)
class BaseConfig:
    """
    Base configuration class with common functionality.

    All configuration classes should inherit from this.
    All methods are async to support async validation and I/O operations.
    """

    # These are instance attributes that need to be defined outside of slots
    _source_map: dict[str, ConfigSource] = attrs_field(init=False, factory=lambda: {})
    _original_values: dict[str, Any] = attrs_field(init=False, factory=lambda: {})

    def __attrs_post_init__(self):
        """Post-initialization hook for subclasses."""
        # The _source_map and _original_values are now handled by attrs with factory
        # Note: validate() is now async, so we can't call it here
        # Users must explicitly call await config.validate() after creation
        pass

    async def validate(self) -> None:
        """
        Validate the configuration.

        Override this method to add custom validation logic.
        Can perform async operations like checking database connections.
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

    def _convert_dict_values(self, d: dict, include_sensitive: bool) -> dict:
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
    def from_dict(
        cls: type[T], data: ConfigDict, source: ConfigSource = ConfigSource.RUNTIME
    ) -> T:
        """
        Create configuration from dictionary.

        Args:
            data: Configuration data
            source: Source of the configuration

        Returns:
            Configuration instance
        """
        # Filter data to only include fields defined in the class, excluding private fields
        field_names = {f.name for f in fields(cls) if not f.name.startswith('_')}
        filtered_data = {k: v for k, v in data.items() if k in field_names}

        # Create instance
        instance = cls(**filtered_data)

        # Track sources
        for key in filtered_data:
            instance._source_map[key] = source
            instance._original_values[key] = filtered_data[key]

        return instance

    def update(
        self, updates: ConfigDict, source: ConfigSource = ConfigSource.RUNTIME
    ) -> None:
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

        # Note: validate() is async, must be called separately if needed

    def get_source(self, field_name: str) -> ConfigSource | None:
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
            # Skip internal fields
            if attr.name.startswith("_"):
                continue

            if attr.default != NOTHING:
                setattr(self, attr.name, attr.default)
            elif attr.factory != NOTHING:
                # attrs factory is always callable
                setattr(self, attr.name, attr.factory())

        self._source_map.clear()
        self._original_values.clear()

        # Note: validate() is async, must be called separately if needed

    def clone(self: T) -> T:
        """Create a deep copy of the configuration."""
        cloned = copy.deepcopy(self)
        # Note: validate() is async, must be called separately if needed
        return cloned

    def diff(self, other: BaseConfig) -> dict[str, tuple[Any, Any]]:
        """
        Compare with another configuration.

        Args:
            other: Configuration to compare with

        Returns:
            Dictionary of differences (field_name: (self_value, other_value))
        """
        if not isinstance(other, self.__class__):
            raise TypeError(
                f"Cannot compare {self.__class__.__name__} with {other.__class__.__name__}"
            )

        differences = {}

        for attr in fields(self.__class__):
            self_value = getattr(self, attr.name)
            other_value = getattr(other, attr.name)

            if self_value != other_value:
                differences[attr.name] = (self_value, other_value)

        return differences

    def __repr__(self) -> str:
        """String representation hiding sensitive fields."""
        # Get the actual attrs fields
        import attrs

        attr_fields = attrs.fields(self.__class__)

        parts = []
        for attr in attr_fields:
            # Skip internal fields
            if attr.name.startswith("_"):
                continue

            value = getattr(self, attr.name)

            # Hide sensitive values
            if attr.metadata.get("sensitive", False):
                value = "***SENSITIVE***"

            parts.append(f"{attr.name}={value!r}")

        return f"{self.__class__.__name__}({', '.join(parts)})"
