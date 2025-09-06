"""Advanced coverage tests for hub components module - targeting missing lines."""

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
    resolve_config_value,
    get_config_chain,
    load_all_configs,
    get_processor_pipeline,
    get_processors_for_stage,
    get_handlers_for_exception,
    execute_error_handlers,
    resolve_component_dependencies,
    check_component_health,
    get_component_config_schema,
    get_or_initialize_component,
    initialize_async_component,
    cleanup_all_components,
    bootstrap_foundation,
    load_config_from_registry,
    initialize_all_async_components,
    reset_registry_for_tests,
    discover_components,
    _component_registry,
    _registry_lock,
    _initialized_components,
)
from provide.foundation.logger.emoji.types import EmojiSet
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
            metadata={"key": "value"}
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
        info = ComponentInfo(
            name="minimal",
            component_class=Mock
        )
        
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
        
        emoji_set = EmojiSet(
            name="test_set",
            emojis={"success": "✅", "error": "❌", "info": "ℹ️"}
        )
        
        registry.register(
            name="test_emoji_set",
            value=emoji_set,
            dimension=ComponentCategory.EMOJI_SET.value,
            metadata={"domain": "test_domain", "priority": 1}
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
        
        low_priority_set = EmojiSet("low", {"info": "🔵"})
        high_priority_set = EmojiSet("high", {"info": "🔴"})
        
        registry.register(
            name="low_priority",
            value=low_priority_set,
            dimension=ComponentCategory.EMOJI_SET.value,
            metadata={"domain": "test_domain", "priority": 1}
        )
        
        registry.register(
            name="high_priority",
            value=high_priority_set,
            dimension=ComponentCategory.EMOJI_SET.value,
            metadata={"domain": "test_domain", "priority": 2}
        )
        
        result = resolve_emoji_for_domain("test_domain", "info")
        assert result == "🔴"  # Should use high priority
    
    def test_get_composed_emoji_set(self):
        """Test get_composed_emoji_set combines multiple sets."""
        registry = get_component_registry()
        
        set1 = EmojiSet("set1", {"info": "ℹ️", "success": "✅"})
        set2 = EmojiSet("set2", {"error": "❌", "info": "🔵"})  # Override info
        
        registry.register(
            name="set1",
            value=set1,
            dimension=ComponentCategory.EMOJI_SET.value,
            metadata={"domain": "compose_test", "priority": 1}
        )
        
        registry.register(
            name="set2", 
            value=set2,
            dimension=ComponentCategory.EMOJI_SET.value,
            metadata={"domain": "compose_test", "priority": 2}
        )
        
        composed = get_composed_emoji_set("compose_test")
        
        assert composed.name == "composed_compose_test"
        assert composed.emojis["success"] == "✅"  # From set1
        assert composed.emojis["error"] == "❌"  # From set2
        assert composed.emojis["info"] == "🔵"  # set2 overrides set1 (higher priority)


class TestAsyncConfigLoading:
    """Test async configuration loading functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        reset_registry_for_tests()
    
    def teardown_method(self):
        """Clean up after tests."""
        reset_registry_for_tests()
    
    @pytest.mark.asyncio
    async def test_load_all_configs_async_sources(self):
        """Test load_all_configs with async config sources."""
        registry = get_component_registry()
        
        async_source = Mock()
        async_source.load_config = AsyncMock(return_value={"async_key": "async_value"})
        
        sync_source = Mock()
        sync_source.load_config = Mock(return_value={"sync_key": "sync_value"})
        
        registry.register(
            name="async_source",
            value=async_source,
            dimension=ComponentCategory.CONFIG_SOURCE.value,
            metadata={"priority": 2}
        )
        
        registry.register(
            name="sync_source",
            value=sync_source,
            dimension=ComponentCategory.CONFIG_SOURCE.value,
            metadata={"priority": 1}
        )
        
        configs = await load_all_configs()
        
        assert "async_key" in configs
        assert "sync_key" in configs
        assert configs["async_key"] == "async_value"
        assert configs["sync_key"] == "sync_value"
    
    @pytest.mark.asyncio
    async def test_load_all_configs_with_exception(self):
        """Test load_all_configs handles source exceptions."""
        registry = get_component_registry()
        
        failing_source = Mock()
        failing_source.load_config = Mock(side_effect=Exception("Config load failed"))
        
        working_source = Mock()
        working_source.load_config = Mock(return_value={"working_key": "working_value"})
        
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
        
        configs = await load_all_configs()
        
        # Should continue loading other sources despite exception
        assert "working_key" in configs
        assert configs["working_key"] == "working_value"


class TestProcessorPipeline:
    """Test processor pipeline functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        reset_registry_for_tests()
    
    def teardown_method(self):
        """Clean up after tests."""
        reset_registry_for_tests()
    
    def test_get_processor_pipeline(self):
        """Test get_processor_pipeline returns processors ordered by priority."""
        registry = get_component_registry()
        
        proc1 = Mock()
        proc2 = Mock()
        proc3 = Mock()
        
        registry.register(
            name="proc1",
            value=proc1,
            dimension=ComponentCategory.PROCESSOR.value,
            metadata={"priority": 1}
        )
        
        registry.register(
            name="proc2",
            value=proc2,
            dimension=ComponentCategory.PROCESSOR.value,
            metadata={"priority": 3}
        )
        
        registry.register(
            name="proc3",
            value=proc3,
            dimension=ComponentCategory.PROCESSOR.value,
            metadata={"priority": 2}
        )
        
        pipeline = get_processor_pipeline()
        
        assert len(pipeline) == 3
        # Should be ordered by priority (highest first)
        assert pipeline[0].value is proc2  # priority 3
        assert pipeline[1].value is proc3  # priority 2
        assert pipeline[2].value is proc1  # priority 1
    
    def test_get_processors_for_stage(self):
        """Test get_processors_for_stage filters by stage."""
        registry = get_component_registry()
        
        pre_proc = Mock()
        post_proc = Mock()
        format_proc = Mock()
        
        registry.register(
            name="pre_processor",
            value=pre_proc,
            dimension=ComponentCategory.PROCESSOR.value,
            metadata={"priority": 1, "stage": "pre_format"}
        )
        
        registry.register(
            name="post_processor",
            value=post_proc,
            dimension=ComponentCategory.PROCESSOR.value,
            metadata={"priority": 2, "stage": "post_format"}
        )
        
        registry.register(
            name="format_processor",
            value=format_proc,
            dimension=ComponentCategory.PROCESSOR.value,
            metadata={"priority": 3, "stage": "format"}
        )
        
        pre_processors = get_processors_for_stage("pre_format")
        post_processors = get_processors_for_stage("post_format")
        format_processors = get_processors_for_stage("format")
        
        assert len(pre_processors) == 1
        assert pre_processors[0].value is pre_proc
        
        assert len(post_processors) == 1
        assert post_processors[0].value is post_proc
        
        assert len(format_processors) == 1
        assert format_processors[0].value is format_proc


class TestErrorHandlers:
    """Test error handler functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        reset_registry_for_tests()
    
    def teardown_method(self):
        """Clean up after tests."""
        reset_registry_for_tests()
    
    def test_get_handlers_for_exception(self):
        """Test get_handlers_for_exception finds matching handlers."""
        registry = get_component_registry()
        
        value_error_handler = Mock()
        runtime_error_handler = Mock()
        general_handler = Mock()
        
        registry.register(
            name="value_handler",
            value=value_error_handler,
            dimension=ComponentCategory.ERROR_HANDLER.value,
            metadata={"exception_types": ["ValueError"], "priority": 1}
        )
        
        registry.register(
            name="runtime_handler",
            value=runtime_error_handler,
            dimension=ComponentCategory.ERROR_HANDLER.value,
            metadata={"exception_types": ["RuntimeError"], "priority": 2}
        )
        
        registry.register(
            name="general_handler",
            value=general_handler,
            dimension=ComponentCategory.ERROR_HANDLER.value,
            metadata={"exception_types": ["Error"], "priority": 3}
        )
        
        # Test ValueError
        value_handlers = get_handlers_for_exception(ValueError("test"))
        assert len(value_handlers) >= 1
        value_handler_names = [entry.name for entry in value_handlers]
        assert "value_handler" in value_handler_names
        assert "general_handler" in value_handler_names  # "Error" matches "ValueError"
        
        # Test RuntimeError  
        runtime_handlers = get_handlers_for_exception(RuntimeError("test"))
        assert len(runtime_handlers) >= 1
        runtime_handler_names = [entry.name for entry in runtime_handlers]
        assert "runtime_handler" in runtime_handler_names
    
    def test_execute_error_handlers(self):
        """Test execute_error_handlers runs handlers until success."""
        registry = get_component_registry()
        
        failing_handler = Mock(return_value=None)
        working_handler = Mock(return_value={"handled": True})
        
        registry.register(
            name="failing_handler",
            value=failing_handler,
            dimension=ComponentCategory.ERROR_HANDLER.value,
            metadata={"exception_types": ["ValueError"], "priority": 2}
        )
        
        registry.register(
            name="working_handler",
            value=working_handler,
            dimension=ComponentCategory.ERROR_HANDLER.value,
            metadata={"exception_types": ["ValueError"], "priority": 1}
        )
        
        exception = ValueError("test error")
        context = {"key": "value"}
        
        result = execute_error_handlers(exception, context)
        
        # Should return result from working handler
        assert result == {"handled": True}
        
        # Both handlers should be called (failing one first due to priority)
        failing_handler.assert_called_once_with(exception, context)
        working_handler.assert_called_once_with(exception, context)
    
    def test_execute_error_handlers_with_handler_exception(self):
        """Test execute_error_handlers handles handler exceptions."""
        registry = get_component_registry()
        
        exception_handler = Mock(side_effect=Exception("Handler failed"))
        working_handler = Mock(return_value={"handled": True})
        
        registry.register(
            name="exception_handler",
            value=exception_handler,
            dimension=ComponentCategory.ERROR_HANDLER.value,
            metadata={"exception_types": ["ValueError"], "priority": 2}
        )
        
        registry.register(
            name="working_handler",
            value=working_handler,
            dimension=ComponentCategory.ERROR_HANDLER.value,
            metadata={"exception_types": ["ValueError"], "priority": 1}
        )
        
        exception = ValueError("test error")
        context = {"key": "value"}
        
        result = execute_error_handlers(exception, context)
        
        # Should continue to working handler despite exception in first handler
        assert result == {"handled": True}


class TestComponentDependencies:
    """Test component dependency resolution."""
    
    def setup_method(self):
        """Set up test environment."""
        reset_registry_for_tests()
    
    def teardown_method(self):
        """Clean up after tests."""
        reset_registry_for_tests()
    
    def test_resolve_component_dependencies_same_dimension(self):
        """Test resolve_component_dependencies finds deps in same dimension."""
        registry = get_component_registry()
        
        dep_component = Mock()
        main_component = Mock()
        
        registry.register(
            name="dependency",
            value=dep_component,
            dimension="test_dimension",
            metadata={}
        )
        
        registry.register(
            name="main",
            value=main_component,
            dimension="test_dimension",
            metadata={"dependencies": ["dependency"]}
        )
        
        deps = resolve_component_dependencies("main", "test_dimension")
        
        assert "dependency" in deps
        assert deps["dependency"] is dep_component
    
    def test_resolve_component_dependencies_cross_dimension(self):
        """Test resolve_component_dependencies searches across dimensions."""
        registry = get_component_registry()
        
        dep_component = Mock()
        main_component = Mock()
        
        registry.register(
            name="cross_dependency",
            value=dep_component,
            dimension="other_dimension",
            metadata={}
        )
        
        registry.register(
            name="main",
            value=main_component,
            dimension="test_dimension", 
            metadata={"dependencies": ["cross_dependency"]}
        )
        
        deps = resolve_component_dependencies("main", "test_dimension")
        
        assert "cross_dependency" in deps
        assert deps["cross_dependency"] is dep_component
    
    def test_resolve_component_dependencies_not_found(self):
        """Test resolve_component_dependencies handles missing components."""
        registry = get_component_registry()
        
        main_component = Mock()
        
        registry.register(
            name="main",
            value=main_component,
            dimension="test_dimension",
            metadata={"dependencies": ["missing_dependency"]}
        )
        
        deps = resolve_component_dependencies("main", "test_dimension")
        
        # Should not include missing dependency
        assert "missing_dependency" not in deps
    
    def test_resolve_component_dependencies_no_entry(self):
        """Test resolve_component_dependencies handles non-existent component."""
        deps = resolve_component_dependencies("nonexistent", "test_dimension")
        assert deps == {}


class TestComponentHealth:
    """Test component health checking."""
    
    def setup_method(self):
        """Set up test environment."""
        reset_registry_for_tests()
    
    def teardown_method(self):
        """Clean up after tests."""
        reset_registry_for_tests()
    
    def test_check_component_health_not_found(self):
        """Test check_component_health with non-existent component."""
        result = check_component_health("nonexistent", "test_dimension")
        assert result == {"status": "not_found"}
    
    def test_check_component_health_no_support(self):
        """Test check_component_health with component that doesn't support health checks."""
        registry = get_component_registry()
        
        component = Mock()
        
        registry.register(
            name="no_health",
            value=component,
            dimension="test_dimension",
            metadata={"supports_health_check": False}
        )
        
        result = check_component_health("no_health", "test_dimension")
        assert result == {"status": "no_health_check"}
    
    def test_check_component_health_with_method(self):
        """Test check_component_health with component that has health_check method."""
        registry = get_component_registry()
        
        component = Mock()
        component.health_check = Mock(return_value={"status": "healthy"})
        
        registry.register(
            name="healthy_component",
            value=component,
            dimension="test_dimension",
            metadata={"supports_health_check": True}
        )
        
        result = check_component_health("healthy_component", "test_dimension")
        assert result == {"status": "healthy"}
        component.health_check.assert_called_once()
    
    def test_check_component_health_method_exception(self):
        """Test check_component_health handles health check exceptions."""
        registry = get_component_registry()
        
        component = Mock()
        component.health_check = Mock(side_effect=Exception("Health check failed"))
        
        registry.register(
            name="failing_health",
            value=component,
            dimension="test_dimension",
            metadata={"supports_health_check": True}
        )
        
        result = check_component_health("failing_health", "test_dimension")
        assert result["status"] == "error"
        assert "Health check failed" in result["error"]
    
    def test_check_component_health_no_method(self):
        """Test check_component_health with component without health_check method."""
        registry = get_component_registry()
        
        component = Mock(spec=[])  # No methods
        
        registry.register(
            name="no_method",
            value=component,
            dimension="test_dimension",
            metadata={"supports_health_check": True}
        )
        
        result = check_component_health("no_method", "test_dimension")
        assert result == {"status": "unknown"}


class TestComponentConfigSchema:
    """Test component configuration schema functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        reset_registry_for_tests()
    
    def teardown_method(self):
        """Clean up after tests."""
        reset_registry_for_tests()
    
    def test_get_component_config_schema(self):
        """Test get_component_config_schema returns schema from metadata."""
        registry = get_component_registry()
        
        component = Mock()
        schema = {"type": "object", "properties": {"key": {"type": "string"}}}
        
        registry.register(
            name="component_with_schema",
            value=component,
            dimension="test_dimension",
            metadata={"config_schema": schema}
        )
        
        result = get_component_config_schema("component_with_schema", "test_dimension")
        assert result == schema
    
    def test_get_component_config_schema_not_found(self):
        """Test get_component_config_schema with non-existent component."""
        result = get_component_config_schema("nonexistent", "test_dimension")
        assert result is None
    
    def test_get_component_config_schema_no_schema(self):
        """Test get_component_config_schema with component that has no schema."""
        registry = get_component_registry()
        
        component = Mock()
        
        registry.register(
            name="no_schema",
            value=component,
            dimension="test_dimension",
            metadata={}
        )
        
        result = get_component_config_schema("no_schema", "test_dimension")
        assert result is None