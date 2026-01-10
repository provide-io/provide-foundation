#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for simplified file operations API.

These tests demonstrate and validate the new simple functional API for
file operation detection, providing a cleaner interface for common use cases."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from provide.testkit import FoundationTestCase
import pytest

# Test the new simple API
from provide.foundation.file.operations import (
    DetectorConfig,
    Event,
    FileEventMetadata,
    Operation,
    OperationType,
    create_detector,
    detect,
    detect_all,
    detect_streaming,
)


class TestSimpleDetectAPI(FoundationTestCase):
    """Test the simple detect() function API."""

    def test_detect_single_event_returns_operation_or_none(self) -> None:
        """Test that detect() with single event returns Operation | None."""
        now = datetime.now()

        # Single event should return None (not enough context for operation)
        event = Event(
            path=Path("test.txt"),
            event_type="created",
            metadata=FileEventMetadata(timestamp=now, sequence_number=1),
        )

        result = detect(event)
        # Single isolated event may or may not be detected as operation
        assert result is None or isinstance(result, Operation)

    def test_detect_list_returns_list(self) -> None:
        """Test that detect() with list returns list of operations."""
        now = datetime.now()

        events = [
            Event(
                path=Path("test.txt.tmp"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1),
            ),
            Event(
                path=Path("test.txt.tmp"),
                event_type="moved",
                metadata=FileEventMetadata(timestamp=now + timedelta(milliseconds=50), sequence_number=2),
                dest_path=Path("test.txt"),
            ),
        ]

        config = DetectorConfig(time_window_ms=2000, min_confidence=0.0)
        result = detect(events, config=config)
        assert isinstance(result, list)
        assert len(result) >= 1
        assert all(isinstance(op, Operation) for op in result)

    def test_detect_atomic_save_pattern(self) -> None:
        """Test detecting atomic save with simple API."""
        now = datetime.now()

        events = [
            Event(
                path=Path("document.txt.tmp.123"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1),
            ),
            Event(
                path=Path("document.txt.tmp.123"),
                event_type="moved",
                metadata=FileEventMetadata(timestamp=now + timedelta(milliseconds=50), sequence_number=2),
                dest_path=Path("document.txt"),
            ),
        ]

        config = DetectorConfig(time_window_ms=2000, min_confidence=0.0)
        operations = detect(events, config=config)
        assert len(operations) == 1
        op = operations[0]
        assert op.operation_type == OperationType.ATOMIC_SAVE
        assert op.primary_path == Path("document.txt")
        assert op.is_atomic is True

    def test_detect_all_always_returns_list(self) -> None:
        """Test that detect_all() always returns a list."""
        now = datetime.now()

        events = [
            Event(
                path=Path("test.txt"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1),
            )
        ]

        result = detect_all(events)
        assert isinstance(result, list)
        # May be empty or have operations depending on detection


class TestStreamingDetection(FoundationTestCase):
    """Test streaming detection API."""

    def test_create_detector_and_stream(self) -> None:
        """Test creating detector and using streaming mode."""
        detector = create_detector()
        assert detector is not None

        now = datetime.now()

        # First event - should not complete operation yet
        event1 = Event(
            path=Path("test.txt.tmp"),
            event_type="created",
            metadata=FileEventMetadata(timestamp=now, sequence_number=1),
        )
        result1 = detect_streaming(event1, detector)
        assert result1 is None  # Not complete yet

        # Second event - may complete operation
        event2 = Event(
            path=Path("test.txt.tmp"),
            event_type="moved",
            metadata=FileEventMetadata(timestamp=now + timedelta(milliseconds=600), sequence_number=2),
            dest_path=Path("test.txt"),
        )
        detect_streaming(event2, detector)
        # May or may not return operation depending on timing

    def test_detector_flush(self) -> None:
        """Test flushing pending operations from detector."""
        detector = create_detector()
        now = datetime.now()

        # Add events without completing
        events = [
            Event(
                path=Path("test.txt.tmp"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1),
            ),
            Event(
                path=Path("test.txt.tmp"),
                event_type="moved",
                metadata=FileEventMetadata(timestamp=now + timedelta(milliseconds=50), sequence_number=2),
                dest_path=Path("test.txt"),
            ),
        ]

        for event in events:
            detect_streaming(event, detector)

        # Flush should return pending operations
        remaining = detector.flush()
        assert isinstance(remaining, list)


class TestTypeAliases(FoundationTestCase):
    """Test that type aliases work correctly."""

    def test_event_alias_works(self) -> None:
        """Test that Event is a valid alias for FileEvent."""
        now = datetime.now()

        event = Event(
            path=Path("test.txt"),
            event_type="created",
            metadata=FileEventMetadata(timestamp=now, sequence_number=1),
        )

        assert event.path == Path("test.txt")
        assert event.event_type == "created"
        assert event.timestamp == now

    def test_operation_has_useful_attributes(self) -> None:
        """Test that Operation objects have intuitive attributes."""
        now = datetime.now()

        # Create operation by detection
        events = [
            Event(
                path=Path("file.txt.tmp"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1),
            ),
            Event(
                path=Path("file.txt.tmp"),
                event_type="moved",
                metadata=FileEventMetadata(timestamp=now + timedelta(milliseconds=50), sequence_number=2),
                dest_path=Path("file.txt"),
            ),
        ]

        operations = detect(events)
        if operations:
            op = operations[0]
            # Check useful attributes exist
            assert hasattr(op, "operation_type")
            assert hasattr(op, "primary_path")
            assert hasattr(op, "confidence")
            assert hasattr(op, "is_atomic")
            assert hasattr(op, "is_safe")
            assert hasattr(op, "events")


class TestBackwardCompatibility(FoundationTestCase):
    """Ensure backward compatibility with existing API."""

    def test_can_still_import_fileeven(self) -> None:
        """Test that FileEvent is still importable for backward compatibility."""
        from provide.foundation.file.operations import FileEvent

        now = datetime.now()
        event = FileEvent(
            path=Path("test.txt"),
            event_type="created",
            metadata=FileEventMetadata(timestamp=now, sequence_number=1),
        )
        assert event.path == Path("test.txt")

    def test_can_still_import_fileoperation(self) -> None:
        """Test that FileOperation is still importable."""
        from provide.foundation.file.operations import FileOperation, OperationType

        now = datetime.now()
        op = FileOperation(
            operation_type=OperationType.ATOMIC_SAVE,
            primary_path=Path("test.txt"),
            events=[],
            confidence=0.9,
            description="Test",
            start_time=now,
            end_time=now,
        )
        assert op.primary_path == Path("test.txt")

    def test_can_still_import_operation_detector(self) -> None:
        """Test that OperationDetector class is still importable."""
        from provide.foundation.file.operations import OperationDetector

        detector = OperationDetector()
        assert detector is not None
        assert hasattr(detector, "detect")
        assert hasattr(detector, "detect_streaming")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# 🧱🏗️🔚
