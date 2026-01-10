#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for detector bug fixes - temp file handling edge cases.

Tests verify that:
1. TEMP_CLEANUP detector returns None when no real file is found
2. BACKUP_CREATE detector rejects operations with temp files as primary_path
3. Integration tests verify bug fixes work end-to-end"""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from provide.testkit import FoundationTestCase

from provide.foundation.file.operations.detectors.batch import BatchOperationDetector
from provide.foundation.file.operations.detectors.helpers import is_temp_file
from provide.foundation.file.operations.detectors.orchestrator import OperationDetector
from provide.foundation.file.operations.detectors.temp import TempPatternDetector
from provide.foundation.file.operations.types import DetectorConfig, FileEvent, FileEventMetadata


class TestTempCleanupBugFix(FoundationTestCase):
    """Test TEMP_CLEANUP detector returns None when no real file exists."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.detector = TempPatternDetector()
        self.base_time = datetime.now()

    def test_temp_create_delete_no_real_file_returns_none(self) -> None:
        """Test that temp file create→delete with no real file returns None."""
        temp_file = Path(".terraform.lock.hcl2392610858")

        events = [
            FileEvent(
                path=temp_file,
                event_type="created",
                metadata=FileEventMetadata(
                    timestamp=self.base_time,
                    sequence_number=1,
                ),
            ),
            FileEvent(
                path=temp_file,
                event_type="deleted",
                metadata=FileEventMetadata(
                    timestamp=self.base_time + timedelta(milliseconds=100),
                    sequence_number=2,
                ),
            ),
        ]

        # Should return None since no real file exists
        operation = self.detector.detect_temp_create_delete_pattern(events)
        assert operation is None, "Should return None for pure temp file operations"

    def test_multiple_temp_files_no_real_file_returns_none(self) -> None:
        """Test multiple temp files created and deleted with no real file."""
        temp_files = [
            Path(".file.txt.tmp.123"),
            Path(".file.txt.tmp.456"),
            Path(".file.txt.tmp.789"),
        ]

        events = []
        for i, temp_file in enumerate(temp_files):
            events.append(
                FileEvent(
                    path=temp_file,
                    event_type="created",
                    metadata=FileEventMetadata(
                        timestamp=self.base_time + timedelta(milliseconds=i * 50),
                        sequence_number=i * 2 + 1,
                    ),
                )
            )
            events.append(
                FileEvent(
                    path=temp_file,
                    event_type="deleted",
                    metadata=FileEventMetadata(
                        timestamp=self.base_time + timedelta(milliseconds=i * 50 + 25),
                        sequence_number=i * 2 + 2,
                    ),
                )
            )

        # Each temp file should return None
        operation = self.detector.detect_temp_create_delete_pattern(events)
        assert operation is None, "Should return None for pure temp file operations"

    def test_orchestrator_handles_temp_only_events_gracefully(self) -> None:
        """Test that orchestrator handles temp-only events without errors."""
        temp_file = Path(".test.tmp.999")

        events = [
            FileEvent(
                path=temp_file,
                event_type="created",
                metadata=FileEventMetadata(
                    timestamp=self.base_time,
                    sequence_number=1,
                ),
            ),
            FileEvent(
                path=temp_file,
                event_type="modified",
                metadata=FileEventMetadata(
                    timestamp=self.base_time + timedelta(milliseconds=50),
                    sequence_number=2,
                ),
            ),
            FileEvent(
                path=temp_file,
                event_type="deleted",
                metadata=FileEventMetadata(
                    timestamp=self.base_time + timedelta(milliseconds=100),
                    sequence_number=3,
                ),
            ),
        ]

        detector = OperationDetector(DetectorConfig(time_window_ms=500))
        operations = detector.detect(events)

        # Should not return an operation with temp file as primary_path
        for operation in operations:
            assert not is_temp_file(operation.primary_path), (
                f"Operation should not have temp file as primary_path: {operation.primary_path}"
            )


class TestBackupCreateBugFix(FoundationTestCase):
    """Test BACKUP_CREATE detector rejects temp files as primary_path."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.detector = BatchOperationDetector()
        self.base_time = datetime.now()

    def test_backup_create_with_temp_file_returns_none(self) -> None:
        """Test that backup create with temp file as created file returns None."""
        temp_file = Path("file.txt.tmp.123")
        backup_file = Path("file.txt.tmp.123.bak")

        events = [
            FileEvent(
                path=temp_file,
                event_type="moved",
                dest_path=backup_file,
                metadata=FileEventMetadata(
                    timestamp=self.base_time,
                    sequence_number=1,
                ),
            ),
            FileEvent(
                path=temp_file,
                event_type="created",
                metadata=FileEventMetadata(
                    timestamp=self.base_time + timedelta(milliseconds=50),
                    sequence_number=2,
                ),
            ),
        ]

        # Should return None because create_event.path is a temp file
        operation = self.detector.detect_backup_create(events)
        assert operation is None, "Should reject backup operations with temp files"

    def test_backup_create_with_real_file_returns_operation(self) -> None:
        """Test that backup create with real file returns valid operation."""
        real_file = Path("important.txt")
        backup_file = Path("important.txt.bak")

        events = [
            FileEvent(
                path=real_file,
                event_type="moved",
                dest_path=backup_file,
                metadata=FileEventMetadata(
                    timestamp=self.base_time,
                    sequence_number=1,
                ),
            ),
            FileEvent(
                path=real_file,
                event_type="created",
                metadata=FileEventMetadata(
                    timestamp=self.base_time + timedelta(milliseconds=50),
                    sequence_number=2,
                ),
            ),
        ]

        operation = self.detector.detect_backup_create(events)
        assert operation is not None, "Should return operation for real file backup"
        assert operation.primary_path == real_file, "Primary path should be real file"
        assert not is_temp_file(operation.primary_path), "Primary path should not be temp file"

    def test_backup_create_terraform_pattern_rejected(self) -> None:
        """Test that Terraform lock file temp pattern is rejected."""
        # This is the pattern from the bug report
        temp_file = Path("http_api_minimal_test.tf.tmp.96627.1760139764744")
        backup_file = Path("http_api_minimal_test.tf.tmp.96627.1760139764744.bak")

        events = [
            FileEvent(
                path=temp_file,
                event_type="moved",
                dest_path=backup_file,
                metadata=FileEventMetadata(
                    timestamp=self.base_time,
                    sequence_number=1,
                ),
            ),
            FileEvent(
                path=temp_file,
                event_type="created",
                metadata=FileEventMetadata(
                    timestamp=self.base_time + timedelta(milliseconds=50),
                    sequence_number=2,
                ),
            ),
        ]

        operation = self.detector.detect_backup_create(events)
        assert operation is None, "Should reject Terraform temp file backup pattern"


class TestIntegrationBugFixes(FoundationTestCase):
    """Integration tests verifying bug fixes work end-to-end."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.detector = OperationDetector(DetectorConfig(time_window_ms=500))
        self.base_time = datetime.now()

    def test_terraform_lock_file_pattern_no_longer_errors(self) -> None:
        """Test Terraform lock file pattern no longer causes rejection errors."""
        # This is the exact pattern from the bug report
        temp_file = Path(".terraform.lock.hcl2392610858")

        events = [
            FileEvent(
                path=temp_file,
                event_type="created",
                metadata=FileEventMetadata(
                    timestamp=self.base_time,
                    sequence_number=1,
                ),
            ),
            FileEvent(
                path=temp_file,
                event_type="deleted",
                metadata=FileEventMetadata(
                    timestamp=self.base_time + timedelta(milliseconds=100),
                    sequence_number=2,
                ),
            ),
        ]

        # Should not raise errors or return invalid operations
        operations = self.detector.detect(events)

        # Either returns no operations, or returns operations with valid primary_path
        for operation in operations:
            assert not is_temp_file(operation.primary_path), (
                f"Should not return temp file as primary_path: {operation.primary_path}"
            )

    def test_vscode_atomic_save_still_works(self) -> None:
        """Test that VSCode atomic save pattern still works correctly."""
        temp_file = Path(".document.txt.tmp.123")
        real_file = Path("document.txt")

        events = [
            FileEvent(
                path=temp_file,
                event_type="created",
                metadata=FileEventMetadata(
                    timestamp=self.base_time,
                    sequence_number=1,
                ),
            ),
            FileEvent(
                path=temp_file,
                event_type="modified",
                metadata=FileEventMetadata(
                    timestamp=self.base_time + timedelta(milliseconds=50),
                    sequence_number=2,
                ),
            ),
            FileEvent(
                path=temp_file,
                event_type="moved",
                dest_path=real_file,
                metadata=FileEventMetadata(
                    timestamp=self.base_time + timedelta(milliseconds=100),
                    sequence_number=3,
                ),
            ),
        ]

        operations = self.detector.detect(events)

        assert len(operations) >= 1, "Should detect atomic save"
        atomic_ops = [op for op in operations if op.operation_type.value == "atomic_save"]
        assert len(atomic_ops) >= 1, "Should detect ATOMIC_SAVE operation"

        operation = atomic_ops[0]
        assert operation.primary_path == real_file, "Should use real file as primary_path"
        assert not is_temp_file(operation.primary_path), "Primary path should not be temp"

    def test_safe_write_with_backup_still_works(self) -> None:
        """Test that safe write with backup still works correctly."""
        real_file = Path("important.txt")
        backup_file = Path("important.txt.bak")

        events = [
            FileEvent(
                path=real_file,
                event_type="moved",
                dest_path=backup_file,
                metadata=FileEventMetadata(
                    timestamp=self.base_time,
                    sequence_number=1,
                ),
            ),
            FileEvent(
                path=real_file,
                event_type="created",
                metadata=FileEventMetadata(
                    timestamp=self.base_time + timedelta(milliseconds=50),
                    sequence_number=2,
                ),
            ),
        ]

        operations = self.detector.detect(events)

        # Should detect backup operation
        assert len(operations) >= 1, "Should detect operation"
        backup_ops = [op for op in operations if op.operation_type.value == "backup"]
        assert len(backup_ops) >= 1, "Should detect BACKUP_CREATE operation"

        operation = backup_ops[0]
        assert operation.primary_path == real_file, "Should use real file as primary_path"
        assert not is_temp_file(operation.primary_path), "Primary path should not be temp"


# 🧱🏗️🔚
