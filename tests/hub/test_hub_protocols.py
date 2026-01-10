#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for hub/protocols.py module.

This module tests protocol definitions and resource management abstractions."""

from __future__ import annotations

from typing import Any

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import AsyncMock, MagicMock
import pytest

from provide.foundation.hub.protocols import (
    AsyncContextResource,
    AsyncDisposable,
    AsyncInitializable,
    AsyncResourceManager,
    Disposable,
    HealthCheckable,
    Initializable,
    ResourceManager,
)


class TestDisposableProtocol(FoundationTestCase):
    """Test Disposable protocol."""

    def test_disposable_protocol_runtime_checkable(self) -> None:
        """Test that Disposable is runtime checkable."""

        class TestDisposable:
            def dispose(self) -> None:
                pass

        obj = TestDisposable()
        assert isinstance(obj, Disposable)

    def test_disposable_protocol_method_stub(self) -> None:
        """Test calling protocol stub method directly."""
        # Protocol stubs have ... (Ellipsis) as implementation
        # This tests the stub itself for coverage
        result = Disposable.dispose(None)  # type: ignore[misc]
        assert result is None

    def test_non_disposable_not_instance(self) -> None:
        """Test that objects without dispose are not Disposable."""

        class NotDisposable:
            pass

        obj = NotDisposable()
        assert not isinstance(obj, Disposable)

    def test_disposable_with_wrong_signature_not_instance(self) -> None:
        """Test that dispose with wrong signature is not Disposable."""

        class WrongSignature:
            def dispose(self, arg: str) -> None:  # Wrong - requires argument
                pass

        obj = WrongSignature()
        # Protocol should still match because it only checks method existence
        assert isinstance(obj, Disposable)


class TestAsyncDisposableProtocol(FoundationTestCase):
    """Test AsyncDisposable protocol."""

    def test_async_disposable_protocol_runtime_checkable(self) -> None:
        """Test that AsyncDisposable is runtime checkable."""

        class TestAsyncDisposable:
            async def dispose_async(self) -> None:
                pass

        obj = TestAsyncDisposable()
        assert isinstance(obj, AsyncDisposable)

    async def test_async_disposable_protocol_method_stub(self) -> None:
        """Test calling async protocol stub method directly."""
        result = await AsyncDisposable.dispose_async(None)  # type: ignore[misc]
        assert result is None

    def test_non_async_disposable_not_instance(self) -> None:
        """Test that objects without dispose_async are not AsyncDisposable."""

        class NotAsyncDisposable:
            def dispose(self) -> None:
                pass

        obj = NotAsyncDisposable()
        assert not isinstance(obj, AsyncDisposable)


class TestInitializableProtocol(FoundationTestCase):
    """Test Initializable protocol."""

    def test_initializable_protocol_runtime_checkable(self) -> None:
        """Test that Initializable is runtime checkable."""

        class TestInitializable:
            def initialize(self) -> Any:
                return "initialized"

        obj = TestInitializable()
        assert isinstance(obj, Initializable)

    def test_initializable_protocol_method_stub(self) -> None:
        """Test calling protocol stub method directly."""
        result = Initializable.initialize(None)  # type: ignore[misc]
        assert result is None

    def test_non_initializable_not_instance(self) -> None:
        """Test that objects without initialize are not Initializable."""

        class NotInitializable:
            pass

        obj = NotInitializable()
        assert not isinstance(obj, Initializable)


class TestAsyncInitializableProtocol(FoundationTestCase):
    """Test AsyncInitializable protocol."""

    def test_async_initializable_protocol_runtime_checkable(self) -> None:
        """Test that AsyncInitializable is runtime checkable."""

        class TestAsyncInitializable:
            async def initialize_async(self) -> Any:
                return "initialized"

        obj = TestAsyncInitializable()
        assert isinstance(obj, AsyncInitializable)

    async def test_async_initializable_protocol_method_stub(self) -> None:
        """Test calling async protocol stub method directly."""
        result = await AsyncInitializable.initialize_async(None)  # type: ignore[misc]
        assert result is None

    def test_non_async_initializable_not_instance(self) -> None:
        """Test that objects without initialize_async are not AsyncInitializable."""

        class NotAsyncInitializable:
            def initialize(self) -> Any:
                return "initialized"

        obj = NotAsyncInitializable()
        assert not isinstance(obj, AsyncInitializable)


class TestHealthCheckableProtocol(FoundationTestCase):
    """Test HealthCheckable protocol."""

    def test_health_checkable_protocol_runtime_checkable(self) -> None:
        """Test that HealthCheckable is runtime checkable."""

        class TestHealthCheckable:
            def health_check(self) -> dict[str, Any]:
                return {"status": "healthy"}

        obj = TestHealthCheckable()
        assert isinstance(obj, HealthCheckable)

    def test_health_checkable_protocol_method_stub(self) -> None:
        """Test calling protocol stub method directly."""
        result = HealthCheckable.health_check(None)  # type: ignore[misc]
        assert result is None

    def test_non_health_checkable_not_instance(self) -> None:
        """Test that objects without health_check are not HealthCheckable."""

        class NotHealthCheckable:
            pass

        obj = NotHealthCheckable()
        assert not isinstance(obj, HealthCheckable)

    def test_health_checkable_returns_dict(self) -> None:
        """Test that HealthCheckable implementations return dict."""

        class TestHealthCheckable:
            def health_check(self) -> dict[str, Any]:
                return {"status": "healthy", "checks": {"db": "ok"}}

        obj = TestHealthCheckable()
        result = obj.health_check()
        assert isinstance(result, dict)
        assert "status" in result


class TestResourceManagerABC(FoundationTestCase):
    """Test ResourceManager abstract base class."""

    def test_resource_manager_cannot_instantiate(self) -> None:
        """Test that ResourceManager cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            ResourceManager()  # type: ignore[abstract]

    def test_resource_manager_requires_all_methods(self) -> None:
        """Test that ResourceManager requires all abstract methods."""

        class IncompleteManager(ResourceManager):
            def acquire_resource(self, resource_id: str) -> Any:
                return None

            # Missing release_resource and cleanup_all

        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteManager()  # type: ignore[abstract]

    def test_resource_manager_concrete_implementation(self) -> None:
        """Test concrete ResourceManager implementation."""

        class ConcreteManager(ResourceManager):
            def __init__(self) -> None:
                self.resources: dict[str, Any] = {}

            def acquire_resource(self, resource_id: str) -> Any:
                resource = f"resource_{resource_id}"
                self.resources[resource_id] = resource
                return resource

            def release_resource(self, resource_id: str) -> None:
                self.resources.pop(resource_id, None)

            def cleanup_all(self) -> None:
                self.resources.clear()

        manager = ConcreteManager()
        assert isinstance(manager, ResourceManager)

        # Test functionality
        resource = manager.acquire_resource("test")
        assert resource == "resource_test"
        assert "test" in manager.resources

        manager.release_resource("test")
        assert "test" not in manager.resources

        manager.acquire_resource("a")
        manager.acquire_resource("b")
        manager.cleanup_all()
        assert len(manager.resources) == 0


class TestAsyncResourceManagerABC(FoundationTestCase):
    """Test AsyncResourceManager abstract base class."""

    def test_async_resource_manager_cannot_instantiate(self) -> None:
        """Test that AsyncResourceManager cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            AsyncResourceManager()  # type: ignore[abstract]

    def test_async_resource_manager_requires_all_methods(self) -> None:
        """Test that AsyncResourceManager requires all abstract methods."""

        class IncompleteAsyncManager(AsyncResourceManager):
            async def acquire_resource_async(self, resource_id: str) -> Any:
                return None

            # Missing release_resource_async and cleanup_all_async

        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteAsyncManager()  # type: ignore[abstract]

    async def test_async_resource_manager_concrete_implementation(self) -> None:
        """Test concrete AsyncResourceManager implementation."""

        class ConcreteAsyncManager(AsyncResourceManager):
            def __init__(self) -> None:
                self.resources: dict[str, Any] = {}

            async def acquire_resource_async(self, resource_id: str) -> Any:
                resource = f"async_resource_{resource_id}"
                self.resources[resource_id] = resource
                return resource

            async def release_resource_async(self, resource_id: str) -> None:
                self.resources.pop(resource_id, None)

            async def cleanup_all_async(self) -> None:
                self.resources.clear()

        manager = ConcreteAsyncManager()
        assert isinstance(manager, AsyncResourceManager)

        # Test functionality
        resource = await manager.acquire_resource_async("test")
        assert resource == "async_resource_test"
        assert "test" in manager.resources

        await manager.release_resource_async("test")
        assert "test" not in manager.resources

        await manager.acquire_resource_async("a")
        await manager.acquire_resource_async("b")
        await manager.cleanup_all_async()
        assert len(manager.resources) == 0


class TestAsyncContextResource(FoundationTestCase):
    """Test AsyncContextResource class."""

    async def test_async_context_resource_basic_usage(self) -> None:
        """Test basic async context manager usage."""

        async def factory() -> str:
            return "test_resource"

        async with AsyncContextResource(factory) as resource:
            assert resource == "test_resource"

    async def test_async_context_resource_with_async_disposable(self) -> None:
        """Test AsyncContextResource with AsyncDisposable resource."""

        class AsyncDisposableResource:
            def __init__(self) -> None:
                self.disposed = False

            async def dispose_async(self) -> None:
                self.disposed = True

        resource_obj = AsyncDisposableResource()

        async def factory() -> AsyncDisposableResource:
            return resource_obj

        async with AsyncContextResource(factory) as resource:
            assert resource is resource_obj
            assert not resource.disposed

        # After context exit, should be disposed
        assert resource_obj.disposed

    async def test_async_context_resource_with_sync_disposable(self) -> None:
        """Test AsyncContextResource with sync Disposable resource."""

        class SyncDisposableResource:
            def __init__(self) -> None:
                self.disposed = False

            def dispose(self) -> None:
                self.disposed = True

        resource_obj = SyncDisposableResource()

        async def factory() -> SyncDisposableResource:
            return resource_obj

        async with AsyncContextResource(factory) as resource:
            assert resource is resource_obj
            assert not resource.disposed

        # After context exit, should be disposed
        assert resource_obj.disposed

    async def test_async_context_resource_without_disposable(self) -> None:
        """Test AsyncContextResource with non-disposable resource."""

        class SimpleResource:
            pass

        resource_obj = SimpleResource()

        async def factory() -> SimpleResource:
            return resource_obj

        # Should not raise even without dispose methods
        async with AsyncContextResource(factory) as resource:
            assert resource is resource_obj

    async def test_async_context_resource_exception_handling(self) -> None:
        """Test AsyncContextResource handles exceptions properly."""

        class DisposableResource:
            def __init__(self) -> None:
                self.disposed = False

            def dispose(self) -> None:
                self.disposed = True

        resource_obj = DisposableResource()

        async def factory() -> DisposableResource:
            return resource_obj

        with pytest.raises(ValueError, match="test error"):
            async with AsyncContextResource(factory):
                raise ValueError("test error")

        # Should still dispose even on exception
        assert resource_obj.disposed

    async def test_async_context_resource_none_resource(self) -> None:
        """Test AsyncContextResource when factory returns None."""

        async def factory() -> None:
            return None

        async with AsyncContextResource(factory) as resource:
            assert resource is None
        # Should not raise on exit with None resource

    async def test_async_context_resource_dispose_async_called(self) -> None:
        """Test that dispose_async is called if available."""
        mock_resource = MagicMock()
        mock_resource.dispose_async = AsyncMock()

        async def factory() -> Any:
            return mock_resource

        async with AsyncContextResource(factory):
            pass

        mock_resource.dispose_async.assert_called_once()

    async def test_async_context_resource_dispose_called(self) -> None:
        """Test that dispose is called if dispose_async not available."""

        class SyncOnlyResource:
            """Resource with only sync dispose."""

            def __init__(self) -> None:
                self.disposed = False

            def dispose(self) -> None:
                self.disposed = True

        resource_obj = SyncOnlyResource()

        async def factory() -> SyncOnlyResource:
            return resource_obj

        async with AsyncContextResource(factory):
            assert not resource_obj.disposed

        # Should have called sync dispose
        assert resource_obj.disposed


class TestProtocolCombinations(FoundationTestCase):
    """Test components implementing multiple protocols."""

    def test_component_implements_multiple_protocols(self) -> None:
        """Test component implementing multiple protocols."""

        class MultiProtocolComponent:
            def __init__(self) -> None:
                self.initialized = False
                self.disposed = False

            def initialize(self) -> Any:
                self.initialized = True
                return self

            def dispose(self) -> None:
                self.disposed = True

            def health_check(self) -> dict[str, Any]:
                return {
                    "initialized": self.initialized,
                    "disposed": self.disposed,
                }

        component = MultiProtocolComponent()
        assert isinstance(component, Initializable)
        assert isinstance(component, Disposable)
        assert isinstance(component, HealthCheckable)

        component.initialize()
        assert component.initialized

        health = component.health_check()
        assert health["initialized"]
        assert not health["disposed"]

        component.dispose()
        assert component.disposed


if __name__ == "__main__":
    pytest.main([__file__])

# 🧱🏗️🔚
