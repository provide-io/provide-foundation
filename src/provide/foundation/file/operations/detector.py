"""File operation detector implementation."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from pathlib import Path
import re

from provide.foundation.file.operations.types import (
    DetectorConfig,
    FileEvent,
    FileOperation,
    OperationType,
)
from provide.foundation.logger import get_logger

log = get_logger(__name__)


class OperationDetector:
    """Detects and classifies file operations from events."""

    def __init__(self, config: DetectorConfig | None = None) -> None:
        """Initialize with optional configuration."""
        self.config = config or DetectorConfig()
        self._pattern_cache: dict[str, re.Pattern] = {}
        self._pending_events: list[FileEvent] = []
        self._last_flush = datetime.now()

    def detect(self, events: list[FileEvent]) -> list[FileOperation]:
        """Detect all operations from a list of events.

        Args:
            events: List of file events to analyze

        Returns:
            List of detected operations, ordered by start time
        """
        if not events:
            return []

        # Sort events by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Group events by time windows
        event_groups = self._group_events_by_time(sorted_events)

        operations = []
        for group in event_groups:
            operation = self._analyze_event_group(group)
            if operation:
                operations.append(operation)

        return operations

    def detect_streaming(self, event: FileEvent) -> FileOperation | None:
        """Process events in streaming fashion.

        Args:
            event: Single file event

        Returns:
            Completed operation if detected, None otherwise
        """
        self._pending_events.append(event)

        # Check if we should flush based on time window
        now = datetime.now()
        time_since_last = (now - self._last_flush).total_seconds() * 1000

        if time_since_last >= self.config.time_window_ms:
            return self._flush_pending()

        return None

    def flush(self) -> list[FileOperation]:
        """Get any pending operations and clear buffer."""
        operations = []
        if self._pending_events:
            operation = self._flush_pending()
            if operation:
                operations.append(operation)
        return operations

    def _flush_pending(self) -> FileOperation | None:
        """Analyze pending events and clear buffer."""
        if not self._pending_events:
            return None

        operation = self._analyze_event_group(self._pending_events)
        self._pending_events.clear()
        self._last_flush = datetime.now()
        return operation

    def _group_events_by_time(self, events: list[FileEvent]) -> list[list[FileEvent]]:
        """Group events that occur within time windows."""
        if not events:
            return []

        groups = []
        current_group = [events[0]]

        for event in events[1:]:
            time_diff = (event.timestamp - current_group[-1].timestamp).total_seconds() * 1000

            if time_diff <= self.config.time_window_ms:
                current_group.append(event)
            else:
                groups.append(current_group)
                current_group = [event]

        if current_group:
            groups.append(current_group)

        return groups

    def _analyze_event_group(self, events: list[FileEvent]) -> FileOperation | None:
        """Analyze a group of events to detect an operation."""
        if not events:
            return None

        # Try different detection strategies in order of specificity
        detectors = [
            self._detect_atomic_save,
            self._detect_safe_write,
            self._detect_rename_sequence,
            self._detect_batch_update,
            self._detect_backup_create,
            self._detect_simple_operation,  # Fallback for basic operations
        ]

        best_operation = None
        best_confidence = 0.0

        for detector in detectors:
            operation = detector(events)
            if operation and operation.confidence > best_confidence:
                best_operation = operation
                best_confidence = operation.confidence

        return best_operation if best_confidence >= self.config.min_confidence else None

    def _detect_atomic_save(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect atomic save pattern (temp file creation -> rename)."""
        confidence = 0.0
        primary_file = None
        atomic_events = []
        final_file = None

        # Look for temp file creation followed by rename to final name
        temp_creates = [e for e in events if e.event_type == "created" and self._is_temp_file(e.path)]
        moves = [e for e in events if e.event_type in ("moved", "renamed")]

        # Pattern 1: Direct temp file rename to final location
        for temp_event in temp_creates:
            for move_event in moves:
                if move_event.path == temp_event.path and move_event.dest_path:
                    # Temp file was renamed to final location - this is the end state
                    primary_file = move_event.dest_path
                    final_file = move_event.dest_path
                    atomic_events = [temp_event, move_event]
                    confidence = 0.95
                    break

        # Pattern 2: Delete original, rename temp (common in atomic saves)
        if not primary_file:
            deletes = [e for e in events if e.event_type == "deleted"]
            for delete_event in deletes:
                for temp_event in temp_creates:
                    if self._files_related(delete_event.path, temp_event.path):
                        # The deleted file is what gets replaced - this becomes the end state
                        primary_file = delete_event.path
                        final_file = delete_event.path
                        atomic_events = [e for e in events if e.path in (delete_event.path, temp_event.path)]
                        confidence = 0.85
                        break

        # Pattern 3: Temp file created, then final file modified (overwrite pattern)
        if not primary_file:
            modifies = [e for e in events if e.event_type == "modified" and not self._is_temp_file(e.path)]
            for temp_event in temp_creates:
                for modify_event in modifies:
                    if self._files_related(temp_event.path, modify_event.path):
                        # The modified file is the end state
                        primary_file = modify_event.path
                        final_file = modify_event.path
                        atomic_events = [temp_event, modify_event]
                        confidence = 0.80
                        break

        if primary_file and final_file and confidence >= self.config.min_confidence:
            start_time = min(e.timestamp for e in atomic_events)
            end_time = max(e.timestamp for e in atomic_events)

            # Collect all file paths affected, but primary_path is the end-state file
            files_affected = list({e.path for e in events} | {e.dest_path for e in events if e.dest_path})

            return FileOperation(
                operation_type=OperationType.ATOMIC_SAVE,
                primary_path=final_file,  # This is the end-state file that git sees
                events=events,  # Include all events for operation history
                confidence=confidence,
                description=f"Atomic save of {final_file.name}",
                start_time=start_time,
                end_time=end_time,
                is_atomic=True,
                is_safe=True,
                files_affected=files_affected,
            )

        return None

    def _detect_safe_write(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect safe write pattern (backup -> write)."""
        # Look for backup creation followed by modification
        backup_events = [e for e in events if e.path.suffix in (".bak", ".backup", ".orig")]
        modify_events = [
            e
            for e in events
            if e.event_type in ("modified", "created") and e.path.suffix not in (".bak", ".backup", ".orig")
        ]

        if backup_events and modify_events:
            primary_file = None
            for backup_event in backup_events:
                base_name = self._extract_base_name(backup_event.path)
                if not base_name:
                    continue
                for modify_event in modify_events:
                    # Compare the backup's base name with the modify event's filename
                    if base_name == modify_event.path.name:
                        primary_file = modify_event.path
                        break

            if primary_file:
                start_time = min(e.timestamp for e in events)
                end_time = max(e.timestamp for e in events)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=primary_file,
                    events=events,
                    confidence=0.95,
                    description=f"Safe write of {primary_file.name}",
                    start_time=start_time,
                    end_time=end_time,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                )

        return None

    def _detect_rename_sequence(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect a sequence of renames/moves."""
        move_events = [e for e in events if e.event_type in ("moved", "renamed")]

        if len(move_events) >= 2:
            # Check if moves form a chain
            first_event = move_events[0]
            last_event = move_events[-1]

            start_time = min(e.timestamp for e in events)
            end_time = max(e.timestamp for e in events)

            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=last_event.dest_path or last_event.path,
                events=events,
                confidence=0.90,
                description=f"Rename sequence: {first_event.path.name} -> {last_event.dest_path.name if last_event.dest_path else last_event.path.name}",
                start_time=start_time,
                end_time=end_time,
                is_atomic=True,
                is_safe=True,
            )

        return None

    def _detect_batch_update(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch file operations (multiple files, similar timing)."""
        if len(events) < self.config.min_events_for_complex:
            return None

        # Group by operation type
        type_groups = defaultdict(list)
        for event in events:
            type_groups[event.event_type].append(event)

        # Look for consistent patterns across multiple files
        if "modified" in type_groups and len(type_groups["modified"]) >= 3:
            # Multiple modifications in quick succession suggests batch operation
            modify_events = type_groups["modified"]
            unique_files = {e.path for e in modify_events}

            if len(unique_files) >= 3:  # At least 3 different files
                start_time = min(e.timestamp for e in events)
                end_time = max(e.timestamp for e in events)

                # Use the directory or first file as primary path
                primary_path = modify_events[0].path.parent

                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=primary_path,
                    events=events,
                    confidence=0.85,
                    description=f"Batch update of {len(unique_files)} files",
                    start_time=start_time,
                    end_time=end_time,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=list(unique_files),
                )

        return None

    def _detect_backup_create(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup file creation."""
        backup_events = [
            e
            for e in events
            if e.event_type == "created" and e.path.suffix in (".bak", ".backup", ".orig", "~")
        ]

        if backup_events:
            backup_event = backup_events[0]
            start_time = backup_event.timestamp
            end_time = backup_event.timestamp

            return FileOperation(
                operation_type=OperationType.BACKUP_CREATE,
                primary_path=backup_event.path,
                events=[backup_event],
                confidence=0.90,
                description=f"Backup created: {backup_event.path.name}",
                start_time=start_time,
                end_time=end_time,
                is_atomic=True,
                is_safe=True,
                has_backup=True,
            )

        return None

    def _detect_simple_operation(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple file operations (create, modify, delete)."""
        if not events:
            return None

        # Filter out directory events
        file_events = [e for e in events if not e.path.name.endswith("/")]
        if not file_events:
            return None

        # Get the primary file (most frequently mentioned or first non-temp file)
        file_paths = [e.path for e in file_events]
        primary_file = None

        # Prefer non-temp files
        non_temp_files = [p for p in file_paths if not self._is_temp_file(p)]
        if non_temp_files:
            primary_file = non_temp_files[0]
        else:
            primary_file = file_paths[0]

        # Determine operation type based on event types
        event_types = {e.event_type for e in file_events}

        if "created" in event_types and "modified" in event_types:
            operation_type = OperationType.ATOMIC_SAVE  # File created and modified
            confidence = 0.75
        elif "created" in event_types:
            operation_type = OperationType.BACKUP_CREATE  # New file created
            confidence = 0.70
        elif "modified" in event_types:
            operation_type = OperationType.ATOMIC_SAVE  # File modified
            confidence = 0.72
        elif "deleted" in event_types:
            operation_type = OperationType.BACKUP_CREATE  # File deleted (use as fallback)
            confidence = 0.70
        else:
            return None

        start_time = min(e.timestamp for e in file_events)
        end_time = max(e.timestamp for e in file_events)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_file,
            events=file_events,
            confidence=confidence,
            description=f"Simple file operation on {primary_file.name}",
            start_time=start_time,
            end_time=end_time,
            is_atomic=len(file_events) == 1,
            is_safe=True,
            files_affected=[primary_file],
        )

    def _is_temp_file(self, path: Path) -> bool:
        """Check if path matches any temp file pattern."""
        filename = path.name
        for pattern_str in self.config.temp_patterns:
            if pattern_str not in self._pattern_cache:
                self._pattern_cache[pattern_str] = re.compile(pattern_str)

            pattern = self._pattern_cache[pattern_str]
            if pattern.search(filename):
                return True
        return False

    def _extract_base_name(self, path: Path) -> str | None:
        """Extract base filename from temp file path."""
        filename = path.name

        # Try each pattern to extract base name
        patterns = [
            (r"^\.(.*)\.tmp\.\w+$", 1),  # .file.tmp.xxxxx -> file
            (r"^(.*)\.tmp\.\d+$", 1),  # file.tmp.12345 -> file
            (r"^(.*)~$", 1),  # file~ -> file
            (r"^\.(.*)\.sw[po]$", lambda m: f".{m.group(1)}"),  # .file.swp -> .file
            (r"^#(.*)#$", 1),  # #file# -> file
            (r"^(.*)\.bak$", 1),  # file.bak -> file
            (r"^(.*)\.orig$", 1),  # file.orig -> file
            (r"^(.*)\.tmp$", 1),  # file.tmp -> file
        ]

        for pattern_str, extractor in patterns:
            if pattern_str not in self._pattern_cache:
                self._pattern_cache[pattern_str] = re.compile(pattern_str)

            pattern = self._pattern_cache[pattern_str]
            match = pattern.match(filename)
            if match:
                if callable(extractor):
                    return extractor(match)
                else:
                    return match.group(extractor)

        return None

    def _files_related(self, path1: Path, path2: Path) -> bool:
        """Check if two file paths are related (same base name)."""
        base1 = self._extract_base_name(path1)
        base2 = self._extract_base_name(path2)

        if base1 and base2:
            return base1 == base2

        # Fallback: check if one path's base name matches the other's full name
        if base1:
            return base1 == path2.name
        if base2:
            return base2 == path1.name

        # Final fallback: check if stems are the same
        return path1.stem == path2.stem
