"""Thread safety tests for provide-foundation."""

import concurrent.futures
import threading
import time

import pytest

from provide.foundation.hub import (
    clear_hub,
    get_hub,
    register_command,
    register_component,
)
from provide.foundation.registry import Registry


class TestRegistryThreadSafety:
    """Test thread safety of the Registry class."""

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
                        f"Thread {thread_id}: Expected value_{i}, got {value}"
                    )

        # Create multiple threads that read from registry
        threads = []
        for thread_id in range(10):
            thread = threading.Thread(target=get_items, args=(thread_id,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Verify no mismatched values
        assert len(results) == 0, f"Mismatched values: {results}"

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
                    time.sleep(0.001)  # Small delay to increase contention
            except Exception as e:
                errors.append(f"Writer {thread_id}: {e}")

        def reader_thread(thread_id: int) -> None:
            """Thread that reads from registry."""
            try:
                for _ in range(100):
                    registry.list_dimension("mixed")
                    # Just accessing the list, checking it doesn't crash
                    time.sleep(0.001)
            except Exception as e:
                errors.append(f"Reader {thread_id}: {e}")

        def remover_thread(thread_id: int) -> None:
            """Thread that removes from registry."""
            try:
                for i in range(25):
                    # Try to remove items that may or may not exist
                    registry.remove(f"writer_0_{i}", dimension="mixed")
                    time.sleep(0.002)
            except Exception as e:
                errors.append(f"Remover {thread_id}: {e}")

        # Start mixed operations
        threads = []

        # Start writers
        for i in range(3):
            thread = threading.Thread(target=writer_thread, args=(i,))
            threads.append(thread)
            thread.start()

        # Start readers
        for i in range(3):
            thread = threading.Thread(target=reader_thread, args=(i,))
            threads.append(thread)
            thread.start()

        # Start remover after a small delay
        time.sleep(0.01)
        thread = threading.Thread(target=remover_thread, args=(0,))
        threads.append(thread)
        thread.start()

        # Wait for all threads
        for thread in threads:
            thread.join()

        # Verify no errors
        assert len(errors) == 0, f"Errors occurred: {errors}"

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
                        f"Thread {thread_id}: Dimension not empty after clear"
                    )
            except Exception as e:
                errors.append(f"Thread {thread_id}: {e}")

        # Run multiple threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(populate_and_clear, i) for i in range(5)]
            concurrent.futures.wait(futures)

        assert len(errors) == 0, f"Errors occurred: {errors}"


class TestHubThreadSafety:
    """Test thread safety of the Hub singleton."""

    def setup_method(self) -> None:
        """Clear hub before each test."""
        clear_hub()

    def teardown_method(self) -> None:
        """Clear hub after each test."""
        clear_hub()

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
            thread = threading.Thread(target=get_hub_instance)
            threads.append(thread)

        # Start all threads at once
        for thread in threads:
            thread.start()

        # Wait for all threads
        for thread in threads:
            thread.join()

        # Verify all threads got the same hub instance
        assert len(hub_instances) == 20
        first_hub = hub_instances[0]
        for hub in hub_instances:
            assert hub is first_hub, "Different hub instances returned!"

    @pytest.mark.serial
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
                    def cmd() -> str:
                        return f"result_{thread_id}_{i}"
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

    @pytest.mark.serial
    def test_concurrent_component_registration(self) -> None:
        """Test concurrent component registration."""
        clear_hub()  # Ensure clean state
        errors = []
        hub = get_hub()

        def register_components(thread_id: int) -> None:
            """Register components from a thread."""
            try:
                for i in range(10):

                    @register_component(f"comp_{thread_id}_{i}")
                    class Component:
                        pass
            except Exception as e:
                errors.append(f"Thread {thread_id}: {e}")

        # Run concurrent registrations
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(register_components, i) for i in range(5)]
            concurrent.futures.wait(futures)

        assert len(errors) == 0, f"Errors occurred: {errors}"

        # Verify all components registered
        components = hub.list_components()
        assert len(components) == 50

    def test_hub_clear_thread_safety(self) -> None:
        """Test that clear_hub is thread-safe."""
        errors = []

        def hub_operations(thread_id: int) -> None:
            """Perform hub operations."""
            try:
                # Get hub
                hub = get_hub()

                # Add a command
                hub.add_command(lambda: f"cmd_{thread_id}", name=f"cmd_{thread_id}")

                # Clear hub (only one thread should succeed)
                if thread_id == 0:
                    time.sleep(0.01)  # Small delay
                    clear_hub()

                # Try to get hub again
                get_hub()
                # This should work - either same hub or new one

            except Exception as e:
                errors.append(f"Thread {thread_id}: {e}")

        # Run operations
        threads = []
        for i in range(5):
            thread = threading.Thread(target=hub_operations, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        assert len(errors) == 0, f"Errors occurred: {errors}"


class TestLoggerThreadSafety:
    """Test that logger remains thread-safe."""

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
            futures = [
                executor.submit(get_named_logger, f"logger_{i}") for i in range(20)
            ]
            concurrent.futures.wait(futures)

        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(loggers) == 20


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
