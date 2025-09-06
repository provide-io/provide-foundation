"""
Configuration schema and validation.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

from attrs import Attribute, define, fields

from provide.foundation.config.base import BaseConfig
from provide.foundation.config.types import ConfigDict
from provide.foundation.errors import ConfigValidationError


@define
class SchemaField:
    """Schema definition for a configuration field."""

    name: str
    type: type | None = None
    required: bool = False
    default: Any = None
    description: str | None = None
    validator: Callable[[Any], bool | Awaitable[bool]] | None = None
    choices: list[Any] | None = None
    min_value: Any = None
    max_value: Any = None
    pattern: str | None = None
    sensitive: bool = False

    async def validate(self, value: Any) -> None:
        """
        Validate a value against this schema field.

        Args:
            value: Value to validate

        Raises:
            ConfigValidationError: If validation fails
        """
        # Check required
        if self.required and value is None:
            raise ConfigValidationError(
                "Field is required", field=self.name, value=value
            )

        # Skip further validation for None values
        if value is None:
            return

        # Check type
        if self.type is not None and not isinstance(value, self.type):
            raise ConfigValidationError(
                f"Expected type {self.type.__name__}, got {type(value).__name__}",
                field=self.name,
                value=value,
            )

        # Check choices
        if self.choices is not None and value not in self.choices:
            raise ConfigValidationError(
                f"Value must be one of {self.choices}", field=self.name, value=value
            )

        # Check min/max
        if self.min_value is not None and value < self.min_value:
            raise ConfigValidationError(
                f"Value must be >= {self.min_value}", field=self.name, value=value
            )

        if self.max_value is not None and value > self.max_value:
            raise ConfigValidationError(
                f"Value must be <= {self.max_value}", field=self.name, value=value
            )

        # Check pattern
        if self.pattern is not None and isinstance(value, str):
            import re

            if not re.match(self.pattern, value):
                raise ConfigValidationError(
                    f"Value does not match pattern: {self.pattern}",
                    field=self.name,
                    value=value,
                )

        # Custom validator
        if self.validator is not None:
            try:
                result = self.validator(value)
                # Handle both sync and async validators
                if asyncio.iscoroutine(result) or asyncio.isfuture(result):
                    result = await result
                if not result:
                    raise ConfigValidationError(
                        "Custom validation failed", field=self.name, value=value
                    )
            except ConfigValidationError:
                raise
            except Exception as e:
                raise ConfigValidationError(
                    f"Validation error: {e}", field=self.name, value=value
                )


class ConfigSchema:
    """Schema definition for configuration classes."""

    def __init__(self, fields: list[SchemaField] | None = None) -> None:
        """
        Initialize configuration schema.

        Args:
            fields: List of schema fields
        """
        self.fields = fields or []
        self._field_map = {field.name: field for field in self.fields}

    def add_field(self, field: SchemaField) -> None:
        """Add a field to the schema."""
        self.fields.append(field)
        self._field_map[field.name] = field

    async def validate(self, data: ConfigDict) -> None:
        """
        Validate configuration data against schema.

        Args:
            data: Configuration data to validate

        Raises:
            ConfigValidationError: If validation fails
        """
        # Check required fields
        for field in self.fields:
            if field.required and field.name not in data:
                raise ConfigValidationError("Required field missing", field=field.name)

        # Validate each field
        for key, value in data.items():
            if key in self._field_map:
                await self._field_map[key].validate(value)

    def apply_defaults(self, data: ConfigDict) -> ConfigDict:
        """
        Apply default values to configuration data.

        Args:
            data: Configuration data

        Returns:
            Data with defaults applied
        """
        result = data.copy()

        for field in self.fields:
            if field.name not in result and field.default is not None:
                result[field.name] = field.default

        return result

    def filter_extra_fields(self, data: ConfigDict) -> ConfigDict:
        """
        Remove fields not defined in schema.

        Args:
            data: Configuration data

        Returns:
            Filtered data
        """
        return {k: v for k, v in data.items() if k in self._field_map}

    @classmethod
    def from_config_class(cls, config_class: type[BaseConfig]) -> ConfigSchema:
        """
        Generate schema from configuration class.

        Args:
            config_class: Configuration class

        Returns:
            Generated schema
        """
        schema_fields = []

        for attr in fields(config_class):
            schema_field = cls._attr_to_schema_field(attr)
            schema_fields.append(schema_field)

        return cls(schema_fields)

    @staticmethod
    def _attr_to_schema_field(attr: Attribute) -> SchemaField:
        """Convert attrs attribute to schema field."""
        # Determine if required
        required = attr.default is None and attr.factory is None

        # Get type from attribute
        field_type = getattr(attr, "type", None)

        # Extract metadata
        description = attr.metadata.get("description")
        sensitive = attr.metadata.get("sensitive", False)

        # Create schema field
        return SchemaField(
            name=attr.name,
            type=field_type,
            required=required,
            default=attr.default if attr.default is not None else None,
            description=description,
            sensitive=sensitive,
        )


async def validate_schema(config: BaseConfig, schema: ConfigSchema) -> None:
    """
    Validate configuration instance against schema.

    Args:
        config: Configuration instance
        schema: Schema to validate against

    Raises:
        ConfigValidationError: If validation fails
    """
    data = config.to_dict(include_sensitive=True)
    await schema.validate(data)


# Common validators (all sync since they're simple checks)
def validate_port(value: int) -> bool:
    """Validate port number."""
    return 1 <= value <= 65535


def validate_url(value: str) -> bool:
    """Validate URL format."""
    from urllib.parse import urlparse

    try:
        result = urlparse(value)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def validate_email(value: str) -> bool:
    """Validate email format."""
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, value))


def validate_path(value: str) -> bool:
    """Validate file path."""
    from pathlib import Path

    try:
        Path(value)
        return True
    except Exception:
        return False


def validate_version(value: str) -> bool:
    """Validate semantic version."""
    import re

    pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$"
    return bool(re.match(pattern, value))


# Example async validator for complex checks
async def validate_url_accessible(value: str) -> bool:
    """Validate URL is accessible (example async validator)."""
    # This is just an example - in real use you'd use aiohttp or similar
    # For now, just do basic URL validation
    return validate_url(value)
