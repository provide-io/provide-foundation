"""Basic coverage tests for hub components module - ComponentInfo, Category, and Emoji functionality."""

import asyncio
from unittest.mock import Mock, AsyncMock, patch
import pytest
import inspect
import threading

from provide.foundation.hub.components import (
    ComponentInfo,
    ComponentCategory,
    ComponentLifecycle,
    get_component_registry,
    find_emoji_set_for_domain,
    get_default_emoji_set,
    resolve_emoji_for_domain,
    get_composed_emoji_set,
    reset_registry_for_tests,
    bootstrap_foundation,
)
from provide.foundation.eventsets.types import EventMapping
from provide.foundation.hub.registry import Registry, RegistryEntry


class TestComponentInfo:
    """Test ComponentInfo dataclass."""

    def test_component_info_creation(self):
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

    def test_component_info_defaults(self):
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


class TestComponentCategory:
    """Test ComponentCategory enum."""

    def test_component_category_values(self):
        """Test ComponentCategory enum values."""
        assert ComponentCategory.EMOJI_SET.value == "emoji_set"
        assert ComponentCategory.CONFIG_SOURCE.value == "config_source"
        assert ComponentCategory.PROCESSOR.value == "processor"
        assert ComponentCategory.ERROR_HANDLER.value == "error_handler"
        assert ComponentCategory.FORMATTER.value == "formatter"
        assert ComponentCategory.FILTER.value == "filter"


class TestEmojiResolution:
    """Test emoji resolution functionality."""

    def setup_method(self):
        """Set up test environment."""
        reset_registry_for_tests()

    def teardown_method(self):
        """Clean up after tests."""
        reset_registry_for_tests()

    def test_resolve_emoji_for_domain_with_action(self):
        """Test resolve_emoji_for_domain finds specific action."""
        registry = get_component_registry()

        emoji_set = EventMapping(
            name="test_set", visual_markers={"success": "✅", "error": "❌", "info": "ℹ️"}
        )

        registry.register(
            name="test_emoji_set",
            value=emoji_set,
            dimension=ComponentCategory.EMOJI_SET.value,
            metadata={"domain": "test_domain", "priority": 1},
        )

        result = resolve_emoji_for_domain("test_domain", "success")
        assert result == "✅"

    def test_resolve_emoji_for_domain_fallback_to_default(self):
        """Test resolve_emoji_for_domain falls back to default set."""
        # Bootstrap to ensure default set exists
        bootstrap_foundation()

        # Request emoji for unknown domain/action
        result = resolve_emoji_for_domain("unknown_domain", "unknown_action")
        assert result == "📝"  # Default fallback emoji

    def test_resolve_emoji_for_domain_priority_ordering(self):
        """Test emoji resolution respects priority ordering."""
        registry = get_component_registry()

        low_priority_set = EventMapping("low", visual_markers={"info": "🔵"})
        high_priority_set = EventMapping("high", visual_markers={"info": "🔴"})

        registry.register(
            name="low_priority",
            value=low_priority_set,
            dimension=ComponentCategory.EMOJI_SET.value,
            metadata={"domain": "test_domain", "priority": 1},
        )

        registry.register(
            name="high_priority",
            value=high_priority_set,
            dimension=ComponentCategory.EMOJI_SET.value,
            metadata={"domain": "test_domain", "priority": 2},
        )

        result = resolve_emoji_for_domain("test_domain", "info")
        assert result == "🔴"  # Should use high priority

    def test_get_composed_emoji_set(self):
        """Test get_composed_emoji_set combines multiple sets."""
        registry = get_component_registry()

        set1 = EventMapping("set1", visual_markers={"info": "ℹ️", "success": "✅"})
        set2 = EventMapping("set2", visual_markers={"error": "❌", "info": "🔵"})  # Override info

        registry.register(
            name="set1",
            value=set1,
            dimension=ComponentCategory.EMOJI_SET.value,
            metadata={"domain": "compose_test", "priority": 1},
        )

        registry.register(
            name="set2",
            value=set2,
            dimension=ComponentCategory.EMOJI_SET.value,
            metadata={"domain": "compose_test", "priority": 2},
        )

        composed = get_composed_emoji_set("compose_test")

        assert composed.name == "composed_compose_test"
        assert composed.visual_markers["success"] == "✅"  # From set1
        assert composed.visual_markers["error"] == "❌"  # From set2
        assert composed.visual_markers["info"] == "🔵"  # set2 overrides set1 (higher priority)