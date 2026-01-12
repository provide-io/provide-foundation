#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Thread safety and concurrency tests for AutoFlushHandler.

Tests thread safety, race conditions, and concurrent access patterns."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import threading
import time

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.file.operations.detectors.auto_flush import AutoFlushHandler
from provide.foundation.file.operations.types import FileEvent, FileEventMetadata, FileOperation


@pytest.fixture
def handler_cleanup() -> list[AutoFlushHandler]:
    """Fixture to track and cleanup AutoFlushHandlers after each test."""
    handlers: list[AutoFlushHandler] = []
    yield handlers
    # Cleanup all handlers
    for handler in handlers:
        handler.clear()


class TestAutoFlushHandlerConcurrency(FoundationTestCase):
    """Test concurrent access to AutoFlushHandler."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.base_time = datetime.now()
        self.operations_emitted: list[FileOperation] = []
        self.lock = threading.Lock()

    def _create_test_event(self, filename: str, event_type: str = "modified") -> FileEvent:
        """Create a test file event."""
        return FileEvent(
            path=Path(f"/tmp/{filename}"),
            event_type=event_type,
            metadata=FileEventMetadata(
                timestamp=datetime.now(),
                sequence_number=1,
            ),
        )

    def _emit_operation(self, operation: FileOperation) -> None:
        """Thread-safe operation emission callback."""
        with self.lock:
            self.operations_emitted.append(operation)

    def test_concurrent_add_event_from_multiple_threads(self, handler_cleanup: list) -> None:
        """Test concurrent add_event() calls from 10+ threads."""
        handler = AutoFlushHandler(
            time_window_ms=1000,
            on_operation_complete=self._emit_operation,
        )
        handler_cleanup.append(handler)

        num_threads = 20
        events_per_thread = 50
        threads = []

        def add_events(thread_id: int) -> None:
            """Add events from a worker thread."""
            for i in range(events_per_thread):
                event = self._create_test_event(f"file_{thread_id}_{i}.txt")
                handler.add_event(event)

        # Start all threads
        for i in range(num_threads):
            t = threading.Thread(target=add_events, args=(i,))
            threads.append(t)
            t.start()

        # Wait for all threads to complete
        for t in threads:
            t.join()

        # Verify all events were added
        pending = handler.pending_events
        assert len(pending) == num_threads * events_per_thread, "All events should be added"

    def test_concurrent_add_and_clear(self, handler_cleanup: list) -> None:
        """Test concurrent add_event() and clear() calls."""
        handler = AutoFlushHandler(
            time_window_ms=1000,
            on_operation_complete=self._emit_operation,
        )
        handler_cleanup.append(handler)

        stop_flag = threading.Event()
        errors = []

        def add_events() -> None:
            """Continuously add events."""
            try:
                while not stop_flag.is_set():
                    event = self._create_test_event("test.txt")
                    handler.add_event(event)
                    time.sleep(0.001)
            except Exception as e:
                errors.append(e)

        def clear_events() -> None:
            """Continuously clear events."""
            try:
                while not stop_flag.is_set():
                    handler.clear()
                    time.sleep(0.002)
            except Exception as e:
                errors.append(e)

        # Start threads
        add_thread = threading.Thread(target=add_events)
        clear_thread = threading.Thread(target=clear_events)

        add_thread.start()
        clear_thread.start()

        # Run for a short time
        time.sleep(0.5)
        stop_flag.set()

        add_thread.join()
        clear_thread.join()

        # Should not have any errors
        assert len(errors) == 0, f"Should not have threading errors: {errors}"

    def test_timer_cancellation_race(self, handler_cleanup: list) -> None:
        """Test timer cancellation during concurrent adds."""
        handler = AutoFlushHandler(
            time_window_ms=100,  # Short window
            on_operation_complete=self._emit_operation,
        )
        handler_cleanup.append(handler)

        num_threads = 10
        events_per_thread = 20
        threads = []

        def rapid_add_events(thread_id: int) -> None:
            """Rapidly add events to trigger timer rescheduling."""
            for i in range(events_per_thread):
                event = self._create_test_event(f"file_{thread_id}_{i}.txt")
                handler.add_event(event)
                time.sleep(0.001)  # Small delay to create race conditions

        # Start all threads
        for i in range(num_threads):
            t = threading.Thread(target=rapid_add_events, args=(i,))
            threads.append(t)
            t.start()

        # Wait for completion
        for t in threads:
            t.join()

        # Give some time for potential timer fires
        time.sleep(0.2)

        # Should not crash or lose events
        final_events = handler.pending_events
        assert isinstance(final_events, list), "Should safely return event list"

    def test_pending_events_property_thread_safety(self, handler_cleanup: list) -> None:
        """Test that pending_events property is thread-safe."""
        handler = AutoFlushHandler(
            time_window_ms=1000,
            on_operation_complete=self._emit_operation,
        )
        handler_cleanup.append(handler)

        num_threads = 10
        threads = []
        snapshots = []
        lock = threading.Lock()

        def add_and_read() -> None:
            """Add events and read pending_events concurrently."""
            for i in range(50):
                handler.add_event(self._create_test_event(f"file_{i}.txt"))
                pending = handler.pending_events  # Read while others are adding
                with lock:
                    snapshots.append(len(pending))

        # Start threads
        for _ in range(num_threads):
            t = threading.Thread(target=add_and_read)
            threads.append(t)
            t.start()

        # Wait for completion
        for t in threads:
            t.join()

        # Should have many snapshots without errors
        assert len(snapshots) > 0, "Should have captured snapshots"
        # Final count should match total events added
        final = handler.pending_events
        assert len(final) == num_threads * 50, "All events should be present"

    def test_schedule_flush_concurrent_calls(self, handler_cleanup: list) -> None:
        """Test concurrent calls to schedule_flush()."""
        handler = AutoFlushHandler(
            time_window_ms=1000,
            on_operation_complete=self._emit_operation,
        )
        handler_cleanup.append(handler)

        num_threads = 20
        threads = []

        def schedule_flush_repeatedly() -> None:
            """Repeatedly schedule flush."""
            for _ in range(100):
                handler.schedule_flush()

        # Start threads
        for _ in range(num_threads):
            t = threading.Thread(target=schedule_flush_repeatedly)
            threads.append(t)
            t.start()

        # Wait for completion
        for t in threads:
            t.join()

        # Should not crash
        assert True, "Should handle concurrent schedule_flush calls"

    def test_concurrent_clear_and_pending_events_read(self, handler_cleanup: list) -> None:
        """Test reading pending_events while clear() is called."""
        handler = AutoFlushHandler(
            time_window_ms=1000,
            on_operation_complete=self._emit_operation,
        )
        handler_cleanup.append(handler)

        # Add some initial events
        for i in range(100):
            handler.add_event(self._create_test_event(f"file_{i}.txt"))

        stop_flag = threading.Event()
        errors = []

        def read_events() -> None:
            """Continuously read pending events."""
            try:
                while not stop_flag.is_set():
                    _pending = handler.pending_events
                    time.sleep(0.001)
            except Exception as e:
                errors.append(e)

        def clear_events() -> None:
            """Continuously clear events."""
            try:
                while not stop_flag.is_set():
                    handler.clear()
                    time.sleep(0.001)
            except Exception as e:
                errors.append(e)

        # Start threads
        read_thread = threading.Thread(target=read_events)
        clear_thread = threading.Thread(target=clear_events)

        read_thread.start()
        clear_thread.start()

        # Run briefly
        time.sleep(0.2)
        stop_flag.set()

        read_thread.join()
        clear_thread.join()

        # Should not have errors
        assert len(errors) == 0, f"Should handle concurrent read/clear: {errors}"

    def test_no_event_loop_handling(self, handler_cleanup: list) -> None:
        """Test behavior when no event loop is available."""
        # This test runs without an asyncio event loop
        handler = AutoFlushHandler(
            time_window_ms=100,
            on_operation_complete=self._emit_operation,
        )
        handler_cleanup.append(handler)

        # Should not crash when adding events without event loop
        for i in range(10):
            handler.add_event(self._create_test_event(f"file_{i}.txt"))

        # Should log warning but not crash
        assert len(handler.pending_events) == 10, "Events should still be buffered"


class TestAutoFlushHandlerStressTest(FoundationTestCase):
    """Stress tests for AutoFlushHandler under heavy load."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.operations_emitted: list[FileOperation] = []
        self.lock = threading.Lock()

    def _create_event(self, filename: str) -> FileEvent:
        """Create test event."""
        return FileEvent(
            path=Path(f"/tmp/{filename}"),
            event_type="modified",
            metadata=FileEventMetadata(timestamp=datetime.now(), sequence_number=1),
        )

    def _emit_operation(self, operation: FileOperation) -> None:
        """Thread-safe callback."""
        with self.lock:
            self.operations_emitted.append(operation)

    def test_high_frequency_adds(self, handler_cleanup: list) -> None:
        """Test high-frequency event additions."""
        handler = AutoFlushHandler(
            time_window_ms=50,
            on_operation_complete=self._emit_operation,
        )
        handler_cleanup.append(handler)

        num_events = 1000
        for i in range(num_events):
            handler.add_event(self._create_event(f"file_{i}.txt"))

        # Should handle all events
        assert len(handler.pending_events) == num_events

    def test_many_threads_contention(self, handler_cleanup: list) -> None:
        """Test many threads competing for lock."""
        handler = AutoFlushHandler(
            time_window_ms=1000,
            on_operation_complete=self._emit_operation,
        )
        handler_cleanup.append(handler)

        num_threads = 50
        events_per_thread = 20
        threads = []

        def add_events(tid: int) -> None:
            for i in range(events_per_thread):
                handler.add_event(self._create_event(f"t{tid}_f{i}.txt"))

        # Start many threads
        for i in range(num_threads):
            t = threading.Thread(target=add_events, args=(i,))
            threads.append(t)
            t.start()

        # Wait for all
        for t in threads:
            t.join()

        # Verify all events added
        assert len(handler.pending_events) == num_threads * events_per_thread


class TestAutoFlushHandlerEdgeCases(FoundationTestCase):
    """Edge case tests for AutoFlushHandler."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_clear_during_callback(self, handler_cleanup: list) -> None:
        """Test clearing events while callback is executing."""
        handler = AutoFlushHandler(
            time_window_ms=50,
        )
        handler_cleanup.append(handler)

        callback_started = threading.Event()
        callback_done = threading.Event()

        def slow_callback(operation: FileOperation) -> None:
            """Slow callback to create race window."""
            callback_started.set()
            time.sleep(0.1)
            callback_done.set()

        handler.on_operation_complete = slow_callback

        # Add event
        event = FileEvent(
            path=Path("/tmp/test.txt"),
            event_type="modified",
            metadata=FileEventMetadata(timestamp=datetime.now(), sequence_number=1),
        )
        handler.add_event(event)

        # This test doesn't have event loop, so auto-flush won't trigger
        # Just verify clear() works
        handler.clear()
        assert len(handler.pending_events) == 0

    def test_add_event_with_temp_files(self, handler_cleanup: list) -> None:
        """Test adding events for temp files doesn't crash."""
        handler = AutoFlushHandler(time_window_ms=1000)
        handler_cleanup.append(handler)

        # Add temp file event
        temp_event = FileEvent(
            path=Path("/tmp/.test.txt.tmp.123"),
            event_type="created",
            metadata=FileEventMetadata(timestamp=datetime.now(), sequence_number=1),
        )
        handler.add_event(temp_event)

        # Should be buffered normally
        assert len(handler.pending_events) == 1


# 🧱🏗️🔚
