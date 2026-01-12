#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Event loss recovery tests for AutoFlushHandler.

Tests recovery mechanisms for failed callback operations."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import threading

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.file.operations.detectors.auto_flush import AutoFlushHandler
from provide.foundation.file.operations.types import FileEvent, FileEventMetadata, FileOperation, OperationType


@pytest.fixture
def handler_cleanup() -> list[AutoFlushHandler]:
    """Fixture to track and cleanup AutoFlushHandlers after each test."""
    handlers: list[AutoFlushHandler] = []
    yield handlers
    # Cleanup all handlers
    for handler in handlers:
        handler.clear()


class TestEventLossRecovery(FoundationTestCase):
    """Test event loss recovery mechanisms."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.operations_emitted: list[FileOperation] = []
        self.callback_fail_count = 0
        self.lock = threading.Lock()

    def _create_event(self, filename: str) -> FileEvent:
        """Create test event."""
        return FileEvent(
            path=Path(f"/tmp/{filename}"),
            event_type="modified",
            metadata=FileEventMetadata(timestamp=datetime.now(), sequence_number=1),
        )

    def _create_operation(self, filename: str) -> FileOperation:
        """Create test operation."""
        event = self._create_event(filename)
        return FileOperation(
            operation_type=OperationType.UNKNOWN,
            primary_path=event.path,
            events=[event],
            confidence=1.0,
            description=f"test {filename}",
            start_time=datetime.now(),
            end_time=datetime.now(),
            files_affected=[event.path],
        )

    def test_callback_exception_queues_for_retry(self, handler_cleanup: list) -> None:
        """Test that callback exceptions queue operations for retry."""

        def failing_callback(operation: FileOperation) -> None:
            """Callback that always fails."""
            raise RuntimeError("Simulated callback failure")

        handler = AutoFlushHandler(
            time_window_ms=100,
            on_operation_complete=failing_callback,
        )
        handler_cleanup.append(handler)

        # Emit an operation that will fail
        operation = self._create_operation("test.txt")
        handler._emit_operation_safe(operation)

        # Should be queued for retry
        assert handler.failed_operations_count == 1

        # Failed operation should be retrievable
        failed = handler.get_failed_operations()
        assert len(failed) == 1
        assert failed[0].primary_path == operation.primary_path

    def test_retry_failed_operations_success(self, handler_cleanup: list) -> None:
        """Test retrying failed operations succeeds when callback works."""
        fail_count = 0

        def sometimes_failing_callback(operation: FileOperation) -> None:
            """Callback that fails first time, succeeds after."""
            nonlocal fail_count
            fail_count += 1
            if fail_count == 1:
                raise RuntimeError("First attempt fails")
            # Second attempt succeeds
            with self.lock:
                self.operations_emitted.append(operation)

        handler = AutoFlushHandler(
            time_window_ms=100,
            on_operation_complete=sometimes_failing_callback,
        )
        handler_cleanup.append(handler)

        # Emit operation (will fail first time)
        operation = self._create_operation("test.txt")
        handler._emit_operation_safe(operation)

        # Should be queued
        assert handler.failed_operations_count == 1

        # Retry should succeed
        retried = handler.retry_failed_operations()
        assert retried == 1
        assert handler.failed_operations_count == 0

        # Operation should be emitted
        assert len(self.operations_emitted) == 1

    @pytest.mark.xdist_group(name="serial_recovery")
    def test_retry_failed_operations_persistent_failure(self, handler_cleanup: list) -> None:
        """Test that persistently failing operations stay in queue."""

        def always_failing_callback(operation: FileOperation) -> None:
            """Callback that always fails."""
            raise RuntimeError("Always fails")

        handler = AutoFlushHandler(
            time_window_ms=100,
            on_operation_complete=always_failing_callback,
        )
        handler_cleanup.append(handler)

        # Emit operation
        operation = self._create_operation("test.txt")
        handler._emit_operation_safe(operation)

        # Should be queued
        assert handler.failed_operations_count == 1

        # Retry should fail, operation stays queued
        retried = handler.retry_failed_operations()
        assert retried == 0
        assert handler.failed_operations_count == 1

    @pytest.mark.xdist_group(name="serial_recovery")
    def test_clear_failed_operations(self, handler_cleanup: list) -> None:
        """Test clearing failed operations."""

        def failing_callback(operation: FileOperation) -> None:
            raise RuntimeError("Fails")

        handler = AutoFlushHandler(
            time_window_ms=100,
            on_operation_complete=failing_callback,
        )
        handler_cleanup.append(handler)

        # Create multiple failed operations
        for i in range(5):
            operation = self._create_operation(f"file{i}.txt")
            handler._emit_operation_safe(operation)

        assert handler.failed_operations_count == 5

        # Clear all
        cleared = handler.clear_failed_operations()
        assert cleared == 5
        assert handler.failed_operations_count == 0

    def test_concurrent_retry_operations(self, handler_cleanup: list) -> None:
        """Test concurrent retry attempts are thread-safe."""
        attempts = 0

        def counting_callback(operation: FileOperation) -> None:
            """Count callback attempts."""
            nonlocal attempts
            attempts += 1
            if attempts < 3:
                raise RuntimeError("Fail first 2 times")
            # Succeed on 3rd attempt
            with self.lock:
                self.operations_emitted.append(operation)

        handler = AutoFlushHandler(
            time_window_ms=100,
            on_operation_complete=counting_callback,
        )
        handler_cleanup.append(handler)

        # Emit operation (will fail)
        operation = self._create_operation("test.txt")
        handler._emit_operation_safe(operation)

        assert handler.failed_operations_count == 1

        # Concurrent retries
        threads = []
        for _ in range(10):
            t = threading.Thread(target=handler.retry_failed_operations)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Should eventually succeed
        assert handler.failed_operations_count == 0
        assert len(self.operations_emitted) >= 1

    def test_no_callback_no_failures(self, handler_cleanup: list) -> None:
        """Test that no callback means no failures."""
        handler = AutoFlushHandler(time_window_ms=100)
        handler_cleanup.append(handler)

        # Emit without callback
        operation = self._create_operation("test.txt")
        result = handler._emit_operation_safe(operation)

        # Should succeed
        assert result is True
        assert handler.failed_operations_count == 0

    def test_failed_operations_not_lost_on_clear(self, handler_cleanup: list) -> None:
        """Test that clear() doesn't affect failed operations."""

        def failing_callback(operation: FileOperation) -> None:
            raise RuntimeError("Fails")

        handler = AutoFlushHandler(
            time_window_ms=100,
            on_operation_complete=failing_callback,
        )
        handler_cleanup.append(handler)

        # Create failed operation
        operation = self._create_operation("test.txt")
        handler._emit_operation_safe(operation)

        # Add some pending events
        handler.add_event(self._create_event("pending.txt"))

        assert handler.failed_operations_count == 1
        assert len(handler.pending_events) == 1

        # Clear pending events
        handler.clear()

        # Failed operations should still be there
        assert handler.failed_operations_count == 1
        assert len(handler.pending_events) == 0

    def test_get_failed_operations_returns_copy(self, handler_cleanup: list) -> None:
        """Test that get_failed_operations returns a copy, not the original."""

        def failing_callback(operation: FileOperation) -> None:
            raise RuntimeError("Fails")

        handler = AutoFlushHandler(
            time_window_ms=100,
            on_operation_complete=failing_callback,
        )
        handler_cleanup.append(handler)

        # Create failed operation
        operation = self._create_operation("test.txt")
        handler._emit_operation_safe(operation)

        # Get failed operations
        failed = handler.get_failed_operations()
        assert len(failed) == 1

        # Modify the copy
        failed.clear()

        # Original should be unchanged
        assert handler.failed_operations_count == 1


# 🧱🏗️🔚
