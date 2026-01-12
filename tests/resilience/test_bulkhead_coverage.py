#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive coverage tests for bulkhead.py.

These tests target uncovered lines and edge cases in the bulkhead pattern."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.resilience.bulkhead import (
    Bulkhead,
    BulkheadManager,
    get_bulkhead_manager,
)
from provide.foundation.resilience.bulkhead_async import AsyncResourcePool
from provide.foundation.resilience.bulkhead_sync import SyncResourcePool


class TestBulkheadTypeValidation(FoundationTestCase):
    """Test bulkhead type validation for pool mismatches."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_execute_with_async_pool_raises_type_error(self) -> None:
        """Test sync execute() with AsyncResourcePool raises TypeError."""
        # Create bulkhead with AsyncResourcePool
        async_pool = AsyncResourcePool(max_concurrent=5)
        bulkhead = Bulkhead(name="test-async-pool", pool=async_pool)

        # Try to execute sync function with async pool
        with pytest.raises(TypeError, match="Sync execution requires SyncResourcePool"):
            bulkhead.execute(lambda: "result")

    @pytest.mark.asyncio
    async def test_execute_async_with_sync_pool_raises_type_error(self) -> None:
        """Test async execute_async() with SyncResourcePool raises TypeError."""
        # Create bulkhead with SyncResourcePool
        sync_pool = SyncResourcePool(max_concurrent=5)
        bulkhead = Bulkhead(name="test-sync-pool", pool=sync_pool)

        # Try to execute async function with sync pool
        async def async_func() -> str:
            return "result"

        with pytest.raises(TypeError, match="Async execution requires AsyncResourcePool"):
            await bulkhead.execute_async(async_func)


class TestBulkheadEventEmission(FoundationTestCase):
    """Test event emission with and without event bus available."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_emit_event_when_event_bus_unavailable(self) -> None:
        """Test _emit_event when events module is unavailable."""
        sync_pool = SyncResourcePool(max_concurrent=5)
        bulkhead = Bulkhead(name="test-no-events", pool=sync_pool)

        # Mock ImportError for events module import
        def mock_import(name: str, *args: object, **kwargs: object) -> object:
            if "provide.foundation.hub.events" in name:
                raise ImportError("Events module not available")
            return __import__(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            # Should not raise, just silently continue
            bulkhead._emit_event("test_operation", test_data="value")

    @pytest.mark.asyncio
    async def test_emit_event_async_when_event_bus_unavailable(self) -> None:
        """Test _emit_event_async when events module is unavailable."""
        async_pool = AsyncResourcePool(max_concurrent=5)
        bulkhead = Bulkhead(name="test-no-async-events", pool=async_pool)

        # Mock ImportError for events module import
        def mock_import(name: str, *args: object, **kwargs: object) -> object:
            if "provide.foundation.hub.events" in name:
                raise ImportError("Events module not available")
            return __import__(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            # Should not raise, just silently continue
            await bulkhead._emit_event_async("test_operation", test_data="value")


class TestBulkheadGetStatus(FoundationTestCase):
    """Test get_status() with different pool types."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_get_status_with_sync_pool(self) -> None:
        """Test get_status() returns pool stats for SyncResourcePool."""
        sync_pool = SyncResourcePool(max_concurrent=10)
        bulkhead = Bulkhead(name="sync-status", pool=sync_pool)

        status = bulkhead.get_status()

        assert status["name"] == "sync-status"
        assert "pool" in status
        # Pool stats should contain data
        assert isinstance(status["pool"], dict)

    def test_get_status_with_async_pool(self) -> None:
        """Test get_status() with AsyncResourcePool returns empty pool dict."""
        async_pool = AsyncResourcePool(max_concurrent=10)
        bulkhead = Bulkhead(name="async-status", pool=async_pool)

        status = bulkhead.get_status()

        # Can't get async pool stats in sync context
        assert status["name"] == "async-status"
        assert status["pool"] == {}

    @pytest.mark.asyncio
    async def test_get_status_async_with_async_pool(self) -> None:
        """Test get_status_async() returns pool stats for AsyncResourcePool."""
        async_pool = AsyncResourcePool(max_concurrent=10)
        bulkhead = Bulkhead(name="async-status-async", pool=async_pool)

        status = await bulkhead.get_status_async()

        assert status["name"] == "async-status-async"
        assert "pool" in status
        # Pool stats should contain data
        assert isinstance(status["pool"], dict)

    @pytest.mark.asyncio
    async def test_get_status_async_with_sync_pool(self) -> None:
        """Test get_status_async() can get sync pool stats from async context."""
        sync_pool = SyncResourcePool(max_concurrent=10)
        bulkhead = Bulkhead(name="sync-from-async", pool=sync_pool)

        status = await bulkhead.get_status_async()

        # Can get sync pool stats from async context
        assert status["name"] == "sync-from-async"
        assert "pool" in status
        assert isinstance(status["pool"], dict)


class TestBulkheadManagerAsyncPool(FoundationTestCase):
    """Test BulkheadManager async pool creation."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.manager = BulkheadManager()

    def test_create_bulkhead_with_async_pool(self) -> None:
        """Test creating bulkhead with use_async_pool=True."""
        bulkhead = self.manager.create_bulkhead(
            name="async-bulkhead",
            max_concurrent=5,
            max_queue_size=50,
            timeout=10.0,
            use_async_pool=True,
        )

        assert bulkhead.name == "async-bulkhead"
        assert isinstance(bulkhead.pool, AsyncResourcePool)
        # Verify pool configuration
        assert bulkhead.pool.max_concurrent == 5

    def test_create_bulkhead_with_sync_pool_default(self) -> None:
        """Test creating bulkhead with default sync pool."""
        bulkhead = self.manager.create_bulkhead(
            name="sync-bulkhead",
            max_concurrent=8,
        )

        assert bulkhead.name == "sync-bulkhead"
        assert isinstance(bulkhead.pool, SyncResourcePool)
        assert bulkhead.pool.max_concurrent == 8

    def test_create_bulkhead_returns_existing(self) -> None:
        """Test create_bulkhead returns existing bulkhead if name exists."""
        # Create first bulkhead
        bulkhead1 = self.manager.create_bulkhead("duplicate", max_concurrent=5)

        # Create with same name should return existing
        bulkhead2 = self.manager.create_bulkhead("duplicate", max_concurrent=10)

        assert bulkhead1 is bulkhead2
        # Should still have original config
        assert bulkhead1.pool.max_concurrent == 5


class TestBulkheadManagerOperations(FoundationTestCase):
    """Test BulkheadManager CRUD operations."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.manager = BulkheadManager()

    def test_get_bulkhead_returns_none_when_not_found(self) -> None:
        """Test get_bulkhead returns None for non-existent bulkhead."""
        result = self.manager.get_bulkhead("non-existent")

        assert result is None

    def test_get_bulkhead_returns_existing_bulkhead(self) -> None:
        """Test get_bulkhead returns existing bulkhead."""
        # Create bulkhead
        created = self.manager.create_bulkhead("existing")

        # Get it back
        retrieved = self.manager.get_bulkhead("existing")

        assert retrieved is created
        assert retrieved.name == "existing"

    def test_list_bulkheads_empty(self) -> None:
        """Test list_bulkheads returns empty list initially."""
        bulkheads = self.manager.list_bulkheads()

        assert bulkheads == []

    def test_list_bulkheads_multiple(self) -> None:
        """Test list_bulkheads returns all bulkhead names."""
        # Create multiple bulkheads
        self.manager.create_bulkhead("first")
        self.manager.create_bulkhead("second")
        self.manager.create_bulkhead("third")

        bulkheads = self.manager.list_bulkheads()

        assert len(bulkheads) == 3
        assert "first" in bulkheads
        assert "second" in bulkheads
        assert "third" in bulkheads

    def test_get_all_status_empty(self) -> None:
        """Test get_all_status returns empty dict initially."""
        status = self.manager.get_all_status()

        assert status == {}

    def test_get_all_status_multiple(self) -> None:
        """Test get_all_status returns status for all bulkheads."""
        # Create bulkheads
        self.manager.create_bulkhead("bulkhead1")
        self.manager.create_bulkhead("bulkhead2")

        status = self.manager.get_all_status()

        assert len(status) == 2
        assert "bulkhead1" in status
        assert "bulkhead2" in status
        assert status["bulkhead1"]["name"] == "bulkhead1"
        assert status["bulkhead2"]["name"] == "bulkhead2"

    def test_remove_bulkhead_success(self) -> None:
        """Test remove_bulkhead removes existing bulkhead."""
        # Create bulkhead
        self.manager.create_bulkhead("to-remove")

        # Remove it
        result = self.manager.remove_bulkhead("to-remove")

        assert result is True
        # Verify it's gone
        assert self.manager.get_bulkhead("to-remove") is None
        assert "to-remove" not in self.manager.list_bulkheads()

    def test_remove_bulkhead_not_found(self) -> None:
        """Test remove_bulkhead returns False for non-existent bulkhead."""
        result = self.manager.remove_bulkhead("non-existent")

        assert result is False


class TestBulkheadManagerThreadSafety(FoundationTestCase):
    """Test BulkheadManager thread safety."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.manager = BulkheadManager()

    def test_concurrent_create_bulkhead(self) -> None:
        """Test creating bulkheads concurrently."""
        import threading

        results = []

        def create_bulkhead(name: str) -> None:
            bulkhead = self.manager.create_bulkhead(name)
            results.append(bulkhead)

        # Create multiple threads trying to create different bulkheads
        threads = [threading.Thread(target=create_bulkhead, args=(f"bulkhead-{i}",)) for i in range(5)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # All bulkheads should be created
        assert len(results) == 5
        assert len(self.manager.list_bulkheads()) == 5

    def test_concurrent_access_same_bulkhead(self) -> None:
        """Test concurrent access to same bulkhead name."""
        import threading

        results = []

        def get_or_create(name: str) -> None:
            bulkhead = self.manager.create_bulkhead(name)
            results.append(bulkhead)

        # Multiple threads trying to get/create same bulkhead
        threads = [threading.Thread(target=get_or_create, args=("shared",)) for _ in range(5)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # All threads should get the same bulkhead instance
        assert len(results) == 5
        first_instance = results[0]
        assert all(bulkhead is first_instance for bulkhead in results)


class TestGlobalBulkheadManager(FoundationTestCase):
    """Test global bulkhead manager singleton."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_get_bulkhead_manager_returns_singleton(self) -> None:
        """Test get_bulkhead_manager returns same instance."""
        manager1 = get_bulkhead_manager()
        manager2 = get_bulkhead_manager()

        assert manager1 is manager2

    def test_get_bulkhead_manager_type(self) -> None:
        """Test get_bulkhead_manager returns BulkheadManager."""
        manager = get_bulkhead_manager()

        assert isinstance(manager, BulkheadManager)


__all__ = [
    "TestBulkheadEventEmission",
    "TestBulkheadGetStatus",
    "TestBulkheadManagerAsyncPool",
    "TestBulkheadManagerOperations",
    "TestBulkheadManagerThreadSafety",
    "TestBulkheadTypeValidation",
    "TestGlobalBulkheadManager",
]

# 🧱🏗️🔚
