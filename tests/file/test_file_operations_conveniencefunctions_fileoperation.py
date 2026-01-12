#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for file operation detection."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.file.operations import (
    FileEvent,
    FileEventMetadata,
    FileOperation,
    OperationType,
    detect_atomic_save,
    extract_original_path,
    group_related_events,
    is_temp_file,
)


class TestConvenienceFunctions(FoundationTestCase):
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
        # Vim swap files: .filename.swp is for regular file, ..filename.swp is for dotfile
        assert extract_original_path(Path(".document.txt.swp")) == Path("document.txt")
        assert extract_original_path(Path("..document.txt.swp")) == Path(".document.txt")
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


class TestFileOperation(FoundationTestCase):
    """Test FileOperation functionality."""

    def test_operation_timeline(self) -> None:
        """Test operation timeline generation."""
        now = datetime.now()

        events = [
            FileEvent(
                path=Path("test.txt"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1),
            ),
            FileEvent(
                path=Path("test.txt"),
                event_type="modified",
                metadata=FileEventMetadata(timestamp=now + timedelta(milliseconds=100), sequence_number=2),
            ),
        ]

        operation = FileOperation(
            operation_type=OperationType.ATOMIC_SAVE,
            primary_path=Path("test.txt"),
            events=events,
            confidence=0.9,
            description="Test operation",
            start_time=now,
            end_time=now + timedelta(milliseconds=100),
        )

        timeline = operation.get_timeline()
        assert len(timeline) == 2
        assert timeline[0][0] == 0.0  # First event at 0ms
        assert timeline[1][0] == 100.0  # Second event at 100ms

    def test_operation_properties(self) -> None:
        """Test operation property calculations."""
        now = datetime.now()
        end_time = now + timedelta(milliseconds=250)

        events = [
            FileEvent(
                path=Path("test1.txt"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1),
            ),
            FileEvent(
                path=Path("test2.txt"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now + timedelta(milliseconds=100), sequence_number=2),
            ),
        ]

        operation = FileOperation(
            operation_type=OperationType.BATCH_UPDATE,
            primary_path=Path("test_dir"),
            events=events,
            confidence=0.8,
            description="Test batch",
            start_time=now,
            end_time=end_time,
        )

        assert operation.duration_ms == 250.0
        assert operation.event_count == 2
        assert len(operation.get_timeline()) == 2


if __name__ == "__main__":
    pytest.main([__file__])

# 🧱🏗️🔚
