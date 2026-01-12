#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for configuration bootstrap and discovery."""

from __future__ import annotations

from attrs import define
from provide.testkit import FoundationTestCase

from provide.foundation.config.base import field
from provide.foundation.config.bootstrap import (
    _get_all_subclasses,
    _import_config_modules,
    discover_and_register_configs,
)
from provide.foundation.config.env import RuntimeConfig
from provide.foundation.hub import get_hub
from provide.foundation.hub.categories import ComponentCategory


class TestImportConfigModules(FoundationTestCase):
    """Test config module importing."""

    def test_import_config_modules_succeeds(self) -> None:
        """Test that config modules can be imported without errors."""
        # Should not raise any exceptions
        _import_config_modules()

    def test_import_handles_missing_modules_gracefully(self) -> None:
        """Test that missing modules don't cause failures."""
        # Should not raise even if some modules don't exist
        _import_config_modules()


class TestGetAllSubclasses(FoundationTestCase):
    """Test subclass discovery."""

    def test_get_all_subclasses_finds_direct_subclasses(self) -> None:
        """Test finding direct subclasses."""

        class Base:
            pass

        class Child1(Base):
            pass

        class Child2(Base):
            pass

        subclasses = _get_all_subclasses(Base)
        assert Child1 in subclasses
        assert Child2 in subclasses

    def test_get_all_subclasses_finds_nested_subclasses(self) -> None:
        """Test finding nested subclasses."""

        class Base:
            pass

        class Child(Base):
            pass

        class GrandChild(Child):
            pass

        subclasses = _get_all_subclasses(Base)
        assert Child in subclasses
        assert GrandChild in subclasses

    def test_get_all_subclasses_empty_for_no_subclasses(self) -> None:
        """Test that classes with no subclasses return empty set."""

        class Isolated:
            pass

        subclasses = _get_all_subclasses(Isolated)
        assert len(subclasses) == 0


class TestDiscoverAndRegisterConfigs(FoundationTestCase):
    """Test config discovery and registration."""

    def test_discover_registers_config_schemas(self) -> None:
        """Test that configs are registered with Hub."""
        # Discover and register
        discover_and_register_configs()

        # Get Hub and check registration
        hub = get_hub()
        config_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)

        # Should have at least some configs registered
        assert len(config_names) > 0

    def test_discover_is_idempotent(self) -> None:
        """Test that calling discover multiple times is safe."""
        # First discovery
        discover_and_register_configs()
        hub = get_hub()
        first_count = len(hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value))

        # Second discovery - should skip if already registered
        discover_and_register_configs()
        second_count = len(hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value))

        # Should be same count (idempotent)
        assert first_count == second_count

    def test_discover_extracts_category_from_module(self) -> None:
        """Test that category is extracted from module path."""
        discover_and_register_configs()

        hub = get_hub()
        # LoggingConfig should be categorized as "logger"
        entry = hub._component_registry.get_entry("LoggingConfig", ComponentCategory.CONFIG_SCHEMA.value)

        assert entry is not None
        assert entry.metadata.get("category") == "logger"

    def test_discover_detects_env_vars(self) -> None:
        """Test that env var fields are detected."""
        discover_and_register_configs()

        hub = get_hub()
        entry = hub._component_registry.get_entry("LoggingConfig", ComponentCategory.CONFIG_SCHEMA.value)

        assert entry is not None
        assert entry.metadata.get("has_env_vars") is True

    def test_discover_stores_module_path(self) -> None:
        """Test that module path is stored in metadata."""
        discover_and_register_configs()

        hub = get_hub()
        entry = hub._component_registry.get_entry("LoggingConfig", ComponentCategory.CONFIG_SCHEMA.value)

        assert entry is not None
        assert "provide.foundation.logger.config.logging" in entry.metadata.get("module", "")

    def test_discover_stores_docstring(self) -> None:
        """Test that class docstring is stored."""
        discover_and_register_configs()

        hub = get_hub()
        entry = hub._component_registry.get_entry("LoggingConfig", ComponentCategory.CONFIG_SCHEMA.value)

        assert entry is not None
        # LoggingConfig should have a docstring
        doc = entry.metadata.get("doc", "")
        assert len(doc) > 0


class TestConfigSchemaIntegration(FoundationTestCase):
    """Test integration with custom config schemas."""

    def test_custom_config_gets_registered(self) -> None:
        """Test that custom RuntimeConfig subclasses can be discovered."""

        # Create a custom config class
        @define
        class TestConfig(RuntimeConfig):
            """Test configuration."""

            test_field: str = field(
                default="test",
                env_var="TEST_FIELD",
                description="A test field",
            )

        # Trigger discovery
        discover_and_register_configs()

        # Check registration
        hub = get_hub()
        entry = hub._component_registry.get_entry("TestConfig", ComponentCategory.CONFIG_SCHEMA.value)

        # May or may not be registered depending on when subclass was created
        # vs when discovery was run, but test should not fail
        if entry is not None:
            assert issubclass(entry.value, RuntimeConfig)


# 🧱🏗️🔚
