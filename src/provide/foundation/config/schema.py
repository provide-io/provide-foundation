#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Configuration schema and validation."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from attrs import Attribute, define, fields

from provide.foundation.config.base import BaseConfig
from provide.foundation.config.types import ConfigDict
from provide.foundation.errors import ConfigValidationError


@define(slots=True)
class SchemaField:
    """Schema definition for a configuration field."""

    name: str
    field_type: type | None = None
    required: bool = False
    default: Any = None
    description: str | None = None
    validator: Callable[[Any], bool] | None = None
    choices: list[Any] | None = None
    min_value: Any = None
    max_value: Any = None
    pattern: str | None = None
    sensitive: bool = False
    env_var: str | None = None
    env_prefix: str | None = None
    env_parser: Callable[[str], Any] | None = None

    def _validate_required(self, value: Any) -> None:
        """Check required field validation."""
        if self.required and value is None:
            raise ConfigValidationError("Field is required", field=self.name, value=value)

    def _validate_type(self, value: Any) -> None:
        """Check type validation."""
        if self.field_type is not None and not isinstance(value, self.field_type):
            raise ConfigValidationError(
                f"Expected type {self.field_type.__name__}, got {type(value).__name__}",
                field=self.name,
                value=value,
            )

    def _validate_choices(self, value: Any) -> None:
        """Check choices validation."""
        if self.choices is not None and value not in self.choices:
            raise ConfigValidationError(f"Value must be one of {self.choices}", field=self.name, value=value)

    def _validate_range(self, value: Any) -> None:
        """Check min/max value validation."""
        if self.min_value is not None and value < self.min_value:
            raise ConfigValidationError(f"Value must be >= {self.min_value}", field=self.name, value=value)
        if self.max_value is not None and value > self.max_value:
            raise ConfigValidationError(f"Value must be <= {self.max_value}", field=self.name, value=value)

    def _validate_pattern(self, value: Any) -> None:
        """Check pattern validation."""
        if self.pattern is not None and isinstance(value, str):
            import re

            if not re.match(self.pattern, value):
                raise ConfigValidationError(
                    f"Value does not match pattern: {self.pattern}",
                    field=self.name,
                    value=value,
                )

    def _validate_custom(self, value: Any) -> None:
        """Check custom validator."""
        if self.validator is not None:
            try:
                result = self.validator(value)
                # Only support sync validators now
                if not result:
                    raise ConfigValidationError("Custom validation failed", field=self.name, value=value)
            except ConfigValidationError:
                raise
            except Exception as e:
                raise ConfigValidationError(f"Validation error: {e}", field=self.name, value=value) from e

    def validate(self, value: Any) -> None:
        """Validate a value against this schema field.

        Args:
            value: Value to validate

        Raises:
            ConfigValidationError: If validation fails

        """
        # Check required
        self._validate_required(value)

        # Skip further validation for None values
        if value is None:
            return

        # Run all validations
        self._validate_type(value)
        self._validate_choices(value)
        self._validate_range(value)
        self._validate_pattern(value)
        self._validate_custom(value)


class ConfigSchema:
    """Schema definition for configuration classes."""

    def __init__(self, fields: list[SchemaField] | None = None) -> None:
        """Initialize configuration schema.

        Args:
            fields: List of schema fields

        """
        self.fields = fields or []
        self._field_map = {field.name: field for field in self.fields}

    def add_field(self, field: SchemaField) -> None:
        """Add a field to the schema."""
        self.fields.append(field)
        self._field_map[field.name] = field

    def validate(self, data: ConfigDict) -> None:
        """Validate configuration data against schema.

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
                self._field_map[key].validate(value)

    def apply_defaults(self, data: ConfigDict) -> ConfigDict:
        """Apply default values to configuration data.

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
        """Remove fields not defined in schema.

        Args:
            data: Configuration data

        Returns:
            Filtered data

        """
        return {k: v for k, v in data.items() if k in self._field_map}

    @classmethod
    def from_config_class(cls, config_class: type[BaseConfig]) -> ConfigSchema:
        """Generate schema from configuration class.

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
        required = attr.default is None and getattr(attr, "factory", None) is None

        # Get type from attribute
        field_type = getattr(attr, "type", None)

        # Extract metadata
        description = attr.metadata.get("description")
        sensitive = attr.metadata.get("sensitive", False)
        env_var = attr.metadata.get("env_var")
        env_prefix = attr.metadata.get("env_prefix")
        env_parser = attr.metadata.get("env_parser")

        # Create schema field
        return SchemaField(
            name=attr.name,
            field_type=field_type,
            required=required,
            default=attr.default if attr.default is not None else None,
            description=description,
            sensitive=sensitive,
            env_var=env_var,
            env_prefix=env_prefix,
            env_parser=env_parser,
        )


def validate_schema(config: BaseConfig, schema: ConfigSchema) -> None:
    """Validate configuration instance against schema.

    Args:
        config: Configuration instance
        schema: Schema to validate against

    Raises:
        ConfigValidationError: If validation fails

    """
    data = config.to_dict(include_sensitive=True)
    schema.validate(data)


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
    except (ValueError, TypeError, AttributeError, Exception):
        # ValueError: Invalid URL format
        # TypeError: Non-string input
        # AttributeError: Missing required attributes
        # Exception: Any other parsing errors
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
    except (ValueError, TypeError, Exception):
        # ValueError: Invalid path characters or format
        # TypeError: Non-string input
        # Exception: Any other path creation errors
        return False


def validate_version(value: str) -> bool:
    """Validate semantic version."""
    import re

    pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$"
    return bool(re.match(pattern, value))


# Example async validator for complex checks
def validate_url_accessible(value: str) -> bool:
    """Validate URL is accessible (example async validator)."""
    # This is just an example - in real use you'd use aiohttp or similar
    # For now, just do basic URL validation
    return validate_url(value)


# 🧱🏗️🔚
