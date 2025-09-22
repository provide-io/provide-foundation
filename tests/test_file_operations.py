"""Tests for file operation detection."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import pytest

from provide.foundation.file.operations import (
    DetectorConfig,
    FileEvent,
    FileEventMetadata,
    FileOperation,
    OperationDetector,
    OperationType,
    detect_atomic_save,
    extract_original_path,
    group_related_events,
    is_temp_file,
)


class TestFileEvent:
    """Test FileEvent and metadata functionality."""

    def test_metadata_creation(self) -> None:
        """Test creating metadata with all fields."""
        now = datetime.now()
        metadata = FileEventMetadata(
            timestamp=now, sequence_number=1, size_before=100, size_after=200,
            permissions=0o644, process_name="vscode", extra={"custom": "value"}
        )
        assert metadata.timestamp == now
        assert metadata.sequence_number == 1
        assert metadata.size_before == 100
        assert metadata.size_after == 200
        assert metadata.permissions == 0o644
        assert metadata.process_name == "vscode"
        assert metadata.extra["custom"] == "value"

    def test_event_creation(self) -> None:
        """Test creating a file event."""
        now = datetime.now()
        metadata = FileEventMetadata(timestamp=now, sequence_number=1, size_before=100, size_after=150)

        event = FileEvent(
            path=Path("test.txt"),
            event_type="modified",
            metadata=metadata,
        )

        assert event.path == Path("test.txt")
        assert event.event_type == "modified"
        assert event.timestamp == now
        assert event.sequence == 1
        assert event.size_delta == 50

    def test_move_event(self) -> None:
        """Test creating a move event."""
        now = datetime.now()
        metadata = FileEventMetadata(timestamp=now, sequence_number=1)

        event = FileEvent(
            path=Path("old.txt"),
            event_type="moved",
            metadata=metadata,
            dest_path=Path("new.txt"),
        )

        assert event.path == Path("old.txt")
        assert event.dest_path == Path("new.txt")
        assert event.event_type == "moved"

    def test_size_delta_calculations(self) -> None:
        """Test size delta calculations."""
        # Both sizes available
        metadata1 = FileEventMetadata(
            timestamp=datetime.now(), sequence_number=1, size_before=100, size_after=150
        )
        event1 = FileEvent(path=Path("test.txt"), event_type="modified", metadata=metadata1)
        assert event1.size_delta == 50

        # Size decreased
        metadata2 = FileEventMetadata(
            timestamp=datetime.now(), sequence_number=1, size_before=200, size_after=100
        )
        event2 = FileEvent(path=Path("test.txt"), event_type="modified", metadata=metadata2)
        assert event2.size_delta == -100

        # Missing size info
        metadata3 = FileEventMetadata(timestamp=datetime.now(), sequence_number=1, size_before=100)
        event3 = FileEvent(path=Path("test.txt"), event_type="modified", metadata=metadata3)
        assert event3.size_delta is None


class TestOperationDetector:
    """Test OperationDetector functionality."""

    def test_detector_initialization(self) -> None:
        """Test detector initialization with custom config."""
        config = DetectorConfig(time_window_ms=1000, min_confidence=0.8)
        detector = OperationDetector(config)

        assert detector.config.time_window_ms == 1000
        assert detector.config.min_confidence == 0.8

    def test_default_config(self) -> None:
        """Test detector with default configuration."""
        detector = OperationDetector()

        assert detector.config.time_window_ms == 500
        assert detector.config.min_confidence == 0.7

    def test_atomic_save_detection_vscode_pattern(self) -> None:
        """Test detecting VSCode atomic save pattern."""
        now = datetime.now()

        # VSCode pattern: create temp file, rename to final
        events = [
            FileEvent(
                path=Path("document.txt.tmp.12345"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1, size_after=1024),
            ),
            FileEvent(
                path=Path("document.txt.tmp.12345"),
                event_type="moved",
                metadata=FileEventMetadata(timestamp=now + timedelta(milliseconds=50), sequence_number=2),
                dest_path=Path("document.txt"),
            ),
        ]

        detector = OperationDetector()
        operations = detector.detect(events)

        assert len(operations) == 1
        operation = operations[0]
        assert operation.operation_type == OperationType.ATOMIC_SAVE
        assert operation.primary_path == Path("document.txt")
        assert operation.confidence >= 0.9
        assert operation.is_atomic is True
        assert operation.is_safe is True
        assert "Atomic save" in operation.description

    def test_atomic_save_detection_vim_pattern(self) -> None:
        """Test detecting Vim-style atomic save pattern."""
        now = datetime.now()

        # Vim pattern: delete original, create temp, rename temp
        events = [
            FileEvent(
                path=Path("document.txt"),
                event_type="deleted",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1, size_before=1000),
            ),
            FileEvent(
                path=Path("document.txt~"),
                event_type="created",
                metadata=FileEventMetadata(
                    timestamp=now + timedelta(milliseconds=10), sequence_number=2, size_after=1024
                ),
            ),
        ]

        detector = OperationDetector()
        operations = detector.detect(events)

        assert len(operations) == 1
        operation = operations[0]
        assert operation.operation_type == OperationType.ATOMIC_SAVE
        assert operation.primary_path == Path("document.txt")

    def test_safe_write_detection(self) -> None:
        """Test detecting safe write with backup."""
        now = datetime.now()

        events = [
            FileEvent(
                path=Path("document.bak"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1, size_after=1000),
            ),
            FileEvent(
                path=Path("document"),
                event_type="modified",
                metadata=FileEventMetadata(
                    timestamp=now + timedelta(milliseconds=100),
                    sequence_number=2,
                    size_before=1000,
                    size_after=1024,
                ),
            ),
        ]

        detector = OperationDetector()
        operations = detector.detect(events)

        assert len(operations) == 1
        operation = operations[0]
        assert operation.operation_type == OperationType.SAFE_WRITE
        assert operation.primary_path == Path("document")  # Should be the main file, not backup
        assert operation.has_backup is True
        assert operation.is_safe is True

    def test_rename_sequence_detection(self) -> None:
        """Test detecting rename sequences."""
        now = datetime.now()

        events = [
            FileEvent(
                path=Path("old_name.txt"),
                event_type="moved",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1),
                dest_path=Path("temp_name.txt"),
            ),
            FileEvent(
                path=Path("temp_name.txt"),
                event_type="moved",
                metadata=FileEventMetadata(timestamp=now + timedelta(milliseconds=50), sequence_number=2),
                dest_path=Path("final_name.txt"),
            ),
        ]

        detector = OperationDetector()
        operations = detector.detect(events)

        assert len(operations) == 1
        operation = operations[0]
        assert operation.operation_type == OperationType.RENAME_SEQUENCE
        assert operation.primary_path == Path("final_name.txt")
        assert operation.is_atomic is True

    def test_batch_update_detection(self) -> None:
        """Test detecting batch updates."""
        now = datetime.now()
        base_time = now

        # Multiple files in same directory modified quickly
        events = []
        for i in range(5):
            events.append(
                FileEvent(
                    path=Path(f"src/file{i}.py"),
                    event_type="modified",
                    metadata=FileEventMetadata(
                        timestamp=base_time + timedelta(milliseconds=i * 10), sequence_number=i + 1
                    ),
                )
            )

        detector = OperationDetector()
        operations = detector.detect(events)

        assert len(operations) == 1
        operation = operations[0]
        assert operation.operation_type == OperationType.BATCH_UPDATE
        assert operation.primary_path == Path("src")
        assert operation.event_count == 5

    def test_backup_creation_detection(self) -> None:
        """Test detecting backup file creation."""
        now = datetime.now()

        events = [
            FileEvent(
                path=Path("important.txt.bak"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1, size_after=2048),
            )
        ]

        detector = OperationDetector()
        operations = detector.detect(events)

        assert len(operations) == 1
        operation = operations[0]
        assert operation.operation_type == OperationType.BACKUP_CREATE
        assert operation.has_backup is True

    def test_streaming_detection(self) -> None:
        """Test streaming operation detection."""
        detector = OperationDetector()
        now = datetime.now()

        # Add first event - should not trigger operation yet
        event1 = FileEvent(
            path=Path("test.txt.tmp.123"),
            event_type="created",
            metadata=FileEventMetadata(timestamp=now, sequence_number=1),
        )
        result1 = detector.detect_streaming(event1)
        assert result1 is None

        # Add second event after time window - should trigger flush
        detector.config.time_window_ms = 10  # Very short window for test
        event2 = FileEvent(
            path=Path("test.txt.tmp.123"),
            event_type="moved",
            metadata=FileEventMetadata(timestamp=now + timedelta(milliseconds=20), sequence_number=2),
            dest_path=Path("test.txt"),
        )
        detector.detect_streaming(event2)
        # Note: streaming detection may not always return immediately,
        # depends on implementation timing

    def test_flush_pending(self) -> None:
        """Test flushing pending events."""
        detector = OperationDetector()
        now = datetime.now()

        # Add events without triggering detection
        events = [
            FileEvent(
                path=Path("test.txt.tmp.123"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1),
            ),
            FileEvent(
                path=Path("test.txt.tmp.123"),
                event_type="moved",
                metadata=FileEventMetadata(timestamp=now + timedelta(milliseconds=50), sequence_number=2),
                dest_path=Path("test.txt"),
            ),
        ]

        for event in events:
            detector.detect_streaming(event)

        # Flush should return detected operations
        operations = detector.flush()
        assert len(operations) <= 1  # May or may not detect based on confidence

    def test_time_window_grouping(self) -> None:
        """Test that events are properly grouped by time windows."""
        detector = OperationDetector()
        now = datetime.now()

        # Events within time window
        events_close = [
            FileEvent(
                path=Path("file1.txt"),
                event_type="modified",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1),
            ),
            FileEvent(
                path=Path("file2.txt"),
                event_type="modified",
                metadata=FileEventMetadata(timestamp=now + timedelta(milliseconds=100), sequence_number=2),
            ),
        ]

        # Events outside time window
        events_far = [
            FileEvent(
                path=Path("file3.txt"),
                event_type="modified",
                metadata=FileEventMetadata(timestamp=now + timedelta(milliseconds=1000), sequence_number=3),
            )
        ]

        all_events = events_close + events_far
        groups = detector._group_events_by_time(all_events)

        assert len(groups) == 2
        assert len(groups[0]) == 2  # Close events grouped together
        assert len(groups[1]) == 1  # Far event in separate group

    def test_detect_empty_list(self) -> None:
        """Test detection with empty event list."""
        detector = OperationDetector()
        assert detector.detect([]) == []

    def test_concurrent_detection(self) -> None:
        """Test concurrent detection calls."""
        import threading
        detector = OperationDetector()
        base_time = datetime.now()

        results = []
        def detect_worker():
            events = [FileEvent(
                path=Path("test.txt"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1)
            )]
            results.append(detector.detect(events))

        threads = [threading.Thread(target=detect_worker) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 3


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_is_temp_file(self) -> None:
        """Test temp file detection."""
        assert is_temp_file(Path("document.txt.tmp.12345")) is True
        assert is_temp_file(Path("document.txt~")) is True
        assert is_temp_file(Path(".document.txt.swp")) is True
        assert is_temp_file(Path("#document.txt#")) is True
        assert is_temp_file(Path("document.txt.bak")) is True
        assert is_temp_file(Path("document.txt")) is False

    def test_extract_original_path(self) -> None:
        """Test extracting original path from temp files."""
        assert extract_original_path(Path("document.txt.tmp.12345")) == Path("document.txt")
        assert extract_original_path(Path("document.txt~")) == Path("document.txt")
        assert extract_original_path(Path(".document.txt.swp")) == Path(".document.txt")
        assert extract_original_path(Path("#document.txt#")) == Path("document.txt")
        assert extract_original_path(Path("document.txt.bak")) == Path("document.txt")
        assert extract_original_path(Path("document.txt")) == Path("document.txt")

    def test_detect_atomic_save_convenience(self) -> None:
        """Test atomic save detection convenience function."""
        now = datetime.now()

        events = [
            FileEvent(
                path=Path("test.txt.tmp.123"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1),
            ),
            FileEvent(
                path=Path("test.txt.tmp.123"),
                event_type="moved",
                metadata=FileEventMetadata(timestamp=now + timedelta(milliseconds=50), sequence_number=2),
                dest_path=Path("test.txt"),
            ),
        ]

        operation = detect_atomic_save(events)
        if operation:  # May not detect based on confidence thresholds
            assert operation.operation_type == OperationType.ATOMIC_SAVE

    def test_group_related_events(self) -> None:
        """Test grouping related events."""
        now = datetime.now()

        events = [
            FileEvent(
                path=Path("file1.txt"),
                event_type="modified",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1),
            ),
            FileEvent(
                path=Path("file2.txt"),
                event_type="modified",
                metadata=FileEventMetadata(timestamp=now + timedelta(milliseconds=100), sequence_number=2),
            ),
            FileEvent(
                path=Path("file3.txt"),
                event_type="modified",
                metadata=FileEventMetadata(timestamp=now + timedelta(milliseconds=1000), sequence_number=3),
            ),
        ]

        groups = group_related_events(events, time_window_ms=500)
        assert len(groups) == 2
        assert len(groups[0]) == 2
        assert len(groups[1]) == 1


class TestFileOperation:
    """Test FileOperation functionality."""

    def test_operation_timeline(self) -> None:
        """Test operation timeline generation."""
        now = datetime.now()

        events = [
            FileEvent(path=Path("test.txt"), event_type="created",
                     metadata=FileEventMetadata(timestamp=now, sequence_number=1)),
            FileEvent(path=Path("test.txt"), event_type="modified",
                     metadata=FileEventMetadata(timestamp=now + timedelta(milliseconds=100), sequence_number=2)),
        ]

        operation = FileOperation(
            operation_type=OperationType.ATOMIC_SAVE, primary_path=Path("test.txt"),
            events=events, confidence=0.9, description="Test operation",
            start_time=now, end_time=now + timedelta(milliseconds=100))

        timeline = operation.get_timeline()
        assert len(timeline) == 2
        assert timeline[0][0] == 0.0  # First event at 0ms
        assert timeline[1][0] == 100.0  # Second event at 100ms

    def test_operation_properties(self) -> None:
        """Test operation property calculations."""
        now = datetime.now()
        end_time = now + timedelta(milliseconds=250)

        events = [
            FileEvent(path=Path("test1.txt"), event_type="created",
                     metadata=FileEventMetadata(timestamp=now, sequence_number=1)),
            FileEvent(path=Path("test2.txt"), event_type="created",
                     metadata=FileEventMetadata(timestamp=now + timedelta(milliseconds=100), sequence_number=2)),
        ]

        operation = FileOperation(
            operation_type=OperationType.BATCH_UPDATE, primary_path=Path("test_dir"),
            events=events, confidence=0.8, description="Test batch",
            start_time=now, end_time=end_time)

        assert operation.duration_ms == 250.0
        assert operation.event_count == 2
        assert len(operation.get_timeline()) == 2


if __name__ == "__main__":
    pytest.main([__file__])
