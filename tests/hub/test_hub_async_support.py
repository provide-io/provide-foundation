#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Async support tests for provide-foundation."""

from __future__ import annotations

import asyncio
from typing import Any

from attrs import define
from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.hub import (
    clear_hub,
    get_hub,
    register_command,
)
from provide.foundation.hub.registry import Registry
from provide.foundation.logger import get_logger


class TestAsyncRegistryCompatibility(FoundationTestCase):
    """Test Registry works correctly with async operations."""

    @pytest.mark.asyncio
    async def test_registry_operations_in_async_context(self) -> None:
        """Test Registry operations work within async functions."""
        registry = Registry()

        # Test registration in async context
        async def register_items() -> bool:
            for i in range(10):
                registry.register(f"item_{i}", f"value_{i}", dimension="async_test")
                await asyncio.sleep(0)  # Yield control
            return True

        result = await register_items()
        assert result is True

        # Verify all items registered
        items = registry.list_dimension("async_test")
        assert len(items) == 10

        # Test retrieval in async context
        async def get_items() -> list[str]:
            results: list[str] = []
            for i in range(10):
                value = registry.get(f"item_{i}", dimension="async_test")
                if value is not None:
                    results.append(value)
                await asyncio.sleep(0)
            return results

        values = await get_items()
        assert all(values[i] == f"value_{i}" for i in range(10))

    @pytest.mark.asyncio
    async def test_concurrent_async_registry_operations(self) -> None:
        """Test Registry handles concurrent async operations."""
        registry = Registry()

        async def register_batch(batch_id: int) -> int:
            """Register a batch of items asynchronously."""
            for i in range(10):
                registry.register(
                    f"batch_{batch_id}_item_{i}",
                    f"value_{batch_id}_{i}",
                    dimension="async_batch",
                )
                await asyncio.sleep(0)  # Minimal async yield
            return batch_id

        # Run multiple batches concurrently
        tasks = [register_batch(i) for i in range(5)]
        results = await asyncio.gather(*tasks)

        assert results == [0, 1, 2, 3, 4]

        # Verify all items registered
        items = registry.list_dimension("async_batch")
        assert len(items) == 50

    @pytest.mark.asyncio
    async def test_registry_iteration_in_async(self) -> None:
        """Test Registry iteration works in async context."""
        registry = Registry()

        # Populate registry
        for i in range(20):
            registry.register(f"async_item_{i}", i, dimension="iter_test")

        # Iterate in async context
        async def iterate_registry() -> list[Any]:
            entries = []
            for entry in registry:
                if entry.dimension == "iter_test":
                    entries.append(entry)
                    await asyncio.sleep(0)  # Yield control
            return entries

        entries = await iterate_registry()
        assert len(entries) == 20
        assert all(e.dimension == "iter_test" for e in entries)


class TestAsyncHubCompatibility(FoundationTestCase):
    """Test Hub works correctly with async operations."""

    def setup_method(self) -> None:
        """Clear hub before each test."""
        clear_hub()

    def teardown_method(self) -> None:
        """Clear hub after each test."""
        clear_hub()

    @pytest.mark.asyncio
    async def test_hub_operations_in_async_context(self) -> None:
        """Test Hub operations work within async functions."""
        hub = get_hub()

        # Legacy test removed - register_component decorator no longer exists in current hub architecture
        # This test was testing component registration via decorator which has been replaced
        # by the registry-based component system

        # Test basic hub access in async context
        async def test_hub_access() -> bool:
            for _i in range(5):
                # Test hub access doesn't fail in async context
                current_hub = get_hub()
                assert current_hub is hub
                await asyncio.sleep(0)
            return True

        result = await test_hub_access()
        assert result is True

    @pytest.mark.asyncio
    async def test_concurrent_async_hub_access(self) -> None:
        """Test multiple async tasks can access hub concurrently."""

        async def task1() -> str:
            hub = get_hub()
            for i in range(10):
                hub.add_command(lambda idx=i: f"cmd1_{idx}", f"async_cmd1_{i}")
                await asyncio.sleep(0)  # Minimal async yield
            return "task1_done"

        async def task2() -> str:
            hub = get_hub()
            for i in range(10):
                hub.add_command(lambda idx=i: f"cmd2_{idx}", f"async_cmd2_{i}")
                await asyncio.sleep(0)  # Minimal async yield
            return "task2_done"

        async def task3() -> str:
            hub = get_hub()
            for _ in range(20):
                commands = hub.list_commands()
                await asyncio.sleep(0)  # Minimal async yield
            return f"found_{len(commands)}_commands"

        # Run all tasks concurrently
        results = await asyncio.gather(task1(), task2(), task3())

        assert "task1_done" in results
        assert "task2_done" in results

        # Verify all commands registered
        hub = get_hub()
        commands = hub.list_commands()
        cmd1_count = sum(1 for c in commands if c.startswith("async_cmd1_"))
        cmd2_count = sum(1 for c in commands if c.startswith("async_cmd2_"))
        assert cmd1_count == 10
        assert cmd2_count == 10


class TestAsyncLoggerCompatibility(FoundationTestCase):
    """Test Logger works correctly with async operations."""

    @pytest.mark.asyncio
    async def test_logger_in_async_context(self) -> None:
        """Test logger operations work within async functions."""
        logger = get_logger("async_test")

        async def log_messages() -> bool:
            for i in range(10):
                logger.info(f"Async message {i}", index=i)
                logger.debug(f"Debug message {i}", index=i)
                await asyncio.sleep(0)
            return True

        result = await log_messages()
        assert result is True

    @pytest.mark.asyncio
    async def test_concurrent_async_logging(self) -> None:
        """Test multiple async tasks can log concurrently."""

        async def log_task(task_id: int) -> str:
            logger = get_logger(f"async_task_{task_id}")
            for i in range(20):
                logger.info(f"Task {task_id} message {i}")
                await asyncio.sleep(0)  # Minimal async yield
            return f"task_{task_id}_complete"

        # Run multiple logging tasks concurrently
        tasks = [log_task(i) for i in range(5)]
        results = await asyncio.gather(*tasks)

        assert all(f"task_{i}_complete" in results for i in range(5))


class TestAsyncContextManagers(FoundationTestCase):
    """Test async context manager patterns."""

    @pytest.mark.asyncio
    async def test_async_component_lifecycle(self) -> None:
        """Test component lifecycle in async context."""

        @define
        class AsyncResource:
            name: str
            initialized: bool = False
            cleaned_up: bool = False

            async def initialize(self) -> None:
                await asyncio.sleep(0)  # Minimal async yield
                self.initialized = True

            async def cleanup(self) -> None:
                await asyncio.sleep(0)  # Minimal async yield
                self.cleaned_up = True

        # Test manual lifecycle
        resource = AsyncResource("test_resource")
        assert not resource.initialized

        await resource.initialize()
        assert resource.initialized

        await resource.cleanup()
        assert resource.cleaned_up

    @pytest.mark.asyncio
    async def test_async_with_sync_registry(self) -> None:
        """Test async wrapper around sync Registry."""

        class AsyncRegistry:
            """Async wrapper for Registry operations."""

            def __init__(self) -> None:
                self._registry = Registry()

            async def register(self, name: str, value: Any, dimension: str = "default") -> Any:
                # Simulate async operation that uses sync registry
                await asyncio.sleep(0)
                return self._registry.register(name, value, dimension)

            async def get(self, name: str, dimension: str | None = None) -> Any:
                await asyncio.sleep(0)
                return self._registry.get(name, dimension)

            async def list_dimension(self, dimension: str) -> list[str]:
                await asyncio.sleep(0)
                return self._registry.list_dimension(dimension)

        async_registry = AsyncRegistry()

        # Test async operations
        await async_registry.register("async_key", "async_value", "async_dim")
        value = await async_registry.get("async_key", "async_dim")
        assert value == "async_value"

        items = await async_registry.list_dimension("async_dim")
        assert "async_key" in items


class TestAsyncTaskCoordination(FoundationTestCase):
    """Test coordination of async tasks with foundation components."""

    @pytest.mark.asyncio
    async def test_producer_consumer_pattern(self) -> None:
        """Test producer-consumer pattern with Registry."""
        registry = Registry()

        async def producer(producer_id: int, count: int) -> str:
            """Produce items and register them."""
            for i in range(count):
                item_name = f"producer_{producer_id}_item_{i}"
                registry.register(item_name, i, dimension="queue")
                await asyncio.sleep(0)  # Minimal async yield
            return f"producer_{producer_id}_done"

        async def consumer(consumer_id: int, max_items: int) -> str:
            """Consume items from registry."""
            consumed = []
            for _ in range(max_items):
                items = registry.list_dimension("queue")
                if items:
                    # Simulate consuming first item
                    item = items[0]
                    value = registry.get(item, dimension="queue")
                    if value is not None:
                        consumed.append((item, value))
                        registry.remove(item, dimension="queue")
                await asyncio.sleep(0)  # Minimal async yield
            return f"consumer_{consumer_id}_consumed_{len(consumed)}"

        # Run producers and consumers concurrently
        producers = [producer(i, 5) for i in range(2)]
        consumers = [consumer(i, 5) for i in range(2)]

        results = await asyncio.gather(*producers, *consumers)

        assert all("producer" in r or "consumer" in r for r in results)
        # Verify queue is empty or has few items left
        remaining = registry.list_dimension("queue")
        assert len(remaining) <= 2  # Some race condition tolerance

    @pytest.mark.asyncio
    async def test_async_event_handling(self) -> None:
        """Test async event handling with Hub."""
        hub = get_hub()
        events = []

        async def event_handler(event_type: str, data: Any) -> None:
            """Handle events asynchronously."""
            await asyncio.sleep(0)  # Minimal async yield
            events.append((event_type, data))

        # Register event handlers as commands using decorator
        async def setup_handlers() -> None:
            for event_type in ["start", "process", "complete"]:

                @register_command(f"handle_{event_type}")
                async def handler(etype: str = event_type) -> None:
                    await event_handler(etype, {"timestamp": 1000.0})  # Fixed timestamp for tests

                await asyncio.sleep(0)

        await setup_handlers()

        # Verify handlers registered
        commands = hub.list_commands()
        handlers = [c for c in commands if c.startswith("handle_")]
        assert len(handlers) == 3


class TestAsyncMixedOperations(FoundationTestCase):
    """Test mixing sync and async operations."""

    @pytest.mark.asyncio
    async def test_sync_in_async_context(self) -> None:
        """Test sync operations work correctly in async context."""
        registry = Registry()

        async def mixed_operations() -> str:
            # Sync operation
            registry.register("sync_item", "sync_value", dimension="mixed")

            # Async sleep
            await asyncio.sleep(0)  # Minimal async yield

            # Another sync operation
            value = registry.get("sync_item", dimension="mixed")

            # Async sleep
            await asyncio.sleep(0)  # Minimal async yield

            # More sync operations
            registry.remove("sync_item", dimension="mixed")

            return value or ""

        result = await mixed_operations()
        assert result == "sync_value"

        # Verify item removed
        items = registry.list_dimension("mixed")
        assert len(items) == 0

    @pytest.mark.asyncio
    async def test_concurrent_sync_async_access(self) -> None:
        """Test concurrent access from sync and async contexts."""
        registry = Registry()
        get_hub()

        async def async_writer() -> str:
            for i in range(10):
                registry.register(f"async_{i}", i, dimension="concurrent")
                await asyncio.sleep(0)  # Minimal async yield
            return "async_done"

        def sync_writer() -> str:
            for i in range(10):
                registry.register(f"sync_{i}", i, dimension="concurrent")
            return "sync_done"

        async def async_reader() -> list[int]:
            counts = []
            for _ in range(5):
                items = registry.list_dimension("concurrent")
                counts.append(len(items))
                await asyncio.sleep(0)  # Minimal async yield
            return counts

        # Run async writer and reader
        async_task = asyncio.create_task(async_writer())
        reader_task = asyncio.create_task(async_reader())

        # Run sync writer in thread executor
        loop = asyncio.get_event_loop()
        sync_result = await loop.run_in_executor(None, sync_writer)

        # Wait for async tasks
        async_result = await async_task
        counts = await reader_task

        assert async_result == "async_done"
        assert sync_result == "sync_done"
        assert max(counts) <= 20  # Should see incremental growth

        # Final verification
        final_items = registry.list_dimension("concurrent")
        assert len(final_items) == 20


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# 🧱🏗️🔚
