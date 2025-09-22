"""File operation data types and structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


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
