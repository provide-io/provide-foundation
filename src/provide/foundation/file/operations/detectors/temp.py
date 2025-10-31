#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Temporary file pattern detectors."""

from __future__ import annotations

from pathlib import Path

from provide.foundation.file.operations.detectors.helpers import (
    extract_base_name,
    is_temp_file,
)
from provide.foundation.file.operations.types import (
    FileEvent,
    FileOperation,
    OperationType,
)
from provide.foundation.logger import get_logger

log = get_logger(__name__)


class TempPatternDetector:
    """Detects patterns involving temporary files."""

    def detect_temp_rename_pattern(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def detect_delete_temp_pattern(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def detect_temp_modify_pattern(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def detect_temp_create_delete_pattern(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None


# 🧱🏗️🔚
