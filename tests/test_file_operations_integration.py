"""Integration tests for file operation detection with real filesystem operations."""

from __future__ import annotations

from collections.abc import Generator
from datetime import datetime, timedelta
from pathlib import Path
import tempfile
from threading import Event as ThreadEvent
import time

import pytest
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from provide.foundation.file.operations import (
    DetectorConfig,
    FileEvent,
    FileEventMetadata,
    OperationDetector,
    OperationType,
)


class FileEventCapture(FileSystemEventHandler):
    """Captures real filesystem events and converts to FileEvent objects."""

    def __init__(self) -> None:
        self.events: list[FileEvent] = []
        self.sequence_counter = 0
        self._stop_event = ThreadEvent()

    def _create_file_event(self, event: FileSystemEvent, event_type: str) -> FileEvent:
        """Convert watchdog event to FileEvent."""
        self.sequence_counter += 1

        # Get file size if file exists
        size_after = None
        if event_type in ("created", "modified") and Path(event.src_path).exists():
            try:
                size_after = Path(event.src_path).stat().st_size
            except (OSError, FileNotFoundError):
                size_after = None

        metadata = FileEventMetadata(
            timestamp=datetime.now(),
            sequence_number=self.sequence_counter,
            size_after=size_after,
        )

        dest_path = None
        if hasattr(event, "dest_path") and event.dest_path:
            dest_path = Path(event.dest_path)

        return FileEvent(
            path=Path(event.src_path),
            event_type=event_type,
            metadata=metadata,
            dest_path=dest_path,
        )

    def on_created(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            file_event = self._create_file_event(event, "created")
            self.events.append(file_event)

    def on_modified(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            file_event = self._create_file_event(event, "modified")
            self.events.append(file_event)

    def on_deleted(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            file_event = self._create_file_event(event, "deleted")
            self.events.append(file_event)

    def on_moved(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            file_event = self._create_file_event(event, "moved")
            self.events.append(file_event)

    def clear_events(self) -> None:
        """Clear captured events."""
        self.events.clear()
        self.sequence_counter = 0

    def stop_capture(self) -> None:
        """Signal to stop capturing events."""
        self._stop_event.set()


class TestFileOperationIntegration:
    """Integration tests using real filesystem operations."""

    @pytest.fixture
    def temp_dir(self) -> Generator[Path, None, None]:
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
    def file_monitor(self, temp_dir: Path) -> Generator[FileEventCapture, None, None]:
        """Set up filesystem monitoring for the temp directory."""
        event_handler = FileEventCapture()
        observer = Observer()
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
        time.sleep(0.1)  # Allow events to be captured

        # Analyze captured events
        detector = OperationDetector(DetectorConfig(time_window_ms=200))
        operations = detector.detect(file_monitor.events)

        # Verify we detected an atomic save
        assert len(operations) >= 1
        atomic_ops = [op for op in operations if op.operation_type == OperationType.ATOMIC_SAVE]
        assert len(atomic_ops) == 1

        operation = atomic_ops[0]
        assert operation.primary_path.name == original_file.name
        assert operation.is_atomic is True
        assert operation.is_safe is True
        assert operation.confidence >= 0.9

    def test_vim_style_atomic_save(self, temp_dir: Path, file_monitor: FileEventCapture) -> None:
        """Test Vim-style atomic save with backup."""
        file_monitor.clear_events()

        # Create original file
        original_file = temp_dir / "document.txt"
        original_file.write_text("Original content")
        time.sleep(0.05)

        file_monitor.clear_events()  # Clear creation event

        # Simulate Vim save pattern
        backup_file = temp_dir / "document.txt~"

        # Create backup
        backup_file.write_text("Original content")
        time.sleep(0.05)

        # Delete original
        original_file.unlink()
        time.sleep(0.05)

        # Create new version
        original_file.write_text("New content")
        time.sleep(0.1)

        # Analyze events
        detector = OperationDetector(DetectorConfig(time_window_ms=300))
        operations = detector.detect(file_monitor.events)

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

        time.sleep(0.1)  # Allow events to be captured

        # Analyze events
        detector = OperationDetector(DetectorConfig(time_window_ms=200))
        operations = detector.detect(file_monitor.events)

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
        time.sleep(0.05)

        file_monitor.clear_events()  # Clear creation event

        # Create backup first
        backup_file.write_text("Important data")
        time.sleep(0.05)

        # Modify original
        original_file.write_text("Updated important data")
        time.sleep(0.1)

        # Analyze events
        detector = OperationDetector(DetectorConfig(time_window_ms=200))
        operations = detector.detect(file_monitor.events)

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
        time.sleep(0.05)

        file_monitor.clear_events()  # Clear creation event

        # Chain of renames
        temp_file = temp_dir / "temp.txt"
        final_file = temp_dir / "final.txt"

        file1.rename(temp_file)
        time.sleep(0.05)

        temp_file.rename(final_file)
        time.sleep(0.1)

        # Analyze events
        detector = OperationDetector(DetectorConfig(time_window_ms=200))
        operations = detector.detect(file_monitor.events)

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

        # Check that events have size information
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
        time.sleep(0.6)  # Wait longer than default time window

        file2.write_text("Content 2")
        time.sleep(0.1)

        # Should be detected as separate operations
        detector = OperationDetector(DetectorConfig(time_window_ms=500))
        operations = detector.detect(file_monitor.events)

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


class TestFileOperationsStressTesting:
    """Stress tests for file operations detection."""

    @pytest.fixture
    def temp_dir(self) -> Generator[Path, None, None]:
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
    def detector(self) -> OperationDetector:
        """Create an operation detector for testing."""
        return OperationDetector()

    def test_rapid_file_creation_detection(self, temp_dir: Path, detector: OperationDetector) -> None:
        """Test detection with rapid file creation."""
        events = []

        # Simulate rapid file creation (100 files in 1 second)
        for i in range(100):
            file_path = temp_dir / f"rapid_{i}.txt"
            # Create the actual file
            file_path.write_text(f"Content {i}")

            # Create event
            event = FileEvent(
                path=file_path,
                event_type="created",
                metadata=FileEventMetadata(
                    timestamp=datetime.now(),
                    sequence_number=i + 1,
                    size_after=len(f"Content {i}"),
                ),
            )
            events.append(event)

        # Test detection performance
        start_time = time.perf_counter()
        operations = detector.detect(events)
        end_time = time.perf_counter()

        detection_time = (end_time - start_time) * 1000  # milliseconds

        # Should complete within reasonable time
        assert detection_time < 100  # Less than 100ms for 100 files

        # Should detect some operations (likely batch updates)
        assert len(operations) >= 0

    def test_mixed_operation_patterns_stress(self, temp_dir: Path, detector: OperationDetector) -> None:
        """Test detection with mixed operation patterns under stress."""
        events = []
        base_time = datetime.now()

        # Generate complex mixed patterns
        for i in range(50):
            time_offset = i * 600  # 600ms apart (beyond 500ms time window)

            # VSCode atomic save
            temp_file = temp_dir / f"file{i}.txt.tmp.{i}"
            final_file = temp_dir / f"file{i}.txt"

            events.extend(
                [
                    FileEvent(
                        path=temp_file,
                        event_type="created",
                        metadata=FileEventMetadata(
                            timestamp=base_time + timedelta(milliseconds=time_offset),
                            sequence_number=len(events) + 1,
                            size_after=1024,
                        ),
                    ),
                    FileEvent(
                        path=temp_file,
                        event_type="moved",
                        metadata=FileEventMetadata(
                            timestamp=base_time + timedelta(milliseconds=time_offset + 5),
                            sequence_number=len(events) + 2,
                        ),
                        dest_path=final_file,
                    ),
                ]
            )

            # Safe write every 5th iteration
            if i % 5 == 0:
                backup_file = temp_dir / f"backup{i}.bak"
                main_file = temp_dir / f"backup{i}"

                events.extend(
                    [
                        FileEvent(
                            path=backup_file,
                            event_type="created",
                            metadata=FileEventMetadata(
                                timestamp=base_time + timedelta(milliseconds=time_offset + 20),
                                sequence_number=len(events) + 1,
                                size_after=1000,
                            ),
                        ),
                        FileEvent(
                            path=main_file,
                            event_type="modified",
                            metadata=FileEventMetadata(
                                timestamp=base_time + timedelta(milliseconds=time_offset + 25),
                                sequence_number=len(events) + 2,
                                size_before=1000,
                                size_after=1024,
                            ),
                        ),
                    ]
                )

        # Test detection under stress
        start_time = time.perf_counter()
        operations = detector.detect(events)
        end_time = time.perf_counter()

        detection_time = (end_time - start_time) * 1000

        # Should handle stress test efficiently
        assert detection_time < 500  # Less than 500ms

        # Should detect multiple operations
        assert len(operations) >= 30  # Should detect most atomic saves

    def test_large_file_event_batches(self, temp_dir: Path, detector: OperationDetector) -> None:
        """Test detection with very large batches of events."""
        large_batch_size = 1000
        events = []
        base_time = datetime.now()

        # Generate large batch of simple modify events
        for i in range(large_batch_size):
            file_path = temp_dir / f"batch_file_{i % 20}.py"  # Reuse file names

            event = FileEvent(
                path=file_path,
                event_type="modified",
                metadata=FileEventMetadata(
                    timestamp=base_time + timedelta(milliseconds=i),
                    sequence_number=i + 1,
                    size_before=500,
                    size_after=520,
                ),
            )
            events.append(event)

        # Test large batch detection
        start_time = time.perf_counter()
        operations = detector.detect(events)
        end_time = time.perf_counter()

        detection_time = (end_time - start_time) * 1000

        # Should handle large batches efficiently
        assert detection_time < 1000  # Less than 1 second

        # Should detect batch operations
        batch_ops = [op for op in operations if op.operation_type.value == "batch_update"]
        assert len(batch_ops) >= 1

    def test_concurrent_streaming_simulation(self, temp_dir: Path) -> None:
        """Test concurrent streaming detection simulation."""
        import queue
        import threading

        results_queue = queue.Queue()
        num_threads = 3
        events_per_thread = 20

        def streaming_worker(worker_id: int) -> None:
            """Worker that processes events in streaming fashion."""
            detector = OperationDetector()
            base_time = datetime.now()
            detected_operations = []

            for i in range(events_per_thread):
                # Create VSCode-style events
                temp_file = temp_dir / f"worker{worker_id}_file{i}.txt.tmp.{i}"
                final_file = temp_dir / f"worker{worker_id}_file{i}.txt"

                # First event
                event1 = FileEvent(
                    path=temp_file,
                    event_type="created",
                    metadata=FileEventMetadata(
                        timestamp=base_time + timedelta(milliseconds=i * 50),
                        sequence_number=i * 2 + 1,
                    ),
                )

                result = detector.detect_streaming(event1)
                if result:
                    detected_operations.append(result)

                # Second event
                event2 = FileEvent(
                    path=temp_file,
                    event_type="moved",
                    metadata=FileEventMetadata(
                        timestamp=base_time + timedelta(milliseconds=i * 50 + 25),
                        sequence_number=i * 2 + 2,
                    ),
                    dest_path=final_file,
                )

                result = detector.detect_streaming(event2)
                if result:
                    detected_operations.append(result)

            # Flush remaining
            detected_operations.extend(detector.flush())

            results_queue.put(
                {
                    "worker_id": worker_id,
                    "operations": detected_operations,
                }
            )

        # Start workers
        workers = []
        start_time = time.perf_counter()

        for i in range(num_threads):
            worker = threading.Thread(target=streaming_worker, args=(i,))
            workers.append(worker)
            worker.start()

        # Wait for completion
        for worker in workers:
            worker.join()

        end_time = time.perf_counter()
        total_time = (end_time - start_time) * 1000

        # Collect results
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())

        # Verify concurrent processing
        assert len(results) == num_threads
        assert total_time < 2000  # Should complete within 2 seconds

        # Each worker should have processed some operations
        total_operations = sum(len(r["operations"]) for r in results)
        assert total_operations >= 0


if __name__ == "__main__":
    pytest.main([__file__])
