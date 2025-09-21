"""File operation detection and analysis.

This module provides intelligent detection and grouping of file system events
into logical operations (e.g., atomic saves, batch updates, rename sequences).
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
import re
from typing import Any

from provide.foundation.logger import get_logger

log = get_logger(__name__)


@dataclass
class FileEventMetadata:
    """Rich metadata for a file event."""

    # Timing
    timestamp: datetime
    sequence_number: int  # Order within operation

    # File info (if available)
    size_before: int | None = None
    size_after: int | None = None
    permissions: int | None = None  # Unix permissions
    owner: str | None = None
    group: str | None = None

    # Content hints
    mime_type: str | None = None
    encoding: str | None = None
    is_binary: bool | None = None

    # Context
    process_id: int | None = None
    process_name: str | None = None
    user: str | None = None

    # Performance
    duration_ms: float | None = None  # Time to complete this event

    # Custom attributes
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class FileEvent:
    """Single file system event with rich metadata."""

    path: Path
    event_type: str  # created, modified, deleted, moved, renamed
    metadata: FileEventMetadata
    dest_path: Path | None = None  # For move/rename events

    @property
    def timestamp(self) -> datetime:
        """Convenience accessor for timestamp."""
        return self.metadata.timestamp

    @property
    def sequence(self) -> int:
        """Convenience accessor for sequence number."""
        return self.metadata.sequence_number

    @property
    def size_delta(self) -> int | None:
        """Change in file size, if known."""
        if self.metadata.size_before is not None and self.metadata.size_after is not None:
            return self.metadata.size_after - self.metadata.size_before
        return None


class OperationType(Enum):
    """Types of detected file operations."""

    ATOMIC_SAVE = "atomic_save"
    SAFE_WRITE = "safe_write"  # Write with backup
    BATCH_UPDATE = "batch_update"
    RENAME_SEQUENCE = "rename_sequence"
    BACKUP_CREATE = "backup"
    BUILD_OUTPUT = "build"
    VCS_OPERATION = "vcs"
    SYNC_OPERATION = "sync"
    ARCHIVE_EXTRACT = "extract"
    TEMP_CLEANUP = "cleanup"
    UNKNOWN = "unknown"


@dataclass
class FileOperation:
    """A detected logical file system operation."""

    operation_type: OperationType
    primary_path: Path  # The main file affected
    events: list[FileEvent]  # Ordered by sequence_number
    confidence: float  # 0.0 to 1.0
    description: str

    # Operation-level metadata
    start_time: datetime
    end_time: datetime
    total_size_changed: int | None = None
    files_affected: list[Path] | None = None

    # Analysis results
    is_atomic: bool = False  # Was this atomic?
    is_safe: bool = True  # Was data preserved?
    has_backup: bool = False  # Was backup created?

    # Optional metadata
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def duration_ms(self) -> float:
        """Total operation duration."""
        return (self.end_time - self.start_time).total_seconds() * 1000

    @property
    def event_count(self) -> int:
        """Number of events in this operation."""
        return len(self.events)

    def get_timeline(self) -> list[tuple[float, FileEvent]]:
        """Get events with relative timestamps (ms from start)."""
        return [
            ((e.timestamp - self.start_time).total_seconds() * 1000, e)
            for e in sorted(self.events, key=lambda x: x.sequence)
        ]


@dataclass
class DetectorConfig:
    """Configuration for operation detection."""

    # Time window for grouping related events (milliseconds)
    time_window_ms: int = 500

    # Maximum time between first and last event in an operation
    max_operation_duration_ms: int = 2000

    # Minimum events to consider for complex operations
    min_events_for_complex: int = 2

    # Confidence threshold for operation detection
    min_confidence: float = 0.7

    # Temp file patterns
    temp_patterns: list[str] = field(
        default_factory=lambda: [
            r"\..*\.tmp\.\w+$",  # .file.tmp.xxxxx (VSCode, Sublime)
            r".*~$",  # file~ (Vim, Emacs)
            r"\..*\.sw[po]$",  # .file.swp, .file.swo (Vim)
            r"^#.*#$",  # #file# (Emacs auto-save)
            r".*\.bak$",  # file.bak (backup files)
            r".*\.orig$",  # file.orig (merge conflicts)
            r".*\.tmp$",  # file.tmp (generic temp)
        ]
    )


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

        # Look for temp file creation followed by rename to final name
        temp_creates = [e for e in events if e.event_type == "created" and self._is_temp_file(e.path)]
        moves = [e for e in events if e.event_type in ("moved", "renamed")]

        for temp_event in temp_creates:
            for move_event in moves:
                if move_event.path == temp_event.path and move_event.dest_path:
                    # Temp file was renamed to final location
                    primary_file = move_event.dest_path
                    atomic_events = [temp_event, move_event]
                    confidence = 0.95
                    break

        # Alternative pattern: delete original, rename temp
        if not primary_file:
            deletes = [e for e in events if e.event_type == "deleted"]
            for delete_event in deletes:
                for temp_event in temp_creates:
                    if self._files_related(delete_event.path, temp_event.path):
                        primary_file = delete_event.path
                        atomic_events = [e for e in events if e.path in (delete_event.path, temp_event.path)]
                        confidence = 0.85
                        break

        if primary_file and confidence >= self.config.min_confidence:
            start_time = min(e.timestamp for e in atomic_events)
            end_time = max(e.timestamp for e in atomic_events)

            return FileOperation(
                operation_type=OperationType.ATOMIC_SAVE,
                primary_path=primary_file,
                events=atomic_events,
                confidence=confidence,
                description=f"Atomic save of {primary_file.name}",
                start_time=start_time,
                end_time=end_time,
                is_atomic=True,
                is_safe=True,
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
                    # Compare the base name of the modify event with the extracted base name
                    modify_base_name = self._extract_base_name(modify_event.path)
                    if modify_base_name == base_name:
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

            start_time = min(e.timestamp for e in move_events)
            end_time = max(e.timestamp for e in move_events)

            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=last_event.dest_path or last_event.path,
                events=move_events,
                confidence=0.75,
                description=f"Rename sequence: {first_event.path.name} → {last_event.dest_path.name if last_event.dest_path else last_event.path.name}",
                start_time=start_time,
                end_time=end_time,
                is_atomic=True,
                is_safe=True,
            )

        return None

    def _detect_batch_update(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update of multiple related files."""
        if len(events) < self.config.min_events_for_complex:
            return None

        # Group by directory
        dir_groups = defaultdict(list)
        for event in events:
            dir_groups[event.path.parent].append(event)

        # Find the directory with the most events
        primary_dir = max(dir_groups.keys(), key=lambda d: len(dir_groups[d]))
        primary_events = dir_groups[primary_dir]

        if len(primary_events) >= self.config.min_events_for_complex:
            start_time = min(e.timestamp for e in primary_events)
            end_time = max(e.timestamp for e in primary_events)

            return FileOperation(
                operation_type=OperationType.BATCH_UPDATE,
                primary_path=primary_dir,
                events=primary_events,
                confidence=0.7,
                description=f"Batch update of {len(primary_events)} files in {primary_dir.name}",
                start_time=start_time,
                end_time=end_time,
                is_atomic=False,
                is_safe=True,
            )

        return None

    def _detect_backup_create(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup file creation."""
        backup_events = [e for e in events if self._is_backup_file(e.path)]

        if backup_events:
            primary_event = backup_events[0]
            start_time = min(e.timestamp for e in backup_events)
            end_time = max(e.timestamp for e in backup_events)

            return FileOperation(
                operation_type=OperationType.BACKUP_CREATE,
                primary_path=primary_event.path,
                events=backup_events,
                confidence=0.9,
                description=f"Backup creation: {primary_event.path.name}",
                start_time=start_time,
                end_time=end_time,
                is_atomic=True,
                is_safe=True,
                has_backup=True,
            )

        return None

    def _is_temp_file(self, path: Path) -> bool:
        """Check if file matches temp patterns."""
        name = path.name
        for pattern in self.config.temp_patterns:
            if pattern not in self._pattern_cache:
                self._pattern_cache[pattern] = re.compile(pattern)
            if self._pattern_cache[pattern].search(name):
                return True
        return False

    def _is_backup_file(self, path: Path) -> bool:
        """Check if file is a backup file."""
        return path.suffix in (".bak", ".backup", ".orig", ".save")

    def _files_related(self, file1: Path, file2: Path) -> bool:
        """Check if two files are related (same base name)."""
        base1 = self._extract_base_name(file1)
        base2 = self._extract_base_name(file2)
        return base1 == base2 and base1 is not None

    def _extract_base_name(self, path: Path) -> str | None:
        """Extract base name from potentially temp file."""
        name = path.name

        # Remove common temp patterns
        patterns = [
            (r"\.tmp\.\w+$", ""),  # .tmp.xxxxx
            (r"~$", ""),  # ~
            (r"\.sw[po]$", ""),  # .swp, .swo
            (r"^#(.+)#$", r"\1"),  # #file#
            (r"\.bak$", ""),  # .bak
            (r"\.orig$", ""),  # .orig
            (r"\.tmp$", ""),  # .tmp
        ]

        for pattern, replacement in patterns:
            cleaned = re.sub(pattern, replacement, name)
            if cleaned != name:
                return cleaned if cleaned else None

        return name


# Convenience functions for simple use cases
def detect_atomic_save(events: list[FileEvent]) -> FileOperation | None:
    """Detect if events represent an atomic save operation."""
    detector = OperationDetector()
    operations = detector.detect(events)
    return next((op for op in operations if op.operation_type == OperationType.ATOMIC_SAVE), None)


def is_temp_file(path: Path) -> bool:
    """Check if a path represents a temporary file."""
    detector = OperationDetector()
    return detector._is_temp_file(path)


def extract_original_path(temp_path: Path) -> Path | None:
    """Extract the original filename from a temp file path."""
    detector = OperationDetector()
    base_name = detector._extract_base_name(temp_path)
    return temp_path.parent / base_name if base_name else None


def group_related_events(events: list[FileEvent], time_window_ms: int = 500) -> list[list[FileEvent]]:
    """Group events that occur within a time window."""
    config = DetectorConfig(time_window_ms=time_window_ms)
    detector = OperationDetector(config)
    return detector._group_events_by_time(sorted(events, key=lambda e: e.timestamp))
