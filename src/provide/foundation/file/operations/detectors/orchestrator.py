"""File operation detector orchestrator.

Coordinates detector functions via registry to identify the best match for file events.
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path
import re
from typing import Any

from provide.foundation.file.operations.detectors.helpers import (
    extract_base_name,
    is_temp_file,
)
from provide.foundation.file.operations.detectors.registry import get_all_detectors
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

    def __init__(
        self, config: DetectorConfig | None = None, on_operation_complete: Any = None
    ) -> None:
        """Initialize with optional configuration and callback.

        Args:
            config: Detector configuration
            on_operation_complete: Callback function(operation: FileOperation) called
                                 when an operation is detected. Used for streaming mode.
        """
        self.config = config or DetectorConfig()
        self._pattern_cache: dict[str, re.Pattern] = {}
        self._pending_events: list[FileEvent] = []
        self._last_flush = datetime.now()
        self.on_operation_complete = on_operation_complete
        self._flush_timer: Any = None  # asyncio.TimerHandle for auto-flush

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

    def add_event(self, event: FileEvent) -> None:
        """Add event with auto-flush and callback support.

        This is the recommended method for streaming detection with automatic
        temp file hiding and callback-based operation reporting.

        Args:
            event: File event to process

        Behavior:
            - Hides temp files automatically (no callback until operation completes)
            - Schedules auto-flush timer for pending operations
            - Calls on_operation_complete(operation) when pattern detected
            - Emits non-temp files immediately if no operation pattern found
        """
        # Add to pending events
        self._pending_events.append(event)

        # Check if this is a temp file
        is_temp = is_temp_file(event.path) or (event.dest_path and is_temp_file(event.dest_path))

        log.trace(
            "Event added to detector",
            path=str(event.path),
            dest_path=str(event.dest_path) if event.dest_path else None,
            is_temp=is_temp,
            pending_count=len(self._pending_events),
        )

        # All events are buffered and processed via auto-flush
        # This allows the detector to analyze event sequences and detect patterns
        log.trace(
            "Event buffered for auto-flush",
            path=str(event.path),
            is_temp=is_temp,
            pending_count=len(self._pending_events),
        )

        # Schedule auto-flush timer to detect operations after time window
        self._schedule_auto_flush()

    def _schedule_auto_flush(self) -> None:
        """Schedule auto-flush timer."""
        # Cancel existing timer
        if self._flush_timer:
            self._flush_timer.cancel()

        # Schedule new timer
        try:
            loop = asyncio.get_event_loop()
            self._flush_timer = loop.call_later(
                self.config.time_window_ms / 1000.0, self._auto_flush
            )
            log.trace(
                "Auto-flush scheduled",
                window_ms=self.config.time_window_ms,
            )
        except RuntimeError:
            # No event loop running - can't schedule timer
            log.warning("Cannot schedule auto-flush: no event loop running")

    def _auto_flush(self) -> None:
        """Auto-flush callback - emits pending operations."""
        if not self._pending_events:
            return

        log.debug(
            "Auto-flush triggered",
            pending_events=len(self._pending_events),
        )

        # Try to detect operation from pending events
        operation = self._analyze_event_group(self._pending_events)

        if operation:
            # Check if operation only involves temp files
            all_temp = all(
                is_temp_file(event.path)
                and (not event.dest_path or is_temp_file(event.dest_path))
                for event in operation.events
            )

            if all_temp:
                # Pure temp file operation - hide it
                log.debug(
                    "Hiding temp-only operation",
                    operation_type=operation.operation_type.value,
                    event_count=len(operation.events),
                )
            else:
                # Operation touches real files - emit it
                log.debug(
                    "Operation detected on auto-flush",
                    operation_type=operation.operation_type.value,
                )
                if self.on_operation_complete:
                    self.on_operation_complete(operation)
        else:
            # No operation detected, emit individual events
            # BUT: Filter out pure temp file events to reduce noise
            log.debug(
                "No operation detected, filtering and emitting individual events",
                event_count=len(self._pending_events),
            )

            emitted_count = 0
            hidden_count = 0

            for event in self._pending_events:
                # Check if this event involves only temp files
                is_temp_source = is_temp_file(event.path)
                is_temp_dest = event.dest_path and is_temp_file(event.dest_path)

                # Hide event if BOTH source and dest (if exists) are temp files
                if is_temp_source and (not event.dest_path or is_temp_dest):
                    # Pure temp file event - hide it
                    log.trace(
                        "Hiding temp-only event",
                        path=str(event.path),
                        dest_path=str(event.dest_path) if event.dest_path else None,
                    )
                    hidden_count += 1
                else:
                    # Event touches a real file - emit it
                    if self.on_operation_complete:
                        single_op = self._create_single_event_operation(event)
                        self.on_operation_complete(single_op)
                        emitted_count += 1

            log.debug(
                "Auto-flush complete",
                emitted=emitted_count,
                hidden=hidden_count,
            )

        self._pending_events.clear()
        self._last_flush = datetime.now()
        self._flush_timer = None

    def _create_single_event_operation(self, event: FileEvent) -> FileOperation:
        """Create a FileOperation from a single event."""
        return FileOperation(
            operation_type=OperationType.UNKNOWN,
            primary_path=event.path,
            events=[event],
            confidence=1.0,
            description=f"{event.event_type} {event.path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            files_affected=[event.path],
        )

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
        """Analyze a group of events to detect an operation using registry-based detectors.

        Performance optimizations:
        - Registry-based detector lookup (extensible)
        - Priority-ordered execution (highest priority first)
        - Early termination on high-confidence matches (>=0.95)
        """
        if not events:
            return None

        # Get all registered detectors sorted by priority (highest first)
        detectors = get_all_detectors()

        best_operation = None
        best_confidence = 0.0
        # Early termination threshold - stop searching if we find a very high confidence match
        HIGH_CONFIDENCE_THRESHOLD = 0.95

        for detector_name, detect_func, priority in detectors:
            try:
                operation = detect_func(events)
                if operation and operation.confidence > best_confidence:
                    best_operation = operation
                    best_confidence = operation.confidence
                    log.debug(
                        "Found better operation match",
                        detector=detector_name,
                        priority=priority,
                        confidence=operation.confidence,
                        operation_type=operation.operation_type.value,
                        primary_path=str(operation.primary_path),
                    )

                    # Early termination: if we found a very high confidence match, stop searching
                    if best_confidence >= HIGH_CONFIDENCE_THRESHOLD:
                        log.debug(
                            "Early termination on high confidence match",
                            confidence=best_confidence,
                            detector=detector_name,
                        )
                        break

            except Exception as e:
                log.warning(
                    "Detector failed",
                    detector=detector_name,
                    priority=priority,
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
