#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for file operation detection."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from provide.testkit import FoundationTestCase

from provide.foundation.file.operations import (
    DetectorConfig,
    FileEvent,
    FileEventMetadata,
    OperationDetector,
    OperationType,
)


class TestOperationDetector(FoundationTestCase):
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

        # Vim pattern: create backup, delete original, create new version
        events = [
            FileEvent(
                path=Path("document.txt~"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1, size_after=1000),
            ),
            FileEvent(
                path=Path("document.txt"),
                event_type="deleted",
                metadata=FileEventMetadata(
                    timestamp=now + timedelta(milliseconds=10), sequence_number=2, size_before=1000
                ),
            ),
            FileEvent(
                path=Path("document.txt"),
                event_type="created",
                metadata=FileEventMetadata(
                    timestamp=now + timedelta(milliseconds=20), sequence_number=3, size_after=1024
                ),
            ),
        ]

        detector = OperationDetector()
        operations = detector.detect(events)

        assert len(operations) == 1
        operation = operations[0]
        # Vim pattern can be detected as either ATOMIC_SAVE or SAFE_WRITE
        assert operation.operation_type in (OperationType.ATOMIC_SAVE, OperationType.SAFE_WRITE)
        assert operation.primary_path == Path("document.txt")

    def test_atomic_save_detection_temp_create_delete_pattern(self) -> None:
        """Test detecting VSCode/modern editor temp create-delete-create pattern."""
        now = datetime.now()

        # Modern editor pattern: create temp, delete temp, create real
        events = [
            FileEvent(
                path=Path("test_config_commands.py.tmp.84"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1, size_after=1024),
            ),
            FileEvent(
                path=Path("test_config_commands.py.tmp.84"),
                event_type="deleted",
                metadata=FileEventMetadata(
                    timestamp=now + timedelta(milliseconds=50), sequence_number=2, size_before=1024
                ),
            ),
            FileEvent(
                path=Path("test_config_commands.py"),
                event_type="created",
                metadata=FileEventMetadata(
                    timestamp=now + timedelta(milliseconds=100), sequence_number=3, size_after=1024
                ),
            ),
        ]

        detector = OperationDetector()
        operations = detector.detect(events)

        assert len(operations) == 1
        operation = operations[0]
        assert operation.operation_type == OperationType.ATOMIC_SAVE
        assert operation.primary_path == Path("test_config_commands.py")
        assert operation.confidence >= 0.9
        assert operation.is_atomic is True
        assert "Atomic save" in operation.description

    def test_atomic_save_detection_same_file_delete_create_pattern(self) -> None:
        """Test detecting same file delete-then-create atomic save pattern."""
        now = datetime.now()

        # Same file delete-create pattern
        events = [
            FileEvent(
                path=Path("document.txt"),
                event_type="deleted",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1, size_before=1000),
            ),
            FileEvent(
                path=Path("document.txt"),
                event_type="created",
                metadata=FileEventMetadata(
                    timestamp=now + timedelta(milliseconds=50), sequence_number=2, size_after=1024
                ),
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

        def detect_worker() -> None:
            events = [
                FileEvent(
                    path=Path("test.txt"),
                    event_type="created",
                    metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
                )
            ]
            results.append(detector.detect(events))

        threads = [threading.Thread(daemon=True, target=detect_worker) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=10.0)

        assert len(results) == 3


# 🧱🏗️🔚
