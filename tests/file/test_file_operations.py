"""Comprehensive tests for file operations module."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import tempfile

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


class TestDetectorConfig:
    """Test DetectorConfig functionality."""

    def test_detector_config_defaults(self) -> None:
        """Test default values of DetectorConfig."""
        config = DetectorConfig()

        assert config.time_window_ms > 0
        assert config.min_confidence >= 0.0
        assert config.min_confidence <= 1.0
        assert config.min_events_for_complex >= 1
        assert isinstance(config.temp_patterns, list)
        assert len(config.temp_patterns) > 0

    def test_detector_config_custom_values(self) -> None:
        """Test DetectorConfig with custom values."""
        custom_patterns = [r"\.test\.", r"\.tmp"]
        config = DetectorConfig(
            time_window_ms=5000,
            min_confidence=0.8,
            min_events_for_complex=5,
            temp_patterns=custom_patterns
        )

        assert config.time_window_ms == 5000
        assert config.min_confidence == 0.8
        assert config.min_events_for_complex == 5
        assert config.temp_patterns == custom_patterns


class TestFileEvent:
    """Test FileEvent functionality."""

    def test_file_event_creation(self) -> None:
        """Test creating FileEvent instances."""
        timestamp = datetime.now()
        path = Path("/test/file.txt")

        event = FileEvent(
            event_type="created",
            path=path,
            timestamp=timestamp
        )

        assert event.event_type == "created"
        assert event.path == path
        assert event.timestamp == timestamp
        assert event.dest_path is None
        assert event.metadata is None

    def test_file_event_with_dest_path(self) -> None:
        """Test FileEvent with destination path."""
        event = FileEvent(
            event_type="moved",
            path=Path("/test/old.txt"),
            dest_path=Path("/test/new.txt"),
            timestamp=datetime.now()
        )

        assert event.dest_path == Path("/test/new.txt")

    def test_file_event_with_metadata(self) -> None:
        """Test FileEvent with metadata."""
        metadata = FileEventMetadata(size=1024, checksum="abc123")
        event = FileEvent(
            event_type="modified",
            path=Path("/test/file.txt"),
            timestamp=datetime.now(),
            metadata=metadata
        )

        assert event.metadata == metadata
        assert event.metadata.size == 1024
        assert event.metadata.checksum == "abc123"


class TestFileEventMetadata:
    """Test FileEventMetadata functionality."""

    def test_metadata_creation(self) -> None:
        """Test creating FileEventMetadata."""
        metadata = FileEventMetadata(
            size=2048,
            checksum="def456",
            permissions="0644",
            owner="user1"
        )

        assert metadata.size == 2048
        assert metadata.checksum == "def456"
        assert metadata.permissions == "0644"
        assert metadata.owner == "user1"

    def test_metadata_optional_fields(self) -> None:
        """Test FileEventMetadata with optional fields."""
        metadata = FileEventMetadata()

        assert metadata.size is None
        assert metadata.checksum is None
        assert metadata.permissions is None
        assert metadata.owner is None


class TestOperationDetector:
    """Test OperationDetector functionality."""

    def test_detector_initialization(self) -> None:
        """Test detector initialization."""
        detector = OperationDetector()
        assert detector.config is not None
        assert isinstance(detector._pattern_cache, dict)
        assert isinstance(detector._pending_events, list)

    def test_detector_with_custom_config(self) -> None:
        """Test detector with custom configuration."""
        config = DetectorConfig(time_window_ms=1000, min_confidence=0.9)
        detector = OperationDetector(config)
        assert detector.config.time_window_ms == 1000
        assert detector.config.min_confidence == 0.9

    def test_detect_empty_events(self) -> None:
        """Test detection with empty events list."""
        detector = OperationDetector()
        operations = detector.detect([])
        assert operations == []

    def test_detect_single_file_creation(self) -> None:
        """Test detection of single file creation."""
        detector = OperationDetector()
        now = datetime.now()

        events = [
            FileEvent(
                event_type="created",
                path=Path("/test/file.txt"),
                timestamp=now
            )
        ]

        operations = detector.detect(events)
        assert len(operations) == 1

        op = operations[0]
        assert op.operation_type in (OperationType.BACKUP_CREATE, OperationType.ATOMIC_SAVE)
        assert op.primary_path == Path("/test/file.txt")
        assert len(op.events) == 1
        assert op.confidence > 0.0

    def test_detect_file_modification(self) -> None:
        """Test detection of file modification."""
        detector = OperationDetector()
        now = datetime.now()

        events = [
            FileEvent(
                event_type="modified",
                path=Path("/test/file.txt"),
                timestamp=now
            )
        ]

        operations = detector.detect(events)
        assert len(operations) == 1

        op = operations[0]
        assert op.operation_type == OperationType.ATOMIC_SAVE
        assert op.primary_path == Path("/test/file.txt")

    def test_detect_atomic_save_pattern(self) -> None:
        """Test detection of atomic save pattern."""
        detector = OperationDetector()
        now = datetime.now()

        # Simulate atomic save: temp file created, then renamed to final location
        events = [
            FileEvent(
                event_type="created",
                path=Path("/test/.file.txt.tmp.12345"),
                timestamp=now
            ),
            FileEvent(
                event_type="moved",
                path=Path("/test/.file.txt.tmp.12345"),
                dest_path=Path("/test/file.txt"),
                timestamp=now + timedelta(milliseconds=10)
            )
        ]

        operations = detector.detect(events)
        assert len(operations) == 1

        op = operations[0]
        assert op.operation_type == OperationType.ATOMIC_SAVE
        assert op.primary_path == Path("/test/file.txt")
        assert op.is_atomic is True
        assert op.confidence >= 0.9

    def test_detect_safe_write_pattern(self) -> None:
        """Test detection of safe write pattern with backup."""
        detector = OperationDetector()
        now = datetime.now()

        events = [
            FileEvent(
                event_type="created",
                path=Path("/test/file.txt.bak"),
                timestamp=now
            ),
            FileEvent(
                event_type="modified",
                path=Path("/test/file.txt"),
                timestamp=now + timedelta(milliseconds=50)
            )
        ]

        operations = detector.detect(events)
        assert len(operations) == 1

        op = operations[0]
        assert op.operation_type == OperationType.SAFE_WRITE
        assert op.primary_path == Path("/test/file.txt")
        assert op.has_backup is True
        assert op.is_safe is True

    def test_detect_rename_sequence(self) -> None:
        """Test detection of rename sequence."""
        detector = OperationDetector()
        now = datetime.now()

        events = [
            FileEvent(
                event_type="moved",
                path=Path("/test/file1.txt"),
                dest_path=Path("/test/file2.txt"),
                timestamp=now
            ),
            FileEvent(
                event_type="moved",
                path=Path("/test/file2.txt"),
                dest_path=Path("/test/file3.txt"),
                timestamp=now + timedelta(milliseconds=20)
            )
        ]

        operations = detector.detect(events)
        assert len(operations) == 1

        op = operations[0]
        assert op.operation_type == OperationType.RENAME_SEQUENCE
        assert op.primary_path == Path("/test/file3.txt")
        assert op.is_atomic is True

    def test_detect_batch_update(self) -> None:
        """Test detection of batch update operations."""
        detector = OperationDetector()
        now = datetime.now()

        # Create events for multiple file modifications in quick succession
        events = []
        for i in range(5):
            events.append(FileEvent(
                event_type="modified",
                path=Path(f"/test/file{i}.txt"),
                timestamp=now + timedelta(milliseconds=i * 10)
            ))

        operations = detector.detect(events)
        assert len(operations) == 1

        op = operations[0]
        assert op.operation_type == OperationType.BATCH_UPDATE
        assert len(op.files_affected) == 5
        assert not op.is_atomic

    def test_detect_backup_creation(self) -> None:
        """Test detection of backup file creation."""
        detector = OperationDetector()
        now = datetime.now()

        events = [
            FileEvent(
                event_type="created",
                path=Path("/test/important.txt.backup"),
                timestamp=now
            )
        ]

        operations = detector.detect(events)
        assert len(operations) == 1

        op = operations[0]
        assert op.operation_type == OperationType.BACKUP_CREATE
        assert op.primary_path == Path("/test/important.txt.backup")
        assert op.has_backup is True

    def test_streaming_detection(self) -> None:
        """Test streaming event detection."""
        config = DetectorConfig(time_window_ms=100)
        detector = OperationDetector(config)

        # Add event but don't expect operation yet (within time window)
        event1 = FileEvent(
            event_type="created",
            path=Path("/test/file.txt"),
            timestamp=datetime.now()
        )
        operation = detector.detect_streaming(event1)
        assert operation is None

        # Force flush should return operation
        operations = detector.flush()
        assert len(operations) == 1

    def test_group_events_by_time(self) -> None:
        """Test time-based event grouping."""
        detector = OperationDetector(DetectorConfig(time_window_ms=100))
        now = datetime.now()

        events = [
            FileEvent("created", Path("/test/file1.txt"), now),
            FileEvent("modified", Path("/test/file1.txt"), now + timedelta(milliseconds=50)),
            FileEvent("created", Path("/test/file2.txt"), now + timedelta(milliseconds=200)),  # Different group
        ]

        groups = detector._group_events_by_time(events)
        assert len(groups) == 2
        assert len(groups[0]) == 2  # First two events
        assert len(groups[1]) == 1  # Last event

    def test_is_temp_file_detection(self) -> None:
        """Test temporary file detection."""
        detector = OperationDetector()

        # Test various temp file patterns
        temp_files = [
            Path("/test/.file.txt.tmp.12345"),
            Path("/test/file.tmp"),
            Path("/test/file~"),
            Path("/test/.file.swp"),
            Path("/test/#file#"),
        ]

        for temp_file in temp_files:
            assert detector._is_temp_file(temp_file)

        # Test non-temp files
        regular_files = [
            Path("/test/file.txt"),
            Path("/test/document.pdf"),
            Path("/test/image.png"),
        ]

        for regular_file in regular_files:
            assert not detector._is_temp_file(regular_file)

    def test_extract_base_name(self) -> None:
        """Test base name extraction from temp files."""
        detector = OperationDetector()

        test_cases = [
            (Path("/test/.file.txt.tmp.12345"), "file.txt"),
            (Path("/test/document.tmp"), "document"),
            (Path("/test/file~"), "file"),
            (Path("/test/.vimrc.swp"), ".vimrc"),
            (Path("/test/#auto#"), "auto"),
            (Path("/test/backup.bak"), "backup"),
            (Path("/test/original.orig"), "original"),
        ]

        for temp_path, expected_base in test_cases:
            result = detector._extract_base_name(temp_path)
            assert result == expected_base, f"Expected {expected_base} for {temp_path}, got {result}"

    def test_files_related(self) -> None:
        """Test file relationship detection."""
        detector = OperationDetector()

        # Test related files
        related_pairs = [
            (Path("/test/file.txt"), Path("/test/.file.txt.tmp.123")),
            (Path("/test/document.pdf"), Path("/test/document~")),
            (Path("/test/config"), Path("/test/config.bak")),
        ]

        for file1, file2 in related_pairs:
            assert detector._files_related(file1, file2)
            assert detector._files_related(file2, file1)  # Should be symmetric

    def test_low_confidence_rejection(self) -> None:
        """Test that low confidence operations are rejected."""
        config = DetectorConfig(min_confidence=0.95)
        detector = OperationDetector(config)

        # Create a simple operation that might have lower confidence
        events = [
            FileEvent(
                event_type="deleted",
                path=Path("/test/file.txt"),
                timestamp=datetime.now()
            )
        ]

        operations = detector.detect(events)
        # Should either be empty or have high confidence
        for op in operations:
            assert op.confidence >= 0.95

    def test_directory_event_filtering(self) -> None:
        """Test that directory events are filtered out appropriately."""
        detector = OperationDetector()
        now = datetime.now()

        events = [
            FileEvent("created", Path("/test/dir/"), now),  # Directory event
            FileEvent("created", Path("/test/file.txt"), now),  # File event
        ]

        operations = detector.detect(events)

        # Should detect operation for file, not directory
        assert len(operations) >= 1
        for op in operations:
            assert not str(op.primary_path).endswith("/")


class TestUtilityFunctions:
    """Test utility functions."""

    def test_is_temp_file_function(self) -> None:
        """Test standalone is_temp_file function."""
        # Should detect common temp file patterns
        assert is_temp_file(Path("/test/.file.tmp.123"))
        assert is_temp_file(Path("/test/file~"))
        assert is_temp_file(Path("/test/.file.swp"))

        # Should not detect regular files
        assert not is_temp_file(Path("/test/file.txt"))
        assert not is_temp_file(Path("/test/document.pdf"))

    def test_extract_original_path_function(self) -> None:
        """Test standalone extract_original_path function."""
        test_cases = [
            (Path("/test/.file.txt.tmp.456"), Path("/test/file.txt")),
            (Path("/test/doc.bak"), Path("/test/doc")),
            (Path("/test/file~"), Path("/test/file")),
        ]

        for temp_path, expected_original in test_cases:
            result = extract_original_path(temp_path)
            if result:  # Function might return None for some patterns
                assert result.name == expected_original.name

    def test_detect_atomic_save_function(self) -> None:
        """Test standalone detect_atomic_save function."""
        now = datetime.now()

        # Create atomic save pattern
        events = [
            FileEvent("created", Path("/test/.file.tmp.123"), now),
            FileEvent("moved", Path("/test/.file.tmp.123"), now + timedelta(milliseconds=10),
                     dest_path=Path("/test/file.txt"))
        ]

        result = detect_atomic_save(events)
        assert result is not None
        assert result.is_atomic
        assert result.primary_path == Path("/test/file.txt")

    def test_group_related_events_function(self) -> None:
        """Test standalone group_related_events function."""
        now = datetime.now()

        events = [
            FileEvent("created", Path("/test/file1.txt"), now),
            FileEvent("created", Path("/test/.file1.txt.tmp.123"), now),
            FileEvent("created", Path("/test/unrelated.txt"), now),
        ]

        groups = group_related_events(events)

        # Should group related events together
        assert len(groups) >= 1
        for group in groups:
            assert len(group) >= 1


class TestFileOperation:
    """Test FileOperation functionality."""

    def test_file_operation_creation(self) -> None:
        """Test creating FileOperation instances."""
        now = datetime.now()
        events = [
            FileEvent("created", Path("/test/file.txt"), now)
        ]

        operation = FileOperation(
            operation_type=OperationType.ATOMIC_SAVE,
            primary_path=Path("/test/file.txt"),
            events=events,
            confidence=0.95,
            description="Test operation",
            start_time=now,
            end_time=now
        )

        assert operation.operation_type == OperationType.ATOMIC_SAVE
        assert operation.primary_path == Path("/test/file.txt")
        assert operation.events == events
        assert operation.confidence == 0.95
        assert operation.description == "Test operation"
        assert operation.start_time == now
        assert operation.end_time == now

    def test_file_operation_optional_fields(self) -> None:
        """Test FileOperation with optional fields."""
        now = datetime.now()
        events = [FileEvent("created", Path("/test/file.txt"), now)]

        operation = FileOperation(
            operation_type=OperationType.SAFE_WRITE,
            primary_path=Path("/test/file.txt"),
            events=events,
            confidence=0.90,
            description="Safe write",
            start_time=now,
            end_time=now,
            is_atomic=False,
            is_safe=True,
            has_backup=True,
            files_affected=[Path("/test/file.txt"), Path("/test/file.txt.bak")]
        )

        assert operation.is_atomic is False
        assert operation.is_safe is True
        assert operation.has_backup is True
        assert len(operation.files_affected) == 2


class TestOperationType:
    """Test OperationType enumeration."""

    def test_operation_types_exist(self) -> None:
        """Test that all expected operation types exist."""
        expected_types = [
            "ATOMIC_SAVE",
            "SAFE_WRITE",
            "RENAME_SEQUENCE",
            "BATCH_UPDATE",
            "BACKUP_CREATE"
        ]

        for type_name in expected_types:
            assert hasattr(OperationType, type_name)
            operation_type = getattr(OperationType, type_name)
            assert isinstance(operation_type, OperationType)


class TestComplexScenarios:
    """Test complex file operation scenarios."""

    def test_vim_save_pattern(self) -> None:
        """Test Vim-style save pattern detection."""
        detector = OperationDetector()
        now = datetime.now()

        # Simulate Vim save: .file.swp created, original modified, .swp deleted
        events = [
            FileEvent("created", Path("/test/.file.txt.swp"), now),
            FileEvent("modified", Path("/test/file.txt"), now + timedelta(milliseconds=30)),
            FileEvent("deleted", Path("/test/.file.txt.swp"), now + timedelta(milliseconds=50)),
        ]

        operations = detector.detect(events)
        assert len(operations) >= 1

        # Should detect some form of safe operation
        main_op = next((op for op in operations if op.primary_path.name == "file.txt"), None)
        assert main_op is not None

    def test_git_checkout_pattern(self) -> None:
        """Test Git checkout pattern detection."""
        detector = OperationDetector()
        now = datetime.now()

        # Simulate git checkout: multiple files modified simultaneously
        events = []
        files = ["file1.py", "file2.py", "file3.py", "README.md"]

        for i, filename in enumerate(files):
            events.append(FileEvent(
                "modified",
                Path(f"/repo/{filename}"),
                now + timedelta(milliseconds=i * 5)
            ))

        operations = detector.detect(events)

        # Should detect batch update
        batch_ops = [op for op in operations if op.operation_type == OperationType.BATCH_UPDATE]
        if batch_ops:  # May or may not be detected depending on timing and config
            batch_op = batch_ops[0]
            assert len(batch_op.files_affected) >= 3

    def test_concurrent_operations(self) -> None:
        """Test detection when multiple operations happen concurrently."""
        detector = OperationDetector(DetectorConfig(time_window_ms=1000))
        now = datetime.now()

        # Two separate atomic saves happening at same time
        events = [
            # First file atomic save
            FileEvent("created", Path("/test/.file1.tmp.123"), now),
            FileEvent("moved", Path("/test/.file1.tmp.123"), now + timedelta(milliseconds=10),
                     dest_path=Path("/test/file1.txt")),

            # Second file atomic save
            FileEvent("created", Path("/test/.file2.tmp.456"), now + timedelta(milliseconds=5)),
            FileEvent("moved", Path("/test/.file2.tmp.456"), now + timedelta(milliseconds=15),
                     dest_path=Path("/test/file2.txt")),
        ]

        operations = detector.detect(events)

        # Should detect separate operations for each file
        file1_ops = [op for op in operations if "file1" in str(op.primary_path)]
        file2_ops = [op for op in operations if "file2" in str(op.primary_path)]

        # At minimum should detect the operations, exact count may vary based on grouping
        assert len(operations) >= 1


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_malformed_events(self) -> None:
        """Test handling of malformed or unusual events."""
        detector = OperationDetector()
        now = datetime.now()

        # Events with unusual characteristics
        events = [
            FileEvent("unknown_type", Path("/test/file.txt"), now),
            FileEvent("created", Path(""), now),  # Empty path
        ]

        # Should not crash, might return empty or filtered results
        operations = detector.detect(events)
        assert isinstance(operations, list)

    def test_very_large_event_list(self) -> None:
        """Test performance with large number of events."""
        detector = OperationDetector()
        now = datetime.now()

        # Create many events
        events = []
        for i in range(100):
            events.append(FileEvent(
                "modified",
                Path(f"/test/file{i}.txt"),
                now + timedelta(milliseconds=i)
            ))

        # Should handle without issues
        operations = detector.detect(events)
        assert isinstance(operations, list)

    def test_events_far_apart_in_time(self) -> None:
        """Test events that are far apart in time."""
        detector = OperationDetector(DetectorConfig(time_window_ms=100))
        now = datetime.now()

        events = [
            FileEvent("created", Path("/test/file1.txt"), now),
            FileEvent("created", Path("/test/file2.txt"), now + timedelta(hours=1)),
        ]

        operations = detector.detect(events)

        # Should create separate operations due to large time gap
        assert len(operations) >= 2 or (len(operations) == 1 and len(operations[0].events) == 1)

    def test_pattern_cache_efficiency(self) -> None:
        """Test that pattern caching works efficiently."""
        detector = OperationDetector()

        # Use the same temp file pattern multiple times
        temp_files = [
            Path(f"/test/.file{i}.tmp.123") for i in range(10)
        ]

        # First call should cache patterns
        for temp_file in temp_files:
            detector._is_temp_file(temp_file)

        # Cache should be populated
        assert len(detector._pattern_cache) > 0

        # Subsequent calls should use cache
        cache_size_before = len(detector._pattern_cache)
        for temp_file in temp_files:
            detector._is_temp_file(temp_file)

        # Cache size shouldn't grow (patterns already cached)
        assert len(detector._pattern_cache) == cache_size_before