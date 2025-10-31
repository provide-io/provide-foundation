#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""File operation detector orchestrator.

Coordinates detector functions via registry to identify the best match for file events."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from provide.foundation.file.operations.detectors.auto_flush import AutoFlushHandler
from provide.foundation.file.operations.detectors.helpers import (
    extract_base_name,
    is_temp_file,
)
from provide.foundation.file.operations.detectors.registry import get_detector_registry
from provide.foundation.file.operations.types import (
    DetectorConfig,
    FileEvent,
    FileOperation,
)
from provide.foundation.hub.registry import Registry
from provide.foundation.logger import get_logger

log = get_logger(__name__)


class OperationDetector:
    """Detects and classifies file operations from events."""

    def __init__(
        self,
        config: DetectorConfig | None = None,
        on_operation_complete: Any = None,
        registry: Registry | None = None,
    ) -> None:
        """Initialize with optional configuration and callback.

        Args:
            config: Detector configuration
            on_operation_complete: Callback function(operation: FileOperation) called
                                 when an operation is detected. Used for streaming mode.
            registry: Optional registry for detectors (defaults to global)
        """
        self.config = config or DetectorConfig()
        self.on_operation_complete = on_operation_complete
        self.registry = registry or get_detector_registry()
        self._pending_events: list[FileEvent] = []
        self._last_flush = datetime.now()

        # Create auto-flush handler for streaming mode
        self._auto_flush_handler = AutoFlushHandler(
            time_window_ms=self.config.time_window_ms,
            on_operation_complete=on_operation_complete,
            analyze_func=self._analyze_event_group,
        )

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
        # Delegate to auto-flush handler
        self._auto_flush_handler.add_event(event)

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

        # Get all registered detectors from the instance's registry, sorted by priority
        all_entries = [entry for entry in self.registry if entry.dimension == "file_operation_detector"]
        sorted_entries = sorted(all_entries, key=lambda e: e.metadata.get("priority", 0), reverse=True)
        detectors = [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]

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


# 🧱🏗️🔚
