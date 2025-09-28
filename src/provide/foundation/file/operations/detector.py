"""File operation detector implementation (refactored)."""

from __future__ import annotations

import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from provide.foundation.file.operations.detectors import (
    AtomicOperationDetector,
    BatchOperationDetector,
    SimpleOperationDetector,
    TempPatternDetector,
)
from provide.foundation.file.operations.types import (
    DetectorConfig,
    FileEvent,
    FileOperation,
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

        # Initialize specialized detectors
        self.atomic_detector = AtomicOperationDetector()
        self.batch_detector = BatchOperationDetector()
        self.simple_detector = SimpleOperationDetector()
        self.temp_detector = TempPatternDetector()

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

        return sorted(operations, key=lambda op: op.start_time)

    def detect_streaming(self, event: FileEvent) -> FileOperation | None:
        """Detect operations from streaming events.

        Args:
            event: New file event to process

        Returns:
            Detected operation if any, or None
        """
        self._pending_events.append(event)

        # Check if we should flush based on time
        now = datetime.now()
        time_since_last = (now - self._last_flush).total_seconds() * 1000

        if time_since_last >= self.config.flush_interval_ms:
            return self.flush()

        # Try to detect operation with current pending events
        return self._flush_pending()

    def flush(self) -> list[FileOperation]:
        """Flush all pending events and return detected operations."""
        if not self._pending_events:
            return []

        operations = self.detect(self._pending_events)
        self._pending_events.clear()
        self._last_flush = datetime.now()

        return operations

    def _flush_pending(self) -> FileOperation | None:
        """Try to detect operation from pending events without full flush."""
        if len(self._pending_events) < 2:
            return None

        # Try to detect with recent events only
        recent_events = self._pending_events[-5:]  # Last 5 events
        return self._analyze_event_group(recent_events)

    def _group_events_by_time(self, events: list[FileEvent]) -> list[list[FileEvent]]:
        """Group events by time windows for batch detection."""
        if not events:
            return []

        groups = []
        current_group = [events[0]]
        window_ms = self.config.time_window_ms

        for event in events[1:]:
            time_diff = (event.timestamp - current_group[-1].timestamp).total_seconds() * 1000

            if time_diff <= window_ms:
                current_group.append(event)
            else:
                groups.append(current_group)
                current_group = [event]

        if current_group:
            groups.append(current_group)

        return groups

    def _analyze_event_group(self, events: list[FileEvent]) -> FileOperation | None:
        """Analyze a group of events to detect operations.

        Tries different detection patterns in order of specificity.
        """
        if not events:
            return None

        # Try specialized detectors in order of specificity
        detectors_and_methods = [
            # Temporary file patterns (most specific)
            (self.temp_detector, "detect_temp_rename_pattern"),
            (self.temp_detector, "detect_delete_temp_pattern"),
            (self.temp_detector, "detect_temp_modify_pattern"),
            (self.temp_detector, "detect_temp_create_delete_pattern"),

            # Simple same-file patterns
            (self.simple_detector, "detect_same_file_delete_create_pattern"),

            # Atomic operations
            (self.atomic_detector, "detect_atomic_save"),
            (self.atomic_detector, "detect_safe_write"),

            # Batch operations
            (self.batch_detector, "detect_rename_sequence"),
            (self.batch_detector, "detect_batch_update"),
            (self.batch_detector, "detect_backup_create"),

            # Simple operations (fallback)
            (self.simple_detector, "detect_simple_operation"),
            (self.simple_detector, "detect_direct_modification"),
        ]

        for detector, method_name in detectors_and_methods:
            try:
                method = getattr(detector, method_name)
                operation = method(events)
                if operation:
                    log.debug(f"Detected operation using {method_name}: {operation.type}")
                    return operation
            except Exception as e:
                log.warning(f"Error in {method_name}: {e}")
                continue

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

    def _extract_base_name(self, path: Path) -> str | None:
        """Extract base filename for grouping related files."""
        name = path.name

        # Remove common temp/backup suffixes
        suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

        base_name = name
        for suffix in suffixes_to_remove:
            if base_name.endswith(suffix):
                base_name = base_name[: -len(suffix)]
                break

        # Remove temp prefixes
        prefixes_to_remove = ["tmp", ".tmp", ".#"]
        for prefix in prefixes_to_remove:
            if base_name.startswith(prefix):
                base_name = base_name[len(prefix) :]
                break

        return base_name if base_name else None

    def _files_related(self, path1: Path, path2: Path) -> bool:
        """Check if two file paths are related."""
        # Same directory
        if path1.parent != path2.parent:
            return False

        # Extract base names
        base1 = self._extract_base_name(path1)
        base2 = self._extract_base_name(path2)

        if not base1 or not base2:
            return False

        # Check if base names are similar
        return base1 == base2 or abs(len(base1) - len(base2)) <= 2