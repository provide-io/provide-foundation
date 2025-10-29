# provide/foundation/config/schema.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Configuration schema and validation."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from attrs import Attribute, define, fields

from provide.foundation.config.base import BaseConfig
from provide.foundation.config.types import ConfigDict
from provide.foundation.errors import ConfigValidationError
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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

    def xǁConfigSchemaǁ__init____mutmut_orig(self, fields: list[SchemaField] | None = None) -> None:
        """Initialize configuration schema.

        Args:
            fields: List of schema fields

        """
        self.fields = fields or []
        self._field_map = {field.name: field for field in self.fields}

    def xǁConfigSchemaǁ__init____mutmut_1(self, fields: list[SchemaField] | None = None) -> None:
        """Initialize configuration schema.

        Args:
            fields: List of schema fields

        """
        self.fields = None
        self._field_map = {field.name: field for field in self.fields}

    def xǁConfigSchemaǁ__init____mutmut_2(self, fields: list[SchemaField] | None = None) -> None:
        """Initialize configuration schema.

        Args:
            fields: List of schema fields

        """
        self.fields = fields and []
        self._field_map = {field.name: field for field in self.fields}

    def xǁConfigSchemaǁ__init____mutmut_3(self, fields: list[SchemaField] | None = None) -> None:
        """Initialize configuration schema.

        Args:
            fields: List of schema fields

        """
        self.fields = fields or []
        self._field_map = None

    xǁConfigSchemaǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigSchemaǁ__init____mutmut_1": xǁConfigSchemaǁ__init____mutmut_1,
        "xǁConfigSchemaǁ__init____mutmut_2": xǁConfigSchemaǁ__init____mutmut_2,
        "xǁConfigSchemaǁ__init____mutmut_3": xǁConfigSchemaǁ__init____mutmut_3,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigSchemaǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁConfigSchemaǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁConfigSchemaǁ__init____mutmut_orig)
    xǁConfigSchemaǁ__init____mutmut_orig.__name__ = "xǁConfigSchemaǁ__init__"

    def xǁConfigSchemaǁadd_field__mutmut_orig(self, field: SchemaField) -> None:
        """Add a field to the schema."""
        self.fields.append(field)
        self._field_map[field.name] = field

    def xǁConfigSchemaǁadd_field__mutmut_1(self, field: SchemaField) -> None:
        """Add a field to the schema."""
        self.fields.append(None)
        self._field_map[field.name] = field

    def xǁConfigSchemaǁadd_field__mutmut_2(self, field: SchemaField) -> None:
        """Add a field to the schema."""
        self.fields.append(field)
        self._field_map[field.name] = None

    xǁConfigSchemaǁadd_field__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigSchemaǁadd_field__mutmut_1": xǁConfigSchemaǁadd_field__mutmut_1,
        "xǁConfigSchemaǁadd_field__mutmut_2": xǁConfigSchemaǁadd_field__mutmut_2,
    }

    def add_field(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigSchemaǁadd_field__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigSchemaǁadd_field__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    add_field.__signature__ = _mutmut_signature(xǁConfigSchemaǁadd_field__mutmut_orig)
    xǁConfigSchemaǁadd_field__mutmut_orig.__name__ = "xǁConfigSchemaǁadd_field"

    def xǁConfigSchemaǁvalidate__mutmut_orig(self, data: ConfigDict) -> None:
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

    def xǁConfigSchemaǁvalidate__mutmut_1(self, data: ConfigDict) -> None:
        """Validate configuration data against schema.

        Args:
            data: Configuration data to validate

        Raises:
            ConfigValidationError: If validation fails

        """
        # Check required fields
        for field in self.fields:
            if field.required or field.name not in data:
                raise ConfigValidationError("Required field missing", field=field.name)

        # Validate each field
        for key, value in data.items():
            if key in self._field_map:
                self._field_map[key].validate(value)

    def xǁConfigSchemaǁvalidate__mutmut_2(self, data: ConfigDict) -> None:
        """Validate configuration data against schema.

        Args:
            data: Configuration data to validate

        Raises:
            ConfigValidationError: If validation fails

        """
        # Check required fields
        for field in self.fields:
            if field.required and field.name in data:
                raise ConfigValidationError("Required field missing", field=field.name)

        # Validate each field
        for key, value in data.items():
            if key in self._field_map:
                self._field_map[key].validate(value)

    def xǁConfigSchemaǁvalidate__mutmut_3(self, data: ConfigDict) -> None:
        """Validate configuration data against schema.

        Args:
            data: Configuration data to validate

        Raises:
            ConfigValidationError: If validation fails

        """
        # Check required fields
        for field in self.fields:
            if field.required and field.name not in data:
                raise ConfigValidationError(None, field=field.name)

        # Validate each field
        for key, value in data.items():
            if key in self._field_map:
                self._field_map[key].validate(value)

    def xǁConfigSchemaǁvalidate__mutmut_4(self, data: ConfigDict) -> None:
        """Validate configuration data against schema.

        Args:
            data: Configuration data to validate

        Raises:
            ConfigValidationError: If validation fails

        """
        # Check required fields
        for field in self.fields:
            if field.required and field.name not in data:
                raise ConfigValidationError("Required field missing", field=None)

        # Validate each field
        for key, value in data.items():
            if key in self._field_map:
                self._field_map[key].validate(value)

    def xǁConfigSchemaǁvalidate__mutmut_5(self, data: ConfigDict) -> None:
        """Validate configuration data against schema.

        Args:
            data: Configuration data to validate

        Raises:
            ConfigValidationError: If validation fails

        """
        # Check required fields
        for field in self.fields:
            if field.required and field.name not in data:
                raise ConfigValidationError(field=field.name)

        # Validate each field
        for key, value in data.items():
            if key in self._field_map:
                self._field_map[key].validate(value)

    def xǁConfigSchemaǁvalidate__mutmut_6(self, data: ConfigDict) -> None:
        """Validate configuration data against schema.

        Args:
            data: Configuration data to validate

        Raises:
            ConfigValidationError: If validation fails

        """
        # Check required fields
        for field in self.fields:
            if field.required and field.name not in data:
                raise ConfigValidationError(
                    "Required field missing",
                )

        # Validate each field
        for key, value in data.items():
            if key in self._field_map:
                self._field_map[key].validate(value)

    def xǁConfigSchemaǁvalidate__mutmut_7(self, data: ConfigDict) -> None:
        """Validate configuration data against schema.

        Args:
            data: Configuration data to validate

        Raises:
            ConfigValidationError: If validation fails

        """
        # Check required fields
        for field in self.fields:
            if field.required and field.name not in data:
                raise ConfigValidationError("XXRequired field missingXX", field=field.name)

        # Validate each field
        for key, value in data.items():
            if key in self._field_map:
                self._field_map[key].validate(value)

    def xǁConfigSchemaǁvalidate__mutmut_8(self, data: ConfigDict) -> None:
        """Validate configuration data against schema.

        Args:
            data: Configuration data to validate

        Raises:
            ConfigValidationError: If validation fails

        """
        # Check required fields
        for field in self.fields:
            if field.required and field.name not in data:
                raise ConfigValidationError("required field missing", field=field.name)

        # Validate each field
        for key, value in data.items():
            if key in self._field_map:
                self._field_map[key].validate(value)

    def xǁConfigSchemaǁvalidate__mutmut_9(self, data: ConfigDict) -> None:
        """Validate configuration data against schema.

        Args:
            data: Configuration data to validate

        Raises:
            ConfigValidationError: If validation fails

        """
        # Check required fields
        for field in self.fields:
            if field.required and field.name not in data:
                raise ConfigValidationError("REQUIRED FIELD MISSING", field=field.name)

        # Validate each field
        for key, value in data.items():
            if key in self._field_map:
                self._field_map[key].validate(value)

    def xǁConfigSchemaǁvalidate__mutmut_10(self, data: ConfigDict) -> None:
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
            if key not in self._field_map:
                self._field_map[key].validate(value)

    def xǁConfigSchemaǁvalidate__mutmut_11(self, data: ConfigDict) -> None:
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
                self._field_map[key].validate(None)

    xǁConfigSchemaǁvalidate__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigSchemaǁvalidate__mutmut_1": xǁConfigSchemaǁvalidate__mutmut_1,
        "xǁConfigSchemaǁvalidate__mutmut_2": xǁConfigSchemaǁvalidate__mutmut_2,
        "xǁConfigSchemaǁvalidate__mutmut_3": xǁConfigSchemaǁvalidate__mutmut_3,
        "xǁConfigSchemaǁvalidate__mutmut_4": xǁConfigSchemaǁvalidate__mutmut_4,
        "xǁConfigSchemaǁvalidate__mutmut_5": xǁConfigSchemaǁvalidate__mutmut_5,
        "xǁConfigSchemaǁvalidate__mutmut_6": xǁConfigSchemaǁvalidate__mutmut_6,
        "xǁConfigSchemaǁvalidate__mutmut_7": xǁConfigSchemaǁvalidate__mutmut_7,
        "xǁConfigSchemaǁvalidate__mutmut_8": xǁConfigSchemaǁvalidate__mutmut_8,
        "xǁConfigSchemaǁvalidate__mutmut_9": xǁConfigSchemaǁvalidate__mutmut_9,
        "xǁConfigSchemaǁvalidate__mutmut_10": xǁConfigSchemaǁvalidate__mutmut_10,
        "xǁConfigSchemaǁvalidate__mutmut_11": xǁConfigSchemaǁvalidate__mutmut_11,
    }

    def validate(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigSchemaǁvalidate__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigSchemaǁvalidate__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    validate.__signature__ = _mutmut_signature(xǁConfigSchemaǁvalidate__mutmut_orig)
    xǁConfigSchemaǁvalidate__mutmut_orig.__name__ = "xǁConfigSchemaǁvalidate"

    def xǁConfigSchemaǁapply_defaults__mutmut_orig(self, data: ConfigDict) -> ConfigDict:
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

    def xǁConfigSchemaǁapply_defaults__mutmut_1(self, data: ConfigDict) -> ConfigDict:
        """Apply default values to configuration data.

        Args:
            data: Configuration data

        Returns:
            Data with defaults applied

        """
        result = None

        for field in self.fields:
            if field.name not in result and field.default is not None:
                result[field.name] = field.default

        return result

    def xǁConfigSchemaǁapply_defaults__mutmut_2(self, data: ConfigDict) -> ConfigDict:
        """Apply default values to configuration data.

        Args:
            data: Configuration data

        Returns:
            Data with defaults applied

        """
        result = data.copy()

        for field in self.fields:
            if field.name not in result or field.default is not None:
                result[field.name] = field.default

        return result

    def xǁConfigSchemaǁapply_defaults__mutmut_3(self, data: ConfigDict) -> ConfigDict:
        """Apply default values to configuration data.

        Args:
            data: Configuration data

        Returns:
            Data with defaults applied

        """
        result = data.copy()

        for field in self.fields:
            if field.name in result and field.default is not None:
                result[field.name] = field.default

        return result

    def xǁConfigSchemaǁapply_defaults__mutmut_4(self, data: ConfigDict) -> ConfigDict:
        """Apply default values to configuration data.

        Args:
            data: Configuration data

        Returns:
            Data with defaults applied

        """
        result = data.copy()

        for field in self.fields:
            if field.name not in result and field.default is None:
                result[field.name] = field.default

        return result

    def xǁConfigSchemaǁapply_defaults__mutmut_5(self, data: ConfigDict) -> ConfigDict:
        """Apply default values to configuration data.

        Args:
            data: Configuration data

        Returns:
            Data with defaults applied

        """
        result = data.copy()

        for field in self.fields:
            if field.name not in result and field.default is not None:
                result[field.name] = None

        return result

    xǁConfigSchemaǁapply_defaults__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigSchemaǁapply_defaults__mutmut_1": xǁConfigSchemaǁapply_defaults__mutmut_1,
        "xǁConfigSchemaǁapply_defaults__mutmut_2": xǁConfigSchemaǁapply_defaults__mutmut_2,
        "xǁConfigSchemaǁapply_defaults__mutmut_3": xǁConfigSchemaǁapply_defaults__mutmut_3,
        "xǁConfigSchemaǁapply_defaults__mutmut_4": xǁConfigSchemaǁapply_defaults__mutmut_4,
        "xǁConfigSchemaǁapply_defaults__mutmut_5": xǁConfigSchemaǁapply_defaults__mutmut_5,
    }

    def apply_defaults(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigSchemaǁapply_defaults__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigSchemaǁapply_defaults__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    apply_defaults.__signature__ = _mutmut_signature(xǁConfigSchemaǁapply_defaults__mutmut_orig)
    xǁConfigSchemaǁapply_defaults__mutmut_orig.__name__ = "xǁConfigSchemaǁapply_defaults"

    def xǁConfigSchemaǁfilter_extra_fields__mutmut_orig(self, data: ConfigDict) -> ConfigDict:
        """Remove fields not defined in schema.

        Args:
            data: Configuration data

        Returns:
            Filtered data

        """
        return {k: v for k, v in data.items() if k in self._field_map}

    def xǁConfigSchemaǁfilter_extra_fields__mutmut_1(self, data: ConfigDict) -> ConfigDict:
        """Remove fields not defined in schema.

        Args:
            data: Configuration data

        Returns:
            Filtered data

        """
        return {k: v for k, v in data.items() if k not in self._field_map}

    xǁConfigSchemaǁfilter_extra_fields__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁConfigSchemaǁfilter_extra_fields__mutmut_1": xǁConfigSchemaǁfilter_extra_fields__mutmut_1
    }

    def filter_extra_fields(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁConfigSchemaǁfilter_extra_fields__mutmut_orig"),
            object.__getattribute__(self, "xǁConfigSchemaǁfilter_extra_fields__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    filter_extra_fields.__signature__ = _mutmut_signature(xǁConfigSchemaǁfilter_extra_fields__mutmut_orig)
    xǁConfigSchemaǁfilter_extra_fields__mutmut_orig.__name__ = "xǁConfigSchemaǁfilter_extra_fields"

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


def x_validate_schema__mutmut_orig(config: BaseConfig, schema: ConfigSchema) -> None:
    """Validate configuration instance against schema.

    Args:
        config: Configuration instance
        schema: Schema to validate against

    Raises:
        ConfigValidationError: If validation fails

    """
    data = config.to_dict(include_sensitive=True)
    schema.validate(data)


def x_validate_schema__mutmut_1(config: BaseConfig, schema: ConfigSchema) -> None:
    """Validate configuration instance against schema.

    Args:
        config: Configuration instance
        schema: Schema to validate against

    Raises:
        ConfigValidationError: If validation fails

    """
    data = None
    schema.validate(data)


def x_validate_schema__mutmut_2(config: BaseConfig, schema: ConfigSchema) -> None:
    """Validate configuration instance against schema.

    Args:
        config: Configuration instance
        schema: Schema to validate against

    Raises:
        ConfigValidationError: If validation fails

    """
    data = config.to_dict(include_sensitive=None)
    schema.validate(data)


def x_validate_schema__mutmut_3(config: BaseConfig, schema: ConfigSchema) -> None:
    """Validate configuration instance against schema.

    Args:
        config: Configuration instance
        schema: Schema to validate against

    Raises:
        ConfigValidationError: If validation fails

    """
    data = config.to_dict(include_sensitive=False)
    schema.validate(data)


def x_validate_schema__mutmut_4(config: BaseConfig, schema: ConfigSchema) -> None:
    """Validate configuration instance against schema.

    Args:
        config: Configuration instance
        schema: Schema to validate against

    Raises:
        ConfigValidationError: If validation fails

    """
    data = config.to_dict(include_sensitive=True)
    schema.validate(None)


x_validate_schema__mutmut_mutants: ClassVar[MutantDict] = {
    "x_validate_schema__mutmut_1": x_validate_schema__mutmut_1,
    "x_validate_schema__mutmut_2": x_validate_schema__mutmut_2,
    "x_validate_schema__mutmut_3": x_validate_schema__mutmut_3,
    "x_validate_schema__mutmut_4": x_validate_schema__mutmut_4,
}


def validate_schema(*args, **kwargs):
    result = _mutmut_trampoline(
        x_validate_schema__mutmut_orig, x_validate_schema__mutmut_mutants, args, kwargs
    )
    return result


validate_schema.__signature__ = _mutmut_signature(x_validate_schema__mutmut_orig)
x_validate_schema__mutmut_orig.__name__ = "x_validate_schema"


# Common validators (all sync since they're simple checks)
def x_validate_port__mutmut_orig(value: int) -> bool:
    """Validate port number."""
    return 1 <= value <= 65535


# Common validators (all sync since they're simple checks)
def x_validate_port__mutmut_1(value: int) -> bool:
    """Validate port number."""
    return 2 <= value <= 65535


# Common validators (all sync since they're simple checks)
def x_validate_port__mutmut_2(value: int) -> bool:
    """Validate port number."""
    return 1 < value <= 65535


# Common validators (all sync since they're simple checks)
def x_validate_port__mutmut_3(value: int) -> bool:
    """Validate port number."""
    return 1 <= value < 65535


# Common validators (all sync since they're simple checks)
def x_validate_port__mutmut_4(value: int) -> bool:
    """Validate port number."""
    return 1 <= value <= 65536


x_validate_port__mutmut_mutants: ClassVar[MutantDict] = {
    "x_validate_port__mutmut_1": x_validate_port__mutmut_1,
    "x_validate_port__mutmut_2": x_validate_port__mutmut_2,
    "x_validate_port__mutmut_3": x_validate_port__mutmut_3,
    "x_validate_port__mutmut_4": x_validate_port__mutmut_4,
}


def validate_port(*args, **kwargs):
    result = _mutmut_trampoline(x_validate_port__mutmut_orig, x_validate_port__mutmut_mutants, args, kwargs)
    return result


validate_port.__signature__ = _mutmut_signature(x_validate_port__mutmut_orig)
x_validate_port__mutmut_orig.__name__ = "x_validate_port"


def x_validate_url__mutmut_orig(value: str) -> bool:
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


def x_validate_url__mutmut_1(value: str) -> bool:
    """Validate URL format."""
    from urllib.parse import urlparse

    try:
        result = None
        return all([result.scheme, result.netloc])
    except (ValueError, TypeError, AttributeError, Exception):
        # ValueError: Invalid URL format
        # TypeError: Non-string input
        # AttributeError: Missing required attributes
        # Exception: Any other parsing errors
        return False


def x_validate_url__mutmut_2(value: str) -> bool:
    """Validate URL format."""
    from urllib.parse import urlparse

    try:
        result = urlparse(None)
        return all([result.scheme, result.netloc])
    except (ValueError, TypeError, AttributeError, Exception):
        # ValueError: Invalid URL format
        # TypeError: Non-string input
        # AttributeError: Missing required attributes
        # Exception: Any other parsing errors
        return False


def x_validate_url__mutmut_3(value: str) -> bool:
    """Validate URL format."""
    from urllib.parse import urlparse

    try:
        result = urlparse(value)
        return all(None)
    except (ValueError, TypeError, AttributeError, Exception):
        # ValueError: Invalid URL format
        # TypeError: Non-string input
        # AttributeError: Missing required attributes
        # Exception: Any other parsing errors
        return False


def x_validate_url__mutmut_4(value: str) -> bool:
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
        return True


x_validate_url__mutmut_mutants: ClassVar[MutantDict] = {
    "x_validate_url__mutmut_1": x_validate_url__mutmut_1,
    "x_validate_url__mutmut_2": x_validate_url__mutmut_2,
    "x_validate_url__mutmut_3": x_validate_url__mutmut_3,
    "x_validate_url__mutmut_4": x_validate_url__mutmut_4,
}


def validate_url(*args, **kwargs):
    result = _mutmut_trampoline(x_validate_url__mutmut_orig, x_validate_url__mutmut_mutants, args, kwargs)
    return result


validate_url.__signature__ = _mutmut_signature(x_validate_url__mutmut_orig)
x_validate_url__mutmut_orig.__name__ = "x_validate_url"


def x_validate_email__mutmut_orig(value: str) -> bool:
    """Validate email format."""
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, value))


def x_validate_email__mutmut_1(value: str) -> bool:
    """Validate email format."""
    import re

    pattern = None
    return bool(re.match(pattern, value))


def x_validate_email__mutmut_2(value: str) -> bool:
    """Validate email format."""
    import re

    pattern = r"XX^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$XX"
    return bool(re.match(pattern, value))


def x_validate_email__mutmut_3(value: str) -> bool:
    """Validate email format."""
    import re

    pattern = r"^[a-za-z0-9._%+-]+@[a-za-z0-9.-]+\.[a-za-z]{2,}$"
    return bool(re.match(pattern, value))


def x_validate_email__mutmut_4(value: str) -> bool:
    """Validate email format."""
    import re

    pattern = r"^[A-ZA-Z0-9._%+-]+@[A-ZA-Z0-9.-]+\.[A-ZA-Z]{2,}$"
    return bool(re.match(pattern, value))


def x_validate_email__mutmut_5(value: str) -> bool:
    """Validate email format."""
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(None)


def x_validate_email__mutmut_6(value: str) -> bool:
    """Validate email format."""
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(None, value))


def x_validate_email__mutmut_7(value: str) -> bool:
    """Validate email format."""
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, None))


def x_validate_email__mutmut_8(value: str) -> bool:
    """Validate email format."""
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(value))


def x_validate_email__mutmut_9(value: str) -> bool:
    """Validate email format."""
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(
        re.match(
            pattern,
        )
    )


x_validate_email__mutmut_mutants: ClassVar[MutantDict] = {
    "x_validate_email__mutmut_1": x_validate_email__mutmut_1,
    "x_validate_email__mutmut_2": x_validate_email__mutmut_2,
    "x_validate_email__mutmut_3": x_validate_email__mutmut_3,
    "x_validate_email__mutmut_4": x_validate_email__mutmut_4,
    "x_validate_email__mutmut_5": x_validate_email__mutmut_5,
    "x_validate_email__mutmut_6": x_validate_email__mutmut_6,
    "x_validate_email__mutmut_7": x_validate_email__mutmut_7,
    "x_validate_email__mutmut_8": x_validate_email__mutmut_8,
    "x_validate_email__mutmut_9": x_validate_email__mutmut_9,
}


def validate_email(*args, **kwargs):
    result = _mutmut_trampoline(x_validate_email__mutmut_orig, x_validate_email__mutmut_mutants, args, kwargs)
    return result


validate_email.__signature__ = _mutmut_signature(x_validate_email__mutmut_orig)
x_validate_email__mutmut_orig.__name__ = "x_validate_email"


def x_validate_path__mutmut_orig(value: str) -> bool:
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


def x_validate_path__mutmut_1(value: str) -> bool:
    """Validate file path."""
    from pathlib import Path

    try:
        Path(None)
        return True
    except (ValueError, TypeError, Exception):
        # ValueError: Invalid path characters or format
        # TypeError: Non-string input
        # Exception: Any other path creation errors
        return False


def x_validate_path__mutmut_2(value: str) -> bool:
    """Validate file path."""
    from pathlib import Path

    try:
        Path(value)
        return False
    except (ValueError, TypeError, Exception):
        # ValueError: Invalid path characters or format
        # TypeError: Non-string input
        # Exception: Any other path creation errors
        return False


def x_validate_path__mutmut_3(value: str) -> bool:
    """Validate file path."""
    from pathlib import Path

    try:
        Path(value)
        return True
    except (ValueError, TypeError, Exception):
        # ValueError: Invalid path characters or format
        # TypeError: Non-string input
        # Exception: Any other path creation errors
        return True


x_validate_path__mutmut_mutants: ClassVar[MutantDict] = {
    "x_validate_path__mutmut_1": x_validate_path__mutmut_1,
    "x_validate_path__mutmut_2": x_validate_path__mutmut_2,
    "x_validate_path__mutmut_3": x_validate_path__mutmut_3,
}


def validate_path(*args, **kwargs):
    result = _mutmut_trampoline(x_validate_path__mutmut_orig, x_validate_path__mutmut_mutants, args, kwargs)
    return result


validate_path.__signature__ = _mutmut_signature(x_validate_path__mutmut_orig)
x_validate_path__mutmut_orig.__name__ = "x_validate_path"


def x_validate_version__mutmut_orig(value: str) -> bool:
    """Validate semantic version."""
    import re

    pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$"
    return bool(re.match(pattern, value))


def x_validate_version__mutmut_1(value: str) -> bool:
    """Validate semantic version."""
    import re

    pattern = None
    return bool(re.match(pattern, value))


def x_validate_version__mutmut_2(value: str) -> bool:
    """Validate semantic version."""
    import re

    pattern = r"XX^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$XX"
    return bool(re.match(pattern, value))


def x_validate_version__mutmut_3(value: str) -> bool:
    """Validate semantic version."""
    import re

    pattern = r"^\d+\.\d+\.\d+(-[a-za-z0-9.-]+)?(\+[a-za-z0-9.-]+)?$"
    return bool(re.match(pattern, value))


def x_validate_version__mutmut_4(value: str) -> bool:
    """Validate semantic version."""
    import re

    pattern = r"^\d+\.\d+\.\d+(-[A-ZA-Z0-9.-]+)?(\+[A-ZA-Z0-9.-]+)?$"
    return bool(re.match(pattern, value))


def x_validate_version__mutmut_5(value: str) -> bool:
    """Validate semantic version."""
    import re

    pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$"
    return bool(None)


def x_validate_version__mutmut_6(value: str) -> bool:
    """Validate semantic version."""
    import re

    pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$"
    return bool(re.match(None, value))


def x_validate_version__mutmut_7(value: str) -> bool:
    """Validate semantic version."""
    import re

    pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$"
    return bool(re.match(pattern, None))


def x_validate_version__mutmut_8(value: str) -> bool:
    """Validate semantic version."""
    import re

    pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$"
    return bool(re.match(value))


def x_validate_version__mutmut_9(value: str) -> bool:
    """Validate semantic version."""
    import re

    pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$"
    return bool(
        re.match(
            pattern,
        )
    )


x_validate_version__mutmut_mutants: ClassVar[MutantDict] = {
    "x_validate_version__mutmut_1": x_validate_version__mutmut_1,
    "x_validate_version__mutmut_2": x_validate_version__mutmut_2,
    "x_validate_version__mutmut_3": x_validate_version__mutmut_3,
    "x_validate_version__mutmut_4": x_validate_version__mutmut_4,
    "x_validate_version__mutmut_5": x_validate_version__mutmut_5,
    "x_validate_version__mutmut_6": x_validate_version__mutmut_6,
    "x_validate_version__mutmut_7": x_validate_version__mutmut_7,
    "x_validate_version__mutmut_8": x_validate_version__mutmut_8,
    "x_validate_version__mutmut_9": x_validate_version__mutmut_9,
}


def validate_version(*args, **kwargs):
    result = _mutmut_trampoline(
        x_validate_version__mutmut_orig, x_validate_version__mutmut_mutants, args, kwargs
    )
    return result


validate_version.__signature__ = _mutmut_signature(x_validate_version__mutmut_orig)
x_validate_version__mutmut_orig.__name__ = "x_validate_version"


# Example async validator for complex checks
def x_validate_url_accessible__mutmut_orig(value: str) -> bool:
    """Validate URL is accessible (example async validator)."""
    # This is just an example - in real use you'd use aiohttp or similar
    # For now, just do basic URL validation
    return validate_url(value)


# Example async validator for complex checks
def x_validate_url_accessible__mutmut_1(value: str) -> bool:
    """Validate URL is accessible (example async validator)."""
    # This is just an example - in real use you'd use aiohttp or similar
    # For now, just do basic URL validation
    return validate_url(None)


x_validate_url_accessible__mutmut_mutants: ClassVar[MutantDict] = {
    "x_validate_url_accessible__mutmut_1": x_validate_url_accessible__mutmut_1
}


def validate_url_accessible(*args, **kwargs):
    result = _mutmut_trampoline(
        x_validate_url_accessible__mutmut_orig, x_validate_url_accessible__mutmut_mutants, args, kwargs
    )
    return result


validate_url_accessible.__signature__ = _mutmut_signature(x_validate_url_accessible__mutmut_orig)
x_validate_url_accessible__mutmut_orig.__name__ = "x_validate_url_accessible"


# <3 🧱🤝⚙️🪄
