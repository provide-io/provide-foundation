#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Basic coverage tests for hub components module - ComponentInfo, Category, and Emoji functionality."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock

from provide.foundation.hub.components import (
    ComponentCategory,
    ComponentInfo,
)


class TestComponentInfo(FoundationTestCase):
    """Test ComponentInfo dataclass."""

    def test_component_info_creation(self) -> None:
        """Test ComponentInfo creation with all fields."""
        info = ComponentInfo(
            name="test_component",
            component_class=Mock,
            dimension="test_dimension",
            version="1.0.0",
            description="Test component",
            author="Test Author",
            tags=["test", "mock"],
            metadata={"key": "value"},
        )

        assert info.name == "test_component"
        assert info.component_class == Mock
        assert info.dimension == "test_dimension"
        assert info.version == "1.0.0"
        assert info.description == "Test component"
        assert info.author == "Test Author"
        assert info.tags == ["test", "mock"]
        assert info.metadata == {"key": "value"}

    def test_component_info_defaults(self) -> None:
        """Test ComponentInfo creation with defaults."""
        info = ComponentInfo(name="minimal", component_class=Mock)

        assert info.name == "minimal"
        assert info.component_class == Mock
        assert info.dimension == "component"
        assert info.version is None
        assert info.description is None
        assert info.author is None
        assert info.tags == []
        assert info.metadata == {}


class TestComponentCategory(FoundationTestCase):
    """Test ComponentCategory enum."""

    def test_component_category_values(self) -> None:
        """Test ComponentCategory enum values."""
        assert ComponentCategory.CONFIG_SOURCE.value == "config_source"
        assert ComponentCategory.PROCESSOR.value == "processor"
        assert ComponentCategory.ERROR_HANDLER.value == "error_handler"
        assert ComponentCategory.FORMATTER.value == "formatter"
        assert ComponentCategory.FILTER.value == "filter"


# 🧱🏗️🔚
