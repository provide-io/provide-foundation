#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for hub type definitions."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.hub.components import ComponentInfo
from provide.foundation.hub.info import CommandInfo
from provide.foundation.hub.registry import RegistryEntry
from provide.foundation.hub.types import (
    Registrable,
)


class TestRegistryEntry(FoundationTestCase):
    """Test RegistryEntry dataclass."""

    def test_create_registry_entry(self) -> None:
        """Test creating a registry entry."""
        entry = RegistryEntry(
            name="test_item",
            dimension="test_dim",
            value="test_value",
        )

        assert entry.name == "test_item"
        assert entry.dimension == "test_dim"
        assert entry.value == "test_value"
        assert entry.metadata == {}

    def test_registry_entry_with_metadata(self) -> None:
        """Test registry entry with metadata."""
        meta = {"version": "1.0", "author": "test"}
        entry = RegistryEntry(
            name="test_item",
            dimension="test_dim",
            value="test_value",
            metadata=meta,
        )

        assert entry.metadata == meta

    def test_registry_entry_key_property(self) -> None:
        """Test the key property."""
        entry = RegistryEntry(
            name="test_item",
            dimension="test_dim",
            value="test_value",
        )

        assert entry.key == ("test_dim", "test_item")

    def test_registry_entry_immutable(self) -> None:
        """Test that registry entry is immutable."""
        entry = RegistryEntry(
            name="test_item",
            dimension="test_dim",
            value="test_value",
        )

        with pytest.raises(AttributeError):
            entry.name = "new_name"  # type: ignore

    def test_registry_entry_equality(self) -> None:
        """Test registry entry equality."""
        entry1 = RegistryEntry(
            name="test_item",
            dimension="test_dim",
            value="test_value",
        )
        entry2 = RegistryEntry(
            name="test_item",
            dimension="test_dim",
            value="test_value",
        )

        assert entry1 == entry2


class TestRegistrable:
    """Test Registrable protocol."""

    def test_registrable_protocol(self) -> None:
        """Test class implementing Registrable protocol."""

        class TestComponent:
            __registry_name__ = "test_component"
            __registry_dimension__ = "components"
            __registry_metadata__ = {"version": "1.0"}

        comp = TestComponent()
        assert comp.__registry_name__ == "test_component"
        assert comp.__registry_dimension__ == "components"
        assert comp.__registry_metadata__ == {"version": "1.0"}

    def test_registrable_type_checking(self) -> None:
        """Test that Registrable works as a type hint."""

        def register_item(item: Registrable) -> str:
            return f"{item.__registry_dimension__}:{item.__registry_name__}"

        class ValidComponent:
            __registry_name__ = "valid"
            __registry_dimension__ = "test"
            __registry_metadata__: dict[str, any] = {}

        comp = ValidComponent()
        result = register_item(comp)
        assert result == "test:valid"


class TestCommandInfo:
    """Test CommandInfo dataclass."""

    def test_create_command_info(self) -> None:
        """Test creating command info."""

        def test_func() -> None:
            pass

        cmd = CommandInfo(name="test_command", func=test_func)

        assert cmd.name == "test_command"
        assert cmd.func is test_func
        assert cmd.description is None
        assert cmd.aliases == []
        assert cmd.hidden is False
        assert cmd.metadata == {}

    def test_command_info_with_all_fields(self) -> None:
        """Test command info with all fields."""

        def test_func() -> None:
            pass

        cmd = CommandInfo(
            name="test_command",
            func=test_func,
            description="Test command description",
            aliases=["tc", "test"],
            hidden=True,
            metadata={"category": "testing"},
        )

        assert cmd.description == "Test command description"
        assert cmd.aliases == ["tc", "test"]
        assert cmd.hidden is True
        assert cmd.metadata == {"category": "testing"}

    def test_command_info_immutable(self) -> None:
        """Test that command info is immutable."""

        def test_func() -> None:
            pass

        cmd = CommandInfo(name="test_command", func=test_func)

        with pytest.raises(AttributeError):
            cmd.name = "new_name"  # type: ignore


class TestComponentInfo:
    """Test ComponentInfo dataclass."""

    def test_create_component_info(self) -> None:
        """Test creating component info."""

        class TestComponent:
            pass

        comp_info = ComponentInfo(name="test_component", component_class=TestComponent)

        assert comp_info.name == "test_component"
        assert comp_info.component_class is TestComponent
        assert comp_info.dimension == "component"
        assert comp_info.description is None
        assert comp_info.version is None
        assert comp_info.metadata == {}

    def test_component_info_with_all_fields(self) -> None:
        """Test component info with all fields."""

        class TestComponent:
            pass

        comp_info = ComponentInfo(
            name="test_component",
            component_class=TestComponent,
            dimension="custom_dimension",
            description="Test component description",
            version="1.0.0",
            metadata={"author": "test", "tags": ["test", "component"]},
        )

        assert comp_info.dimension == "custom_dimension"
        assert comp_info.description == "Test component description"
        assert comp_info.version == "1.0.0"
        assert comp_info.metadata == {"author": "test", "tags": ["test", "component"]}

    def test_component_info_immutable(self) -> None:
        """Test that component info is immutable."""

        class TestComponent:
            pass

        comp_info = ComponentInfo(name="test_component", component_class=TestComponent)

        with pytest.raises(AttributeError):
            comp_info.name = "new_name"  # type: ignore

    def test_component_info_equality(self) -> None:
        """Test component info equality."""

        class TestComponent:
            pass

        comp_info1 = ComponentInfo(
            name="test_component",
            component_class=TestComponent,
            version="1.0.0",
        )
        comp_info2 = ComponentInfo(
            name="test_component",
            component_class=TestComponent,
            version="1.0.0",
        )

        assert comp_info1 == comp_info2


# 🧱🏗️🔚
