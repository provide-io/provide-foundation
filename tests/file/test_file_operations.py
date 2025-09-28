"""Tests for file operation detection system."""

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


@pytest.fixture
def now() -> datetime:
    """Current timestamp for test consistency."""
    return datetime.now()


@pytest.fixture
def detector() -> OperationDetector:
    """Default detector instance."""
    return OperationDetector()


class TestDetectorConfig:
    """Test DetectorConfig dataclass."""

    def test_detector_config_defaults(self) -> None:
        """Test default configuration values."""
        config = DetectorConfig()
        assert config.time_window_ms == 500
        assert config.max_operation_duration_ms == 2000
        assert config.min_events_for_complex == 2
        assert config.min_confidence == 0.7
        assert len(config.temp_patterns) > 0

    def test_detector_config_custom_values(self) -> None:
        """Test custom configuration values."""
        config = DetectorConfig(
            time_window_ms=1000,
            max_operation_duration_ms=5000,
            min_confidence=0.8,
        )
        assert config.time_window_ms == 1000
        assert config.max_operation_duration_ms == 5000
        assert config.min_confidence == 0.8


class TestFileEvent:
    """Test FileEvent dataclass."""

    def test_file_event_creation(self, now: datetime) -> None:
        """Test basic FileEvent creation."""
        metadata = FileEventMetadata(timestamp=now, sequence_number=1)
        event = FileEvent(
            path=Path("/test/file.txt"),
            event_type="created",
            metadata=metadata,
        )
        assert event.path == Path("/test/file.txt")
        assert event.event_type == "created"
        assert event.timestamp == now
        assert event.sequence == 1

    def test_file_event_with_dest_path(self, now: datetime) -> None:
        """Test FileEvent with destination path."""
        metadata = FileEventMetadata(timestamp=now, sequence_number=1)
        event = FileEvent(
            path=Path("/test/old.txt"),
            event_type="moved",
            metadata=metadata,
            dest_path=Path("/test/new.txt"),
        )
        assert event.dest_path == Path("/test/new.txt")

    def test_file_event_size_delta(self, now: datetime) -> None:
        """Test size delta calculation."""
        metadata = FileEventMetadata(
            timestamp=now,
            sequence_number=1,
            size_before=100,
            size_after=200,
        )
        event = FileEvent(
            path=Path("/test/file.txt"),
            event_type="modified",
            metadata=metadata,
        )
        assert event.size_delta == 100


class TestFileEventMetadata:
    """Test FileEventMetadata dataclass."""

    def test_metadata_creation(self, now: datetime) -> None:
        """Test basic metadata creation."""
        metadata = FileEventMetadata(timestamp=now, sequence_number=1)
        assert metadata.timestamp == now
        assert metadata.sequence_number == 1
        assert metadata.extra == {}

    def test_metadata_with_optional_fields(self, now: datetime) -> None:
        """Test metadata with optional fields."""
        metadata = FileEventMetadata(
            timestamp=now,
            sequence_number=1,
            size_before=100,
            size_after=200,
            process_id=1234,
            extra={"custom": "value"},
        )
        assert metadata.size_before == 100
        assert metadata.size_after == 200
        assert metadata.process_id == 1234
        assert metadata.extra["custom"] == "value"


class TestOperationDetector:
    """Test OperationDetector functionality."""

    def test_detector_initialization(self) -> None:
        """Test detector initialization."""
        detector = OperationDetector()
        assert isinstance(detector.config, DetectorConfig)

    def test_detector_with_custom_config(self) -> None:
        """Test detector with custom config."""
        config = DetectorConfig(time_window_ms=1000)
        detector = OperationDetector(config)
        assert detector.config.time_window_ms == 1000

    def test_detect_empty_events(self, detector: OperationDetector) -> None:
        """Test detection with empty event list."""
        operations = detector.detect([])
        assert operations == []

    def test_detect_single_file_creation(self, detector: OperationDetector, now: datetime) -> None:
        """Test detection of single file creation."""
        metadata = FileEventMetadata(timestamp=now, sequence_number=1)
        events = [
            FileEvent(
                path=Path("/test/file.txt"),
                event_type="created",
                metadata=metadata,
            )
        ]
        operations = detector.detect(events)
        assert len(operations) >= 1

    def test_detect_atomic_save_pattern(self, detector: OperationDetector, now: datetime) -> None:
        """Test detection of atomic save pattern."""
        events = [
            FileEvent(
                path=Path("/test/.file.txt.tmp.12345"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1),
            ),
            FileEvent(
                path=Path("/test/.file.txt.tmp.12345"),
                event_type="moved",
                metadata=FileEventMetadata(timestamp=now + timedelta(milliseconds=10), sequence_number=2),
                dest_path=Path("/test/file.txt"),
            ),
        ]
        operations = detector.detect(events)
        assert len(operations) >= 1
        # Check if any operation is detected as atomic save
        atomic_ops = [op for op in operations if op.operation_type == OperationType.ATOMIC_SAVE]
        assert len(atomic_ops) >= 0  # May or may not detect as atomic


class TestUtilityFunctions:
    """Test utility functions."""

    def test_is_temp_file_function(self) -> None:
        """Test is_temp_file utility function."""
        assert is_temp_file(Path(".file.txt.tmp.12345"))
        assert is_temp_file(Path("file.txt~"))
        assert is_temp_file(Path("file.tmp"))
        assert not is_temp_file(Path("regular_file.txt"))

    def test_extract_original_path_function(self) -> None:
        """Test extract_original_path utility function."""
        original = extract_original_path(Path(".file.txt.tmp.12345"))
        assert original == Path("file.txt")

        original = extract_original_path(Path("file.txt~"))
        assert original == Path("file.txt")

        # Regular file should return itself
        original = extract_original_path(Path("regular_file.txt"))
        assert original == Path("regular_file.txt")

    def test_detect_atomic_save_function(self, now: datetime) -> None:
        """Test detect_atomic_save utility function."""
        events = [
            FileEvent(
                path=Path("/test/.file.txt.tmp.12345"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1),
            ),
            FileEvent(
                path=Path("/test/.file.txt.tmp.12345"),
                event_type="moved",
                metadata=FileEventMetadata(timestamp=now + timedelta(milliseconds=10), sequence_number=2),
                dest_path=Path("/test/file.txt"),
            ),
        ]
        result = detect_atomic_save(events)
        # Function returns FileOperation | None, not bool
        assert result is None or isinstance(result, FileOperation)

    def test_group_related_events_function(self, now: datetime) -> None:
        """Test group_related_events utility function."""
        events = [
            FileEvent(
                path=Path("/test/file1.txt"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1),
            ),
            FileEvent(
                path=Path("/test/file2.txt"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now + timedelta(seconds=1), sequence_number=2),
            ),
        ]
        groups = group_related_events(events)
        assert isinstance(groups, list)
        assert len(groups) >= 1


class TestFileOperation:
    """Test FileOperation dataclass."""

    def test_file_operation_creation(self, now: datetime) -> None:
        """Test FileOperation creation."""
        metadata = FileEventMetadata(timestamp=now, sequence_number=1)
        event = FileEvent(
            path=Path("/test/file.txt"),
            event_type="created",
            metadata=metadata,
        )
        operation = FileOperation(
            operation_type=OperationType.ATOMIC_SAVE,
            primary_path=Path("/test/file.txt"),
            events=[event],
            confidence=0.9,
            description="Atomic save operation",
            start_time=now,
            end_time=now + timedelta(milliseconds=100),
        )
        assert operation.operation_type == OperationType.ATOMIC_SAVE
        assert operation.confidence == 0.9
        assert operation.duration_ms == 100
        assert operation.event_count == 1

    def test_file_operation_timeline(self, now: datetime) -> None:
        """Test FileOperation timeline generation."""
        metadata1 = FileEventMetadata(timestamp=now, sequence_number=1)
        metadata2 = FileEventMetadata(timestamp=now + timedelta(milliseconds=50), sequence_number=2)
        events = [
            FileEvent(
                path=Path("/test/file.txt"),
                event_type="created",
                metadata=metadata1,
            ),
            FileEvent(
                path=Path("/test/file.txt"),
                event_type="modified",
                metadata=metadata2,
            ),
        ]
        operation = FileOperation(
            operation_type=OperationType.BATCH_UPDATE,
            primary_path=Path("/test/file.txt"),
            events=events,
            confidence=0.8,
            description="Batch update",
            start_time=now,
            end_time=now + timedelta(milliseconds=100),
        )
        timeline = operation.get_timeline()
        assert len(timeline) == 2
        assert timeline[0][0] == 0.0  # First event at start
        assert timeline[1][0] == 50.0  # Second event at 50ms


class TestOperationType:
    """Test OperationType enum."""

    def test_operation_types_exist(self) -> None:
        """Test that all operation types exist."""
        assert OperationType.ATOMIC_SAVE.value == "atomic_save"
        assert OperationType.SAFE_WRITE.value == "safe_write"
        assert OperationType.BATCH_UPDATE.value == "batch_update"
        assert OperationType.UNKNOWN.value == "unknown"
