#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Atomic operation detectors."""

from __future__ import annotations

from provide.foundation.file.operations.detectors.helpers import (
    extract_base_name,
    is_backup_file,
    is_temp_file,
)
from provide.foundation.file.operations.types import (
    FileEvent,
    FileOperation,
    OperationType,
)
from provide.foundation.logger import get_logger

log = get_logger(__name__)


class AtomicOperationDetector:
    """Detects atomic file operations like safe writes and atomic saves."""

    def detect_atomic_save(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def detect_safe_write(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None


# 🧱🏗️🔚
