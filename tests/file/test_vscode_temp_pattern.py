#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for VSCode temporary file pattern detection and handling.

This test module verifies that VSCode's atomic save pattern (.filename.ext.tmp.XX)
is correctly detected and processed, ensuring the final file path is correctly
extracted without the leading dot that's part of the temp file pattern."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import pytest

from provide.foundation.file.operations import (
    DetectorConfig,
    FileEvent,
    FileEventMetadata,
    OperationDetector,
    OperationType,
)
from provide.foundation.file.operations.detectors.helpers import (
    extract_base_name,
    is_temp_file,
)


class TestVSCodeTempFileDetection:
    """Test detection of VSCode temporary file patterns."""

    def test_is_temp_file_detects_vscode_pattern(self) -> None:
        """Test that is_temp_file() recognizes VSCode temp pattern."""
        # VSCode pattern: .filename.ext.tmp.XXXX
        test_cases = [
            (Path(".orchestrator.py.tmp.84"), True),
            (Path(".test.txt.tmp.123"), True),
            (Path(".config.json.tmp.abc"), True),
            (Path(".file.tmp.1"), True),
            # Non-temp files
            (Path("orchestrator.py"), False),
            (Path("test.txt"), False),
            # Other temp patterns (should also be detected)
            (Path("file.tmp"), True),
            (Path("file~"), True),
        ]

        for path, expected in test_cases:
            result = is_temp_file(path)
            assert result == expected, f"is_temp_file({path}) should be {expected}, got {result}"

    def test_extract_base_name_from_vscode_pattern(self) -> None:
        """Test that extract_base_name() correctly extracts the real filename from VSCode pattern."""
        test_cases = [
            # (temp_file, expected_base_name)
            (Path(".orchestrator.py.tmp.84"), "orchestrator.py"),
            (Path(".test.txt.tmp.123"), "test.txt"),
            (Path(".config.json.tmp.abc"), "config.json"),
            (Path(".file.tmp.1"), "file"),
            (Path(".multiple.dots.file.py.tmp.99"), "multiple.dots.file.py"),
            # Edge case: file with leading dot in actual name (not temp)
            # This won't match VSCode pattern because it doesn't end with .tmp.XX
            (Path(".gitignore"), None),
        ]

        for temp_path, expected in test_cases:
            result = extract_base_name(temp_path)
            assert result == expected, f"extract_base_name({temp_path}) should be '{expected}', got '{result}'"

    def test_extract_base_name_preserves_nested_dots(self) -> None:
        """Test that extract_base_name() preserves dots in the middle of filenames."""
        test_cases = [
            (Path(".test.config.py.tmp.84"), "test.config.py"),
            (Path(".my.test.file.txt.tmp.123"), "my.test.file.txt"),
            (Path(".a.b.c.d.tmp.99"), "a.b.c.d"),
        ]

        for temp_path, expected in test_cases:
            result = extract_base_name(temp_path)
            assert result == expected, (
                f"extract_base_name({temp_path}) should preserve dots: '{expected}', got '{result}'"
            )

    def test_extract_base_name_handles_vim_pattern(self) -> None:
        """Test that extract_base_name() also handles vim swap files correctly."""
        test_cases = [
            # Vim swap files also have leading dots
            (Path(".test.txt.swp"), "test.txt"),
            (Path(".orchestrator.py.swo"), "orchestrator.py"),
            (Path(".config.swx"), "config"),
        ]

        for temp_path, expected in test_cases:
            result = extract_base_name(temp_path)
            assert result == expected, f"extract_base_name({temp_path}) should be '{expected}', got '{result}'"


class TestVSCodeAtomicSaveDetection:
    """Test full atomic save operation detection with VSCode pattern."""

    def test_vscode_atomic_save_operation_detection(self) -> None:
        """Test that VSCode atomic save pattern is detected as ATOMIC_SAVE operation."""
        base_time = datetime.now()
        temp_file = Path(".orchestrator.py.tmp.84")
        final_file = Path("orchestrator.py")

        events = [
            FileEvent(
                path=temp_file,
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            ),
            FileEvent(
                path=temp_file,
                event_type="modified",
                metadata=FileEventMetadata(
                    timestamp=base_time + timedelta(milliseconds=10),
                    sequence_number=2,
                ),
            ),
            FileEvent(
                path=temp_file,
                event_type="moved",
                dest_path=final_file,
                metadata=FileEventMetadata(
                    timestamp=base_time + timedelta(milliseconds=20),
                    sequence_number=3,
                ),
            ),
        ]

        detector = OperationDetector(DetectorConfig(time_window_ms=500))
        operations = detector.detect(events)

        assert len(operations) >= 1, "Should detect at least one operation"

        # Find the atomic save operation
        atomic_ops = [op for op in operations if op.operation_type == OperationType.ATOMIC_SAVE]
        assert len(atomic_ops) >= 1, "Should detect ATOMIC_SAVE operation"

        operation = atomic_ops[0]
        assert operation.primary_path == final_file, (
            f"Primary path should be '{final_file}', got '{operation.primary_path}'"
        )
        assert operation.confidence >= 0.9, f"Confidence should be >= 0.9, got {operation.confidence}"
        assert operation.is_atomic is True, "Operation should be marked as atomic"

    def test_vscode_pattern_with_multiple_dots_in_filename(self) -> None:
        """Test VSCode pattern detection with filenames containing multiple dots."""
        base_time = datetime.now()
        temp_file = Path(".test.config.py.tmp.42")
        final_file = Path("test.config.py")

        events = [
            FileEvent(
                path=temp_file,
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            ),
            FileEvent(
                path=temp_file,
                event_type="moved",
                dest_path=final_file,
                metadata=FileEventMetadata(
                    timestamp=base_time + timedelta(milliseconds=50),
                    sequence_number=2,
                ),
            ),
        ]

        detector = OperationDetector(DetectorConfig(time_window_ms=500))
        operations = detector.detect(events)

        assert len(operations) >= 1
        atomic_ops = [op for op in operations if op.operation_type == OperationType.ATOMIC_SAVE]
        assert len(atomic_ops) >= 1

        operation = atomic_ops[0]
        assert operation.primary_path == final_file, (
            f"Primary path should preserve all dots: '{final_file}', got '{operation.primary_path}'"
        )

    def test_vscode_pattern_returns_correct_file_in_operation(self) -> None:
        """Test that the detected operation contains the correct final file, not the temp file."""
        base_time = datetime.now()
        temp_file = Path(".my_module.py.tmp.999")
        final_file = Path("my_module.py")

        events = [
            FileEvent(
                path=temp_file,
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            ),
            FileEvent(
                path=temp_file,
                event_type="moved",
                dest_path=final_file,
                metadata=FileEventMetadata(
                    timestamp=base_time + timedelta(milliseconds=30),
                    sequence_number=2,
                ),
            ),
        ]

        detector = OperationDetector(DetectorConfig(time_window_ms=500))
        operations = detector.detect(events)

        assert len(operations) >= 1
        operation = operations[0]

        # Verify primary_path is NOT a temp file
        assert not is_temp_file(operation.primary_path), (
            f"Primary path should not be a temp file: {operation.primary_path}"
        )

        # Verify primary_path matches the final file
        assert operation.primary_path == final_file, (
            f"Primary path should be '{final_file}', got '{operation.primary_path}'"
        )

        # Verify files_affected contains the final file
        assert final_file in operation.files_affected, (
            f"Files affected should contain '{final_file}', got {operation.files_affected}"
        )


@pytest.mark.asyncio
class TestVSCodeStreamingDetection:
    """Test streaming detection with VSCode patterns."""

    async def test_streaming_detection_with_vscode_pattern(self) -> None:
        """Test that streaming detection correctly handles VSCode temp files."""
        import asyncio
        from unittest.mock import Mock

        base_time = datetime.now()
        temp_file = Path(".test.py.tmp.456")
        final_file = Path("test.py")

        mock_callback = Mock()
        config = DetectorConfig(time_window_ms=100, min_confidence=0.7)
        detector = OperationDetector(config=config, on_operation_complete=mock_callback)

        # Add events via streaming API
        detector.add_event(
            FileEvent(
                path=temp_file,
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            )
        )

        detector.add_event(
            FileEvent(
                path=temp_file,
                event_type="moved",
                dest_path=final_file,
                metadata=FileEventMetadata(
                    timestamp=base_time + timedelta(milliseconds=10),
                    sequence_number=2,
                ),
            )
        )

        # Wait for auto-flush
        await asyncio.sleep(0.15)

        # Verify callback was called with correct operation
        assert mock_callback.call_count == 1, "Callback should be called once"
        operation = mock_callback.call_args[0][0]
        assert operation.primary_path == final_file, (
            f"Primary path should be '{final_file}', got '{operation.primary_path}'"
        )
        assert operation.operation_type == OperationType.ATOMIC_SAVE


class TestVSCodePatternEdgeCases:
    """Test edge cases and boundary conditions for VSCode patterns."""

    def test_single_character_filename(self) -> None:
        """Test VSCode pattern with single-character filename."""
        temp_path = Path(".a.tmp.1")
        assert is_temp_file(temp_path) is True
        assert extract_base_name(temp_path) == "a"

    def test_very_long_filename(self) -> None:
        """Test VSCode pattern with very long filename."""
        long_name = "a" * 200 + ".py"
        temp_path = Path(f".{long_name}.tmp.123")
        assert is_temp_file(temp_path) is True
        assert extract_base_name(temp_path) == long_name

    def test_filename_with_special_characters(self) -> None:
        """Test VSCode pattern with special characters in filename."""
        test_cases = [
            Path(".my-file.py.tmp.1"),
            Path(".my_file.py.tmp.2"),
            Path(".my file.txt.tmp.3"),  # Space in filename
        ]

        for temp_path in test_cases:
            assert is_temp_file(temp_path) is True
            base = extract_base_name(temp_path)
            assert base is not None
            assert not base.startswith("."), f"Base name should not start with dot: {base}"

    def test_non_numeric_temp_suffix(self) -> None:
        """Test VSCode pattern with non-numeric temp suffix (alphanumeric)."""
        temp_path = Path(".file.txt.tmp.abc123")
        assert is_temp_file(temp_path) is True
        assert extract_base_name(temp_path) == "file.txt"


# 🧱🏗️🔚
