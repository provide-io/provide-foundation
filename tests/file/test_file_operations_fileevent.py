#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for file operation detection."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from provide.testkit import FoundationTestCase

from provide.foundation.file.operations import (
    FileEvent,
    FileEventMetadata,
)


class TestFileEvent(FoundationTestCase):
    """Test FileEvent and metadata functionality."""

    def test_metadata_creation(self) -> None:
        """Test creating metadata with all fields."""
        now = datetime.now()
        metadata = FileEventMetadata(
            timestamp=now,
            sequence_number=1,
            size_before=100,
            size_after=200,
            permissions=0o644,
            process_name="vscode",
            extra={"custom": "value"},
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


# 🧱🏗️🔚
