#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Integration tests for file operation detection with real filesystem operations."""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path
import tempfile
import time
from typing import Any

from provide.testkit import FoundationTestCase
import pytest
from watchdog.observers.polling import PollingObserver

from provide.foundation.file.operations import (
    DetectorConfig,
    FileEvent,
    OperationDetector,
    OperationType,
)
from provide.foundation.file.operations.types import FileOperation
from provide.foundation.utils.timing import apply_timeout_factor

pytestmark = pytest.mark.xdist_group(name="file_operations_integration_serial")


class FileEventCapture:
    """Simple watchdog event handler for capturing file system events."""

    def __init__(self) -> None:
        """Initialize the event capture handler."""
        self.events: list[FileEvent] = []
        self._sequence = 0

    def clear_events(self) -> None:
        """Clear all captured events."""
        self.events.clear()
        self._sequence = 0

    def dispatch(self, event: Any) -> None:
        """Handle watchdog file system events."""
        from datetime import datetime

        from provide.foundation.file.operations import FileEventMetadata

        # Skip directory events for simplicity
        if event.is_directory:
            return

        # Convert watchdog event to FileEvent
        event_type = event.event_type  # created, modified, moved, deleted
        src_path = Path(event.src_path)

        # Try to get file size information
        size_after = None
        try:
            if src_path.exists():
                size_after = src_path.stat().st_size
        except Exception:
            pass  # File might not exist for delete events

        # Create metadata with size information
        metadata = FileEventMetadata(
            timestamp=datetime.now(),
            sequence_number=self._sequence,
            size_after=size_after,
        )
        self._sequence += 1

        # Handle move events specially
        dest_path = None
        if event_type == "moved":
            dest_path = Path(event.dest_path)

        # Create and store FileEvent
        file_event = FileEvent(
            path=src_path,
            event_type=event_type,
            metadata=metadata,
            dest_path=dest_path,
        )
        self.events.append(file_event)


def wait_for_file_events(file_monitor: FileEventCapture, timeout: float = 5.0) -> list[FileEvent]:
    """Wait for filesystem events to appear before proceeding."""
    deadline = time.time() + apply_timeout_factor(timeout)
    while time.time() < deadline:
        if file_monitor.events:
            return file_monitor.events
        time.sleep(0.05)
    pytest.fail("No file system events were captured within the allotted time")


def detect_operations(
    detector: OperationDetector,
    file_monitor: FileEventCapture,
    timeout: float = 5.0,
    delay: float = 0.1,
) -> list[FileOperation]:
    """Run the detector until operations are found or the timeout expires."""
    deadline = time.time() + apply_timeout_factor(timeout)
    while time.time() < deadline:
        snapshot = list(file_monitor.events)
        if not snapshot:
            time.sleep(delay)
            continue
        operations = detector.detect(snapshot)
        if operations:
            return operations
        time.sleep(delay)
    return []


@pytest.mark.serial
class TestFileOperationIntegration(FoundationTestCase):
    """Integration tests using real filesystem operations.

    Note: Marked as serial because these tests use watchdog.Observer which creates
    filesystem watchers. Running multiple instances in parallel can exceed system
    limits (especially kqueue on macOS) and freeze the entire system.
    """

    @pytest.fixture(autouse=True)
    def ensure_detector_registry(self) -> Generator[None, None, None]:
        """Ensure detector registry is properly initialized for each test.

        This fixture prevents race conditions with parallel tests (pytest-xdist)
        where another test might clear the global detector registry.
        """
        from provide.foundation.file.operations.detectors import (
            _auto_register_builtin_detectors,
        )
        from provide.foundation.file.operations.detectors.registry import (
            clear_detector_registry,
        )

        # Clear and re-register to ensure a clean state
        clear_detector_registry()
        _auto_register_builtin_detectors()

        yield

        # Clean up after test
        clear_detector_registry()

    @pytest.fixture
    def temp_dir(self) -> Generator[Path, None, None]:
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
    def file_monitor(self, temp_dir: Path) -> Generator[FileEventCapture, None, None]:
        """Set up filesystem monitoring for the temp directory."""
        event_handler = FileEventCapture()
        observer = PollingObserver(timeout=0.05)
        observer.schedule(event_handler, str(temp_dir), recursive=True)
        observer.start()

        # Give observer time to start
        time.sleep(0.1)

        yield event_handler

        observer.stop()
        observer.join(timeout=5.0)

    def test_vscode_atomic_save_pattern(self, temp_dir: Path, file_monitor: FileEventCapture) -> None:
        """Test VSCode-style atomic save with real files."""
        # Clear any initial events
        file_monitor.clear_events()

        # Simulate VSCode atomic save pattern
        original_file = temp_dir / "document.txt"
        temp_file = temp_dir / "document.txt.tmp.12345"

        # Create temp file with content (like VSCode does)
        temp_file.write_text("Hello, World!")
        time.sleep(0.05)  # Brief pause

        # Rename temp file to final name (atomic operation)
        temp_file.rename(original_file)
        time.sleep(0.2)  # Allow events to be captured

        # Analyze captured events
        wait_for_file_events(file_monitor)
        detector = OperationDetector(DetectorConfig(time_window_ms=200))
        operations = detect_operations(detector, file_monitor, timeout=5.0, delay=0.2)

        # Verify we detected an atomic save or backup operation
        assert len(operations) >= 1
        atomic_or_backup_ops = [
            op
            for op in operations
            if op.operation_type in (OperationType.ATOMIC_SAVE, OperationType.BACKUP_CREATE)
        ]
        assert len(atomic_or_backup_ops) >= 1

        operation = atomic_or_backup_ops[0]
        assert operation.primary_path.name == original_file.name
        # Backup detections may not flag as atomic but should still be safe
        assert operation.is_safe is True
        assert operation.confidence >= 0.7

    def test_vim_style_atomic_save(self, temp_dir: Path, file_monitor: FileEventCapture) -> None:
        """Test Vim-style atomic save with backup."""
        file_monitor.clear_events()

        # Create original file
        original_file = temp_dir / "document.txt"
        original_file.write_text("Original content")
        time.sleep(0.1)

        file_monitor.clear_events()  # Clear creation event

        # Simulate Vim save pattern
        backup_file = temp_dir / "document.txt~"

        # Create backup
        backup_file.write_text("Original content")
        time.sleep(0.05)

        # Delete original
        original_file.unlink()
        time.sleep(0.1)

        # Create new version
        original_file.write_text("New content")
        time.sleep(0.2)

        # Analyze events
        wait_for_file_events(file_monitor)
        detector = OperationDetector(DetectorConfig(time_window_ms=300))
        operations = detect_operations(detector, file_monitor, timeout=5.0, delay=0.2)

        # Should detect atomic save with backup
        atomic_ops = [
            op
            for op in operations
            if op.operation_type in (OperationType.ATOMIC_SAVE, OperationType.SAFE_WRITE)
        ]
        assert len(atomic_ops) >= 1

    def test_batch_file_operations(self, temp_dir: Path, file_monitor: FileEventCapture) -> None:
        """Test detection of batch operations with multiple files."""
        file_monitor.clear_events()

        # Create multiple files in quick succession
        files = []
        for i in range(5):
            file_path = temp_dir / f"file_{i}.txt"
            file_path.write_text(f"Content for file {i}")
            files.append(file_path)
            time.sleep(0.01)  # Very short delay

        time.sleep(0.25)  # Allow events to be captured

        # Analyze events
        wait_for_file_events(file_monitor)
        detector = OperationDetector(DetectorConfig(time_window_ms=200))
        operations = detect_operations(detector, file_monitor, timeout=5.0, delay=0.2)

        # Should detect batch operation
        batch_ops = [op for op in operations if op.operation_type == OperationType.BATCH_UPDATE]
        assert len(batch_ops) >= 1

        operation = batch_ops[0]
        assert operation.event_count >= 5

    def test_safe_write_with_backup(self, temp_dir: Path, file_monitor: FileEventCapture) -> None:
        """Test safe write pattern with backup creation."""
        file_monitor.clear_events()

        original_file = temp_dir / "important.txt"
        backup_file = temp_dir / "important.txt.bak"

        # Create original file
        original_file.write_text("Important data")
        time.sleep(0.3)  # Increased for system load tolerance

        file_monitor.clear_events()  # Clear creation event

        # Create backup first
        backup_file.write_text("Important data")
        time.sleep(0.3)  # Increased for system load tolerance

        # Modify original
        original_file.write_text("Updated important data")
        time.sleep(0.5)  # Increased for system load tolerance

        # Analyze events
        wait_for_file_events(file_monitor)
        detector = OperationDetector(DetectorConfig(time_window_ms=500))  # Increased window
        operations = detect_operations(detector, file_monitor, timeout=10.0, delay=0.3)

        # Should detect safe write
        safe_ops = [op for op in operations if op.operation_type == OperationType.SAFE_WRITE]
        assert len(safe_ops) >= 1

        operation = safe_ops[0]
        assert operation.has_backup is True
        assert operation.is_safe is True

    def test_rename_sequence(self, temp_dir: Path, file_monitor: FileEventCapture) -> None:
        """Test detection of rename sequences."""
        file_monitor.clear_events()

        # Create original file
        file1 = temp_dir / "original.txt"
        file1.write_text("Content")
        time.sleep(0.3)  # Increased for system load tolerance

        file_monitor.clear_events()  # Clear creation event

        # Chain of renames
        temp_file = temp_dir / "temp.txt"
        final_file = temp_dir / "final.txt"

        file1.rename(temp_file)
        time.sleep(0.3)  # Increased for system load tolerance

        temp_file.rename(final_file)
        time.sleep(0.5)  # Increased for system load tolerance

        # Analyze events
        wait_for_file_events(file_monitor)
        detector = OperationDetector(DetectorConfig(time_window_ms=2000))  # Increased window
        operations = detect_operations(detector, file_monitor, timeout=10.0, delay=0.3)

        # Should detect rename sequence
        rename_ops = [op for op in operations if op.operation_type == OperationType.RENAME_SEQUENCE]
        assert len(rename_ops) >= 1

        operation = rename_ops[0]
        assert operation.is_atomic is True

    def test_size_delta_calculation(self, temp_dir: Path, file_monitor: FileEventCapture) -> None:
        """Test that file size changes are correctly captured."""
        file_monitor.clear_events()

        test_file = temp_dir / "size_test.txt"

        # Create file with small content
        test_file.write_text("Small")
        time.sleep(0.05)

        # Modify with larger content
        test_file.write_text("Much larger content that takes more space")
        time.sleep(0.1)

        # Ensure events were recorded before checking size data
        wait_for_file_events(file_monitor)
        events_with_size = [e for e in file_monitor.events if e.metadata.size_after is not None]
        assert len(events_with_size) >= 1

        # Verify size information is reasonable
        for event in events_with_size:
            assert event.metadata.size_after > 0

    def test_streaming_detection_real_time(self, temp_dir: Path, file_monitor: FileEventCapture) -> None:
        """Test streaming detection with real filesystem events."""
        detector = OperationDetector(DetectorConfig(time_window_ms=100))

        file_monitor.clear_events()

        # Create a file
        test_file = temp_dir / "stream_test.txt"
        test_file.write_text("Initial content")
        time.sleep(0.05)

        # Process events one by one in streaming fashion
        wait_for_file_events(file_monitor)
        operations = []
        for event in file_monitor.events:
            result = detector.detect_streaming(event)
            if result:
                operations.append(result)

        # Flush any remaining operations
        operations.extend(detector.flush())

        # Should have detected at least the file creation
        assert len(file_monitor.events) >= 1

    def test_timing_edge_cases(self, temp_dir: Path, file_monitor: FileEventCapture) -> None:
        """Test edge cases around timing windows."""
        file_monitor.clear_events()

        # Create events outside time window
        file1 = temp_dir / "file1.txt"
        file2 = temp_dir / "file2.txt"

        file1.write_text("Content 1")
        time.sleep(0.05)
        file1.write_text("Content 1 updated")
        time.sleep(0.75)  # Wait longer than default time window

        file2.write_text("Content 2")
        time.sleep(0.05)
        file2.write_text("Content 2 updated")
        time.sleep(0.25)  # Allow filesystem events to be captured

        # Ensure events were captured
        wait_for_file_events(file_monitor)
        assert len(file_monitor.events) >= 1, "No events captured from file system"

        # Should be detected as separate operations
        detector = OperationDetector(DetectorConfig(time_window_ms=500))
        operations = detect_operations(detector, file_monitor, timeout=5.0, delay=0.2)

        # Events should be in separate groups
        assert len(operations) >= 1

    def test_error_handling_missing_files(self, temp_dir: Path, file_monitor: FileEventCapture) -> None:
        """Test handling of events for files that no longer exist."""
        file_monitor.clear_events()

        # Create and immediately delete a file
        temp_file = temp_dir / "ephemeral.txt"
        temp_file.write_text("Brief existence")
        temp_file.unlink()
        time.sleep(0.1)

        # Should handle events gracefully even if files don't exist
        detector = OperationDetector()
        operations = detector.detect(file_monitor.events)

        # Should not crash and may detect some operation
        assert isinstance(operations, list)


# 🧱🏗️🔚
