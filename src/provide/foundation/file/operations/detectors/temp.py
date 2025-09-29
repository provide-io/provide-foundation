"""Temporary file pattern detectors."""

from __future__ import annotations

from pathlib import Path

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
                current.type == "created"
                and self._is_temp_file(current.path)
                and next_event.type == "moved"
                and next_event.src_path == current.path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    type=OperationType.CREATE,
                    path=next_event.path,
                    events=[current, next_event],
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
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
                delete_event.type == "deleted"
                and temp_create.type == "created"
                and self._is_temp_file(temp_create.path)
                and temp_rename.type == "moved"
                and temp_rename.src_path == temp_create.path
                and temp_rename.path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        type=OperationType.UPDATE,
                        path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
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
        temp_groups = {}
        for event in events:
            if self._is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if (
                temp_events[0].type == "created"
                and any(e.type == "modified" for e in temp_events[1:])
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [
                    e for e in events
                    if e.type == "moved" and e.src_path == temp_path
                ]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = temp_events + [rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (
                        all_events[-1].timestamp - all_events[0].timestamp
                    ).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        return FileOperation(
                            type=OperationType.SAVE,
                            path=rename_event.path,
                            events=all_events,
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def detect_temp_create_delete_pattern(
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp (usually failed operations)."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion
        temp_files = {}
        for event in events:
            if self._is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)

        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern
            if (
                temp_events[0].type == "created"
                and temp_events[-1].type == "deleted"
            ):
                time_span = (
                    temp_events[-1].timestamp - temp_events[0].timestamp
                ).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        type=OperationType.TEMP,
                        path=Path(temp_path_str),
                        events=temp_events,
                        start_time=temp_events[0].timestamp,
                        end_time=temp_events[-1].timestamp,
                        metadata={
                            "pattern": "temp_create_delete",
                            "description": "Temporary file created and deleted",
                        },
                    )

        return None

    def _is_temp_file(self, path: Path) -> bool:
        """Check if path looks like a temporary file."""
        name = path.name.lower()
        stem = path.stem.lower()

        # Common temp file patterns
        temp_patterns = [
            name.startswith(".tmp"),
            name.startswith("tmp"),
            name.endswith(".tmp"),
            name.endswith(".temp"),
            name.endswith("~"),
            ".$" in name,  # .$ prefix (common in Windows)
            stem.endswith(".tmp"),
            ".swp" in name,  # vim swap files
            ".#" in name,  # emacs temp files
        ]

        return any(temp_patterns)