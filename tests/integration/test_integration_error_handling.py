#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Integration tests for error handling across foundation modules."""

from __future__ import annotations

import tempfile
from typing import Never

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.config.loader import FileConfigLoader
from provide.foundation.errors import (
    AlreadyExistsError,
    ConfigurationError,
    NotFoundError,
    ValidationError,
)
from provide.foundation.hub import Hub
from provide.foundation.hub.registry import Registry


class TestErrorHandlingIntegration(FoundationTestCase):
    """Test error handling integration across modules."""

    def test_registry_error_handling(self) -> None:
        """Test registry raises proper errors."""
        registry = Registry()

        # Register an item
        registry.register("test", "value", dimension="test")

        # Try to register again without replace=True
        with pytest.raises(AlreadyExistsError) as exc_info:
            registry.register("test", "value2", dimension="test")

        assert exc_info.value.code == "REGISTRY_ITEM_EXISTS"
        assert exc_info.value.context["item_name"] == "test"
        assert exc_info.value.context["dimension"] == "test"

    def test_hub_error_handling(self) -> None:
        """Test hub raises proper errors."""
        hub = Hub()

        # Add a component
        class TestComponent:
            pass

        hub.add_component(TestComponent, "test")

        # Try to add again
        with pytest.raises(AlreadyExistsError) as exc_info:
            hub.add_component(TestComponent, "test")

        assert exc_info.value.code == "HUB_COMPONENT_EXISTS"
        assert exc_info.value.context["component_name"] == "test"

        # Try to add non-class
        with pytest.raises(ValidationError) as exc_info:
            hub.add_component("not a class", "invalid")

        assert exc_info.value.code == "HUB_INVALID_COMPONENT"

    async def test_config_loader_error_handling(self) -> None:
        """Test config loader raises proper errors."""
        # Test with non-existent file
        loader = FileConfigLoader("/non/existent/file.json")

        class TestConfig:
            @classmethod
            def from_dict(cls, data, source=None):
                return cls()

        with pytest.raises(NotFoundError) as exc_info:
            await loader.load(TestConfig)

        assert exc_info.value.code == "CONFIG_FILE_NOT_FOUND"
        assert "/non/existent/file.json" in str(exc_info.value)

        # Test with unknown format
        with tempfile.NamedTemporaryFile(suffix=".xyz") as f:
            with pytest.raises(ConfigurationError) as exc_info:
                loader = FileConfigLoader(f.name)

            assert exc_info.value.code == "CONFIG_FORMAT_UNKNOWN"

    def test_error_context_propagation(self) -> None:
        """Test that error context is properly propagated."""
        registry = Registry()

        # Register with metadata
        registry.register(
            "test_item",
            "value",
            dimension="test",
            metadata={"version": "1.0.0"},
        )

        # Try duplicate registration
        try:
            registry.register("test_item", "new_value", dimension="test")
        except AlreadyExistsError as e:
            # Check error has proper context
            assert e.message
            assert e.code
            assert e.context["item_name"] == "test_item"
            assert e.context["dimension"] == "test"

            # Check string representation
            assert "test_item" in str(e)
            assert "dimension 'test'" in str(e)

    def test_no_circular_dependency(self) -> None:
        """Verify no circular dependency between logger and errors."""
        # This test passes if it can import both without issues
        from provide.foundation.errors import FoundationError
        from provide.foundation.logger import logger

        # Logger can log without importing errors
        logger.info("Test message", extra_field="value")

        # Errors can be raised and use logger internally
        try:
            raise FoundationError("Test error", code="TEST_001", test_field="value")
        except FoundationError as e:
            # Error decorators use logger internally
            assert e.code == "TEST_001"
            assert e.context["test_field"] == "value"

    async def test_async_error_handling(self) -> None:
        """Test error handling with async functions."""
        from provide.foundation.errors.decorators import resilient

        @resilient(fallback="default", suppress=(ValueError,))
        async def async_func(should_fail: bool = False) -> str:
            if should_fail:
                raise ValueError("Test error")
            return "success"

        # Test normal execution
        result = await async_func()
        assert result == "success"

        # Test suppressed error returns fallback
        result = await async_func(should_fail=True)
        assert result == "default"

    def test_error_logging_integration(self, captured_stderr_for_foundation) -> None:
        """Test that errors are properly logged."""
        from provide.foundation import TelemetryConfig, get_hub
        from provide.foundation.errors.decorators import resilient

        # Setup telemetry
        hub = get_hub()
        hub.initialize_foundation(TelemetryConfig(), force=True)

        @resilient(log_errors=True)
        def failing_func() -> Never:
            raise ValueError("Test error for logging")

        # Call function and let it raise
        with pytest.raises(ValueError):
            failing_func()

        # Check that error was logged
        output = captured_stderr_for_foundation.getvalue()
        assert "Error in failing_func" in output
        assert "Test error for logging" in output


# 🧱🏗️🔚
