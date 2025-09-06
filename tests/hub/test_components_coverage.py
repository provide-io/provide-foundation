#
# test_components_coverage.py
#
"""
Tests to cover missing lines in hub/components.py for 100% coverage.
"""

import asyncio
from unittest.mock import Mock, AsyncMock
import pytest

from provide.foundation.hub.components import (
    ComponentCategory,
    get_component_registry,
    find_emoji_set_for_domain,
    get_default_emoji_set,
    resolve_config_value,
    get_config_chain,
    cleanup_all_components,
    bootstrap_foundation,
)
from provide.foundation.logger.emoji.types import EmojiSet


class TestComponentLifecycle:
    """Test component lifecycle management functionality."""
    
    def test_cleanup_all_components_with_cleanup_support(self):
        """Test cleanup of components that support cleanup."""
        registry = get_component_registry()
        
        # Create components with and without cleanup support
        component_with_cleanup = Mock()
        component_with_cleanup.cleanup = Mock()
        
        component_without_cleanup = Mock()
        
        registry.register(
            name="cleanup_component",
            value=component_with_cleanup,
            dimension="test_components",
            metadata={"supports_cleanup": True}
        )
        
        registry.register(
            name="no_cleanup_component", 
            value=component_without_cleanup,
            dimension="test_components",
            metadata={}
        )
        
        # Cleanup should only call cleanup on components that support it
        cleanup_all_components("test_components")
        
        component_with_cleanup.cleanup.assert_called_once()
        assert not hasattr(component_without_cleanup, 'cleanup') or not component_without_cleanup.cleanup.called
        
        # Cleanup
        registry.clear()
    
    def test_cleanup_all_components_with_exception(self):
        """Test cleanup continues even if one component fails."""
        registry = get_component_registry()
        
        # Component that raises exception during cleanup
        failing_component = Mock()
        failing_component.cleanup = Mock(side_effect=Exception("Cleanup failed"))
        
        # Component that should still get cleaned up
        working_component = Mock()
        working_component.cleanup = Mock()
        
        registry.register(
            name="failing_component",
            value=failing_component,
            dimension="test_components", 
            metadata={"supports_cleanup": True}
        )
        
        registry.register(
            name="working_component",
            value=working_component,
            dimension="test_components",
            metadata={"supports_cleanup": True}
        )
        
        # Cleanup should not fail and should continue to other components
        cleanup_all_components("test_components")
        
        failing_component.cleanup.assert_called_once()
        working_component.cleanup.assert_called_once()
        
        # Cleanup
        registry.clear()


class TestConfigSourceFunctionality:
    """Test configuration source functionality."""
    
    def test_get_config_value_with_sources(self):
        """Test getting config value from registered sources."""
        registry = get_component_registry()
        
        # Create mock config sources
        source1 = Mock()
        source1.get_value = Mock(return_value=None)
        
        source2 = Mock()
        source2.get_value = Mock(return_value="test_value")
        
        registry.register(
            name="low_priority_source",
            value=source1,
            dimension=ComponentCategory.CONFIG_SOURCE.value,
            metadata={"priority": 1}
        )
        
        registry.register(
            name="high_priority_source",
            value=source2,
            dimension=ComponentCategory.CONFIG_SOURCE.value,
            metadata={"priority": 2}
        )
        
        # Should return value from highest priority source
        result = resolve_config_value("test_key")
        assert result == "test_value"
        
        # Should try high priority first
        source2.get_value.assert_called_with("test_key")
        
        # Cleanup
        registry.clear()
    
    def test_get_config_value_with_exception(self):
        """Test config value retrieval with source exceptions."""
        registry = get_component_registry()
        
        # Source that raises exception
        failing_source = Mock()
        failing_source.get_value = Mock(side_effect=Exception("Source failed"))
        
        # Source that works
        working_source = Mock()
        working_source.get_value = Mock(return_value="fallback_value")
        
        registry.register(
            name="failing_source",
            value=failing_source,
            dimension=ComponentCategory.CONFIG_SOURCE.value,
            metadata={"priority": 2}
        )
        
        registry.register(
            name="working_source", 
            value=working_source,
            dimension=ComponentCategory.CONFIG_SOURCE.value,
            metadata={"priority": 1}
        )
        
        # Should continue to next source after exception
        result = resolve_config_value("test_key")
        assert result == "fallback_value"
        
        # Cleanup
        registry.clear()
    
    def test_resolve_config_value_no_sources(self):
        """Test config value retrieval with no sources."""
        result = resolve_config_value("test_key")
        assert result is None
    
    def test_get_config_value_no_matching_sources(self):
        """Test config value with sources that don't have get_value method."""
        registry = get_component_registry()
        
        # Source without get_value method
        invalid_source = Mock(spec=[])  # spec=[] means no methods
        
        registry.register(
            name="invalid_source",
            value=invalid_source,
            dimension=ComponentCategory.CONFIG_SOURCE.value,
            metadata={"priority": 1}
        )
        
        result = resolve_config_value("test_key")
        assert result is None
        
        # Cleanup
        registry.clear()
    
    def test_get_config_chain(self):
        """Test getting configuration sources chain."""
        registry = get_component_registry()
        
        source1 = Mock()
        source2 = Mock()
        
        registry.register(
            name="source1",
            value=source1,
            dimension=ComponentCategory.CONFIG_SOURCE.value,
            metadata={"priority": 1}
        )
        
        registry.register(
            name="source2",
            value=source2,
            dimension=ComponentCategory.CONFIG_SOURCE.value, 
            metadata={"priority": 2}
        )
        
        chain = get_config_chain()
        
        # Should be ordered by priority (highest first)
        assert len(chain) == 2
        assert chain[0].value is source2  # Higher priority first
        assert chain[1].value is source1
        
        # Cleanup
        registry.clear()


class TestEmojiSetFunctionality:
    """Test emoji set functionality coverage."""
    
    def test_find_emoji_set_for_domain_fallback_to_default(self):
        """Test that unknown domains fall back to default emoji set."""
        registry = get_component_registry()
        
        # Ensure no domain-specific sets are registered for our test domain
        result = find_emoji_set_for_domain("nonexistent_domain")
        
        # Should return default emoji set
        assert result is not None
        assert isinstance(result, EmojiSet)
        
        # Cleanup
        registry.clear()
    
    def test_find_emoji_set_for_domain_with_priority(self):
        """Test emoji set selection respects priority ordering."""
        registry = get_component_registry()
        
        # Create emoji sets with different priorities
        low_priority_set = EmojiSet("low", {"info": "🔵"})
        high_priority_set = EmojiSet("high", {"info": "🔴"})
        
        registry.register(
            name="low_priority_emoji_set",
            value=low_priority_set,
            dimension=ComponentCategory.EMOJI_SET.value,
            metadata={"domain": "test_domain", "priority": 1}
        )
        
        registry.register(
            name="high_priority_emoji_set", 
            value=high_priority_set,
            dimension=ComponentCategory.EMOJI_SET.value,
            metadata={"domain": "test_domain", "priority": 2}
        )
        
        # Should return highest priority set
        result = find_emoji_set_for_domain("test_domain")
        assert result is high_priority_set
        
        # Cleanup
        registry.clear()
    
    def test_get_default_emoji_set_fallback(self):
        """Test default emoji set retrieval."""
        registry = get_component_registry()
        
        # Clear any existing emoji sets
        registry.clear()
        
        # Bootstrap to ensure default set exists
        bootstrap_foundation()
        
        default_set = get_default_emoji_set()
        assert default_set is not None
        assert isinstance(default_set, EmojiSet)
        
        # Should be the default emoji set
        assert default_set.name == "foundation_default"