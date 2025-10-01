"""Atomic operation detectors."""

from __future__ import annotations

from pathlib import Path

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

        Common pattern: rename original to backup -> create new -> delete backup
        """
        if len(events) < 2:
            return None

        # Group events by base file name
        file_groups = {}
        for event in events:
            base_name = extract_base_name(event.path)
            if base_name:
                if base_name not in file_groups:
                    file_groups[base_name] = []
                file_groups[base_name].append(event)

        for base_name, group_events in file_groups.items():
            if len(group_events) < 2:
                continue

            group_events.sort(key=lambda e: e.timestamp)

            # Look for backup creation followed by file creation or modification
            backup_created = None
            original_updated = None

            for event in group_events:
                if event.event_type in {"moved", "created"} and is_backup_file(event.path):
                    backup_created = event
                elif event.event_type in {"created", "modified"} and not is_backup_file(event.path):
                    original_updated = event

            if backup_created and original_updated:
                # Found safe write pattern
                target_path = original_updated.path

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=target_path,
                    events=group_events,
                    confidence=0.95,
                    description=f"Safe write to {target_path.name}",
                    start_time=group_events[0].timestamp,
                    end_time=group_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[target_path],
                    metadata={
                        "backup_file": str(backup_created.path),
                        "pattern": "safe_write",
                    },
                )

        return None
