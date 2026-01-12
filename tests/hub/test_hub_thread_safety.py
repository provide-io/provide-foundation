#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Thread safety tests for provide-foundation."""

from __future__ import annotations

import concurrent.futures
import threading

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.hub import (
    clear_hub,
    get_hub,
    register_command,
)
from provide.foundation.hub.registry import Registry


class TestRegistryThreadSafety(FoundationTestCase):
    """Test thread safety of the Registry class."""

    @pytest.mark.slow
    def test_concurrent_registration(self) -> None:
        """Test concurrent registration doesn't cause race conditions."""
        registry = Registry()
        errors = []
        successful_registrations = []

        def register_item(thread_id: int, item_id: int) -> None:
            """Register an item from a thread."""
            try:
                name = f"item_{thread_id}_{item_id}"
                registry.register(
                    name=name,
                    value=f"value_{thread_id}_{item_id}",
                    dimension="test",
                    metadata={"thread": thread_id, "item": item_id},
                )
                successful_registrations.append((thread_id, item_id))
            except Exception as e:
                errors.append((thread_id, item_id, str(e)))

        # Create multiple threads that register items
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for thread_id in range(10):
                for item_id in range(100):
                    future = executor.submit(register_item, thread_id, item_id)
                    futures.append(future)

            # Wait for all registrations to complete
            concurrent.futures.wait(futures)

        # Verify no errors occurred
        assert len(errors) == 0, f"Errors occurred: {errors}"

        # Verify all items were registered
        assert len(successful_registrations) == 1000

        # Verify registry contains all items
        all_items = registry.list_dimension("test")
        assert len(all_items) == 1000

    @pytest.mark.slow
    def test_concurrent_get_operations(self) -> None:
        """Test concurrent get operations are thread-safe."""
        registry = Registry()

        # Pre-populate registry
        for i in range(100):
            registry.register(f"item_{i}", f"value_{i}", dimension="test")

        results = []

        def get_items(thread_id: int) -> None:
            """Get items from registry."""
            for i in range(100):
                value = registry.get(f"item_{i}", dimension="test")
                if value != f"value_{i}":
                    results.append(
                        f"Thread {thread_id}: Expected value_{i}, got {value}",
                    )

        # Create multiple threads that read from registry
        threads = []
        for thread_id in range(10):
            thread = threading.Thread(daemon=True, target=get_items, args=(thread_id,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=10.0)

        # Verify no mismatched values
        assert len(results) == 0, f"Mismatched values: {results}"

    @pytest.mark.slow
    def test_concurrent_mixed_operations(self) -> None:
        """Test mixed read/write operations are thread-safe."""
        registry = Registry()
        errors = []

        def writer_thread(thread_id: int) -> None:
            """Thread that writes to registry."""
            try:
                for i in range(50):
                    registry.register(
                        f"writer_{thread_id}_{i}",
                        f"value_{thread_id}_{i}",
                        dimension="mixed",
                    )
                    pass  # Small delay to increase contention
            except Exception as e:
                errors.append(f"Writer {thread_id}: {e}")

        def reader_thread(thread_id: int) -> None:
            """Thread that reads from registry."""
            try:
                for _ in range(100):
                    registry.list_dimension("mixed")
                    # Just accessing the list, checking it doesn't crash
                    pass  # Small delay
            except Exception as e:
                errors.append(f"Reader {thread_id}: {e}")

        def remover_thread(thread_id: int) -> None:
            """Thread that removes from registry."""
            try:
                for i in range(25):
                    # Try to remove items that may or may not exist
                    registry.remove(f"writer_0_{i}", dimension="mixed")
                    pass  # Small delay
            except Exception as e:
                errors.append(f"Remover {thread_id}: {e}")

        # Start mixed operations
        threads = []

        # Start writers
        for i in range(3):
            thread = threading.Thread(daemon=True, target=writer_thread, args=(i,))
            threads.append(thread)
            thread.start()

        # Start readers
        for i in range(3):
            thread = threading.Thread(daemon=True, target=reader_thread, args=(i,))
            threads.append(thread)
            thread.start()

        # Start remover after a small delay
        pass  # Small delay
        thread = threading.Thread(daemon=True, target=remover_thread, args=(0,))
        threads.append(thread)
        thread.start()

        # Wait for all threads
        for thread in threads:
            thread.join(timeout=10.0)

        # Verify no errors
        assert len(errors) == 0, f"Errors occurred: {errors}"

    @pytest.mark.slow
    def test_registry_clear_thread_safety(self) -> None:
        """Test that clear operation is thread-safe."""
        registry = Registry()
        errors = []

        def populate_and_clear(thread_id: int) -> None:
            """Populate and then clear a dimension."""
            try:
                dim = f"dim_{thread_id}"
                for i in range(10):
                    registry.register(f"item_{i}", i, dimension=dim)

                # Clear the dimension
                registry.clear(dimension=dim)

                # Verify it's empty
                items = registry.list_dimension(dim)
                if len(items) != 0:
                    errors.append(
                        f"Thread {thread_id}: Dimension not empty after clear",
                    )
            except Exception as e:
                errors.append(f"Thread {thread_id}: {e}")

        # Run multiple threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(populate_and_clear, i) for i in range(5)]
            concurrent.futures.wait(futures)

        assert len(errors) == 0, f"Errors occurred: {errors}"


class TestHubThreadSafety(FoundationTestCase):
    """Test thread safety of the Hub singleton."""

    def setup_method(self) -> None:
        """Clear hub before each test."""
        clear_hub()

    def teardown_method(self) -> None:
        """Clear hub after each test."""
        clear_hub()

    @pytest.mark.slow
    def test_concurrent_hub_initialization(self) -> None:
        """Test that get_hub() is thread-safe during initialization."""
        hub_instances = []

        def get_hub_instance() -> None:
            """Get hub instance and store it."""
            hub = get_hub()
            hub_instances.append(hub)

        # Create multiple threads that all try to get hub at once
        threads = []
        for _ in range(20):
            thread = threading.Thread(daemon=True, target=get_hub_instance)
            threads.append(thread)

        # Start all threads at once
        for thread in threads:
            thread.start()

        # Wait for all threads
        for thread in threads:
            thread.join(timeout=10.0)

        # Verify all threads got the same hub instance
        assert len(hub_instances) == 20
        first_hub = hub_instances[0]
        for hub in hub_instances:
            assert hub is first_hub, "Different hub instances returned!"

    @pytest.mark.serial
    @pytest.mark.slow
    def test_concurrent_command_registration(self) -> None:
        """Test concurrent command registration via decorators."""
        clear_hub()  # Ensure clean state
        errors = []
        hub = get_hub()

        def register_commands(thread_id: int) -> None:
            """Register commands from a thread."""
            try:
                for i in range(10):

                    @register_command(f"cmd_{thread_id}_{i}")
                    def cmd(tid: int = thread_id, idx: int = i) -> str:
                        return f"result_{tid}_{idx}"
            except Exception as e:
                errors.append(f"Thread {thread_id}: {e}")

        # Run concurrent registrations
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(register_commands, i) for i in range(5)]
            concurrent.futures.wait(futures)

        assert len(errors) == 0, f"Errors occurred: {errors}"

        # Verify all commands registered
        commands = hub.list_commands()
        assert len(commands) == 50

    # Legacy test removed - register_component decorator no longer exists
    # Original test was for concurrent component registration via decorators
    # which has been replaced by the registry-based component system
    @pytest.mark.serial
    @pytest.mark.slow
    def test_concurrent_component_registration(self) -> None:
        """Test concurrent component registration - legacy test removed."""
        # Test replacement: verify registry operations are thread-safe
        clear_hub()
        hub = get_hub()
        registry = hub._component_registry
        errors = []

        def register_via_registry(thread_id: int) -> None:
            """Register components via registry directly."""
            try:
                for i in range(10):
                    registry.register(
                        name=f"comp_{thread_id}_{i}",
                        value=type(f"Component_{thread_id}_{i}", (), {}),
                        dimension="component",
                    )
            except Exception as e:
                errors.append(f"Thread {thread_id}: {e}")

        # Run concurrent registrations
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(register_via_registry, i) for i in range(5)]
            concurrent.futures.wait(futures)

        assert len(errors) == 0, f"Errors occurred: {errors}"

        # Verify all components registered
        components = registry.list_dimension("component")
        assert len(components) == 50

    @pytest.mark.slow
    def test_hub_clear_thread_safety(self) -> None:
        """Test that clear_hub results in a new hub instance for subsequent calls."""
        errors = []

        # Get the initial hub instance
        hub1 = get_hub()
        assert hub1 is not None

        # Clear the hub
        clear_hub()

        # In multiple threads, get the hub again and check it's a new, consistent instance
        hub_instances = []

        def get_new_hub_instance() -> None:
            try:
                hub = get_hub()
                hub_instances.append(hub)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(daemon=True, target=get_new_hub_instance) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=10.0)

        assert not errors, f"Errors occurred during re-initialization: {errors}"
        assert len(hub_instances) == 5

        # All threads should have received the same NEW hub instance
        hub2 = hub_instances[0]
        assert all(h is hub2 for h in hub_instances)

        # The new hub should be different from the original one
        assert hub1 is not hub2


class TestLoggerThreadSafety(FoundationTestCase):
    """Test that logger remains thread-safe."""

    @pytest.mark.slow
    def test_concurrent_logging(self) -> None:
        """Test that multiple threads can log concurrently."""
        from provide.foundation import logger

        errors = []

        def log_messages(thread_id: int) -> None:
            """Log messages from a thread."""
            try:
                for i in range(100):
                    logger.debug(f"Debug from thread {thread_id}", iteration=i)
                    logger.info(f"Info from thread {thread_id}", iteration=i)
                    logger.warning(f"Warning from thread {thread_id}", iteration=i)
                    logger.error(f"Error from thread {thread_id}", iteration=i)
            except Exception as e:
                errors.append(f"Thread {thread_id}: {e}")

        # Run concurrent logging
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(log_messages, i) for i in range(10)]
            concurrent.futures.wait(futures)

        assert len(errors) == 0, f"Errors occurred: {errors}"

    @pytest.mark.slow
    def test_logger_configuration_thread_safety(self) -> None:
        """Test that logger configuration is thread-safe."""
        from provide.foundation import get_logger

        errors = []
        loggers = []

        def get_named_logger(name: str) -> None:
            """Get a named logger."""
            try:
                logger = get_logger(name)
                loggers.append(logger)
                # Try to log something
                logger.info(f"Test from {name}")
            except Exception as e:
                errors.append(f"Logger {name}: {e}")

        # Get multiple named loggers concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(get_named_logger, f"logger_{i}") for i in range(20)]
            concurrent.futures.wait(futures)

        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(loggers) == 20


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# 🧱🏗️🔚
