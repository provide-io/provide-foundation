#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Utility functions for file operation detection."""

from __future__ import annotations

from pathlib import Path

from provide.foundation.file.operations.types import DetectorConfig, FileEvent, FileOperation, OperationType


def detect_atomic_save(events: list[FileEvent]) -> FileOperation | None:
    """Detect if events represent an atomic save operation."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    detector = OperationDetector()
    operations = detector.detect(events)
    return next((op for op in operations if op.operation_type == OperationType.ATOMIC_SAVE), None)


def is_temp_file(path: Path) -> bool:
    """Check if a path represents a temporary file."""
    from provide.foundation.file.operations.detectors.helpers import is_temp_file as helper_is_temp_file

    return helper_is_temp_file(path)


def extract_original_path(temp_path: Path) -> Path | None:
    """Extract the original filename from a temp file path."""
    from provide.foundation.file.operations.detectors.helpers import extract_base_name

    base_name = extract_base_name(temp_path)
    if base_name:
        return temp_path.parent / base_name
    else:
        # If no temp pattern matches, return the original path
        return temp_path


def group_related_events(events: list[FileEvent], time_window_ms: int = 500) -> list[list[FileEvent]]:
    """Group events that occur within a time window."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    config = DetectorConfig(time_window_ms=time_window_ms)
    detector = OperationDetector(config)
    return detector._group_events_by_time(sorted(events, key=lambda e: e.timestamp))


# 🧱🏗️🔚
