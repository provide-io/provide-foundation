#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Component health, configuration schema, and initialization tests for hub components module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import AsyncMock, Mock
import pytest

from provide.foundation.hub.components import (
    check_component_health,
    get_component_config_schema,
    get_component_registry,
    get_or_initialize_component,
    initialize_all_async_components,
    initialize_async_component,
)


class TestComponentHealth(FoundationTestCase):
    """Test component health checking."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

    def teardown_method(self) -> None:
        """Clean up after tests."""
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

    def test_check_component_health_not_found(self) -> None:
        """Test check_component_health with non-existent component."""
        result = check_component_health("nonexistent", "test_dimension")
        assert result == {"status": "not_found"}

    def test_check_component_health_no_support(self) -> None:
        """Test check_component_health with component that doesn't support health checks."""
        registry = get_component_registry()

        component = Mock()

        registry.register(
            name="no_health",
            value=component,
            dimension="test_dimension",
            metadata={"supports_health_check": False},
        )

        result = check_component_health("no_health", "test_dimension")
        assert result == {"status": "no_health_check"}

    def test_check_component_health_with_method(self) -> None:
        """Test check_component_health with component that has health_check method."""
        registry = get_component_registry()

        component = Mock()
        component.health_check = Mock(return_value={"status": "healthy"})

        registry.register(
            name="healthy_component",
            value=component,
            dimension="test_dimension",
            metadata={"supports_health_check": True},
        )

        result = check_component_health("healthy_component", "test_dimension")
        assert result == {"status": "healthy"}
        component.health_check.assert_called_once()

    def test_check_component_health_method_exception(self) -> None:
        """Test check_component_health handles health check exceptions."""
        registry = get_component_registry()

        component = Mock()
        component.health_check = Mock(side_effect=Exception("Health check failed"))

        registry.register(
            name="failing_health",
            value=component,
            dimension="test_dimension",
            metadata={"supports_health_check": True},
        )

        result = check_component_health("failing_health", "test_dimension")
        assert result["status"] == "error"
        assert "Health check failed" in result["error"]

    def test_check_component_health_no_method(self) -> None:
        """Test check_component_health with component without health_check method."""
        registry = get_component_registry()

        component = Mock(spec=[])  # No methods

        registry.register(
            name="no_method",
            value=component,
            dimension="test_dimension",
            metadata={"supports_health_check": True},
        )

        result = check_component_health("no_method", "test_dimension")
        assert result == {"status": "unknown"}


class TestComponentConfigSchema(FoundationTestCase):
    """Test component configuration schema functionality."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

    def teardown_method(self) -> None:
        """Clean up after tests."""
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

    def test_get_component_config_schema(self) -> None:
        """Test get_component_config_schema returns schema from metadata."""
        registry = get_component_registry()

        component = Mock()
        schema = {"type": "object", "properties": {"key": {"type": "string"}}}

        registry.register(
            name="component_with_schema",
            value=component,
            dimension="test_dimension",
            metadata={"config_schema": schema},
        )

        result = get_component_config_schema("component_with_schema", "test_dimension")
        assert result == schema

    def test_get_component_config_schema_not_found(self) -> None:
        """Test get_component_config_schema with non-existent component."""
        result = get_component_config_schema("nonexistent", "test_dimension")
        assert result is None

    def test_get_component_config_schema_no_schema(self) -> None:
        """Test get_component_config_schema with component that has no schema."""
        registry = get_component_registry()

        component = Mock()

        registry.register(
            name="no_schema",
            value=component,
            dimension="test_dimension",
            metadata={},
        )

        result = get_component_config_schema("no_schema", "test_dimension")
        assert result is None


class TestComponentInitialization(FoundationTestCase):
    """Test component initialization functionality."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

    def teardown_method(self) -> None:
        """Clean up after tests."""
        from provide.foundation.testmode.internal import reset_hub_state

        reset_hub_state()

    def test_get_or_initialize_component_already_initialized(self) -> None:
        """Test get_or_initialize_component returns cached component."""
        registry = get_component_registry()

        component = Mock()

        registry.register(
            name="initialized",
            value=component,
            dimension="test_dimension",
            metadata={},
        )

        # First call
        result1 = get_or_initialize_component("initialized", "test_dimension")
        assert result1 is component

        # Second call should return cached version
        result2 = get_or_initialize_component("initialized", "test_dimension")
        assert result2 is component
        assert result1 is result2

    def test_get_or_initialize_component_lazy_initialization(self) -> None:
        """Test get_or_initialize_component with lazy initialization."""
        registry = get_component_registry()

        # Create a factory that returns a component
        factory = Mock(return_value=Mock())

        registry.register(
            name="lazy_component",
            value=None,  # Not initialized yet
            dimension="test_dimension",
            metadata={"lazy": True, "factory": factory},
        )

        result = get_or_initialize_component("lazy_component", "test_dimension")

        # Should call factory and return component
        factory.assert_called_once()
        assert result is not None
        assert result == factory.return_value

    def test_get_or_initialize_component_lazy_initialization_failure(self) -> None:
        """Test get_or_initialize_component handles lazy initialization failures."""
        registry = get_component_registry()

        # Factory that raises exception
        factory = Mock(side_effect=Exception("Initialization failed"))

        registry.register(
            name="failing_lazy",
            value=None,
            dimension="test_dimension",
            metadata={"lazy": True, "factory": factory},
        )

        result = get_or_initialize_component("failing_lazy", "test_dimension")

        # Should return None when initialization fails
        assert result is None
        factory.assert_called_once()

    def test_get_or_initialize_component_not_found(self) -> None:
        """Test get_or_initialize_component with non-existent component."""
        result = get_or_initialize_component("nonexistent", "test_dimension")
        assert result is None

    @pytest.mark.asyncio
    async def test_initialize_async_component_already_cached(self) -> None:
        """Test initialize_async_component returns cached component."""
        registry = get_component_registry()

        component = Mock()

        registry.register(
            name="async_component",
            value=component,
            dimension="test_dimension",
            metadata={"async": True},
        )

        result = await initialize_async_component("async_component", "test_dimension")
        assert result is component

    @pytest.mark.asyncio
    async def test_initialize_async_component_with_async_factory(self) -> None:
        """Test initialize_async_component with async factory."""
        registry = get_component_registry()

        # Create async factory
        async_factory = AsyncMock(return_value=Mock())

        registry.register(
            name="async_factory_component",
            value=None,
            dimension="test_dimension",
            metadata={"async": True, "factory": async_factory},
        )

        result = await initialize_async_component(
            "async_factory_component",
            "test_dimension",
        )

        async_factory.assert_called_once()
        assert result is not None
        assert result == async_factory.return_value

    @pytest.mark.asyncio
    async def test_initialize_async_component_with_sync_factory(self) -> None:
        """Test initialize_async_component with sync factory."""
        registry = get_component_registry()

        sync_factory = Mock(return_value=Mock())

        registry.register(
            name="sync_factory_component",
            value=None,
            dimension="test_dimension",
            metadata={"async": True, "factory": sync_factory},
        )

        result = await initialize_async_component(
            "sync_factory_component",
            "test_dimension",
        )

        sync_factory.assert_called_once()
        assert result is not None
        assert result == sync_factory.return_value

    @pytest.mark.asyncio
    async def test_initialize_async_component_initialization_failure(self) -> None:
        """Test initialize_async_component handles initialization failures."""
        registry = get_component_registry()

        failing_factory = Mock(side_effect=Exception("Async init failed"))

        registry.register(
            name="failing_async",
            value=None,
            dimension="test_dimension",
            metadata={"async": True, "factory": failing_factory},
        )

        result = await initialize_async_component("failing_async", "test_dimension")
        assert result is None

    @pytest.mark.asyncio
    async def test_initialize_async_component_not_found(self) -> None:
        """Test initialize_async_component with non-existent component."""
        result = await initialize_async_component("nonexistent", "test_dimension")
        assert result is None

    @pytest.mark.asyncio
    async def test_initialize_all_async_components(self) -> None:
        """Test initialize_all_async_components processes all async components."""
        registry = get_component_registry()

        # Register multiple async components
        factory1 = Mock(return_value=Mock())
        factory2 = Mock(return_value=Mock())

        registry.register(
            name="async1",
            value=None,
            dimension="test_dimension",
            metadata={"async": True, "factory": factory1, "priority": 1},
        )

        registry.register(
            name="async2",
            value=None,
            dimension="test_dimension",
            metadata={"async": True, "factory": factory2, "priority": 2},
        )

        await initialize_all_async_components()

        # Both factories should be called
        factory1.assert_called_once()
        factory2.assert_called_once()

    @pytest.mark.asyncio
    async def test_initialize_all_async_components_with_failure(self) -> None:
        """Test initialize_all_async_components continues despite failures."""
        registry = get_component_registry()

        failing_factory = Mock(side_effect=Exception("Init failed"))
        working_factory = Mock(return_value=Mock())

        registry.register(
            name="failing_async",
            value=None,
            dimension="test_dimension",
            metadata={"async": True, "factory": failing_factory, "priority": 2},
        )

        registry.register(
            name="working_async",
            value=None,
            dimension="test_dimension",
            metadata={"async": True, "factory": working_factory, "priority": 1},
        )

        # Should not raise exception and should continue to initialize working components
        await initialize_all_async_components()

        failing_factory.assert_called_once()
        working_factory.assert_called_once()


# 🧱🏗️🔚
