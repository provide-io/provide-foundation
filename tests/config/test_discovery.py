#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for configuration schema discovery."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.config.bootstrap import discover_and_register_configs
from provide.foundation.config.discovery import (
    ConsolidatedSchema,
    EnvVarInfo,
    discover_all_config_schemas,
    get_config_metadata,
    get_consolidated_schema,
)
from provide.foundation.config.env import RuntimeConfig
from provide.foundation.config.schema import ConfigSchema


class TestDiscoverAllConfigSchemas(FoundationTestCase):
    """Test discovering all config schemas from Hub."""

    def test_discover_all_config_schemas_returns_dict(self) -> None:
        """Test that discover returns a dictionary."""
        # Ensure configs are registered
        discover_and_register_configs()

        schemas = discover_all_config_schemas()
        assert isinstance(schemas, dict)

    def test_discover_all_config_schemas_contains_logging_config(self) -> None:
        """Test that LoggingConfig is discovered."""
        discover_and_register_configs()

        schemas = discover_all_config_schemas()
        assert "LoggingConfig" in schemas

    def test_discover_all_config_schemas_returns_config_classes(self) -> None:
        """Test that returned values are config classes."""
        discover_and_register_configs()

        schemas = discover_all_config_schemas()
        for _name, config_cls in schemas.items():
            # Should be a class (type)
            assert isinstance(config_cls, type)
            # Should be a RuntimeConfig subclass
            assert issubclass(config_cls, RuntimeConfig)


class TestGetConfigMetadata(FoundationTestCase):
    """Test retrieving config metadata."""

    def test_get_config_metadata_returns_dict(self) -> None:
        """Test that metadata returns a dictionary."""
        discover_and_register_configs()

        metadata = get_config_metadata()
        assert isinstance(metadata, dict)

    def test_get_config_metadata_contains_module_info(self) -> None:
        """Test that metadata contains module information."""
        discover_and_register_configs()

        metadata = get_config_metadata()
        if "LoggingConfig" in metadata:
            logging_meta = metadata["LoggingConfig"]
            assert "module" in logging_meta
            assert "provide.foundation.logger.config.logging" in logging_meta["module"]

    def test_get_config_metadata_contains_category(self) -> None:
        """Test that metadata contains category."""
        discover_and_register_configs()

        metadata = get_config_metadata()
        if "LoggingConfig" in metadata:
            logging_meta = metadata["LoggingConfig"]
            assert "category" in logging_meta
            assert logging_meta["category"] == "logger"

    def test_get_config_metadata_contains_has_env_vars(self) -> None:
        """Test that metadata indicates env var presence."""
        discover_and_register_configs()

        metadata = get_config_metadata()
        if "LoggingConfig" in metadata:
            logging_meta = metadata["LoggingConfig"]
            assert "has_env_vars" in logging_meta
            assert logging_meta["has_env_vars"] is True


class TestGetConsolidatedSchema(FoundationTestCase):
    """Test consolidated schema generation."""

    def test_get_consolidated_schema_returns_consolidated_schema(self) -> None:
        """Test that function returns ConsolidatedSchema instance."""
        discover_and_register_configs()

        schema = get_consolidated_schema()
        assert isinstance(schema, ConsolidatedSchema)

    def test_get_consolidated_schema_has_schemas(self) -> None:
        """Test that consolidated schema contains schemas."""
        discover_and_register_configs()

        schema = get_consolidated_schema()
        assert len(schema.schemas) > 0

    def test_get_consolidated_schema_has_metadata(self) -> None:
        """Test that consolidated schema contains metadata."""
        discover_and_register_configs()

        schema = get_consolidated_schema()
        assert len(schema.metadata) > 0

    def test_get_consolidated_schema_schemas_are_config_schemas(self) -> None:
        """Test that schemas are ConfigSchema instances."""
        discover_and_register_configs()

        schema = get_consolidated_schema()
        for _name, config_schema in schema.schemas.items():
            assert isinstance(config_schema, ConfigSchema)


class TestConsolidatedSchemaGetByCategory(FoundationTestCase):
    """Test filtering schemas by category."""

    def test_get_by_category_filters_correctly(self) -> None:
        """Test that get_by_category returns only matching schemas."""
        discover_and_register_configs()

        schema = get_consolidated_schema()
        logger_schemas = schema.get_by_category("logger")

        # Should have at least LoggingConfig
        assert len(logger_schemas) > 0

        # All returned schemas should be logger category
        for name in logger_schemas:
            meta = schema.metadata.get(name, {})
            assert meta.get("category") == "logger"

    def test_get_by_category_returns_empty_for_nonexistent(self) -> None:
        """Test that nonexistent category returns empty dict."""
        discover_and_register_configs()

        schema = get_consolidated_schema()
        result = schema.get_by_category("nonexistent_category")

        assert isinstance(result, dict)
        assert len(result) == 0


class TestConsolidatedSchemaGetAllEnvVars(FoundationTestCase):
    """Test extracting environment variables."""

    def test_get_all_env_vars_returns_list(self) -> None:
        """Test that env vars returns a list."""
        discover_and_register_configs()

        schema = get_consolidated_schema()
        env_vars = schema.get_all_env_vars()

        assert isinstance(env_vars, list)

    def test_get_all_env_vars_contains_env_var_info(self) -> None:
        """Test that returned items are EnvVarInfo instances."""
        discover_and_register_configs()

        schema = get_consolidated_schema()
        env_vars = schema.get_all_env_vars()

        if len(env_vars) > 0:
            assert all(isinstance(var, EnvVarInfo) for var in env_vars)

    def test_get_all_env_vars_filters_non_env_fields(self) -> None:
        """Test that only env var fields are returned."""
        discover_and_register_configs()

        schema = get_consolidated_schema()
        env_vars = schema.get_all_env_vars()

        # All returned vars should have env_var set
        for var in env_vars:
            assert var.env_var is not None
            assert len(var.env_var) > 0

    def test_get_all_env_vars_hides_sensitive_by_default(self) -> None:
        """Test that sensitive fields are hidden by default."""
        discover_and_register_configs()

        schema = get_consolidated_schema()
        env_vars = schema.get_all_env_vars(show_sensitive=False)

        # No sensitive vars should be in the list
        for var in env_vars:
            assert not var.sensitive

    def test_get_all_env_vars_shows_sensitive_when_requested(self) -> None:
        """Test that sensitive fields can be shown."""
        discover_and_register_configs()

        schema = get_consolidated_schema()
        all_vars = schema.get_all_env_vars(show_sensitive=True)
        hidden_vars = schema.get_all_env_vars(show_sensitive=False)

        # Should have at least as many vars when showing sensitive
        assert len(all_vars) >= len(hidden_vars)


class TestConsolidatedSchemaGetCategories(FoundationTestCase):
    """Test getting unique categories."""

    def test_get_categories_returns_set(self) -> None:
        """Test that categories returns a set."""
        discover_and_register_configs()

        schema = get_consolidated_schema()
        categories = schema.get_categories()

        assert isinstance(categories, set)

    def test_get_categories_contains_logger(self) -> None:
        """Test that logger category is present."""
        discover_and_register_configs()

        schema = get_consolidated_schema()
        categories = schema.get_categories()

        assert "logger" in categories

    def test_get_categories_has_multiple_categories(self) -> None:
        """Test that multiple categories are found."""
        discover_and_register_configs()

        schema = get_consolidated_schema()
        categories = schema.get_categories()

        # Should have at least a few categories
        assert len(categories) >= 2


class TestEnvVarInfo(FoundationTestCase):
    """Test EnvVarInfo dataclass."""

    def test_env_var_info_creation(self) -> None:
        """Test creating EnvVarInfo instance."""
        info = EnvVarInfo(
            config_class="TestConfig",
            field_name="test_field",
            env_var="TEST_VAR",
            field_type="str",
            default="default",
            required=False,
            description="Test description",
            sensitive=False,
            category="test",
        )

        assert info.config_class == "TestConfig"
        assert info.field_name == "test_field"
        assert info.env_var == "TEST_VAR"
        assert info.field_type == "str"
        assert info.default == "default"
        assert info.required is False
        assert info.description == "Test description"
        assert info.sensitive is False
        assert info.category == "test"

    def test_env_var_info_is_frozen(self) -> None:
        """Test that EnvVarInfo is immutable."""
        import attrs

        info = EnvVarInfo(
            config_class="TestConfig",
            field_name="test_field",
            env_var="TEST_VAR",
            field_type="str",
            default="default",
            required=False,
            description="Test description",
            sensitive=False,
            category="test",
        )

        # Should not be able to modify
        with pytest.raises(attrs.exceptions.FrozenInstanceError):
            info.config_class = "Modified"  # type: ignore


class TestConsolidatedSchema(FoundationTestCase):
    """Test ConsolidatedSchema dataclass."""

    def test_consolidated_schema_creation(self) -> None:
        """Test creating ConsolidatedSchema instance."""
        schemas = {"TestConfig": ConfigSchema(fields=[])}
        metadata = {"TestConfig": {"category": "test"}}

        consolidated = ConsolidatedSchema(schemas=schemas, metadata=metadata)

        assert consolidated.schemas == schemas
        assert consolidated.metadata == metadata


# 🧱🏗️🔚
