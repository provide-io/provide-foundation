# provide/foundation/config/discovery.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Configuration schema discovery system.

This module provides functionality to discover and introspect all configuration
classes registered with the Foundation Hub. It enables programmatic access to
configuration schemas, environment variable mappings, and metadata.
"""

from __future__ import annotations

from typing import Any

from attrs import define

from provide.foundation.config.base import BaseConfig
from provide.foundation.config.schema import ConfigSchema
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


@define(frozen=True, slots=True)
class EnvVarInfo:
    """Information about an environment variable and its configuration field.

    Attributes:
        config_class: Name of the configuration class
        field_name: Name of the field in the config class
        env_var: Environment variable name
        field_type: Type of the field
        default: Default value
        required: Whether the field is required
        description: Field description
        sensitive: Whether the field contains sensitive data
        category: Configuration category (e.g., "logger", "transport")

    """

    config_class: str
    field_name: str
    env_var: str
    field_type: str
    default: Any
    required: bool
    description: str | None
    sensitive: bool
    category: str


@define(slots=True)
class ConsolidatedSchema:
    """Consolidated schema containing all configuration schemas.

    Attributes:
        schemas: Mapping of config class names to their schemas
        metadata: Additional metadata about each config class

    """

    schemas: dict[str, ConfigSchema]
    metadata: dict[str, dict[str, Any]]

    def get_by_category(self, category: str) -> dict[str, ConfigSchema]:
        """Filter schemas by category.

        Args:
            category: Category to filter by (e.g., "logger", "transport")

        Returns:
            Filtered schemas matching the category

        """
        result = {}
        for name, schema in self.schemas.items():
            meta = self.metadata.get(name, {})
            if meta.get("category") == category:
                result[name] = schema
        return result

    def get_all_env_vars(self, show_sensitive: bool = False) -> list[EnvVarInfo]:
        """Extract all environment variables from all schemas.

        Args:
            show_sensitive: Whether to include sensitive fields

        Returns:
            List of environment variable information

        """
        env_vars = []

        for config_name, schema in self.schemas.items():
            meta = self.metadata.get(config_name, {})
            category = meta.get("category", "core")

            for field in schema.fields:
                # Skip if no env var mapping
                if not field.env_var:
                    continue

                # Skip sensitive fields unless explicitly requested
                if field.sensitive and not show_sensitive:
                    continue

                # Get type name
                type_name = "Any"
                if field.field_type is not None:
                    type_name = getattr(field.field_type, "__name__", str(field.field_type))

                env_vars.append(
                    EnvVarInfo(
                        config_class=config_name,
                        field_name=field.name,
                        env_var=field.env_var,
                        field_type=type_name,
                        default=field.default,
                        required=field.required,
                        description=field.description,
                        sensitive=field.sensitive,
                        category=category,
                    )
                )

        return env_vars

    def get_categories(self) -> set[str]:
        """Get all unique categories.

        Returns:
            Set of all categories

        """
        return {meta.get("category", "core") for meta in self.metadata.values()}


def x_discover_all_config_schemas__mutmut_orig() -> dict[str, type[BaseConfig]]:
    """Get all registered configuration schemas from the Hub.

    This function retrieves all configuration classes that have been
    registered with the Foundation Hub under the CONFIG_SCHEMA dimension.

    Returns:
        Mapping of config class names to their types

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = get_hub()

    # Get all entry names in the CONFIG_SCHEMA dimension
    config_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)

    # Retrieve each config class
    result = {}
    for name in config_names:
        entry = hub._component_registry.get_entry(name, ComponentCategory.CONFIG_SCHEMA.value)
        if entry:
            result[name] = entry.value

    return result


def x_discover_all_config_schemas__mutmut_1() -> dict[str, type[BaseConfig]]:
    """Get all registered configuration schemas from the Hub.

    This function retrieves all configuration classes that have been
    registered with the Foundation Hub under the CONFIG_SCHEMA dimension.

    Returns:
        Mapping of config class names to their types

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = None

    # Get all entry names in the CONFIG_SCHEMA dimension
    config_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)

    # Retrieve each config class
    result = {}
    for name in config_names:
        entry = hub._component_registry.get_entry(name, ComponentCategory.CONFIG_SCHEMA.value)
        if entry:
            result[name] = entry.value

    return result


def x_discover_all_config_schemas__mutmut_2() -> dict[str, type[BaseConfig]]:
    """Get all registered configuration schemas from the Hub.

    This function retrieves all configuration classes that have been
    registered with the Foundation Hub under the CONFIG_SCHEMA dimension.

    Returns:
        Mapping of config class names to their types

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = get_hub()

    # Get all entry names in the CONFIG_SCHEMA dimension
    config_names = None

    # Retrieve each config class
    result = {}
    for name in config_names:
        entry = hub._component_registry.get_entry(name, ComponentCategory.CONFIG_SCHEMA.value)
        if entry:
            result[name] = entry.value

    return result


def x_discover_all_config_schemas__mutmut_3() -> dict[str, type[BaseConfig]]:
    """Get all registered configuration schemas from the Hub.

    This function retrieves all configuration classes that have been
    registered with the Foundation Hub under the CONFIG_SCHEMA dimension.

    Returns:
        Mapping of config class names to their types

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = get_hub()

    # Get all entry names in the CONFIG_SCHEMA dimension
    config_names = hub._component_registry.list_dimension(None)

    # Retrieve each config class
    result = {}
    for name in config_names:
        entry = hub._component_registry.get_entry(name, ComponentCategory.CONFIG_SCHEMA.value)
        if entry:
            result[name] = entry.value

    return result


def x_discover_all_config_schemas__mutmut_4() -> dict[str, type[BaseConfig]]:
    """Get all registered configuration schemas from the Hub.

    This function retrieves all configuration classes that have been
    registered with the Foundation Hub under the CONFIG_SCHEMA dimension.

    Returns:
        Mapping of config class names to their types

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = get_hub()

    # Get all entry names in the CONFIG_SCHEMA dimension
    config_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)

    # Retrieve each config class
    result = None
    for name in config_names:
        entry = hub._component_registry.get_entry(name, ComponentCategory.CONFIG_SCHEMA.value)
        if entry:
            result[name] = entry.value

    return result


def x_discover_all_config_schemas__mutmut_5() -> dict[str, type[BaseConfig]]:
    """Get all registered configuration schemas from the Hub.

    This function retrieves all configuration classes that have been
    registered with the Foundation Hub under the CONFIG_SCHEMA dimension.

    Returns:
        Mapping of config class names to their types

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = get_hub()

    # Get all entry names in the CONFIG_SCHEMA dimension
    config_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)

    # Retrieve each config class
    result = {}
    for name in config_names:
        entry = None
        if entry:
            result[name] = entry.value

    return result


def x_discover_all_config_schemas__mutmut_6() -> dict[str, type[BaseConfig]]:
    """Get all registered configuration schemas from the Hub.

    This function retrieves all configuration classes that have been
    registered with the Foundation Hub under the CONFIG_SCHEMA dimension.

    Returns:
        Mapping of config class names to their types

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = get_hub()

    # Get all entry names in the CONFIG_SCHEMA dimension
    config_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)

    # Retrieve each config class
    result = {}
    for name in config_names:
        entry = hub._component_registry.get_entry(None, ComponentCategory.CONFIG_SCHEMA.value)
        if entry:
            result[name] = entry.value

    return result


def x_discover_all_config_schemas__mutmut_7() -> dict[str, type[BaseConfig]]:
    """Get all registered configuration schemas from the Hub.

    This function retrieves all configuration classes that have been
    registered with the Foundation Hub under the CONFIG_SCHEMA dimension.

    Returns:
        Mapping of config class names to their types

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = get_hub()

    # Get all entry names in the CONFIG_SCHEMA dimension
    config_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)

    # Retrieve each config class
    result = {}
    for name in config_names:
        entry = hub._component_registry.get_entry(name, None)
        if entry:
            result[name] = entry.value

    return result


def x_discover_all_config_schemas__mutmut_8() -> dict[str, type[BaseConfig]]:
    """Get all registered configuration schemas from the Hub.

    This function retrieves all configuration classes that have been
    registered with the Foundation Hub under the CONFIG_SCHEMA dimension.

    Returns:
        Mapping of config class names to their types

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = get_hub()

    # Get all entry names in the CONFIG_SCHEMA dimension
    config_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)

    # Retrieve each config class
    result = {}
    for name in config_names:
        entry = hub._component_registry.get_entry(ComponentCategory.CONFIG_SCHEMA.value)
        if entry:
            result[name] = entry.value

    return result


def x_discover_all_config_schemas__mutmut_9() -> dict[str, type[BaseConfig]]:
    """Get all registered configuration schemas from the Hub.

    This function retrieves all configuration classes that have been
    registered with the Foundation Hub under the CONFIG_SCHEMA dimension.

    Returns:
        Mapping of config class names to their types

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = get_hub()

    # Get all entry names in the CONFIG_SCHEMA dimension
    config_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)

    # Retrieve each config class
    result = {}
    for name in config_names:
        entry = hub._component_registry.get_entry(
            name,
        )
        if entry:
            result[name] = entry.value

    return result


def x_discover_all_config_schemas__mutmut_10() -> dict[str, type[BaseConfig]]:
    """Get all registered configuration schemas from the Hub.

    This function retrieves all configuration classes that have been
    registered with the Foundation Hub under the CONFIG_SCHEMA dimension.

    Returns:
        Mapping of config class names to their types

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = get_hub()

    # Get all entry names in the CONFIG_SCHEMA dimension
    config_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)

    # Retrieve each config class
    result = {}
    for name in config_names:
        entry = hub._component_registry.get_entry(name, ComponentCategory.CONFIG_SCHEMA.value)
        if entry:
            result[name] = None

    return result


x_discover_all_config_schemas__mutmut_mutants: ClassVar[MutantDict] = {
    "x_discover_all_config_schemas__mutmut_1": x_discover_all_config_schemas__mutmut_1,
    "x_discover_all_config_schemas__mutmut_2": x_discover_all_config_schemas__mutmut_2,
    "x_discover_all_config_schemas__mutmut_3": x_discover_all_config_schemas__mutmut_3,
    "x_discover_all_config_schemas__mutmut_4": x_discover_all_config_schemas__mutmut_4,
    "x_discover_all_config_schemas__mutmut_5": x_discover_all_config_schemas__mutmut_5,
    "x_discover_all_config_schemas__mutmut_6": x_discover_all_config_schemas__mutmut_6,
    "x_discover_all_config_schemas__mutmut_7": x_discover_all_config_schemas__mutmut_7,
    "x_discover_all_config_schemas__mutmut_8": x_discover_all_config_schemas__mutmut_8,
    "x_discover_all_config_schemas__mutmut_9": x_discover_all_config_schemas__mutmut_9,
    "x_discover_all_config_schemas__mutmut_10": x_discover_all_config_schemas__mutmut_10,
}


def discover_all_config_schemas(*args, **kwargs):
    result = _mutmut_trampoline(
        x_discover_all_config_schemas__mutmut_orig, x_discover_all_config_schemas__mutmut_mutants, args, kwargs
    )
    return result


discover_all_config_schemas.__signature__ = _mutmut_signature(x_discover_all_config_schemas__mutmut_orig)
x_discover_all_config_schemas__mutmut_orig.__name__ = "x_discover_all_config_schemas"


def x_get_config_metadata__mutmut_orig() -> dict[str, dict[str, Any]]:
    """Get metadata for all registered config schemas.

    Returns:
        Mapping of config class names to their metadata

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = get_hub()

    config_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)

    result = {}
    for name in config_names:
        entry = hub._component_registry.get_entry(name, ComponentCategory.CONFIG_SCHEMA.value)
        if entry:
            result[name] = entry.metadata

    return result


def x_get_config_metadata__mutmut_1() -> dict[str, dict[str, Any]]:
    """Get metadata for all registered config schemas.

    Returns:
        Mapping of config class names to their metadata

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = None

    config_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)

    result = {}
    for name in config_names:
        entry = hub._component_registry.get_entry(name, ComponentCategory.CONFIG_SCHEMA.value)
        if entry:
            result[name] = entry.metadata

    return result


def x_get_config_metadata__mutmut_2() -> dict[str, dict[str, Any]]:
    """Get metadata for all registered config schemas.

    Returns:
        Mapping of config class names to their metadata

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = get_hub()

    config_names = None

    result = {}
    for name in config_names:
        entry = hub._component_registry.get_entry(name, ComponentCategory.CONFIG_SCHEMA.value)
        if entry:
            result[name] = entry.metadata

    return result


def x_get_config_metadata__mutmut_3() -> dict[str, dict[str, Any]]:
    """Get metadata for all registered config schemas.

    Returns:
        Mapping of config class names to their metadata

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = get_hub()

    config_names = hub._component_registry.list_dimension(None)

    result = {}
    for name in config_names:
        entry = hub._component_registry.get_entry(name, ComponentCategory.CONFIG_SCHEMA.value)
        if entry:
            result[name] = entry.metadata

    return result


def x_get_config_metadata__mutmut_4() -> dict[str, dict[str, Any]]:
    """Get metadata for all registered config schemas.

    Returns:
        Mapping of config class names to their metadata

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = get_hub()

    config_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)

    result = None
    for name in config_names:
        entry = hub._component_registry.get_entry(name, ComponentCategory.CONFIG_SCHEMA.value)
        if entry:
            result[name] = entry.metadata

    return result


def x_get_config_metadata__mutmut_5() -> dict[str, dict[str, Any]]:
    """Get metadata for all registered config schemas.

    Returns:
        Mapping of config class names to their metadata

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = get_hub()

    config_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)

    result = {}
    for name in config_names:
        entry = None
        if entry:
            result[name] = entry.metadata

    return result


def x_get_config_metadata__mutmut_6() -> dict[str, dict[str, Any]]:
    """Get metadata for all registered config schemas.

    Returns:
        Mapping of config class names to their metadata

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = get_hub()

    config_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)

    result = {}
    for name in config_names:
        entry = hub._component_registry.get_entry(None, ComponentCategory.CONFIG_SCHEMA.value)
        if entry:
            result[name] = entry.metadata

    return result


def x_get_config_metadata__mutmut_7() -> dict[str, dict[str, Any]]:
    """Get metadata for all registered config schemas.

    Returns:
        Mapping of config class names to their metadata

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = get_hub()

    config_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)

    result = {}
    for name in config_names:
        entry = hub._component_registry.get_entry(name, None)
        if entry:
            result[name] = entry.metadata

    return result


def x_get_config_metadata__mutmut_8() -> dict[str, dict[str, Any]]:
    """Get metadata for all registered config schemas.

    Returns:
        Mapping of config class names to their metadata

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = get_hub()

    config_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)

    result = {}
    for name in config_names:
        entry = hub._component_registry.get_entry(ComponentCategory.CONFIG_SCHEMA.value)
        if entry:
            result[name] = entry.metadata

    return result


def x_get_config_metadata__mutmut_9() -> dict[str, dict[str, Any]]:
    """Get metadata for all registered config schemas.

    Returns:
        Mapping of config class names to their metadata

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = get_hub()

    config_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)

    result = {}
    for name in config_names:
        entry = hub._component_registry.get_entry(
            name,
        )
        if entry:
            result[name] = entry.metadata

    return result


def x_get_config_metadata__mutmut_10() -> dict[str, dict[str, Any]]:
    """Get metadata for all registered config schemas.

    Returns:
        Mapping of config class names to their metadata

    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    hub = get_hub()

    config_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)

    result = {}
    for name in config_names:
        entry = hub._component_registry.get_entry(name, ComponentCategory.CONFIG_SCHEMA.value)
        if entry:
            result[name] = None

    return result


x_get_config_metadata__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_config_metadata__mutmut_1": x_get_config_metadata__mutmut_1,
    "x_get_config_metadata__mutmut_2": x_get_config_metadata__mutmut_2,
    "x_get_config_metadata__mutmut_3": x_get_config_metadata__mutmut_3,
    "x_get_config_metadata__mutmut_4": x_get_config_metadata__mutmut_4,
    "x_get_config_metadata__mutmut_5": x_get_config_metadata__mutmut_5,
    "x_get_config_metadata__mutmut_6": x_get_config_metadata__mutmut_6,
    "x_get_config_metadata__mutmut_7": x_get_config_metadata__mutmut_7,
    "x_get_config_metadata__mutmut_8": x_get_config_metadata__mutmut_8,
    "x_get_config_metadata__mutmut_9": x_get_config_metadata__mutmut_9,
    "x_get_config_metadata__mutmut_10": x_get_config_metadata__mutmut_10,
}


def get_config_metadata(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_config_metadata__mutmut_orig, x_get_config_metadata__mutmut_mutants, args, kwargs
    )
    return result


get_config_metadata.__signature__ = _mutmut_signature(x_get_config_metadata__mutmut_orig)
x_get_config_metadata__mutmut_orig.__name__ = "x_get_config_metadata"


def x_get_consolidated_schema__mutmut_orig() -> ConsolidatedSchema:
    """Get consolidated schema with all configuration options.

    This function discovers all registered configuration classes,
    generates schemas for each, and consolidates them into a single
    schema object with full metadata.

    Returns:
        Consolidated schema with all config options

    """
    config_classes = discover_all_config_schemas()
    metadata = get_config_metadata()
    schemas = {}

    for name, config_cls in config_classes.items():
        try:
            schemas[name] = ConfigSchema.from_config_class(config_cls)
        except Exception:
            # If schema generation fails for any class, skip it
            # but continue processing others
            continue

    return ConsolidatedSchema(schemas=schemas, metadata=metadata)


def x_get_consolidated_schema__mutmut_1() -> ConsolidatedSchema:
    """Get consolidated schema with all configuration options.

    This function discovers all registered configuration classes,
    generates schemas for each, and consolidates them into a single
    schema object with full metadata.

    Returns:
        Consolidated schema with all config options

    """
    config_classes = None
    metadata = get_config_metadata()
    schemas = {}

    for name, config_cls in config_classes.items():
        try:
            schemas[name] = ConfigSchema.from_config_class(config_cls)
        except Exception:
            # If schema generation fails for any class, skip it
            # but continue processing others
            continue

    return ConsolidatedSchema(schemas=schemas, metadata=metadata)


def x_get_consolidated_schema__mutmut_2() -> ConsolidatedSchema:
    """Get consolidated schema with all configuration options.

    This function discovers all registered configuration classes,
    generates schemas for each, and consolidates them into a single
    schema object with full metadata.

    Returns:
        Consolidated schema with all config options

    """
    config_classes = discover_all_config_schemas()
    metadata = None
    schemas = {}

    for name, config_cls in config_classes.items():
        try:
            schemas[name] = ConfigSchema.from_config_class(config_cls)
        except Exception:
            # If schema generation fails for any class, skip it
            # but continue processing others
            continue

    return ConsolidatedSchema(schemas=schemas, metadata=metadata)


def x_get_consolidated_schema__mutmut_3() -> ConsolidatedSchema:
    """Get consolidated schema with all configuration options.

    This function discovers all registered configuration classes,
    generates schemas for each, and consolidates them into a single
    schema object with full metadata.

    Returns:
        Consolidated schema with all config options

    """
    config_classes = discover_all_config_schemas()
    metadata = get_config_metadata()
    schemas = None

    for name, config_cls in config_classes.items():
        try:
            schemas[name] = ConfigSchema.from_config_class(config_cls)
        except Exception:
            # If schema generation fails for any class, skip it
            # but continue processing others
            continue

    return ConsolidatedSchema(schemas=schemas, metadata=metadata)


def x_get_consolidated_schema__mutmut_4() -> ConsolidatedSchema:
    """Get consolidated schema with all configuration options.

    This function discovers all registered configuration classes,
    generates schemas for each, and consolidates them into a single
    schema object with full metadata.

    Returns:
        Consolidated schema with all config options

    """
    config_classes = discover_all_config_schemas()
    metadata = get_config_metadata()
    schemas = {}

    for name, config_cls in config_classes.items():
        try:
            schemas[name] = None
        except Exception:
            # If schema generation fails for any class, skip it
            # but continue processing others
            continue

    return ConsolidatedSchema(schemas=schemas, metadata=metadata)


def x_get_consolidated_schema__mutmut_5() -> ConsolidatedSchema:
    """Get consolidated schema with all configuration options.

    This function discovers all registered configuration classes,
    generates schemas for each, and consolidates them into a single
    schema object with full metadata.

    Returns:
        Consolidated schema with all config options

    """
    config_classes = discover_all_config_schemas()
    metadata = get_config_metadata()
    schemas = {}

    for name, config_cls in config_classes.items():
        try:
            schemas[name] = ConfigSchema.from_config_class(None)
        except Exception:
            # If schema generation fails for any class, skip it
            # but continue processing others
            continue

    return ConsolidatedSchema(schemas=schemas, metadata=metadata)


def x_get_consolidated_schema__mutmut_6() -> ConsolidatedSchema:
    """Get consolidated schema with all configuration options.

    This function discovers all registered configuration classes,
    generates schemas for each, and consolidates them into a single
    schema object with full metadata.

    Returns:
        Consolidated schema with all config options

    """
    config_classes = discover_all_config_schemas()
    metadata = get_config_metadata()
    schemas = {}

    for name, config_cls in config_classes.items():
        try:
            schemas[name] = ConfigSchema.from_config_class(config_cls)
        except Exception:
            # If schema generation fails for any class, skip it
            # but continue processing others
            break

    return ConsolidatedSchema(schemas=schemas, metadata=metadata)


def x_get_consolidated_schema__mutmut_7() -> ConsolidatedSchema:
    """Get consolidated schema with all configuration options.

    This function discovers all registered configuration classes,
    generates schemas for each, and consolidates them into a single
    schema object with full metadata.

    Returns:
        Consolidated schema with all config options

    """
    config_classes = discover_all_config_schemas()
    metadata = get_config_metadata()
    schemas = {}

    for name, config_cls in config_classes.items():
        try:
            schemas[name] = ConfigSchema.from_config_class(config_cls)
        except Exception:
            # If schema generation fails for any class, skip it
            # but continue processing others
            continue

    return ConsolidatedSchema(schemas=None, metadata=metadata)


def x_get_consolidated_schema__mutmut_8() -> ConsolidatedSchema:
    """Get consolidated schema with all configuration options.

    This function discovers all registered configuration classes,
    generates schemas for each, and consolidates them into a single
    schema object with full metadata.

    Returns:
        Consolidated schema with all config options

    """
    config_classes = discover_all_config_schemas()
    metadata = get_config_metadata()
    schemas = {}

    for name, config_cls in config_classes.items():
        try:
            schemas[name] = ConfigSchema.from_config_class(config_cls)
        except Exception:
            # If schema generation fails for any class, skip it
            # but continue processing others
            continue

    return ConsolidatedSchema(schemas=schemas, metadata=None)


def x_get_consolidated_schema__mutmut_9() -> ConsolidatedSchema:
    """Get consolidated schema with all configuration options.

    This function discovers all registered configuration classes,
    generates schemas for each, and consolidates them into a single
    schema object with full metadata.

    Returns:
        Consolidated schema with all config options

    """
    config_classes = discover_all_config_schemas()
    metadata = get_config_metadata()
    schemas = {}

    for name, config_cls in config_classes.items():
        try:
            schemas[name] = ConfigSchema.from_config_class(config_cls)
        except Exception:
            # If schema generation fails for any class, skip it
            # but continue processing others
            continue

    return ConsolidatedSchema(metadata=metadata)


def x_get_consolidated_schema__mutmut_10() -> ConsolidatedSchema:
    """Get consolidated schema with all configuration options.

    This function discovers all registered configuration classes,
    generates schemas for each, and consolidates them into a single
    schema object with full metadata.

    Returns:
        Consolidated schema with all config options

    """
    config_classes = discover_all_config_schemas()
    metadata = get_config_metadata()
    schemas = {}

    for name, config_cls in config_classes.items():
        try:
            schemas[name] = ConfigSchema.from_config_class(config_cls)
        except Exception:
            # If schema generation fails for any class, skip it
            # but continue processing others
            continue

    return ConsolidatedSchema(
        schemas=schemas,
    )


x_get_consolidated_schema__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_consolidated_schema__mutmut_1": x_get_consolidated_schema__mutmut_1,
    "x_get_consolidated_schema__mutmut_2": x_get_consolidated_schema__mutmut_2,
    "x_get_consolidated_schema__mutmut_3": x_get_consolidated_schema__mutmut_3,
    "x_get_consolidated_schema__mutmut_4": x_get_consolidated_schema__mutmut_4,
    "x_get_consolidated_schema__mutmut_5": x_get_consolidated_schema__mutmut_5,
    "x_get_consolidated_schema__mutmut_6": x_get_consolidated_schema__mutmut_6,
    "x_get_consolidated_schema__mutmut_7": x_get_consolidated_schema__mutmut_7,
    "x_get_consolidated_schema__mutmut_8": x_get_consolidated_schema__mutmut_8,
    "x_get_consolidated_schema__mutmut_9": x_get_consolidated_schema__mutmut_9,
    "x_get_consolidated_schema__mutmut_10": x_get_consolidated_schema__mutmut_10,
}


def get_consolidated_schema(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_consolidated_schema__mutmut_orig, x_get_consolidated_schema__mutmut_mutants, args, kwargs
    )
    return result


get_consolidated_schema.__signature__ = _mutmut_signature(x_get_consolidated_schema__mutmut_orig)
x_get_consolidated_schema__mutmut_orig.__name__ = "x_get_consolidated_schema"


# <3 🧱🤝⚙️🪄
