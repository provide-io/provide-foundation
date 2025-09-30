"""Simple operation detectors."""

from __future__ import annotations

from pathlib import Path

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
        path_groups = {}
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

                if (
                    delete_event.type == "deleted"
                    and create_event.type == "created"
                ):
                    time_diff = (
                        create_event.timestamp - delete_event.timestamp
                    ).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            type=OperationType.UPDATE,
                            path=Path(path_str),
                            events=[delete_event, create_event],
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            metadata={
                                "pattern": "delete_create_replace",
                                "description": f"File replaced: {Path(path_str).name}",
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
            "created": OperationType.CREATE,
            "modified": OperationType.UPDATE,
            "deleted": OperationType.DELETE,
            "moved": OperationType.MOVE,
        }

        if event.type not in type_mapping:
            return None

        operation_type = type_mapping[event.type]

        # Special handling for move operations
        if event.type == "moved":
            metadata = {
                "original_path": str(event.src_path) if event.src_path else None,
                "pattern": "simple_move",
            }
        else:
            metadata = {
                "pattern": f"simple_{event.type}",
            }

        return FileOperation(
            type=operation_type,
            path=event.path,
            events=[event],
            start_time=event.timestamp,
            end_time=event.timestamp,
            metadata=metadata,
        )

    def detect_direct_modification(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple modify events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are modifications of the same file
        first_event = events[0]
        if not all(
            event.path == first_event.path and event.type == "modified"
            for event in events
        ):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        return FileOperation(
            type=OperationType.UPDATE,
            path=first_event.path,
            events=sorted_events,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            metadata={
                "modification_count": len(sorted_events),
                "pattern": "direct_modification",
                "description": f"Multiple modifications to {first_event.path.name}",
            },
        )
