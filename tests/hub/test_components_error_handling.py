#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Error handling and dependency resolution tests for hub components module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock

from provide.foundation.hub.components import (
    ComponentCategory,
    execute_error_handlers,
    get_component_registry,
    get_handlers_for_exception,
    resolve_component_dependencies,
)


class TestErrorHandlers(FoundationTestCase):
    """Test error handler functionality."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

    def teardown_method(self) -> None:
        """Clean up after tests."""
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

    def test_get_handlers_for_exception(self) -> None:
        """Test get_handlers_for_exception finds matching handlers."""
        registry = get_component_registry()

        value_error_handler = Mock()
        runtime_error_handler = Mock()
        general_handler = Mock()

        registry.register(
            name="value_handler",
            value=value_error_handler,
            dimension=ComponentCategory.ERROR_HANDLER.value,
            metadata={"exception_types": ["ValueError"], "priority": 1},
        )

        registry.register(
            name="runtime_handler",
            value=runtime_error_handler,
            dimension=ComponentCategory.ERROR_HANDLER.value,
            metadata={"exception_types": ["RuntimeError"], "priority": 2},
        )

        registry.register(
            name="general_handler",
            value=general_handler,
            dimension=ComponentCategory.ERROR_HANDLER.value,
            metadata={"exception_types": ["Error"], "priority": 3},
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

    def test_execute_error_handlers(self) -> None:
        """Test execute_error_handlers runs handlers until success."""
        registry = get_component_registry()

        failing_handler = Mock(return_value=None)
        working_handler = Mock(return_value={"handled": True})

        registry.register(
            name="failing_handler",
            value=failing_handler,
            dimension=ComponentCategory.ERROR_HANDLER.value,
            metadata={"exception_types": ["ValueError"], "priority": 2},
        )

        registry.register(
            name="working_handler",
            value=working_handler,
            dimension=ComponentCategory.ERROR_HANDLER.value,
            metadata={"exception_types": ["ValueError"], "priority": 1},
        )

        exception = ValueError("test error")
        context = {"key": "value"}

        result = execute_error_handlers(exception, context)

        # Should return result from working handler
        assert result == {"handled": True}

        # Both handlers should be called (failing one first due to priority)
        failing_handler.assert_called_once_with(exception, context)
        working_handler.assert_called_once_with(exception, context)

    def test_execute_error_handlers_with_handler_exception(self) -> None:
        """Test execute_error_handlers handles handler exceptions."""
        registry = get_component_registry()

        exception_handler = Mock(side_effect=Exception("Handler failed"))
        working_handler = Mock(return_value={"handled": True})

        registry.register(
            name="exception_handler",
            value=exception_handler,
            dimension=ComponentCategory.ERROR_HANDLER.value,
            metadata={"exception_types": ["ValueError"], "priority": 2},
        )

        registry.register(
            name="working_handler",
            value=working_handler,
            dimension=ComponentCategory.ERROR_HANDLER.value,
            metadata={"exception_types": ["ValueError"], "priority": 1},
        )

        exception = ValueError("test error")
        context = {"key": "value"}

        result = execute_error_handlers(exception, context)

        # Should continue to working handler despite exception in first handler
        assert result == {"handled": True}


class TestComponentDependencies(FoundationTestCase):
    """Test component dependency resolution."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

    def teardown_method(self) -> None:
        """Clean up after tests."""
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

    def test_resolve_component_dependencies_same_dimension(self) -> None:
        """Test resolve_component_dependencies finds deps in same dimension."""
        registry = get_component_registry()

        dep_component = Mock()
        main_component = Mock()

        registry.register(
            name="dependency",
            value=dep_component,
            dimension="test_dimension",
            metadata={},
        )

        registry.register(
            name="main",
            value=main_component,
            dimension="test_dimension",
            metadata={"dependencies": ["dependency"]},
        )

        deps = resolve_component_dependencies("main", "test_dimension")

        assert "dependency" in deps
        assert deps["dependency"] is dep_component

    def test_resolve_component_dependencies_cross_dimension(self) -> None:
        """Test resolve_component_dependencies searches across dimensions."""
        registry = get_component_registry()

        dep_component = Mock()
        main_component = Mock()

        registry.register(
            name="cross_dependency",
            value=dep_component,
            dimension="other_dimension",
            metadata={},
        )

        registry.register(
            name="main",
            value=main_component,
            dimension="test_dimension",
            metadata={"dependencies": ["cross_dependency"]},
        )

        deps = resolve_component_dependencies("main", "test_dimension")

        assert "cross_dependency" in deps
        assert deps["cross_dependency"] is dep_component

    def test_resolve_component_dependencies_not_found(self) -> None:
        """Test resolve_component_dependencies handles missing components."""
        registry = get_component_registry()

        main_component = Mock()

        registry.register(
            name="main",
            value=main_component,
            dimension="test_dimension",
            metadata={"dependencies": ["missing_dependency"]},
        )

        deps = resolve_component_dependencies("main", "test_dimension")

        # Should not include missing dependency
        assert "missing_dependency" not in deps

    def test_resolve_component_dependencies_no_entry(self) -> None:
        """Test resolve_component_dependencies handles non-existent component."""
        deps = resolve_component_dependencies("nonexistent", "test_dimension")
        assert deps == {}


# 🧱🏗️🔚
