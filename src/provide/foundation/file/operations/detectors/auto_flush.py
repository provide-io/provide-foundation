#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Auto-flush handler for streaming file operation detection.

Handles automatic flushing of pending events after a time window,
with temp file filtering and operation emission callbacks."""

from __future__ import annotations

import asyncio
from datetime import datetime
import threading
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from provide.foundation.file.operations.detectors.types import (  # type: ignore[import-untyped]
        FileEvent,
        FileOperation,
    )

from provide.foundation.file.operations.detectors.helpers import is_temp_file
from provide.foundation.file.operations.types import OperationType
from provide.foundation.logger import get_logger

log = get_logger(__name__)


class AutoFlushHandler:
    """Handles automatic flushing of pending events with temp file filtering.

    Thread-safe: Uses internal locking to protect shared state from concurrent access.
    Multiple threads can safely call add_event() simultaneously.
    """

    def __init__(
        self,
        time_window_ms: float,
        on_operation_complete: Any = None,
        analyze_func: Any = None,
    ) -> None:
        """Initialize auto-flush handler.

        Args:
            time_window_ms: Time window in milliseconds for event grouping
            on_operation_complete: Callback function(operation: FileOperation)
            analyze_func: Function to analyze event groups and detect operations
        """
        self.time_window_ms = time_window_ms
        self.on_operation_complete = on_operation_complete
        self.analyze_func = analyze_func
        self._pending_events: list[FileEvent] = []
        self._last_flush = datetime.now()
        self._flush_timer: Any = None  # asyncio.TimerHandle or threading.Timer
        self._lock = threading.RLock()  # Protect shared state from concurrent threads
        self._failed_operations: list[FileOperation] = []  # Queue for retry on callback failure
        self._no_loop_buffer: list[FileOperation] = []  # Buffer when no event loop available
        self._currently_retrying: set[int] = set()  # Track operations being retried to prevent infinite loops

    def add_event(self, event: FileEvent) -> None:
        """Add event and schedule auto-flush.

        Thread-safe: Uses internal locking for concurrent add_event() calls.

        Args:
            event: File event to buffer for processing
        """
        with self._lock:
            self._pending_events.append(event)

            # Check if this is a temp file
            is_temp = is_temp_file(event.path) or (event.dest_path and is_temp_file(event.dest_path))

            log.trace(
                "Event added to auto-flush buffer",
                path=str(event.path),
                dest_path=str(event.dest_path) if event.dest_path else None,
                is_temp=is_temp,
                pending_count=len(self._pending_events),
            )

            # Schedule auto-flush timer
            self._schedule_auto_flush()

    def schedule_flush(self) -> None:
        """Schedule auto-flush timer (public interface).

        Thread-safe: Uses internal locking.
        """
        with self._lock:
            self._schedule_auto_flush()

    def _schedule_auto_flush(self) -> None:
        """Schedule auto-flush timer.

        Uses asyncio timer if event loop is running, otherwise uses threading.Timer.
        This prevents creating event loops that are never closed.

        Note: Must be called with self._lock held.
        """
        # Cancel existing timer
        if self._flush_timer:
            if isinstance(self._flush_timer, threading.Timer):
                self._flush_timer.cancel()
            else:
                # asyncio.TimerHandle
                self._flush_timer.cancel()
            self._flush_timer = None

        # Try to schedule with asyncio first (if event loop is running)
        try:
            loop = asyncio.get_running_loop()
            # We're in an async context, use asyncio timer
            self._flush_timer = loop.call_later(self.time_window_ms / 1000.0, self._auto_flush)
            log.trace(
                "Auto-flush scheduled (asyncio)",
                window_ms=self.time_window_ms,
            )
        except RuntimeError:
            # No event loop running - use threading.Timer instead
            # This prevents creating unclosed event loops
            self._flush_timer = threading.Timer(self.time_window_ms / 1000.0, self._auto_flush)
            self._flush_timer.start()
            log.trace(
                "Auto-flush scheduled (threading)",
                window_ms=self.time_window_ms,
            )

    def _auto_flush(self) -> None:
        """Auto-flush callback - emits pending operations.

        Thread-safe: Uses internal locking to protect state during callback.
        """
        with self._lock:
            if not self._pending_events:
                return

            event_summary = [
                f"{e.event_type}:{e.path.name}" + (f"→{e.dest_path.name}" if e.dest_path else "")
                for e in self._pending_events
            ]

            log.info(
                "⏰ AUTO-FLUSH TRIGGERED",
                pending_events=len(self._pending_events),
                events=event_summary,
            )

            # Try to detect operation from pending events
            operation = None
            if self.analyze_func:
                operation = self.analyze_func(self._pending_events)

            if operation:
                self._handle_detected_operation(operation)
            else:
                self._handle_no_operation()

            self._pending_events.clear()
            self._last_flush = datetime.now()
            self._flush_timer = None

    def _emit_operation_safe(self, operation: FileOperation) -> bool:
        """Safely emit operation with error handling and recovery.

        Args:
            operation: Operation to emit

        Returns:
            True if emission succeeded, False otherwise
        """
        if not self.on_operation_complete:
            return True

        try:
            self.on_operation_complete(operation)
            return True
        except Exception as e:
            log.error(
                "Callback failed - queueing operation for retry",
                error=str(e),
                operation_type=operation.operation_type.value,
                primary_file=operation.primary_path.name,
            )
            # Queue for retry only if this operation is NOT currently being retried
            # (prevents infinite loop in retry_failed_operations)
            with self._lock:
                op_id = id(operation)
                if op_id not in self._currently_retrying:
                    self._failed_operations.append(operation)
            return False

    def _handle_detected_operation(self, operation: FileOperation) -> None:
        """Handle a detected operation with temp file filtering.

        Args:
            operation: Detected file operation
        """
        # Check if operation touches any real files
        has_real_file = any(
            not is_temp_file(event.path) or (event.dest_path and not is_temp_file(event.dest_path))
            for event in operation.events
        )

        if has_real_file:
            # Operation touches at least one real file - emit it
            log.info(
                operation_type=operation.operation_type.value,
                primary_file=operation.primary_path.name,
                event_count=len(operation.events),
            )
            self._emit_operation_safe(operation)
        else:
            # Pure temp file operation - hide it
            log.info(
                "🚫 TEMP-ONLY OPERATION - HIDING",
                operation_type=operation.operation_type.value,
                primary_file=operation.primary_path.name,
                event_count=len(operation.events),
            )

        # Check for remaining events not included in the detected operation
        operation_event_ids = {id(event) for event in operation.events}
        remaining_events = [event for event in self._pending_events if id(event) not in operation_event_ids]

        if remaining_events:
            log.debug(
                "Emitting remaining events not included in detected operation",
                remaining_count=len(remaining_events),
            )
            self._emit_individual_events(remaining_events)

    def _handle_no_operation(self) -> None:
        """Handle case where no operation was detected."""
        log.info(
            "❓ NO OPERATION DETECTED - Filtering individual events",
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
                log.info(
                    "  🚫 Hiding temp-only event",
                    file=event.path.name,
                    event_type=event.event_type,
                )
                hidden_count += 1
            else:
                # Event touches a real file - emit it
                log.info(
                    file=event.path.name,
                    event_type=event.event_type,
                )
                single_op = self._create_single_event_operation(event)
                if self._emit_operation_safe(single_op):
                    emitted_count += 1

        log.info(
            "Auto-flush complete",
            emitted=emitted_count,
            hidden=hidden_count,
        )

    def _emit_individual_events(self, events: list[FileEvent]) -> None:
        """Emit individual events with temp filtering.

        Args:
            events: Events to emit individually
        """
        for event in events:
            is_temp_source = is_temp_file(event.path)
            is_temp_dest = event.dest_path and is_temp_file(event.dest_path)

            if not (is_temp_source and (not event.dest_path or is_temp_dest)):
                # Event touches a real file - emit it
                single_op = self._create_single_event_operation(event)
                self._emit_operation_safe(single_op)

    def _create_single_event_operation(self, event: FileEvent) -> FileOperation:
        """Create a FileOperation from a single event.

        Args:
            event: File event to wrap

        Returns:
            FileOperation representing the single event
        """
        from provide.foundation.file.operations.types import FileOperation

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

    @property
    def pending_events(self) -> list[FileEvent]:
        """Get pending events (read-only access).

        Thread-safe: Returns a copy to prevent external modification.
        """
        with self._lock:
            return self._pending_events.copy()

    def clear(self) -> None:
        """Clear pending events and cancel timer.

        Thread-safe: Uses internal locking.
        """
        with self._lock:
            self._pending_events.clear()
            if self._flush_timer:
                if isinstance(self._flush_timer, threading.Timer):
                    self._flush_timer.cancel()
                else:
                    # asyncio.TimerHandle
                    self._flush_timer.cancel()
                self._flush_timer = None

    def retry_failed_operations(self) -> int:
        """Retry failed operations.

        Thread-safe: Uses internal locking.

        Returns:
            Number of operations successfully retried
        """
        with self._lock:
            if not self._failed_operations:
                return 0

            retry_count = 0
            remaining = []

            # Mark all operations as being retried to prevent infinite loop
            for operation in self._failed_operations:
                self._currently_retrying.add(id(operation))

            try:
                for operation in self._failed_operations:
                    if self._emit_operation_safe(operation):
                        retry_count += 1
                        log.info(
                            "Retry successful",
                            operation_type=operation.operation_type.value,
                            primary_file=operation.primary_path.name,
                        )
                    else:
                        # Still failing, keep for next retry
                        remaining.append(operation)

                self._failed_operations = remaining

                if retry_count > 0:
                    log.info(f"Retried {retry_count} failed operations, {len(remaining)} still pending")

                return retry_count
            finally:
                # Clear retry tracking
                self._currently_retrying.clear()

    @property
    def failed_operations_count(self) -> int:
        """Get count of failed operations awaiting retry.

        Thread-safe: Uses internal locking.
        """
        with self._lock:
            return len(self._failed_operations)

    def get_failed_operations(self) -> list[FileOperation]:
        """Get copy of failed operations list for inspection.

        Thread-safe: Returns a copy.
        """
        with self._lock:
            return self._failed_operations.copy()

    def clear_failed_operations(self) -> int:
        """Clear all failed operations (data loss - use carefully).

        Thread-safe: Uses internal locking.

        Returns:
            Number of operations that were cleared
        """
        with self._lock:
            count = len(self._failed_operations)
            self._failed_operations.clear()
            if count > 0:
                log.warning(f"Cleared {count} failed operations - data loss!")
            return count


# 🧱🏗️🔚
