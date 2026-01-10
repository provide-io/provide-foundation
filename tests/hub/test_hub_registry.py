#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for the hub registry functionality."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.errors import AlreadyExistsError
from provide.foundation.hub.registry import Registry


class TestRegistry(FoundationTestCase):
    """Test the core Registry class."""

    def test_registry_stores_by_dimension(self) -> None:
        """Test that registry can store items in different dimensions."""
        reg = Registry()

        class MyClass:
            pass

        def my_func() -> None:
            pass

        reg.register("foo", MyClass, dimension="component")
        reg.register("bar", my_func, dimension="command")

        assert reg.get("foo", dimension="component") == MyClass
        assert reg.get("bar", dimension="command") == my_func
        assert reg.get("foo", dimension="command") is None
        assert reg.get("bar", dimension="component") is None

    def test_registry_get_without_dimension(self) -> None:
        """Test getting items without specifying dimension."""
        reg = Registry()

        class MyClass:
            pass

        reg.register("unique_name", MyClass, dimension="component")

        # Should find it without dimension
        assert reg.get("unique_name") == MyClass

    def test_registry_prevents_duplicate_names(self) -> None:
        """Test that registry prevents duplicate names in same dimension."""
        reg = Registry()

        reg.register("foo", "value1", dimension="component")

        with pytest.raises(AlreadyExistsError, match="already registered"):
            reg.register("foo", "value2", dimension="component")

    def test_registry_allows_replace(self) -> None:
        """Test that registry allows replacement with replace=True."""
        reg = Registry()

        reg.register("foo", "value1", dimension="component")
        reg.register("foo", "value2", dimension="component", replace=True)

        assert reg.get("foo", dimension="component") == "value2"

    def test_registry_allows_same_name_different_dimensions(self) -> None:
        """Test that same name can exist in different dimensions."""
        reg = Registry()

        reg.register("foo", "component_value", dimension="component")
        reg.register("foo", "command_value", dimension="command")

        assert reg.get("foo", dimension="component") == "component_value"
        assert reg.get("foo", dimension="command") == "command_value"

    def test_registry_aliases(self) -> None:
        """Test that aliases work correctly."""
        reg = Registry()

        reg.register(
            "primary",
            "value",
            dimension="component",
            aliases=["alt1", "alt2"],
        )

        assert reg.get("primary") == "value"
        assert reg.get("alt1") == "value"
        assert reg.get("alt2") == "value"

    def test_registry_metadata(self) -> None:
        """Test that metadata is stored and retrievable."""
        reg = Registry()

        metadata = {"version": "1.0", "author": "test"}
        reg.register("foo", "value", dimension="component", metadata=metadata)

        entry = reg.get_entry("foo")
        assert entry is not None
        assert entry.metadata["version"] == "1.0"
        assert entry.metadata["author"] == "test"

    def test_registry_list_dimension(self) -> None:
        """Test listing items in a dimension."""
        reg = Registry()

        reg.register("comp1", "v1", dimension="component")
        reg.register("comp2", "v2", dimension="component")
        reg.register("cmd1", "v3", dimension="command")

        components = reg.list_dimension("component")
        assert set(components) == {"comp1", "comp2"}

        commands = reg.list_dimension("command")
        assert commands == ["cmd1"]

    def test_registry_list_all(self) -> None:
        """Test listing all dimensions and items."""
        reg = Registry()

        reg.register("comp1", "v1", dimension="component")
        reg.register("cmd1", "v2", dimension="command")
        reg.register("res1", "v3", dimension="resource")

        all_items = reg.list_all()
        assert "component" in all_items
        assert "command" in all_items
        assert "resource" in all_items
        assert "comp1" in all_items["component"]
        assert "cmd1" in all_items["command"]
        assert "res1" in all_items["resource"]

    def test_registry_remove(self) -> None:
        """Test removing items from registry."""
        reg = Registry()

        reg.register("foo", "value", dimension="component", aliases=["bar"])
        assert reg.get("foo") == "value"
        assert reg.get("bar") == "value"

        assert reg.remove("foo", dimension="component") is True
        assert reg.get("foo") is None
        assert reg.get("bar") is None

        # Removing non-existent returns False
        assert reg.remove("foo", dimension="component") is False

    def test_registry_clear_dimension(self) -> None:
        """Test clearing a specific dimension."""
        reg = Registry()

        reg.register("comp1", "v1", dimension="component")
        reg.register("cmd1", "v2", dimension="command")

        reg.clear(dimension="component")

        assert reg.get("comp1") is None
        assert reg.get("cmd1") == "v2"

    def test_registry_clear_all(self) -> None:
        """Test clearing entire registry."""
        reg = Registry()

        reg.register("comp1", "v1", dimension="component")
        reg.register("cmd1", "v2", dimension="command")

        reg.clear()

        assert reg.get("comp1") is None
        assert reg.get("cmd1") is None
        assert len(reg) == 0

    def test_registry_contains(self) -> None:
        """Test __contains__ protocol."""
        reg = Registry()

        reg.register("foo", "value", dimension="component")

        assert "foo" in reg
        assert ("component", "foo") in reg
        assert "bar" not in reg
        assert ("command", "foo") not in reg

    def test_registry_iteration(self) -> None:
        """Test iterating over registry entries."""
        reg = Registry()

        reg.register("comp1", "v1", dimension="component")
        reg.register("cmd1", "v2", dimension="command")

        entries = list(reg)
        assert len(entries) == 2

        names = {entry.name for entry in entries}
        assert names == {"comp1", "cmd1"}

    def test_registry_length(self) -> None:
        """Test __len__ protocol."""
        reg = Registry()

        assert len(reg) == 0

        reg.register("comp1", "v1", dimension="component")
        assert len(reg) == 1

        reg.register("cmd1", "v2", dimension="command")
        assert len(reg) == 2

        reg.remove("comp1")
        assert len(reg) == 1


# 🧱🏗️🔚
