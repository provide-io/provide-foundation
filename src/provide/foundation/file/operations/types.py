#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""File operation data types and structures."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from attrs import define, field

from provide.foundation.config.defaults import (
    DEFAULT_FILE_OP_HAS_BACKUP,
    DEFAULT_FILE_OP_IS_ATOMIC,
    DEFAULT_FILE_OP_IS_SAFE,
)


@define(frozen=True, slots=True, kw_only=True)
class FileEventMetadata:
    """Rich metadata for a file event."""

    # Timing
    timestamp: datetime
    sequence_number: int  # Order within operation

    # File info (if available)
    size_before: int | None = field(default=None)
    size_after: int | None = field(default=None)
    permissions: int | None = field(default=None)  # Unix permissions
    owner: str | None = field(default=None)
    group: str | None = field(default=None)

    # Content hints
    mime_type: str | None = field(default=None)
    encoding: str | None = field(default=None)
    is_binary: bool | None = field(default=None)

    # Context
    process_id: int | None = field(default=None)
    process_name: str | None = field(default=None)
    user: str | None = field(default=None)

    # Performance
    duration_ms: float | None = field(default=None)  # Time to complete this event

    # Custom attributes
    extra: dict[str, Any] = field(factory=dict)


@define(frozen=True, slots=True, kw_only=True)
class FileEvent:
    """Single file system event with rich metadata."""

    path: Path
    event_type: str  # created, modified, deleted, moved, renamed
    metadata: FileEventMetadata
    dest_path: Path | None = field(default=None)  # For move/rename events

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


@define(slots=True, kw_only=True)
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
    total_size_changed: int | None = field(default=None)
    files_affected: list[Path] | None = field(default=None)

    # Analysis results
    is_atomic: bool = field(default=DEFAULT_FILE_OP_IS_ATOMIC)
    is_safe: bool = field(default=DEFAULT_FILE_OP_IS_SAFE)
    has_backup: bool = field(default=DEFAULT_FILE_OP_HAS_BACKUP)

    # Optional metadata
    metadata: dict[str, Any] = field(factory=dict)

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


@define(slots=True, kw_only=True)
class DetectorConfig:
    """Configuration for operation detection."""

    # Time window for grouping related events (milliseconds)
    time_window_ms: int = field(default=500)

    # Maximum time between first and last event in an operation
    max_operation_duration_ms: int = field(default=2000)

    # Minimum events to consider for complex operations
    min_events_for_complex: int = field(default=2)

    # Confidence threshold for operation detection
    min_confidence: float = field(default=0.7)

    # Temp file patterns
    temp_patterns: list[str] = field(
        factory=lambda: [
            r"\..*\.tmp\.\w+$",  # .file.tmp.xxxxx (VSCode, Sublime)
            r".*~$",  # file~ (Vim, Emacs)
            r"\..*\.sw[po]$",  # .file.swp, .file.swo (Vim)
            r"^#.*#$",  # #file# (Emacs auto-save)
            r".*\.bak$",  # file.bak (backup files)
            r".*\.orig$",  # file.orig (merge conflicts)
            r".*\.tmp$",  # file.tmp (generic temp)
        ]
    )


# 🧱🏗️🔚
