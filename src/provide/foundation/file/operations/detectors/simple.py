#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Simple operation detectors."""

from __future__ import annotations

from pathlib import Path

from provide.foundation.file.operations.detectors.helpers import is_backup_file
from provide.foundation.file.operations.types import (
    FileEvent,
    FileOperation,
    OperationType,
)
from provide.foundation.logger import get_logger

log = get_logger(__name__)


class SimpleOperationDetector:
    """Detects simple, direct file operations."""

    def detect_same_file_delete_create_pattern(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def detect_simple_operation(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def detect_direct_modification(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )


# 🧱🏗️🔚
