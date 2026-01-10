#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for streaming file operation detection with callback API."""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
from pathlib import Path

from provide.testkit.mocking import Mock
import pytest

from provide.foundation.file.operations import (
    DetectorConfig,
    FileEvent,
    FileEventMetadata,
    OperationDetector,
    OperationType,
)


@pytest.fixture
def mock_callback():
    """Mock callback for operation completion."""
    return Mock()


@pytest.fixture
def detector_with_callback(mock_callback):
    """Create detector with callback configured."""
    config = DetectorConfig(time_window_ms=100, min_confidence=0.7)
    return OperationDetector(config=config, on_operation_complete=mock_callback)


class TestStreamingDetectionCallback:
    """Test streaming detection with callback API."""

    @pytest.mark.asyncio
    async def test_callback_fires_on_operation_complete(self, detector_with_callback, mock_callback) -> None:
        """Test that callback is called when operation is detected."""
        base_time = datetime.now()
        temp_file = Path(".test.py.tmp.123")
        final_file = Path("test.py")

        # Atomic save pattern
        events = [
            FileEvent(
                path=temp_file,
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            ),
            FileEvent(
                path=temp_file,
                event_type="modified",
                metadata=FileEventMetadata(timestamp=base_time + timedelta(milliseconds=5), sequence_number=2),
            ),
            FileEvent(
                path=temp_file,
                event_type="moved",
                dest_path=final_file,
                metadata=FileEventMetadata(
                    timestamp=base_time + timedelta(milliseconds=10), sequence_number=3
                ),
            ),
        ]

        for event in events:
            detector_with_callback.add_event(event)

        # Wait for auto-flush timer to fire
        await asyncio.sleep(0.15)

        # Should have called callback once with the atomic operation
        assert mock_callback.call_count == 1
        operation = mock_callback.call_args[0][0]
        assert operation.operation_type == OperationType.ATOMIC_SAVE
        assert operation.primary_path == final_file

    @pytest.mark.asyncio
    async def test_temp_files_hidden_until_completion(self, detector_with_callback, mock_callback) -> None:
        """Test that temp file events don't trigger callback until operation completes."""
        base_time = datetime.now()
        temp_file = Path(".test.py.tmp.456")
        final_file = Path("test.py")

        # Add temp file creation
        detector_with_callback.add_event(
            FileEvent(
                path=temp_file,
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            )
        )

        # No callback yet - temp file is hidden
        assert mock_callback.call_count == 0

        # Add temp file modification
        detector_with_callback.add_event(
            FileEvent(
                path=temp_file,
                event_type="modified",
                metadata=FileEventMetadata(timestamp=base_time + timedelta(milliseconds=5), sequence_number=2),
            )
        )

        # Still no callback - still buffering
        assert mock_callback.call_count == 0

        # Complete the operation with rename
        detector_with_callback.add_event(
            FileEvent(
                path=temp_file,
                event_type="moved",
                dest_path=final_file,
                metadata=FileEventMetadata(
                    timestamp=base_time + timedelta(milliseconds=10), sequence_number=3
                ),
            )
        )

        # Wait for auto-flush
        await asyncio.sleep(0.15)

        # NOW callback fires with complete operation
        assert mock_callback.call_count == 1
        operation = mock_callback.call_args[0][0]
        assert operation.primary_path == final_file
        assert operation.event_count == 3

    @pytest.mark.asyncio
    async def test_non_temp_file_emits_after_flush(self, detector_with_callback, mock_callback) -> None:
        """Test that non-temp files emit after auto-flush if no operation detected."""
        base_time = datetime.now()
        regular_file = Path("test.py")

        # Single non-temp file event
        detector_with_callback.add_event(
            FileEvent(
                path=regular_file,
                event_type="modified",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            )
        )

        # Not immediate - need to wait for auto-flush
        assert mock_callback.call_count == 0

        # Wait for auto-flush
        await asyncio.sleep(0.15)

        # Should emit after flush
        assert mock_callback.call_count == 1
        operation = mock_callback.call_args[0][0]
        assert operation.primary_path == regular_file

    @pytest.mark.asyncio
    async def test_auto_flush_on_timeout(self, mock_callback) -> None:
        """Test that pending events flush automatically after time window."""
        config = DetectorConfig(time_window_ms=100)
        detector = OperationDetector(config=config, on_operation_complete=mock_callback)

        base_time = datetime.now()
        real_file = Path("incomplete.txt")

        # Add real file event
        detector.add_event(
            FileEvent(
                path=real_file,
                event_type="modified",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            )
        )

        # No immediate callback
        assert mock_callback.call_count == 0

        # Wait for auto-flush
        await asyncio.sleep(0.15)

        # Should have flushed the event
        assert mock_callback.call_count == 1
        operation = mock_callback.call_args[0][0]
        assert operation.primary_path == real_file

    @pytest.mark.asyncio
    async def test_multiple_operations_detected(self, detector_with_callback, mock_callback) -> None:
        """Test that multiple separate operations are detected correctly."""
        base_time = datetime.now()

        # First atomic save
        temp1 = Path(".file1.tmp")
        final1 = Path("file1.py")

        detector_with_callback.add_event(
            FileEvent(
                path=temp1,
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            )
        )
        detector_with_callback.add_event(
            FileEvent(
                path=temp1,
                event_type="moved",
                dest_path=final1,
                metadata=FileEventMetadata(timestamp=base_time + timedelta(milliseconds=5), sequence_number=2),
            )
        )

        # Wait for first operation to flush
        await asyncio.sleep(0.15)
        assert mock_callback.call_count == 1

        # Second atomic save
        temp2 = Path(".file2.tmp")
        final2 = Path("file2.py")

        detector_with_callback.add_event(
            FileEvent(
                path=temp2,
                event_type="created",
                metadata=FileEventMetadata(
                    timestamp=base_time + timedelta(milliseconds=20), sequence_number=3
                ),
            )
        )
        detector_with_callback.add_event(
            FileEvent(
                path=temp2,
                event_type="moved",
                dest_path=final2,
                metadata=FileEventMetadata(
                    timestamp=base_time + timedelta(milliseconds=25), sequence_number=4
                ),
            )
        )

        # Wait for second operation to flush
        await asyncio.sleep(0.15)
        assert mock_callback.call_count == 2

        # Verify both operations
        first_op = mock_callback.call_args_list[0][0][0]
        second_op = mock_callback.call_args_list[1][0][0]

        assert first_op.primary_path == final1
        assert second_op.primary_path == final2


class TestTempFileFiltering:
    """Test filtering of pure temp file events."""

    @pytest.mark.asyncio
    async def test_temp_file_churn_hidden(self, mock_callback) -> None:
        """Test that temp file create/delete churn is hidden."""
        config = DetectorConfig(time_window_ms=100)
        detector = OperationDetector(config=config, on_operation_complete=mock_callback)

        base_time = datetime.now()
        temp_file = Path(".build_cache.tmp")

        # Temp file created and deleted - pure noise
        events = [
            FileEvent(
                path=temp_file,
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            ),
            FileEvent(
                path=temp_file,
                event_type="deleted",
                metadata=FileEventMetadata(timestamp=base_time + timedelta(milliseconds=5), sequence_number=2),
            ),
        ]

        for event in events:
            detector.add_event(event)

        # Wait for auto-flush
        await asyncio.sleep(0.15)

        # Should NOT emit anything - pure temp file churn
        assert mock_callback.call_count == 0

    @pytest.mark.asyncio
    async def test_temp_to_temp_move_hidden(self, mock_callback) -> None:
        """Test that temp to temp moves are hidden."""
        config = DetectorConfig(time_window_ms=100)
        detector = OperationDetector(config=config, on_operation_complete=mock_callback)

        base_time = datetime.now()
        temp1 = Path(".foo.tmp.1")
        temp2 = Path(".foo.tmp.2")

        # Move between temp files - still noise
        detector.add_event(
            FileEvent(
                path=temp1,
                event_type="moved",
                dest_path=temp2,
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            )
        )

        # Wait for auto-flush
        await asyncio.sleep(0.15)

        # Should NOT emit - both source and dest are temp
        assert mock_callback.call_count == 0

    @pytest.mark.asyncio
    async def test_real_file_with_temp_churn_emitted(self, mock_callback) -> None:
        """Test that real file events are emitted even with temp file churn."""
        config = DetectorConfig(time_window_ms=100)
        detector = OperationDetector(config=config, on_operation_complete=mock_callback)

        base_time = datetime.now()
        temp_file = Path(".cache.tmp")
        real_file = Path("data.json")

        # Mix of temp churn and real file change
        events = [
            FileEvent(
                path=temp_file,
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            ),
            FileEvent(
                path=real_file,
                event_type="modified",
                metadata=FileEventMetadata(timestamp=base_time + timedelta(milliseconds=5), sequence_number=2),
            ),
            FileEvent(
                path=temp_file,
                event_type="deleted",
                metadata=FileEventMetadata(
                    timestamp=base_time + timedelta(milliseconds=10), sequence_number=3
                ),
            ),
        ]

        for event in events:
            detector.add_event(event)

        # Wait for auto-flush
        await asyncio.sleep(0.15)

        # Should emit only the real file event
        assert mock_callback.call_count == 1
        operation = mock_callback.call_args[0][0]
        assert operation.primary_path == real_file


class TestRealWorldPatterns:
    """Test real-world editor save patterns."""

    @pytest.mark.asyncio
    async def test_vscode_atomic_save(self, mock_callback) -> None:
        """Test VSCode atomic save pattern."""
        config = DetectorConfig(time_window_ms=100)
        detector = OperationDetector(config=config, on_operation_complete=mock_callback)

        base_time = datetime.now()
        temp_file = Path(".document.txt.tmp.84")
        final_file = Path("document.txt")

        # VSCode pattern: create temp → write temp → rename temp to final
        events = [
            FileEvent(
                path=temp_file,
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            ),
            FileEvent(
                path=temp_file,
                event_type="modified",
                metadata=FileEventMetadata(timestamp=base_time + timedelta(milliseconds=2), sequence_number=2),
            ),
            FileEvent(
                path=temp_file,
                event_type="moved",
                dest_path=final_file,
                metadata=FileEventMetadata(timestamp=base_time + timedelta(milliseconds=5), sequence_number=3),
            ),
        ]

        for event in events:
            detector.add_event(event)

        # Wait for auto-flush
        await asyncio.sleep(0.15)

        # Should detect atomic save
        assert mock_callback.call_count == 1
        operation = mock_callback.call_args[0][0]
        assert operation.operation_type == OperationType.ATOMIC_SAVE
        assert operation.primary_path == final_file
        assert operation.is_atomic is True

    @pytest.mark.asyncio
    async def test_vim_backup_pattern(self, mock_callback) -> None:
        """Test Vim backup file pattern."""
        config = DetectorConfig(time_window_ms=150)
        detector = OperationDetector(config=config, on_operation_complete=mock_callback)

        base_time = datetime.now()
        backup_file = Path("document.txt~")
        main_file = Path("document.txt")

        # Vim pattern: create backup → modify original
        events = [
            FileEvent(
                path=backup_file,
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            ),
            FileEvent(
                path=main_file,
                event_type="modified",
                metadata=FileEventMetadata(timestamp=base_time + timedelta(milliseconds=5), sequence_number=2),
            ),
        ]

        for event in events:
            detector.add_event(event)

        # Wait for auto-flush since this might not be immediately detected
        await asyncio.sleep(0.2)

        # Should have emitted something
        assert mock_callback.call_count >= 1

        # Main file should be in the results
        all_operations = [call[0][0] for call in mock_callback.call_args_list]
        assert any(op.primary_path == main_file for op in all_operations)


# 🧱🏗️🔚
