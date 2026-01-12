#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""File operations testing fixtures for the provide-foundation.

This module provides pytest fixtures and utilities for testing file operation detection,
simulating various editor save patterns, and validating operation detection accuracy."""

from __future__ import annotations

from collections.abc import Generator
from datetime import datetime, timedelta
from pathlib import Path
import random
import tempfile
from typing import Any

import pytest

try:
    from provide.foundation.file.operations import (
        DetectorConfig,
        FileEvent,
        FileEventMetadata,
        OperationDetector,
        OperationType,  # noqa: F401 - Used conditionally
    )

    HAS_OPERATIONS_MODULE = True
except ImportError:
    HAS_OPERATIONS_MODULE = False


class FileOperationSimulator:
    """Simulator for various file operation patterns."""

    def __init__(self, base_path: Path, detector_config: DetectorConfig | None = None) -> None:
        """Initialize the file operation simulator.

        Args:
            base_path: Base directory for file operations
            detector_config: Configuration for the operation detector
        """
        self.base_path = base_path

        # Ensure built-in detectors are registered (idempotent)
        # This is needed because test teardown may clear the registry
        if HAS_OPERATIONS_MODULE:
            from provide.foundation.file.operations.detectors import _auto_register_builtin_detectors

            _auto_register_builtin_detectors()

        self.detector = OperationDetector(detector_config or DetectorConfig())
        self.sequence_counter = 0
        self.operations_detected: list[Any] = []
        self._base_time = datetime.now()
        self._operation_counter = 0

    def _get_next_operation_time(self) -> datetime:
        """Get timestamp for the next operation, with proper spacing."""
        # Space operations 1 second apart to avoid grouping
        self._operation_counter += 1
        return self._base_time + timedelta(seconds=self._operation_counter)

    def _create_event(
        self,
        path: Path,
        event_type: str,
        size_before: int | None = None,
        size_after: int | None = None,
        process_name: str | None = None,
        dest_path: Path | None = None,
        timestamp: datetime | None = None,
    ) -> Any:
        """Create a file event with metadata."""
        if not HAS_OPERATIONS_MODULE:
            return None

        self.sequence_counter += 1
        metadata = FileEventMetadata(
            timestamp=timestamp or datetime.now(),
            sequence_number=self.sequence_counter,
            size_before=size_before,
            size_after=size_after,
            process_name=process_name,
        )

        return FileEvent(
            path=path,
            event_type=event_type,
            metadata=metadata,
            dest_path=dest_path,
        )

    def simulate_vscode_save(self, filename: str = "document.txt", content_size: int = 1024) -> list[Any]:
        """Simulate VSCode atomic save pattern.

        Args:
            filename: Name of the file to save
            content_size: Size of the file content in bytes

        Returns:
            List of generated file events
        """
        if not HAS_OPERATIONS_MODULE:
            return []

        final_file = self.base_path / filename
        # VSCode uses pattern: .filename.ext.tmp.vscode.XXXX (leading dot + random suffix)
        temp_file = self.base_path / f".{filename}.tmp.vscode.{random.randint(1, 999)}"
        base_time = self._get_next_operation_time()

        events = [
            # Create temp file
            self._create_event(
                temp_file,
                "created",
                size_after=content_size,
                process_name="Code",
                timestamp=base_time,
            ),
            # Rename temp to final
            self._create_event(
                temp_file,
                "moved",
                dest_path=final_file,
                timestamp=base_time + timedelta(milliseconds=50),
            ),
        ]

        return [e for e in events if e is not None]

    def simulate_vim_save(self, filename: str = "document.txt", content_size: int = 1024) -> list[Any]:
        """Simulate Vim atomic save pattern with backup.

        Args:
            filename: Name of the file to save
            content_size: Size of the file content in bytes

        Returns:
            List of generated file events
        """
        if not HAS_OPERATIONS_MODULE:
            return []

        main_file = self.base_path / filename
        backup_file = self.base_path / f"{filename}~"
        base_time = self._get_next_operation_time()

        events = [
            # Delete original
            self._create_event(
                main_file,
                "deleted",
                size_before=content_size,
                process_name="vim",
                timestamp=base_time,
            ),
            # Create backup
            self._create_event(
                backup_file,
                "created",
                size_after=content_size,
                process_name="vim",
                timestamp=base_time + timedelta(milliseconds=25),
            ),
            # Create new version
            self._create_event(
                main_file,
                "created",
                size_after=content_size + 50,  # Slightly larger after edit
                process_name="vim",
                timestamp=base_time + timedelta(milliseconds=50),
            ),
        ]

        return [e for e in events if e is not None]

    def simulate_safe_write(self, filename: str = "document.txt", content_size: int = 1024) -> list[Any]:
        """Simulate safe write pattern with backup creation.

        Args:
            filename: Name of the file to save
            content_size: Size of the file content in bytes

        Returns:
            List of generated file events
        """
        if not HAS_OPERATIONS_MODULE:
            return []

        main_file = self.base_path / filename
        backup_file = self.base_path / f"{filename}.bak"
        base_time = self._get_next_operation_time()

        events = [
            # Create backup first
            self._create_event(
                backup_file,
                "created",
                size_after=content_size,
                timestamp=base_time,
            ),
            # Modify original
            self._create_event(
                main_file,
                "modified",
                size_before=content_size,
                size_after=content_size + 100,
                timestamp=base_time + timedelta(milliseconds=50),
            ),
        ]

        return [e for e in events if e is not None]

    def simulate_batch_operation(
        self,
        file_count: int = 5,
        base_name: str = "module",
        extension: str = ".py",
        content_size: int = 500,
    ) -> list[Any]:
        """Simulate batch file operation (like code formatting).

        Args:
            file_count: Number of files to modify
            base_name: Base name for the files
            extension: File extension
            content_size: Size of each file in bytes

        Returns:
            List of generated file events
        """
        if not HAS_OPERATIONS_MODULE:
            return []

        events = []
        base_time = self._get_next_operation_time()

        for i in range(file_count):
            file_path = self.base_path / f"{base_name}_{i}{extension}"
            # Simulate rapid modifications with small time gaps
            event_time = base_time + timedelta(milliseconds=i * 10)

            self.sequence_counter += 1
            metadata = FileEventMetadata(
                timestamp=event_time,
                sequence_number=self.sequence_counter,
                size_before=content_size,
                size_after=content_size + 20,  # Formatted files slightly larger
                process_name="black",  # Python formatter
            )

            event = FileEvent(
                path=file_path,
                event_type="modified",
                metadata=metadata,
            )
            events.append(event)

        return events

    def simulate_all_patterns(self) -> dict[str, list[Any]]:
        """Simulate all supported file operation patterns.

        Returns:
            Dictionary mapping pattern names to their events
        """
        if not HAS_OPERATIONS_MODULE:
            return {}

        return {
            "vscode_save": self.simulate_vscode_save("vscode_file.txt"),
            "vim_save": self.simulate_vim_save("vim_file.txt"),
            "safe_write": self.simulate_safe_write("safe_file.txt"),
            "batch_operation": self.simulate_batch_operation(3, "batch_file", ".py"),
        }

    def detect_operations(self, events: list[Any]) -> list[Any]:
        """Detect operations from a list of events.

        Args:
            events: List of file events

        Returns:
            List of detected operations
        """
        if not HAS_OPERATIONS_MODULE or not events:
            return []

        return self.detector.detect(events)


class FileOperationValidator:
    """Validator for file operation detection results."""

    def __init__(self) -> None:
        """Initialize the validator."""
        self.validation_results: list[dict[str, Any]] = []

    def validate_operation(
        self,
        operation: Any,
        expected_type: str,
        expected_confidence_min: float = 0.8,
        expected_atomic: bool | None = None,
        expected_safe: bool | None = None,
        expected_backup: bool | None = None,
    ) -> dict[str, Any]:
        """Validate a detected operation against expected criteria.

        Args:
            operation: The detected operation
            expected_type: Expected operation type
            expected_confidence_min: Minimum expected confidence
            expected_atomic: Expected atomic flag
            expected_safe: Expected safe flag
            expected_backup: Expected backup flag

        Returns:
            Validation result dictionary
        """
        if not HAS_OPERATIONS_MODULE or not operation:
            return {"valid": False, "error": "Operations module not available"}

        result = {
            "valid": True,
            "operation_type": operation.operation_type.value,
            "confidence": operation.confidence,
            "is_atomic": operation.is_atomic,
            "is_safe": operation.is_safe,
            "has_backup": operation.has_backup,
            "errors": [],
        }

        # Validate operation type
        if operation.operation_type.value != expected_type:
            result["errors"].append(f"Expected type {expected_type}, got {operation.operation_type.value}")
            result["valid"] = False

        # Validate confidence
        if operation.confidence < expected_confidence_min:
            result["errors"].append(
                f"Confidence {operation.confidence:.2f} below minimum {expected_confidence_min:.2f}"
            )
            result["valid"] = False

        # Validate flags if specified
        if expected_atomic is not None and operation.is_atomic != expected_atomic:
            result["errors"].append(f"Expected atomic={expected_atomic}, got {operation.is_atomic}")
            result["valid"] = False

        if expected_safe is not None and operation.is_safe != expected_safe:
            result["errors"].append(f"Expected safe={expected_safe}, got {operation.is_safe}")
            result["valid"] = False

        if expected_backup is not None and operation.has_backup != expected_backup:
            result["errors"].append(f"Expected backup={expected_backup}, got {operation.has_backup}")
            result["valid"] = False

        self.validation_results.append(result)
        return result

    def get_summary(self) -> dict[str, Any]:
        """Get validation summary statistics.

        Returns:
            Summary of validation results
        """
        if not self.validation_results:
            return {"total": 0, "valid": 0, "invalid": 0, "success_rate": 0.0}

        total = len(self.validation_results)
        valid = sum(1 for r in self.validation_results if r["valid"])

        return {
            "total": total,
            "valid": valid,
            "invalid": total - valid,
            "success_rate": valid / total if total > 0 else 0.0,
            "average_confidence": sum(r.get("confidence", 0) for r in self.validation_results) / total
            if total > 0
            else 0.0,
        }


@pytest.fixture
def temp_workspace() -> Generator[Path, None, None]:
    """Create a temporary workspace for file operations testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def file_operation_simulator(temp_workspace: Path) -> FileOperationSimulator:
    """Create a file operation simulator fixture."""
    return FileOperationSimulator(temp_workspace)


@pytest.fixture
def file_operation_validator() -> FileOperationValidator:
    """Create a file operation validator fixture."""
    return FileOperationValidator()


@pytest.fixture
def operation_detector() -> OperationDetector | None:
    """Create an operation detector fixture."""
    if not HAS_OPERATIONS_MODULE:
        return None
    return OperationDetector()


# Decorator for tests that require file operations module
def requires_file_operations(func):
    """Decorator to skip tests when file operations module is not available."""
    return pytest.mark.skipif(not HAS_OPERATIONS_MODULE, reason="File operations module not available")(func)


# Pattern-specific test decorators
def file_operation_pattern(*patterns: str):
    """Decorator for file operation pattern tests.

    Args:
        *patterns: Patterns to test (vscode, vim, emacs, sublime, batch, etc.)
    """

    def decorator(func):
        func._file_operation_patterns = patterns
        return requires_file_operations(func)

    return decorator


# 🧱🏗️🔚
