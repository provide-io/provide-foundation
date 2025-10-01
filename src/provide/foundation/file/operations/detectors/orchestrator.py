"""File operation detector orchestrator.

Coordinates specialized detector classes to identify the best match for file events.
"""

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
from provide.foundation.file.operations.detectors.atomic import AtomicOperationDetector
from provide.foundation.file.operations.detectors.batch import BatchOperationDetector
from provide.foundation.file.operations.detectors.simple import SimpleOperationDetector
from provide.foundation.file.operations.detectors.temp import TempPatternDetector
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
        """Group events that occur within time windows.

        Uses a fixed time window from the first event in each group to ensure
        all related events are captured together, even if they span longer than
        the window between consecutive events.
        """
        if not events:
            return []

        groups = []
        current_group = [events[0]]
        group_start_time = events[0].timestamp  # Track first event in group

        for event in events[1:]:
            # Compare to FIRST event in group, not last (fixes bundling bug)
            time_diff = (event.timestamp - group_start_time).total_seconds() * 1000

            if time_diff <= self.config.time_window_ms:
                current_group.append(event)
            else:
                groups.append(current_group)
                current_group = [event]
                group_start_time = event.timestamp  # Reset for new group

        if current_group:
            groups.append(current_group)

        return groups

    def _analyze_event_group(self, events: list[FileEvent]) -> FileOperation | None:
        """Analyze a group of events to detect an operation using specialized detectors."""
        if not events:
            return None

        # Initialize specialized detector instances
        atomic_detector = AtomicOperationDetector()
        temp_detector = TempPatternDetector()
        batch_detector = BatchOperationDetector()
        simple_detector = SimpleOperationDetector()

        # Try detectors in order of specificity (most specific patterns first)
        # This ensures that editor-specific patterns are detected before generic ones
        detection_attempts = [
            # Temp file patterns (highest specificity for atomic saves)
            (temp_detector.detect_temp_rename_pattern, (events,)),
            (temp_detector.detect_delete_temp_pattern, (events,)),
            (temp_detector.detect_temp_modify_pattern, (events,)),
            (temp_detector.detect_temp_create_delete_pattern, (events,)),

            # Atomic save patterns
            (atomic_detector.detect_atomic_save, (events,)),
            (atomic_detector.detect_safe_write, (events,)),

            # Batch and sequence patterns
            (batch_detector.detect_rename_sequence, (events,)),
            (batch_detector.detect_backup_create, (events,)),
            (batch_detector.detect_batch_update, (events,)),

            # Simple patterns (lower specificity)
            (simple_detector.detect_same_file_delete_create_pattern, (events,)),
            (simple_detector.detect_direct_modification, (events,)),

            # Fallback for unmatched events
            (simple_detector.detect_simple_operation, (events,)),
        ]

        best_operation = None
        best_confidence = 0.0

        for detect_func, args in detection_attempts:
            try:
                operation = detect_func(*args)
                if operation and operation.confidence > best_confidence:
                    best_operation = operation
                    best_confidence = operation.confidence
                    log.debug(
                        "Found better operation match",
                        detector=detect_func.__name__,
                        confidence=operation.confidence,
                        operation_type=operation.operation_type.value,
                        primary_path=str(operation.primary_path),
                    )
            except Exception as e:
                log.warning(
                    "Detector failed",
                    detector=detect_func.__name__,
                    error=str(e),
                )

        if best_operation and best_confidence >= self.config.min_confidence:
            # Validate that primary_path is not a temp file
            if is_temp_file(best_operation.primary_path):
                log.warning(
                    "Detector returned temp file as primary_path, attempting to fix",
                    temp_path=str(best_operation.primary_path),
                    operation_type=best_operation.operation_type.value,
                )
                # Try to find the real file from the events
                real_file = self._find_real_file_from_events(best_operation.events)
                if real_file:
                    # Create a new operation with the corrected path
                    # (FileOperation is frozen, so we need attrs.evolve or recreate)
                    from attrs import evolve
                    best_operation = evolve(best_operation, primary_path=real_file)
                    log.info(
                        "Corrected primary_path from temp to real file",
                        corrected_path=str(real_file),
                    )
                else:
                    log.error(
                        "Could not find real file, rejecting operation",
                        temp_path=str(best_operation.primary_path),
                    )
                    return None

            log.debug(
                "Selected operation",
                operation_type=best_operation.operation_type.value,
                primary_path=str(best_operation.primary_path),
                confidence=best_confidence,
                is_temp=is_temp_file(best_operation.primary_path),
            )
            return best_operation

        return None

    def _find_real_file_from_events(self, events: list[FileEvent]) -> Path | None:
        """Find the real (non-temp) file path from a list of events."""
        # Look for non-temp files in the events
        for event in reversed(events):  # Start from most recent
            # Check dest_path first (for move/rename operations)
            if event.dest_path and not is_temp_file(event.dest_path):
                return event.dest_path
            # Then check regular path
            if not is_temp_file(event.path):
                return event.path

        # If all files are temp files, try to extract the base name
        for event in events:
            if event.dest_path:
                base_name = extract_base_name(event.dest_path)
                if base_name:
                    # Try to construct real path from base name
                    real_path = event.dest_path.parent / base_name
                    if real_path != event.dest_path:
                        return real_path

            base_name = extract_base_name(event.path)
            if base_name:
                real_path = event.path.parent / base_name
                if real_path != event.path:
                    return real_path

        return None

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
        patterns: list[tuple[str, int | object]] = [
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
                elif isinstance(extractor, int):
                    return match.group(extractor)

        return None

    def _files_related(self, path1: Path, path2: Path) -> bool:
        """Check if two file paths are related (same base name)."""
        base1 = extract_base_name(path1)
        base2 = extract_base_name(path2)

        if base1 and base2:
            return base1 == base2

        # Fallback: check if one path's base name matches the other's full name
        if base1:
            return base1 == path2.name
        if base2:
            return base2 == path1.name

        # Final fallback: check if stems are the same
        return path1.stem == path2.stem
