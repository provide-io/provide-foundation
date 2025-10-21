# provide/foundation/file/operations/detectors/auto_flush.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Auto-flush handler for streaming file operation detection.

Handles automatic flushing of pending events after a time window,
with temp file filtering and operation emission callbacks.
"""

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class AutoFlushHandler:
    """Handles automatic flushing of pending events with temp file filtering.

    Thread-safe: Uses internal locking to protect shared state from concurrent access.
    Multiple threads can safely call add_event() simultaneously.
    """

    def xǁAutoFlushHandlerǁ__init____mutmut_orig(
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

    def xǁAutoFlushHandlerǁ__init____mutmut_1(
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
        self.time_window_ms = None
        self.on_operation_complete = on_operation_complete
        self.analyze_func = analyze_func
        self._pending_events: list[FileEvent] = []
        self._last_flush = datetime.now()
        self._flush_timer: Any = None  # asyncio.TimerHandle or threading.Timer
        self._lock = threading.RLock()  # Protect shared state from concurrent threads
        self._failed_operations: list[FileOperation] = []  # Queue for retry on callback failure
        self._no_loop_buffer: list[FileOperation] = []  # Buffer when no event loop available
        self._currently_retrying: set[int] = set()  # Track operations being retried to prevent infinite loops

    def xǁAutoFlushHandlerǁ__init____mutmut_2(
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
        self.on_operation_complete = None
        self.analyze_func = analyze_func
        self._pending_events: list[FileEvent] = []
        self._last_flush = datetime.now()
        self._flush_timer: Any = None  # asyncio.TimerHandle or threading.Timer
        self._lock = threading.RLock()  # Protect shared state from concurrent threads
        self._failed_operations: list[FileOperation] = []  # Queue for retry on callback failure
        self._no_loop_buffer: list[FileOperation] = []  # Buffer when no event loop available
        self._currently_retrying: set[int] = set()  # Track operations being retried to prevent infinite loops

    def xǁAutoFlushHandlerǁ__init____mutmut_3(
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
        self.analyze_func = None
        self._pending_events: list[FileEvent] = []
        self._last_flush = datetime.now()
        self._flush_timer: Any = None  # asyncio.TimerHandle or threading.Timer
        self._lock = threading.RLock()  # Protect shared state from concurrent threads
        self._failed_operations: list[FileOperation] = []  # Queue for retry on callback failure
        self._no_loop_buffer: list[FileOperation] = []  # Buffer when no event loop available
        self._currently_retrying: set[int] = set()  # Track operations being retried to prevent infinite loops

    def xǁAutoFlushHandlerǁ__init____mutmut_4(
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
        self._pending_events: list[FileEvent] = None
        self._last_flush = datetime.now()
        self._flush_timer: Any = None  # asyncio.TimerHandle or threading.Timer
        self._lock = threading.RLock()  # Protect shared state from concurrent threads
        self._failed_operations: list[FileOperation] = []  # Queue for retry on callback failure
        self._no_loop_buffer: list[FileOperation] = []  # Buffer when no event loop available
        self._currently_retrying: set[int] = set()  # Track operations being retried to prevent infinite loops

    def xǁAutoFlushHandlerǁ__init____mutmut_5(
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
        self._last_flush = None
        self._flush_timer: Any = None  # asyncio.TimerHandle or threading.Timer
        self._lock = threading.RLock()  # Protect shared state from concurrent threads
        self._failed_operations: list[FileOperation] = []  # Queue for retry on callback failure
        self._no_loop_buffer: list[FileOperation] = []  # Buffer when no event loop available
        self._currently_retrying: set[int] = set()  # Track operations being retried to prevent infinite loops

    def xǁAutoFlushHandlerǁ__init____mutmut_6(
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
        self._flush_timer: Any = ""  # asyncio.TimerHandle or threading.Timer
        self._lock = threading.RLock()  # Protect shared state from concurrent threads
        self._failed_operations: list[FileOperation] = []  # Queue for retry on callback failure
        self._no_loop_buffer: list[FileOperation] = []  # Buffer when no event loop available
        self._currently_retrying: set[int] = set()  # Track operations being retried to prevent infinite loops

    def xǁAutoFlushHandlerǁ__init____mutmut_7(
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
        self._lock = None  # Protect shared state from concurrent threads
        self._failed_operations: list[FileOperation] = []  # Queue for retry on callback failure
        self._no_loop_buffer: list[FileOperation] = []  # Buffer when no event loop available
        self._currently_retrying: set[int] = set()  # Track operations being retried to prevent infinite loops

    def xǁAutoFlushHandlerǁ__init____mutmut_8(
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
        self._failed_operations: list[FileOperation] = None  # Queue for retry on callback failure
        self._no_loop_buffer: list[FileOperation] = []  # Buffer when no event loop available
        self._currently_retrying: set[int] = set()  # Track operations being retried to prevent infinite loops

    def xǁAutoFlushHandlerǁ__init____mutmut_9(
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
        self._no_loop_buffer: list[FileOperation] = None  # Buffer when no event loop available
        self._currently_retrying: set[int] = set()  # Track operations being retried to prevent infinite loops

    def xǁAutoFlushHandlerǁ__init____mutmut_10(
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
        self._currently_retrying: set[int] = None  # Track operations being retried to prevent infinite loops
    
    xǁAutoFlushHandlerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAutoFlushHandlerǁ__init____mutmut_1': xǁAutoFlushHandlerǁ__init____mutmut_1, 
        'xǁAutoFlushHandlerǁ__init____mutmut_2': xǁAutoFlushHandlerǁ__init____mutmut_2, 
        'xǁAutoFlushHandlerǁ__init____mutmut_3': xǁAutoFlushHandlerǁ__init____mutmut_3, 
        'xǁAutoFlushHandlerǁ__init____mutmut_4': xǁAutoFlushHandlerǁ__init____mutmut_4, 
        'xǁAutoFlushHandlerǁ__init____mutmut_5': xǁAutoFlushHandlerǁ__init____mutmut_5, 
        'xǁAutoFlushHandlerǁ__init____mutmut_6': xǁAutoFlushHandlerǁ__init____mutmut_6, 
        'xǁAutoFlushHandlerǁ__init____mutmut_7': xǁAutoFlushHandlerǁ__init____mutmut_7, 
        'xǁAutoFlushHandlerǁ__init____mutmut_8': xǁAutoFlushHandlerǁ__init____mutmut_8, 
        'xǁAutoFlushHandlerǁ__init____mutmut_9': xǁAutoFlushHandlerǁ__init____mutmut_9, 
        'xǁAutoFlushHandlerǁ__init____mutmut_10': xǁAutoFlushHandlerǁ__init____mutmut_10
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAutoFlushHandlerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁAutoFlushHandlerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁAutoFlushHandlerǁ__init____mutmut_orig)
    xǁAutoFlushHandlerǁ__init____mutmut_orig.__name__ = 'xǁAutoFlushHandlerǁ__init__'

    def xǁAutoFlushHandlerǁadd_event__mutmut_orig(self, event: FileEvent) -> None:
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

    def xǁAutoFlushHandlerǁadd_event__mutmut_1(self, event: FileEvent) -> None:
        """Add event and schedule auto-flush.

        Thread-safe: Uses internal locking for concurrent add_event() calls.

        Args:
            event: File event to buffer for processing
        """
        with self._lock:
            self._pending_events.append(None)

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

    def xǁAutoFlushHandlerǁadd_event__mutmut_2(self, event: FileEvent) -> None:
        """Add event and schedule auto-flush.

        Thread-safe: Uses internal locking for concurrent add_event() calls.

        Args:
            event: File event to buffer for processing
        """
        with self._lock:
            self._pending_events.append(event)

            # Check if this is a temp file
            is_temp = None

            log.trace(
                "Event added to auto-flush buffer",
                path=str(event.path),
                dest_path=str(event.dest_path) if event.dest_path else None,
                is_temp=is_temp,
                pending_count=len(self._pending_events),
            )

            # Schedule auto-flush timer
            self._schedule_auto_flush()

    def xǁAutoFlushHandlerǁadd_event__mutmut_3(self, event: FileEvent) -> None:
        """Add event and schedule auto-flush.

        Thread-safe: Uses internal locking for concurrent add_event() calls.

        Args:
            event: File event to buffer for processing
        """
        with self._lock:
            self._pending_events.append(event)

            # Check if this is a temp file
            is_temp = is_temp_file(event.path) and (event.dest_path and is_temp_file(event.dest_path))

            log.trace(
                "Event added to auto-flush buffer",
                path=str(event.path),
                dest_path=str(event.dest_path) if event.dest_path else None,
                is_temp=is_temp,
                pending_count=len(self._pending_events),
            )

            # Schedule auto-flush timer
            self._schedule_auto_flush()

    def xǁAutoFlushHandlerǁadd_event__mutmut_4(self, event: FileEvent) -> None:
        """Add event and schedule auto-flush.

        Thread-safe: Uses internal locking for concurrent add_event() calls.

        Args:
            event: File event to buffer for processing
        """
        with self._lock:
            self._pending_events.append(event)

            # Check if this is a temp file
            is_temp = is_temp_file(None) or (event.dest_path and is_temp_file(event.dest_path))

            log.trace(
                "Event added to auto-flush buffer",
                path=str(event.path),
                dest_path=str(event.dest_path) if event.dest_path else None,
                is_temp=is_temp,
                pending_count=len(self._pending_events),
            )

            # Schedule auto-flush timer
            self._schedule_auto_flush()

    def xǁAutoFlushHandlerǁadd_event__mutmut_5(self, event: FileEvent) -> None:
        """Add event and schedule auto-flush.

        Thread-safe: Uses internal locking for concurrent add_event() calls.

        Args:
            event: File event to buffer for processing
        """
        with self._lock:
            self._pending_events.append(event)

            # Check if this is a temp file
            is_temp = is_temp_file(event.path) or (event.dest_path or is_temp_file(event.dest_path))

            log.trace(
                "Event added to auto-flush buffer",
                path=str(event.path),
                dest_path=str(event.dest_path) if event.dest_path else None,
                is_temp=is_temp,
                pending_count=len(self._pending_events),
            )

            # Schedule auto-flush timer
            self._schedule_auto_flush()

    def xǁAutoFlushHandlerǁadd_event__mutmut_6(self, event: FileEvent) -> None:
        """Add event and schedule auto-flush.

        Thread-safe: Uses internal locking for concurrent add_event() calls.

        Args:
            event: File event to buffer for processing
        """
        with self._lock:
            self._pending_events.append(event)

            # Check if this is a temp file
            is_temp = is_temp_file(event.path) or (event.dest_path and is_temp_file(None))

            log.trace(
                "Event added to auto-flush buffer",
                path=str(event.path),
                dest_path=str(event.dest_path) if event.dest_path else None,
                is_temp=is_temp,
                pending_count=len(self._pending_events),
            )

            # Schedule auto-flush timer
            self._schedule_auto_flush()

    def xǁAutoFlushHandlerǁadd_event__mutmut_7(self, event: FileEvent) -> None:
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
                None,
                path=str(event.path),
                dest_path=str(event.dest_path) if event.dest_path else None,
                is_temp=is_temp,
                pending_count=len(self._pending_events),
            )

            # Schedule auto-flush timer
            self._schedule_auto_flush()

    def xǁAutoFlushHandlerǁadd_event__mutmut_8(self, event: FileEvent) -> None:
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
                path=None,
                dest_path=str(event.dest_path) if event.dest_path else None,
                is_temp=is_temp,
                pending_count=len(self._pending_events),
            )

            # Schedule auto-flush timer
            self._schedule_auto_flush()

    def xǁAutoFlushHandlerǁadd_event__mutmut_9(self, event: FileEvent) -> None:
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
                dest_path=None,
                is_temp=is_temp,
                pending_count=len(self._pending_events),
            )

            # Schedule auto-flush timer
            self._schedule_auto_flush()

    def xǁAutoFlushHandlerǁadd_event__mutmut_10(self, event: FileEvent) -> None:
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
                is_temp=None,
                pending_count=len(self._pending_events),
            )

            # Schedule auto-flush timer
            self._schedule_auto_flush()

    def xǁAutoFlushHandlerǁadd_event__mutmut_11(self, event: FileEvent) -> None:
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
                pending_count=None,
            )

            # Schedule auto-flush timer
            self._schedule_auto_flush()

    def xǁAutoFlushHandlerǁadd_event__mutmut_12(self, event: FileEvent) -> None:
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
                path=str(event.path),
                dest_path=str(event.dest_path) if event.dest_path else None,
                is_temp=is_temp,
                pending_count=len(self._pending_events),
            )

            # Schedule auto-flush timer
            self._schedule_auto_flush()

    def xǁAutoFlushHandlerǁadd_event__mutmut_13(self, event: FileEvent) -> None:
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
                dest_path=str(event.dest_path) if event.dest_path else None,
                is_temp=is_temp,
                pending_count=len(self._pending_events),
            )

            # Schedule auto-flush timer
            self._schedule_auto_flush()

    def xǁAutoFlushHandlerǁadd_event__mutmut_14(self, event: FileEvent) -> None:
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
                is_temp=is_temp,
                pending_count=len(self._pending_events),
            )

            # Schedule auto-flush timer
            self._schedule_auto_flush()

    def xǁAutoFlushHandlerǁadd_event__mutmut_15(self, event: FileEvent) -> None:
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
                pending_count=len(self._pending_events),
            )

            # Schedule auto-flush timer
            self._schedule_auto_flush()

    def xǁAutoFlushHandlerǁadd_event__mutmut_16(self, event: FileEvent) -> None:
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
                )

            # Schedule auto-flush timer
            self._schedule_auto_flush()

    def xǁAutoFlushHandlerǁadd_event__mutmut_17(self, event: FileEvent) -> None:
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
                "XXEvent added to auto-flush bufferXX",
                path=str(event.path),
                dest_path=str(event.dest_path) if event.dest_path else None,
                is_temp=is_temp,
                pending_count=len(self._pending_events),
            )

            # Schedule auto-flush timer
            self._schedule_auto_flush()

    def xǁAutoFlushHandlerǁadd_event__mutmut_18(self, event: FileEvent) -> None:
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
                "event added to auto-flush buffer",
                path=str(event.path),
                dest_path=str(event.dest_path) if event.dest_path else None,
                is_temp=is_temp,
                pending_count=len(self._pending_events),
            )

            # Schedule auto-flush timer
            self._schedule_auto_flush()

    def xǁAutoFlushHandlerǁadd_event__mutmut_19(self, event: FileEvent) -> None:
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
                "EVENT ADDED TO AUTO-FLUSH BUFFER",
                path=str(event.path),
                dest_path=str(event.dest_path) if event.dest_path else None,
                is_temp=is_temp,
                pending_count=len(self._pending_events),
            )

            # Schedule auto-flush timer
            self._schedule_auto_flush()

    def xǁAutoFlushHandlerǁadd_event__mutmut_20(self, event: FileEvent) -> None:
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
                path=str(None),
                dest_path=str(event.dest_path) if event.dest_path else None,
                is_temp=is_temp,
                pending_count=len(self._pending_events),
            )

            # Schedule auto-flush timer
            self._schedule_auto_flush()

    def xǁAutoFlushHandlerǁadd_event__mutmut_21(self, event: FileEvent) -> None:
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
                dest_path=str(None) if event.dest_path else None,
                is_temp=is_temp,
                pending_count=len(self._pending_events),
            )

            # Schedule auto-flush timer
            self._schedule_auto_flush()
    
    xǁAutoFlushHandlerǁadd_event__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAutoFlushHandlerǁadd_event__mutmut_1': xǁAutoFlushHandlerǁadd_event__mutmut_1, 
        'xǁAutoFlushHandlerǁadd_event__mutmut_2': xǁAutoFlushHandlerǁadd_event__mutmut_2, 
        'xǁAutoFlushHandlerǁadd_event__mutmut_3': xǁAutoFlushHandlerǁadd_event__mutmut_3, 
        'xǁAutoFlushHandlerǁadd_event__mutmut_4': xǁAutoFlushHandlerǁadd_event__mutmut_4, 
        'xǁAutoFlushHandlerǁadd_event__mutmut_5': xǁAutoFlushHandlerǁadd_event__mutmut_5, 
        'xǁAutoFlushHandlerǁadd_event__mutmut_6': xǁAutoFlushHandlerǁadd_event__mutmut_6, 
        'xǁAutoFlushHandlerǁadd_event__mutmut_7': xǁAutoFlushHandlerǁadd_event__mutmut_7, 
        'xǁAutoFlushHandlerǁadd_event__mutmut_8': xǁAutoFlushHandlerǁadd_event__mutmut_8, 
        'xǁAutoFlushHandlerǁadd_event__mutmut_9': xǁAutoFlushHandlerǁadd_event__mutmut_9, 
        'xǁAutoFlushHandlerǁadd_event__mutmut_10': xǁAutoFlushHandlerǁadd_event__mutmut_10, 
        'xǁAutoFlushHandlerǁadd_event__mutmut_11': xǁAutoFlushHandlerǁadd_event__mutmut_11, 
        'xǁAutoFlushHandlerǁadd_event__mutmut_12': xǁAutoFlushHandlerǁadd_event__mutmut_12, 
        'xǁAutoFlushHandlerǁadd_event__mutmut_13': xǁAutoFlushHandlerǁadd_event__mutmut_13, 
        'xǁAutoFlushHandlerǁadd_event__mutmut_14': xǁAutoFlushHandlerǁadd_event__mutmut_14, 
        'xǁAutoFlushHandlerǁadd_event__mutmut_15': xǁAutoFlushHandlerǁadd_event__mutmut_15, 
        'xǁAutoFlushHandlerǁadd_event__mutmut_16': xǁAutoFlushHandlerǁadd_event__mutmut_16, 
        'xǁAutoFlushHandlerǁadd_event__mutmut_17': xǁAutoFlushHandlerǁadd_event__mutmut_17, 
        'xǁAutoFlushHandlerǁadd_event__mutmut_18': xǁAutoFlushHandlerǁadd_event__mutmut_18, 
        'xǁAutoFlushHandlerǁadd_event__mutmut_19': xǁAutoFlushHandlerǁadd_event__mutmut_19, 
        'xǁAutoFlushHandlerǁadd_event__mutmut_20': xǁAutoFlushHandlerǁadd_event__mutmut_20, 
        'xǁAutoFlushHandlerǁadd_event__mutmut_21': xǁAutoFlushHandlerǁadd_event__mutmut_21
    }
    
    def add_event(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAutoFlushHandlerǁadd_event__mutmut_orig"), object.__getattribute__(self, "xǁAutoFlushHandlerǁadd_event__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_event.__signature__ = _mutmut_signature(xǁAutoFlushHandlerǁadd_event__mutmut_orig)
    xǁAutoFlushHandlerǁadd_event__mutmut_orig.__name__ = 'xǁAutoFlushHandlerǁadd_event'

    def schedule_flush(self) -> None:
        """Schedule auto-flush timer (public interface).

        Thread-safe: Uses internal locking.
        """
        with self._lock:
            self._schedule_auto_flush()

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_orig(self) -> None:
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

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_1(self) -> None:
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
            self._flush_timer = ""

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

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_2(self) -> None:
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
            loop = None
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

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_3(self) -> None:
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
            self._flush_timer = None
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

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_4(self) -> None:
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
            self._flush_timer = loop.call_later(None, self._auto_flush)
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

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_5(self) -> None:
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
            self._flush_timer = loop.call_later(self.time_window_ms / 1000.0, None)
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

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_6(self) -> None:
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
            self._flush_timer = loop.call_later(self._auto_flush)
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

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_7(self) -> None:
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
            self._flush_timer = loop.call_later(self.time_window_ms / 1000.0, )
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

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_8(self) -> None:
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
            self._flush_timer = loop.call_later(self.time_window_ms * 1000.0, self._auto_flush)
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

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_9(self) -> None:
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
            self._flush_timer = loop.call_later(self.time_window_ms / 1001.0, self._auto_flush)
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

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_10(self) -> None:
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
                None,
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

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_11(self) -> None:
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
                window_ms=None,
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

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_12(self) -> None:
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

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_13(self) -> None:
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

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_14(self) -> None:
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
                "XXAuto-flush scheduled (asyncio)XX",
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

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_15(self) -> None:
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
                "auto-flush scheduled (asyncio)",
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

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_16(self) -> None:
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
                "AUTO-FLUSH SCHEDULED (ASYNCIO)",
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

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_17(self) -> None:
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
            self._flush_timer = None
            self._flush_timer.start()
            log.trace(
                "Auto-flush scheduled (threading)",
                window_ms=self.time_window_ms,
            )

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_18(self) -> None:
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
            self._flush_timer = threading.Timer(None, self._auto_flush)
            self._flush_timer.start()
            log.trace(
                "Auto-flush scheduled (threading)",
                window_ms=self.time_window_ms,
            )

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_19(self) -> None:
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
            self._flush_timer = threading.Timer(self.time_window_ms / 1000.0, None)
            self._flush_timer.start()
            log.trace(
                "Auto-flush scheduled (threading)",
                window_ms=self.time_window_ms,
            )

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_20(self) -> None:
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
            self._flush_timer = threading.Timer(self._auto_flush)
            self._flush_timer.start()
            log.trace(
                "Auto-flush scheduled (threading)",
                window_ms=self.time_window_ms,
            )

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_21(self) -> None:
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
            self._flush_timer = threading.Timer(self.time_window_ms / 1000.0, )
            self._flush_timer.start()
            log.trace(
                "Auto-flush scheduled (threading)",
                window_ms=self.time_window_ms,
            )

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_22(self) -> None:
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
            self._flush_timer = threading.Timer(self.time_window_ms * 1000.0, self._auto_flush)
            self._flush_timer.start()
            log.trace(
                "Auto-flush scheduled (threading)",
                window_ms=self.time_window_ms,
            )

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_23(self) -> None:
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
            self._flush_timer = threading.Timer(self.time_window_ms / 1001.0, self._auto_flush)
            self._flush_timer.start()
            log.trace(
                "Auto-flush scheduled (threading)",
                window_ms=self.time_window_ms,
            )

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_24(self) -> None:
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
                None,
                window_ms=self.time_window_ms,
            )

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_25(self) -> None:
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
                window_ms=None,
            )

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_26(self) -> None:
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
                window_ms=self.time_window_ms,
            )

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_27(self) -> None:
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
                )

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_28(self) -> None:
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
                "XXAuto-flush scheduled (threading)XX",
                window_ms=self.time_window_ms,
            )

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_29(self) -> None:
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
                "auto-flush scheduled (threading)",
                window_ms=self.time_window_ms,
            )

    def xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_30(self) -> None:
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
                "AUTO-FLUSH SCHEDULED (THREADING)",
                window_ms=self.time_window_ms,
            )
    
    xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_1': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_1, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_2': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_2, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_3': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_3, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_4': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_4, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_5': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_5, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_6': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_6, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_7': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_7, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_8': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_8, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_9': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_9, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_10': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_10, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_11': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_11, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_12': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_12, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_13': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_13, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_14': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_14, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_15': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_15, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_16': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_16, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_17': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_17, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_18': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_18, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_19': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_19, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_20': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_20, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_21': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_21, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_22': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_22, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_23': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_23, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_24': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_24, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_25': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_25, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_26': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_26, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_27': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_27, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_28': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_28, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_29': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_29, 
        'xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_30': xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_30
    }
    
    def _schedule_auto_flush(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_orig"), object.__getattribute__(self, "xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _schedule_auto_flush.__signature__ = _mutmut_signature(xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_orig)
    xǁAutoFlushHandlerǁ_schedule_auto_flush__mutmut_orig.__name__ = 'xǁAutoFlushHandlerǁ_schedule_auto_flush'

    def xǁAutoFlushHandlerǁ_auto_flush__mutmut_orig(self) -> None:
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

    def xǁAutoFlushHandlerǁ_auto_flush__mutmut_1(self) -> None:
        """Auto-flush callback - emits pending operations.

        Thread-safe: Uses internal locking to protect state during callback.
        """
        with self._lock:
            if self._pending_events:
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

    def xǁAutoFlushHandlerǁ_auto_flush__mutmut_2(self) -> None:
        """Auto-flush callback - emits pending operations.

        Thread-safe: Uses internal locking to protect state during callback.
        """
        with self._lock:
            if not self._pending_events:
                return

            event_summary = None

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

    def xǁAutoFlushHandlerǁ_auto_flush__mutmut_3(self) -> None:
        """Auto-flush callback - emits pending operations.

        Thread-safe: Uses internal locking to protect state during callback.
        """
        with self._lock:
            if not self._pending_events:
                return

            event_summary = [
                f"{e.event_type}:{e.path.name}" - (f"→{e.dest_path.name}" if e.dest_path else "")
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

    def xǁAutoFlushHandlerǁ_auto_flush__mutmut_4(self) -> None:
        """Auto-flush callback - emits pending operations.

        Thread-safe: Uses internal locking to protect state during callback.
        """
        with self._lock:
            if not self._pending_events:
                return

            event_summary = [
                f"{e.event_type}:{e.path.name}" + (f"→{e.dest_path.name}" if e.dest_path else "XXXX")
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

    def xǁAutoFlushHandlerǁ_auto_flush__mutmut_5(self) -> None:
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
                None,
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

    def xǁAutoFlushHandlerǁ_auto_flush__mutmut_6(self) -> None:
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
                pending_events=None,
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

    def xǁAutoFlushHandlerǁ_auto_flush__mutmut_7(self) -> None:
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
                events=None,
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

    def xǁAutoFlushHandlerǁ_auto_flush__mutmut_8(self) -> None:
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

    def xǁAutoFlushHandlerǁ_auto_flush__mutmut_9(self) -> None:
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

    def xǁAutoFlushHandlerǁ_auto_flush__mutmut_10(self) -> None:
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

    def xǁAutoFlushHandlerǁ_auto_flush__mutmut_11(self) -> None:
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
                "XX⏰ AUTO-FLUSH TRIGGEREDXX",
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

    def xǁAutoFlushHandlerǁ_auto_flush__mutmut_12(self) -> None:
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
                "⏰ auto-flush triggered",
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

    def xǁAutoFlushHandlerǁ_auto_flush__mutmut_13(self) -> None:
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
            operation = ""
            if self.analyze_func:
                operation = self.analyze_func(self._pending_events)

            if operation:
                self._handle_detected_operation(operation)
            else:
                self._handle_no_operation()

            self._pending_events.clear()
            self._last_flush = datetime.now()
            self._flush_timer = None

    def xǁAutoFlushHandlerǁ_auto_flush__mutmut_14(self) -> None:
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
                operation = None

            if operation:
                self._handle_detected_operation(operation)
            else:
                self._handle_no_operation()

            self._pending_events.clear()
            self._last_flush = datetime.now()
            self._flush_timer = None

    def xǁAutoFlushHandlerǁ_auto_flush__mutmut_15(self) -> None:
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
                operation = self.analyze_func(None)

            if operation:
                self._handle_detected_operation(operation)
            else:
                self._handle_no_operation()

            self._pending_events.clear()
            self._last_flush = datetime.now()
            self._flush_timer = None

    def xǁAutoFlushHandlerǁ_auto_flush__mutmut_16(self) -> None:
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
                self._handle_detected_operation(None)
            else:
                self._handle_no_operation()

            self._pending_events.clear()
            self._last_flush = datetime.now()
            self._flush_timer = None

    def xǁAutoFlushHandlerǁ_auto_flush__mutmut_17(self) -> None:
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
            self._last_flush = None
            self._flush_timer = None

    def xǁAutoFlushHandlerǁ_auto_flush__mutmut_18(self) -> None:
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
            self._flush_timer = ""
    
    xǁAutoFlushHandlerǁ_auto_flush__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAutoFlushHandlerǁ_auto_flush__mutmut_1': xǁAutoFlushHandlerǁ_auto_flush__mutmut_1, 
        'xǁAutoFlushHandlerǁ_auto_flush__mutmut_2': xǁAutoFlushHandlerǁ_auto_flush__mutmut_2, 
        'xǁAutoFlushHandlerǁ_auto_flush__mutmut_3': xǁAutoFlushHandlerǁ_auto_flush__mutmut_3, 
        'xǁAutoFlushHandlerǁ_auto_flush__mutmut_4': xǁAutoFlushHandlerǁ_auto_flush__mutmut_4, 
        'xǁAutoFlushHandlerǁ_auto_flush__mutmut_5': xǁAutoFlushHandlerǁ_auto_flush__mutmut_5, 
        'xǁAutoFlushHandlerǁ_auto_flush__mutmut_6': xǁAutoFlushHandlerǁ_auto_flush__mutmut_6, 
        'xǁAutoFlushHandlerǁ_auto_flush__mutmut_7': xǁAutoFlushHandlerǁ_auto_flush__mutmut_7, 
        'xǁAutoFlushHandlerǁ_auto_flush__mutmut_8': xǁAutoFlushHandlerǁ_auto_flush__mutmut_8, 
        'xǁAutoFlushHandlerǁ_auto_flush__mutmut_9': xǁAutoFlushHandlerǁ_auto_flush__mutmut_9, 
        'xǁAutoFlushHandlerǁ_auto_flush__mutmut_10': xǁAutoFlushHandlerǁ_auto_flush__mutmut_10, 
        'xǁAutoFlushHandlerǁ_auto_flush__mutmut_11': xǁAutoFlushHandlerǁ_auto_flush__mutmut_11, 
        'xǁAutoFlushHandlerǁ_auto_flush__mutmut_12': xǁAutoFlushHandlerǁ_auto_flush__mutmut_12, 
        'xǁAutoFlushHandlerǁ_auto_flush__mutmut_13': xǁAutoFlushHandlerǁ_auto_flush__mutmut_13, 
        'xǁAutoFlushHandlerǁ_auto_flush__mutmut_14': xǁAutoFlushHandlerǁ_auto_flush__mutmut_14, 
        'xǁAutoFlushHandlerǁ_auto_flush__mutmut_15': xǁAutoFlushHandlerǁ_auto_flush__mutmut_15, 
        'xǁAutoFlushHandlerǁ_auto_flush__mutmut_16': xǁAutoFlushHandlerǁ_auto_flush__mutmut_16, 
        'xǁAutoFlushHandlerǁ_auto_flush__mutmut_17': xǁAutoFlushHandlerǁ_auto_flush__mutmut_17, 
        'xǁAutoFlushHandlerǁ_auto_flush__mutmut_18': xǁAutoFlushHandlerǁ_auto_flush__mutmut_18
    }
    
    def _auto_flush(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAutoFlushHandlerǁ_auto_flush__mutmut_orig"), object.__getattribute__(self, "xǁAutoFlushHandlerǁ_auto_flush__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _auto_flush.__signature__ = _mutmut_signature(xǁAutoFlushHandlerǁ_auto_flush__mutmut_orig)
    xǁAutoFlushHandlerǁ_auto_flush__mutmut_orig.__name__ = 'xǁAutoFlushHandlerǁ_auto_flush'

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_orig(self, operation: FileOperation) -> bool:
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

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_1(self, operation: FileOperation) -> bool:
        """Safely emit operation with error handling and recovery.

        Args:
            operation: Operation to emit

        Returns:
            True if emission succeeded, False otherwise
        """
        if self.on_operation_complete:
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

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_2(self, operation: FileOperation) -> bool:
        """Safely emit operation with error handling and recovery.

        Args:
            operation: Operation to emit

        Returns:
            True if emission succeeded, False otherwise
        """
        if not self.on_operation_complete:
            return False

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

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_3(self, operation: FileOperation) -> bool:
        """Safely emit operation with error handling and recovery.

        Args:
            operation: Operation to emit

        Returns:
            True if emission succeeded, False otherwise
        """
        if not self.on_operation_complete:
            return True

        try:
            self.on_operation_complete(None)
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

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_4(self, operation: FileOperation) -> bool:
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
            return False
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

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_5(self, operation: FileOperation) -> bool:
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
                None,
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

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_6(self, operation: FileOperation) -> bool:
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
                error=None,
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

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_7(self, operation: FileOperation) -> bool:
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
                operation_type=None,
                primary_file=operation.primary_path.name,
            )
            # Queue for retry only if this operation is NOT currently being retried
            # (prevents infinite loop in retry_failed_operations)
            with self._lock:
                op_id = id(operation)
                if op_id not in self._currently_retrying:
                    self._failed_operations.append(operation)
            return False

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_8(self, operation: FileOperation) -> bool:
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
                primary_file=None,
            )
            # Queue for retry only if this operation is NOT currently being retried
            # (prevents infinite loop in retry_failed_operations)
            with self._lock:
                op_id = id(operation)
                if op_id not in self._currently_retrying:
                    self._failed_operations.append(operation)
            return False

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_9(self, operation: FileOperation) -> bool:
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

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_10(self, operation: FileOperation) -> bool:
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

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_11(self, operation: FileOperation) -> bool:
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
                primary_file=operation.primary_path.name,
            )
            # Queue for retry only if this operation is NOT currently being retried
            # (prevents infinite loop in retry_failed_operations)
            with self._lock:
                op_id = id(operation)
                if op_id not in self._currently_retrying:
                    self._failed_operations.append(operation)
            return False

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_12(self, operation: FileOperation) -> bool:
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
                )
            # Queue for retry only if this operation is NOT currently being retried
            # (prevents infinite loop in retry_failed_operations)
            with self._lock:
                op_id = id(operation)
                if op_id not in self._currently_retrying:
                    self._failed_operations.append(operation)
            return False

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_13(self, operation: FileOperation) -> bool:
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
                "XXCallback failed - queueing operation for retryXX",
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

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_14(self, operation: FileOperation) -> bool:
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
                "callback failed - queueing operation for retry",
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

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_15(self, operation: FileOperation) -> bool:
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
                "CALLBACK FAILED - QUEUEING OPERATION FOR RETRY",
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

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_16(self, operation: FileOperation) -> bool:
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
                error=str(None),
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

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_17(self, operation: FileOperation) -> bool:
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
                op_id = None
                if op_id not in self._currently_retrying:
                    self._failed_operations.append(operation)
            return False

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_18(self, operation: FileOperation) -> bool:
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
                op_id = id(None)
                if op_id not in self._currently_retrying:
                    self._failed_operations.append(operation)
            return False

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_19(self, operation: FileOperation) -> bool:
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
                if op_id in self._currently_retrying:
                    self._failed_operations.append(operation)
            return False

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_20(self, operation: FileOperation) -> bool:
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
                    self._failed_operations.append(None)
            return False

    def xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_21(self, operation: FileOperation) -> bool:
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
            return True
    
    xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_1': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_1, 
        'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_2': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_2, 
        'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_3': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_3, 
        'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_4': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_4, 
        'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_5': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_5, 
        'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_6': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_6, 
        'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_7': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_7, 
        'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_8': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_8, 
        'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_9': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_9, 
        'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_10': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_10, 
        'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_11': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_11, 
        'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_12': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_12, 
        'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_13': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_13, 
        'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_14': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_14, 
        'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_15': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_15, 
        'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_16': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_16, 
        'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_17': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_17, 
        'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_18': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_18, 
        'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_19': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_19, 
        'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_20': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_20, 
        'xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_21': xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_21
    }
    
    def _emit_operation_safe(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_orig"), object.__getattribute__(self, "xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _emit_operation_safe.__signature__ = _mutmut_signature(xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_orig)
    xǁAutoFlushHandlerǁ_emit_operation_safe__mutmut_orig.__name__ = 'xǁAutoFlushHandlerǁ_emit_operation_safe'

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_orig(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_1(self, operation: FileOperation) -> None:
        """Handle a detected operation with temp file filtering.

        Args:
            operation: Detected file operation
        """
        # Check if operation touches any real files
        has_real_file = None

        if has_real_file:
            # Operation touches at least one real file - emit it
            log.info(
                "✅ OPERATION DETECTED - EMITTING",
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_2(self, operation: FileOperation) -> None:
        """Handle a detected operation with temp file filtering.

        Args:
            operation: Detected file operation
        """
        # Check if operation touches any real files
        has_real_file = any(
            None
        )

        if has_real_file:
            # Operation touches at least one real file - emit it
            log.info(
                "✅ OPERATION DETECTED - EMITTING",
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_3(self, operation: FileOperation) -> None:
        """Handle a detected operation with temp file filtering.

        Args:
            operation: Detected file operation
        """
        # Check if operation touches any real files
        has_real_file = any(
            not is_temp_file(event.path) and (event.dest_path and not is_temp_file(event.dest_path))
            for event in operation.events
        )

        if has_real_file:
            # Operation touches at least one real file - emit it
            log.info(
                "✅ OPERATION DETECTED - EMITTING",
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_4(self, operation: FileOperation) -> None:
        """Handle a detected operation with temp file filtering.

        Args:
            operation: Detected file operation
        """
        # Check if operation touches any real files
        has_real_file = any(
            is_temp_file(event.path) or (event.dest_path and not is_temp_file(event.dest_path))
            for event in operation.events
        )

        if has_real_file:
            # Operation touches at least one real file - emit it
            log.info(
                "✅ OPERATION DETECTED - EMITTING",
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_5(self, operation: FileOperation) -> None:
        """Handle a detected operation with temp file filtering.

        Args:
            operation: Detected file operation
        """
        # Check if operation touches any real files
        has_real_file = any(
            not is_temp_file(None) or (event.dest_path and not is_temp_file(event.dest_path))
            for event in operation.events
        )

        if has_real_file:
            # Operation touches at least one real file - emit it
            log.info(
                "✅ OPERATION DETECTED - EMITTING",
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_6(self, operation: FileOperation) -> None:
        """Handle a detected operation with temp file filtering.

        Args:
            operation: Detected file operation
        """
        # Check if operation touches any real files
        has_real_file = any(
            not is_temp_file(event.path) or (event.dest_path or not is_temp_file(event.dest_path))
            for event in operation.events
        )

        if has_real_file:
            # Operation touches at least one real file - emit it
            log.info(
                "✅ OPERATION DETECTED - EMITTING",
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_7(self, operation: FileOperation) -> None:
        """Handle a detected operation with temp file filtering.

        Args:
            operation: Detected file operation
        """
        # Check if operation touches any real files
        has_real_file = any(
            not is_temp_file(event.path) or (event.dest_path and is_temp_file(event.dest_path))
            for event in operation.events
        )

        if has_real_file:
            # Operation touches at least one real file - emit it
            log.info(
                "✅ OPERATION DETECTED - EMITTING",
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_8(self, operation: FileOperation) -> None:
        """Handle a detected operation with temp file filtering.

        Args:
            operation: Detected file operation
        """
        # Check if operation touches any real files
        has_real_file = any(
            not is_temp_file(event.path) or (event.dest_path and not is_temp_file(None))
            for event in operation.events
        )

        if has_real_file:
            # Operation touches at least one real file - emit it
            log.info(
                "✅ OPERATION DETECTED - EMITTING",
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_9(self, operation: FileOperation) -> None:
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
                None,
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_10(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
                operation_type=None,
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_11(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
                operation_type=operation.operation_type.value,
                primary_file=None,
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_12(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
                operation_type=operation.operation_type.value,
                primary_file=operation.primary_path.name,
                event_count=None,
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_13(self, operation: FileOperation) -> None:
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_14(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_15(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
                operation_type=operation.operation_type.value,
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_16(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
                operation_type=operation.operation_type.value,
                primary_file=operation.primary_path.name,
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_17(self, operation: FileOperation) -> None:
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
                "XX✅ OPERATION DETECTED - EMITTINGXX",
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_18(self, operation: FileOperation) -> None:
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
                "✅ operation detected - emitting",
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_19(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
                operation_type=operation.operation_type.value,
                primary_file=operation.primary_path.name,
                event_count=len(operation.events),
            )
            self._emit_operation_safe(None)
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_20(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
                operation_type=operation.operation_type.value,
                primary_file=operation.primary_path.name,
                event_count=len(operation.events),
            )
            self._emit_operation_safe(operation)
        else:
            # Pure temp file operation - hide it
            log.info(
                None,
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_21(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
                operation_type=operation.operation_type.value,
                primary_file=operation.primary_path.name,
                event_count=len(operation.events),
            )
            self._emit_operation_safe(operation)
        else:
            # Pure temp file operation - hide it
            log.info(
                "🚫 TEMP-ONLY OPERATION - HIDING",
                operation_type=None,
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_22(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
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
                primary_file=None,
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_23(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
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
                event_count=None,
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_24(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
                operation_type=operation.operation_type.value,
                primary_file=operation.primary_path.name,
                event_count=len(operation.events),
            )
            self._emit_operation_safe(operation)
        else:
            # Pure temp file operation - hide it
            log.info(
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_25(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
                operation_type=operation.operation_type.value,
                primary_file=operation.primary_path.name,
                event_count=len(operation.events),
            )
            self._emit_operation_safe(operation)
        else:
            # Pure temp file operation - hide it
            log.info(
                "🚫 TEMP-ONLY OPERATION - HIDING",
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_26(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_27(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_28(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
                operation_type=operation.operation_type.value,
                primary_file=operation.primary_path.name,
                event_count=len(operation.events),
            )
            self._emit_operation_safe(operation)
        else:
            # Pure temp file operation - hide it
            log.info(
                "XX🚫 TEMP-ONLY OPERATION - HIDINGXX",
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_29(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
                operation_type=operation.operation_type.value,
                primary_file=operation.primary_path.name,
                event_count=len(operation.events),
            )
            self._emit_operation_safe(operation)
        else:
            # Pure temp file operation - hide it
            log.info(
                "🚫 temp-only operation - hiding",
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

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_30(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
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
        operation_event_ids = None
        remaining_events = [event for event in self._pending_events if id(event) not in operation_event_ids]

        if remaining_events:
            log.debug(
                "Emitting remaining events not included in detected operation",
                remaining_count=len(remaining_events),
            )
            self._emit_individual_events(remaining_events)

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_31(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
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
        operation_event_ids = {id(None) for event in operation.events}
        remaining_events = [event for event in self._pending_events if id(event) not in operation_event_ids]

        if remaining_events:
            log.debug(
                "Emitting remaining events not included in detected operation",
                remaining_count=len(remaining_events),
            )
            self._emit_individual_events(remaining_events)

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_32(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
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
        remaining_events = None

        if remaining_events:
            log.debug(
                "Emitting remaining events not included in detected operation",
                remaining_count=len(remaining_events),
            )
            self._emit_individual_events(remaining_events)

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_33(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
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
        remaining_events = [event for event in self._pending_events if id(None) not in operation_event_ids]

        if remaining_events:
            log.debug(
                "Emitting remaining events not included in detected operation",
                remaining_count=len(remaining_events),
            )
            self._emit_individual_events(remaining_events)

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_34(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
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
        remaining_events = [event for event in self._pending_events if id(event) in operation_event_ids]

        if remaining_events:
            log.debug(
                "Emitting remaining events not included in detected operation",
                remaining_count=len(remaining_events),
            )
            self._emit_individual_events(remaining_events)

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_35(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
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
                None,
                remaining_count=len(remaining_events),
            )
            self._emit_individual_events(remaining_events)

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_36(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
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
                remaining_count=None,
            )
            self._emit_individual_events(remaining_events)

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_37(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
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
                remaining_count=len(remaining_events),
            )
            self._emit_individual_events(remaining_events)

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_38(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
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
                )
            self._emit_individual_events(remaining_events)

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_39(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
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
                "XXEmitting remaining events not included in detected operationXX",
                remaining_count=len(remaining_events),
            )
            self._emit_individual_events(remaining_events)

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_40(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
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
                "emitting remaining events not included in detected operation",
                remaining_count=len(remaining_events),
            )
            self._emit_individual_events(remaining_events)

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_41(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
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
                "EMITTING REMAINING EVENTS NOT INCLUDED IN DETECTED OPERATION",
                remaining_count=len(remaining_events),
            )
            self._emit_individual_events(remaining_events)

    def xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_42(self, operation: FileOperation) -> None:
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
                "✅ OPERATION DETECTED - EMITTING",
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
            self._emit_individual_events(None)
    
    xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_1': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_1, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_2': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_2, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_3': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_3, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_4': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_4, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_5': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_5, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_6': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_6, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_7': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_7, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_8': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_8, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_9': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_9, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_10': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_10, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_11': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_11, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_12': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_12, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_13': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_13, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_14': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_14, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_15': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_15, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_16': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_16, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_17': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_17, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_18': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_18, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_19': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_19, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_20': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_20, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_21': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_21, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_22': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_22, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_23': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_23, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_24': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_24, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_25': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_25, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_26': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_26, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_27': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_27, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_28': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_28, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_29': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_29, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_30': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_30, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_31': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_31, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_32': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_32, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_33': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_33, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_34': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_34, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_35': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_35, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_36': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_36, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_37': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_37, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_38': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_38, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_39': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_39, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_40': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_40, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_41': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_41, 
        'xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_42': xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_42
    }
    
    def _handle_detected_operation(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_orig"), object.__getattribute__(self, "xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _handle_detected_operation.__signature__ = _mutmut_signature(xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_orig)
    xǁAutoFlushHandlerǁ_handle_detected_operation__mutmut_orig.__name__ = 'xǁAutoFlushHandlerǁ_handle_detected_operation'

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_orig(self) -> None:
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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_1(self) -> None:
        """Handle case where no operation was detected."""
        log.info(
            None,
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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_2(self) -> None:
        """Handle case where no operation was detected."""
        log.info(
            "❓ NO OPERATION DETECTED - Filtering individual events",
            event_count=None,
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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_3(self) -> None:
        """Handle case where no operation was detected."""
        log.info(
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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_4(self) -> None:
        """Handle case where no operation was detected."""
        log.info(
            "❓ NO OPERATION DETECTED - Filtering individual events",
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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_5(self) -> None:
        """Handle case where no operation was detected."""
        log.info(
            "XX❓ NO OPERATION DETECTED - Filtering individual eventsXX",
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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_6(self) -> None:
        """Handle case where no operation was detected."""
        log.info(
            "❓ no operation detected - filtering individual events",
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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_7(self) -> None:
        """Handle case where no operation was detected."""
        log.info(
            "❓ NO OPERATION DETECTED - FILTERING INDIVIDUAL EVENTS",
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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_8(self) -> None:
        """Handle case where no operation was detected."""
        log.info(
            "❓ NO OPERATION DETECTED - Filtering individual events",
            event_count=len(self._pending_events),
        )

        emitted_count = None
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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_9(self) -> None:
        """Handle case where no operation was detected."""
        log.info(
            "❓ NO OPERATION DETECTED - Filtering individual events",
            event_count=len(self._pending_events),
        )

        emitted_count = 1
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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_10(self) -> None:
        """Handle case where no operation was detected."""
        log.info(
            "❓ NO OPERATION DETECTED - Filtering individual events",
            event_count=len(self._pending_events),
        )

        emitted_count = 0
        hidden_count = None

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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_11(self) -> None:
        """Handle case where no operation was detected."""
        log.info(
            "❓ NO OPERATION DETECTED - Filtering individual events",
            event_count=len(self._pending_events),
        )

        emitted_count = 0
        hidden_count = 1

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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_12(self) -> None:
        """Handle case where no operation was detected."""
        log.info(
            "❓ NO OPERATION DETECTED - Filtering individual events",
            event_count=len(self._pending_events),
        )

        emitted_count = 0
        hidden_count = 0

        for event in self._pending_events:
            # Check if this event involves only temp files
            is_temp_source = None
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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_13(self) -> None:
        """Handle case where no operation was detected."""
        log.info(
            "❓ NO OPERATION DETECTED - Filtering individual events",
            event_count=len(self._pending_events),
        )

        emitted_count = 0
        hidden_count = 0

        for event in self._pending_events:
            # Check if this event involves only temp files
            is_temp_source = is_temp_file(None)
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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_14(self) -> None:
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
            is_temp_dest = None

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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_15(self) -> None:
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
            is_temp_dest = event.dest_path or is_temp_file(event.dest_path)

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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_16(self) -> None:
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
            is_temp_dest = event.dest_path and is_temp_file(None)

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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_17(self) -> None:
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
            if is_temp_source or (not event.dest_path or is_temp_dest):
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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_18(self) -> None:
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
            if is_temp_source and (not event.dest_path and is_temp_dest):
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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_19(self) -> None:
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
            if is_temp_source and (event.dest_path or is_temp_dest):
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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_20(self) -> None:
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
                    None,
                    file=event.path.name,
                    event_type=event.event_type,
                )
                hidden_count += 1
            else:
                # Event touches a real file - emit it
                log.info(
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_21(self) -> None:
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
                    file=None,
                    event_type=event.event_type,
                )
                hidden_count += 1
            else:
                # Event touches a real file - emit it
                log.info(
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_22(self) -> None:
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
                    event_type=None,
                )
                hidden_count += 1
            else:
                # Event touches a real file - emit it
                log.info(
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_23(self) -> None:
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
                    file=event.path.name,
                    event_type=event.event_type,
                )
                hidden_count += 1
            else:
                # Event touches a real file - emit it
                log.info(
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_24(self) -> None:
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
                    event_type=event.event_type,
                )
                hidden_count += 1
            else:
                # Event touches a real file - emit it
                log.info(
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_25(self) -> None:
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
                    )
                hidden_count += 1
            else:
                # Event touches a real file - emit it
                log.info(
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_26(self) -> None:
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
                    "XX  🚫 Hiding temp-only eventXX",
                    file=event.path.name,
                    event_type=event.event_type,
                )
                hidden_count += 1
            else:
                # Event touches a real file - emit it
                log.info(
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_27(self) -> None:
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
                    "  🚫 hiding temp-only event",
                    file=event.path.name,
                    event_type=event.event_type,
                )
                hidden_count += 1
            else:
                # Event touches a real file - emit it
                log.info(
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_28(self) -> None:
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
                    "  🚫 HIDING TEMP-ONLY EVENT",
                    file=event.path.name,
                    event_type=event.event_type,
                )
                hidden_count += 1
            else:
                # Event touches a real file - emit it
                log.info(
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_29(self) -> None:
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
                hidden_count = 1
            else:
                # Event touches a real file - emit it
                log.info(
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_30(self) -> None:
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
                hidden_count -= 1
            else:
                # Event touches a real file - emit it
                log.info(
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_31(self) -> None:
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
                hidden_count += 2
            else:
                # Event touches a real file - emit it
                log.info(
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_32(self) -> None:
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
                    None,
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_33(self) -> None:
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
                    "  ✅ Emitting real file event",
                    file=None,
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_34(self) -> None:
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
                    "  ✅ Emitting real file event",
                    file=event.path.name,
                    event_type=None,
                )
                single_op = self._create_single_event_operation(event)
                if self._emit_operation_safe(single_op):
                    emitted_count += 1

        log.info(
            "Auto-flush complete",
            emitted=emitted_count,
            hidden=hidden_count,
        )

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_35(self) -> None:
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_36(self) -> None:
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
                    "  ✅ Emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_37(self) -> None:
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
                    "  ✅ Emitting real file event",
                    file=event.path.name,
                    )
                single_op = self._create_single_event_operation(event)
                if self._emit_operation_safe(single_op):
                    emitted_count += 1

        log.info(
            "Auto-flush complete",
            emitted=emitted_count,
            hidden=hidden_count,
        )

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_38(self) -> None:
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
                    "XX  ✅ Emitting real file eventXX",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_39(self) -> None:
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
                    "  ✅ emitting real file event",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_40(self) -> None:
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
                    "  ✅ EMITTING REAL FILE EVENT",
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

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_41(self) -> None:
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
                    "  ✅ Emitting real file event",
                    file=event.path.name,
                    event_type=event.event_type,
                )
                single_op = None
                if self._emit_operation_safe(single_op):
                    emitted_count += 1

        log.info(
            "Auto-flush complete",
            emitted=emitted_count,
            hidden=hidden_count,
        )

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_42(self) -> None:
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
                    "  ✅ Emitting real file event",
                    file=event.path.name,
                    event_type=event.event_type,
                )
                single_op = self._create_single_event_operation(None)
                if self._emit_operation_safe(single_op):
                    emitted_count += 1

        log.info(
            "Auto-flush complete",
            emitted=emitted_count,
            hidden=hidden_count,
        )

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_43(self) -> None:
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
                    "  ✅ Emitting real file event",
                    file=event.path.name,
                    event_type=event.event_type,
                )
                single_op = self._create_single_event_operation(event)
                if self._emit_operation_safe(None):
                    emitted_count += 1

        log.info(
            "Auto-flush complete",
            emitted=emitted_count,
            hidden=hidden_count,
        )

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_44(self) -> None:
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
                    "  ✅ Emitting real file event",
                    file=event.path.name,
                    event_type=event.event_type,
                )
                single_op = self._create_single_event_operation(event)
                if self._emit_operation_safe(single_op):
                    emitted_count = 1

        log.info(
            "Auto-flush complete",
            emitted=emitted_count,
            hidden=hidden_count,
        )

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_45(self) -> None:
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
                    "  ✅ Emitting real file event",
                    file=event.path.name,
                    event_type=event.event_type,
                )
                single_op = self._create_single_event_operation(event)
                if self._emit_operation_safe(single_op):
                    emitted_count -= 1

        log.info(
            "Auto-flush complete",
            emitted=emitted_count,
            hidden=hidden_count,
        )

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_46(self) -> None:
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
                    "  ✅ Emitting real file event",
                    file=event.path.name,
                    event_type=event.event_type,
                )
                single_op = self._create_single_event_operation(event)
                if self._emit_operation_safe(single_op):
                    emitted_count += 2

        log.info(
            "Auto-flush complete",
            emitted=emitted_count,
            hidden=hidden_count,
        )

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_47(self) -> None:
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
                    "  ✅ Emitting real file event",
                    file=event.path.name,
                    event_type=event.event_type,
                )
                single_op = self._create_single_event_operation(event)
                if self._emit_operation_safe(single_op):
                    emitted_count += 1

        log.info(
            None,
            emitted=emitted_count,
            hidden=hidden_count,
        )

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_48(self) -> None:
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
                    "  ✅ Emitting real file event",
                    file=event.path.name,
                    event_type=event.event_type,
                )
                single_op = self._create_single_event_operation(event)
                if self._emit_operation_safe(single_op):
                    emitted_count += 1

        log.info(
            "Auto-flush complete",
            emitted=None,
            hidden=hidden_count,
        )

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_49(self) -> None:
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
                    "  ✅ Emitting real file event",
                    file=event.path.name,
                    event_type=event.event_type,
                )
                single_op = self._create_single_event_operation(event)
                if self._emit_operation_safe(single_op):
                    emitted_count += 1

        log.info(
            "Auto-flush complete",
            emitted=emitted_count,
            hidden=None,
        )

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_50(self) -> None:
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
                    "  ✅ Emitting real file event",
                    file=event.path.name,
                    event_type=event.event_type,
                )
                single_op = self._create_single_event_operation(event)
                if self._emit_operation_safe(single_op):
                    emitted_count += 1

        log.info(
            emitted=emitted_count,
            hidden=hidden_count,
        )

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_51(self) -> None:
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
                    "  ✅ Emitting real file event",
                    file=event.path.name,
                    event_type=event.event_type,
                )
                single_op = self._create_single_event_operation(event)
                if self._emit_operation_safe(single_op):
                    emitted_count += 1

        log.info(
            "Auto-flush complete",
            hidden=hidden_count,
        )

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_52(self) -> None:
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
                    "  ✅ Emitting real file event",
                    file=event.path.name,
                    event_type=event.event_type,
                )
                single_op = self._create_single_event_operation(event)
                if self._emit_operation_safe(single_op):
                    emitted_count += 1

        log.info(
            "Auto-flush complete",
            emitted=emitted_count,
            )

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_53(self) -> None:
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
                    "  ✅ Emitting real file event",
                    file=event.path.name,
                    event_type=event.event_type,
                )
                single_op = self._create_single_event_operation(event)
                if self._emit_operation_safe(single_op):
                    emitted_count += 1

        log.info(
            "XXAuto-flush completeXX",
            emitted=emitted_count,
            hidden=hidden_count,
        )

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_54(self) -> None:
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
                    "  ✅ Emitting real file event",
                    file=event.path.name,
                    event_type=event.event_type,
                )
                single_op = self._create_single_event_operation(event)
                if self._emit_operation_safe(single_op):
                    emitted_count += 1

        log.info(
            "auto-flush complete",
            emitted=emitted_count,
            hidden=hidden_count,
        )

    def xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_55(self) -> None:
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
                    "  ✅ Emitting real file event",
                    file=event.path.name,
                    event_type=event.event_type,
                )
                single_op = self._create_single_event_operation(event)
                if self._emit_operation_safe(single_op):
                    emitted_count += 1

        log.info(
            "AUTO-FLUSH COMPLETE",
            emitted=emitted_count,
            hidden=hidden_count,
        )
    
    xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_1': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_1, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_2': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_2, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_3': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_3, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_4': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_4, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_5': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_5, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_6': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_6, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_7': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_7, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_8': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_8, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_9': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_9, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_10': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_10, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_11': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_11, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_12': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_12, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_13': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_13, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_14': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_14, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_15': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_15, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_16': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_16, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_17': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_17, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_18': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_18, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_19': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_19, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_20': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_20, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_21': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_21, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_22': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_22, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_23': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_23, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_24': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_24, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_25': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_25, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_26': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_26, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_27': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_27, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_28': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_28, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_29': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_29, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_30': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_30, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_31': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_31, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_32': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_32, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_33': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_33, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_34': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_34, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_35': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_35, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_36': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_36, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_37': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_37, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_38': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_38, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_39': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_39, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_40': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_40, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_41': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_41, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_42': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_42, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_43': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_43, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_44': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_44, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_45': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_45, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_46': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_46, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_47': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_47, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_48': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_48, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_49': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_49, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_50': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_50, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_51': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_51, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_52': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_52, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_53': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_53, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_54': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_54, 
        'xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_55': xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_55
    }
    
    def _handle_no_operation(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_orig"), object.__getattribute__(self, "xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _handle_no_operation.__signature__ = _mutmut_signature(xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_orig)
    xǁAutoFlushHandlerǁ_handle_no_operation__mutmut_orig.__name__ = 'xǁAutoFlushHandlerǁ_handle_no_operation'

    def xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_orig(self, events: list[FileEvent]) -> None:
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

    def xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_1(self, events: list[FileEvent]) -> None:
        """Emit individual events with temp filtering.

        Args:
            events: Events to emit individually
        """
        for event in events:
            is_temp_source = None
            is_temp_dest = event.dest_path and is_temp_file(event.dest_path)

            if not (is_temp_source and (not event.dest_path or is_temp_dest)):
                # Event touches a real file - emit it
                single_op = self._create_single_event_operation(event)
                self._emit_operation_safe(single_op)

    def xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_2(self, events: list[FileEvent]) -> None:
        """Emit individual events with temp filtering.

        Args:
            events: Events to emit individually
        """
        for event in events:
            is_temp_source = is_temp_file(None)
            is_temp_dest = event.dest_path and is_temp_file(event.dest_path)

            if not (is_temp_source and (not event.dest_path or is_temp_dest)):
                # Event touches a real file - emit it
                single_op = self._create_single_event_operation(event)
                self._emit_operation_safe(single_op)

    def xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_3(self, events: list[FileEvent]) -> None:
        """Emit individual events with temp filtering.

        Args:
            events: Events to emit individually
        """
        for event in events:
            is_temp_source = is_temp_file(event.path)
            is_temp_dest = None

            if not (is_temp_source and (not event.dest_path or is_temp_dest)):
                # Event touches a real file - emit it
                single_op = self._create_single_event_operation(event)
                self._emit_operation_safe(single_op)

    def xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_4(self, events: list[FileEvent]) -> None:
        """Emit individual events with temp filtering.

        Args:
            events: Events to emit individually
        """
        for event in events:
            is_temp_source = is_temp_file(event.path)
            is_temp_dest = event.dest_path or is_temp_file(event.dest_path)

            if not (is_temp_source and (not event.dest_path or is_temp_dest)):
                # Event touches a real file - emit it
                single_op = self._create_single_event_operation(event)
                self._emit_operation_safe(single_op)

    def xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_5(self, events: list[FileEvent]) -> None:
        """Emit individual events with temp filtering.

        Args:
            events: Events to emit individually
        """
        for event in events:
            is_temp_source = is_temp_file(event.path)
            is_temp_dest = event.dest_path and is_temp_file(None)

            if not (is_temp_source and (not event.dest_path or is_temp_dest)):
                # Event touches a real file - emit it
                single_op = self._create_single_event_operation(event)
                self._emit_operation_safe(single_op)

    def xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_6(self, events: list[FileEvent]) -> None:
        """Emit individual events with temp filtering.

        Args:
            events: Events to emit individually
        """
        for event in events:
            is_temp_source = is_temp_file(event.path)
            is_temp_dest = event.dest_path and is_temp_file(event.dest_path)

            if (is_temp_source and (not event.dest_path or is_temp_dest)):
                # Event touches a real file - emit it
                single_op = self._create_single_event_operation(event)
                self._emit_operation_safe(single_op)

    def xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_7(self, events: list[FileEvent]) -> None:
        """Emit individual events with temp filtering.

        Args:
            events: Events to emit individually
        """
        for event in events:
            is_temp_source = is_temp_file(event.path)
            is_temp_dest = event.dest_path and is_temp_file(event.dest_path)

            if not (is_temp_source or (not event.dest_path or is_temp_dest)):
                # Event touches a real file - emit it
                single_op = self._create_single_event_operation(event)
                self._emit_operation_safe(single_op)

    def xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_8(self, events: list[FileEvent]) -> None:
        """Emit individual events with temp filtering.

        Args:
            events: Events to emit individually
        """
        for event in events:
            is_temp_source = is_temp_file(event.path)
            is_temp_dest = event.dest_path and is_temp_file(event.dest_path)

            if not (is_temp_source and (not event.dest_path and is_temp_dest)):
                # Event touches a real file - emit it
                single_op = self._create_single_event_operation(event)
                self._emit_operation_safe(single_op)

    def xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_9(self, events: list[FileEvent]) -> None:
        """Emit individual events with temp filtering.

        Args:
            events: Events to emit individually
        """
        for event in events:
            is_temp_source = is_temp_file(event.path)
            is_temp_dest = event.dest_path and is_temp_file(event.dest_path)

            if not (is_temp_source and (event.dest_path or is_temp_dest)):
                # Event touches a real file - emit it
                single_op = self._create_single_event_operation(event)
                self._emit_operation_safe(single_op)

    def xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_10(self, events: list[FileEvent]) -> None:
        """Emit individual events with temp filtering.

        Args:
            events: Events to emit individually
        """
        for event in events:
            is_temp_source = is_temp_file(event.path)
            is_temp_dest = event.dest_path and is_temp_file(event.dest_path)

            if not (is_temp_source and (not event.dest_path or is_temp_dest)):
                # Event touches a real file - emit it
                single_op = None
                self._emit_operation_safe(single_op)

    def xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_11(self, events: list[FileEvent]) -> None:
        """Emit individual events with temp filtering.

        Args:
            events: Events to emit individually
        """
        for event in events:
            is_temp_source = is_temp_file(event.path)
            is_temp_dest = event.dest_path and is_temp_file(event.dest_path)

            if not (is_temp_source and (not event.dest_path or is_temp_dest)):
                # Event touches a real file - emit it
                single_op = self._create_single_event_operation(None)
                self._emit_operation_safe(single_op)

    def xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_12(self, events: list[FileEvent]) -> None:
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
                self._emit_operation_safe(None)
    
    xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_1': xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_1, 
        'xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_2': xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_2, 
        'xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_3': xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_3, 
        'xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_4': xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_4, 
        'xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_5': xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_5, 
        'xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_6': xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_6, 
        'xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_7': xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_7, 
        'xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_8': xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_8, 
        'xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_9': xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_9, 
        'xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_10': xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_10, 
        'xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_11': xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_11, 
        'xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_12': xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_12
    }
    
    def _emit_individual_events(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_orig"), object.__getattribute__(self, "xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _emit_individual_events.__signature__ = _mutmut_signature(xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_orig)
    xǁAutoFlushHandlerǁ_emit_individual_events__mutmut_orig.__name__ = 'xǁAutoFlushHandlerǁ_emit_individual_events'

    def xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_orig(self, event: FileEvent) -> FileOperation:
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

    def xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_1(self, event: FileEvent) -> FileOperation:
        """Create a FileOperation from a single event.

        Args:
            event: File event to wrap

        Returns:
            FileOperation representing the single event
        """
        from provide.foundation.file.operations.types import FileOperation

        return FileOperation(
            operation_type=None,
            primary_path=event.path,
            events=[event],
            confidence=1.0,
            description=f"{event.event_type} {event.path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            files_affected=[event.path],
        )

    def xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_2(self, event: FileEvent) -> FileOperation:
        """Create a FileOperation from a single event.

        Args:
            event: File event to wrap

        Returns:
            FileOperation representing the single event
        """
        from provide.foundation.file.operations.types import FileOperation

        return FileOperation(
            operation_type=OperationType.UNKNOWN,
            primary_path=None,
            events=[event],
            confidence=1.0,
            description=f"{event.event_type} {event.path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            files_affected=[event.path],
        )

    def xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_3(self, event: FileEvent) -> FileOperation:
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
            events=None,
            confidence=1.0,
            description=f"{event.event_type} {event.path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            files_affected=[event.path],
        )

    def xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_4(self, event: FileEvent) -> FileOperation:
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
            confidence=None,
            description=f"{event.event_type} {event.path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            files_affected=[event.path],
        )

    def xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_5(self, event: FileEvent) -> FileOperation:
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
            description=None,
            start_time=event.timestamp,
            end_time=event.timestamp,
            files_affected=[event.path],
        )

    def xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_6(self, event: FileEvent) -> FileOperation:
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
            start_time=None,
            end_time=event.timestamp,
            files_affected=[event.path],
        )

    def xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_7(self, event: FileEvent) -> FileOperation:
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
            end_time=None,
            files_affected=[event.path],
        )

    def xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_8(self, event: FileEvent) -> FileOperation:
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
            files_affected=None,
        )

    def xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_9(self, event: FileEvent) -> FileOperation:
        """Create a FileOperation from a single event.

        Args:
            event: File event to wrap

        Returns:
            FileOperation representing the single event
        """
        from provide.foundation.file.operations.types import FileOperation

        return FileOperation(
            primary_path=event.path,
            events=[event],
            confidence=1.0,
            description=f"{event.event_type} {event.path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            files_affected=[event.path],
        )

    def xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_10(self, event: FileEvent) -> FileOperation:
        """Create a FileOperation from a single event.

        Args:
            event: File event to wrap

        Returns:
            FileOperation representing the single event
        """
        from provide.foundation.file.operations.types import FileOperation

        return FileOperation(
            operation_type=OperationType.UNKNOWN,
            events=[event],
            confidence=1.0,
            description=f"{event.event_type} {event.path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            files_affected=[event.path],
        )

    def xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_11(self, event: FileEvent) -> FileOperation:
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
            confidence=1.0,
            description=f"{event.event_type} {event.path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            files_affected=[event.path],
        )

    def xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_12(self, event: FileEvent) -> FileOperation:
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
            description=f"{event.event_type} {event.path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            files_affected=[event.path],
        )

    def xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_13(self, event: FileEvent) -> FileOperation:
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
            start_time=event.timestamp,
            end_time=event.timestamp,
            files_affected=[event.path],
        )

    def xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_14(self, event: FileEvent) -> FileOperation:
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
            end_time=event.timestamp,
            files_affected=[event.path],
        )

    def xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_15(self, event: FileEvent) -> FileOperation:
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
            files_affected=[event.path],
        )

    def xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_16(self, event: FileEvent) -> FileOperation:
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
            )

    def xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_17(self, event: FileEvent) -> FileOperation:
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
            confidence=2.0,
            description=f"{event.event_type} {event.path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            files_affected=[event.path],
        )
    
    xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_1': xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_1, 
        'xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_2': xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_2, 
        'xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_3': xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_3, 
        'xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_4': xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_4, 
        'xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_5': xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_5, 
        'xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_6': xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_6, 
        'xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_7': xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_7, 
        'xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_8': xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_8, 
        'xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_9': xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_9, 
        'xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_10': xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_10, 
        'xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_11': xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_11, 
        'xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_12': xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_12, 
        'xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_13': xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_13, 
        'xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_14': xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_14, 
        'xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_15': xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_15, 
        'xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_16': xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_16, 
        'xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_17': xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_17
    }
    
    def _create_single_event_operation(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_orig"), object.__getattribute__(self, "xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _create_single_event_operation.__signature__ = _mutmut_signature(xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_orig)
    xǁAutoFlushHandlerǁ_create_single_event_operation__mutmut_orig.__name__ = 'xǁAutoFlushHandlerǁ_create_single_event_operation'

    @property
    def pending_events(self) -> list[FileEvent]:
        """Get pending events (read-only access).

        Thread-safe: Returns a copy to prevent external modification.
        """
        with self._lock:
            return self._pending_events.copy()

    def xǁAutoFlushHandlerǁclear__mutmut_orig(self) -> None:
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

    def xǁAutoFlushHandlerǁclear__mutmut_1(self) -> None:
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
                self._flush_timer = ""
    
    xǁAutoFlushHandlerǁclear__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAutoFlushHandlerǁclear__mutmut_1': xǁAutoFlushHandlerǁclear__mutmut_1
    }
    
    def clear(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAutoFlushHandlerǁclear__mutmut_orig"), object.__getattribute__(self, "xǁAutoFlushHandlerǁclear__mutmut_mutants"), args, kwargs, self)
        return result 
    
    clear.__signature__ = _mutmut_signature(xǁAutoFlushHandlerǁclear__mutmut_orig)
    xǁAutoFlushHandlerǁclear__mutmut_orig.__name__ = 'xǁAutoFlushHandlerǁclear'

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_orig(self) -> int:
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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_1(self) -> int:
        """Retry failed operations.

        Thread-safe: Uses internal locking.

        Returns:
            Number of operations successfully retried
        """
        with self._lock:
            if self._failed_operations:
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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_2(self) -> int:
        """Retry failed operations.

        Thread-safe: Uses internal locking.

        Returns:
            Number of operations successfully retried
        """
        with self._lock:
            if not self._failed_operations:
                return 1

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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_3(self) -> int:
        """Retry failed operations.

        Thread-safe: Uses internal locking.

        Returns:
            Number of operations successfully retried
        """
        with self._lock:
            if not self._failed_operations:
                return 0

            retry_count = None
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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_4(self) -> int:
        """Retry failed operations.

        Thread-safe: Uses internal locking.

        Returns:
            Number of operations successfully retried
        """
        with self._lock:
            if not self._failed_operations:
                return 0

            retry_count = 1
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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_5(self) -> int:
        """Retry failed operations.

        Thread-safe: Uses internal locking.

        Returns:
            Number of operations successfully retried
        """
        with self._lock:
            if not self._failed_operations:
                return 0

            retry_count = 0
            remaining = None

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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_6(self) -> int:
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
                self._currently_retrying.add(None)

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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_7(self) -> int:
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
                self._currently_retrying.add(id(None))

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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_8(self) -> int:
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
                    if self._emit_operation_safe(None):
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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_9(self) -> int:
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
                        retry_count = 1
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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_10(self) -> int:
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
                        retry_count -= 1
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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_11(self) -> int:
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
                        retry_count += 2
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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_12(self) -> int:
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
                            None,
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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_13(self) -> int:
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
                            operation_type=None,
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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_14(self) -> int:
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
                            primary_file=None,
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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_15(self) -> int:
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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_16(self) -> int:
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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_17(self) -> int:
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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_18(self) -> int:
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
                            "XXRetry successfulXX",
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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_19(self) -> int:
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
                            "retry successful",
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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_20(self) -> int:
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
                            "RETRY SUCCESSFUL",
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

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_21(self) -> int:
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
                        remaining.append(None)

                self._failed_operations = remaining

                if retry_count > 0:
                    log.info(f"Retried {retry_count} failed operations, {len(remaining)} still pending")

                return retry_count
            finally:
                # Clear retry tracking
                self._currently_retrying.clear()

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_22(self) -> int:
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

                self._failed_operations = None

                if retry_count > 0:
                    log.info(f"Retried {retry_count} failed operations, {len(remaining)} still pending")

                return retry_count
            finally:
                # Clear retry tracking
                self._currently_retrying.clear()

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_23(self) -> int:
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

                if retry_count >= 0:
                    log.info(f"Retried {retry_count} failed operations, {len(remaining)} still pending")

                return retry_count
            finally:
                # Clear retry tracking
                self._currently_retrying.clear()

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_24(self) -> int:
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

                if retry_count > 1:
                    log.info(f"Retried {retry_count} failed operations, {len(remaining)} still pending")

                return retry_count
            finally:
                # Clear retry tracking
                self._currently_retrying.clear()

    def xǁAutoFlushHandlerǁretry_failed_operations__mutmut_25(self) -> int:
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
                    log.info(None)

                return retry_count
            finally:
                # Clear retry tracking
                self._currently_retrying.clear()
    
    xǁAutoFlushHandlerǁretry_failed_operations__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_1': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_1, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_2': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_2, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_3': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_3, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_4': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_4, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_5': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_5, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_6': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_6, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_7': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_7, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_8': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_8, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_9': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_9, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_10': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_10, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_11': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_11, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_12': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_12, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_13': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_13, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_14': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_14, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_15': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_15, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_16': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_16, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_17': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_17, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_18': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_18, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_19': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_19, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_20': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_20, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_21': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_21, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_22': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_22, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_23': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_23, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_24': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_24, 
        'xǁAutoFlushHandlerǁretry_failed_operations__mutmut_25': xǁAutoFlushHandlerǁretry_failed_operations__mutmut_25
    }
    
    def retry_failed_operations(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAutoFlushHandlerǁretry_failed_operations__mutmut_orig"), object.__getattribute__(self, "xǁAutoFlushHandlerǁretry_failed_operations__mutmut_mutants"), args, kwargs, self)
        return result 
    
    retry_failed_operations.__signature__ = _mutmut_signature(xǁAutoFlushHandlerǁretry_failed_operations__mutmut_orig)
    xǁAutoFlushHandlerǁretry_failed_operations__mutmut_orig.__name__ = 'xǁAutoFlushHandlerǁretry_failed_operations'

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

    def xǁAutoFlushHandlerǁclear_failed_operations__mutmut_orig(self) -> int:
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

    def xǁAutoFlushHandlerǁclear_failed_operations__mutmut_1(self) -> int:
        """Clear all failed operations (data loss - use carefully).

        Thread-safe: Uses internal locking.

        Returns:
            Number of operations that were cleared
        """
        with self._lock:
            count = None
            self._failed_operations.clear()
            if count > 0:
                log.warning(f"Cleared {count} failed operations - data loss!")
            return count

    def xǁAutoFlushHandlerǁclear_failed_operations__mutmut_2(self) -> int:
        """Clear all failed operations (data loss - use carefully).

        Thread-safe: Uses internal locking.

        Returns:
            Number of operations that were cleared
        """
        with self._lock:
            count = len(self._failed_operations)
            self._failed_operations.clear()
            if count >= 0:
                log.warning(f"Cleared {count} failed operations - data loss!")
            return count

    def xǁAutoFlushHandlerǁclear_failed_operations__mutmut_3(self) -> int:
        """Clear all failed operations (data loss - use carefully).

        Thread-safe: Uses internal locking.

        Returns:
            Number of operations that were cleared
        """
        with self._lock:
            count = len(self._failed_operations)
            self._failed_operations.clear()
            if count > 1:
                log.warning(f"Cleared {count} failed operations - data loss!")
            return count

    def xǁAutoFlushHandlerǁclear_failed_operations__mutmut_4(self) -> int:
        """Clear all failed operations (data loss - use carefully).

        Thread-safe: Uses internal locking.

        Returns:
            Number of operations that were cleared
        """
        with self._lock:
            count = len(self._failed_operations)
            self._failed_operations.clear()
            if count > 0:
                log.warning(None)
            return count
    
    xǁAutoFlushHandlerǁclear_failed_operations__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAutoFlushHandlerǁclear_failed_operations__mutmut_1': xǁAutoFlushHandlerǁclear_failed_operations__mutmut_1, 
        'xǁAutoFlushHandlerǁclear_failed_operations__mutmut_2': xǁAutoFlushHandlerǁclear_failed_operations__mutmut_2, 
        'xǁAutoFlushHandlerǁclear_failed_operations__mutmut_3': xǁAutoFlushHandlerǁclear_failed_operations__mutmut_3, 
        'xǁAutoFlushHandlerǁclear_failed_operations__mutmut_4': xǁAutoFlushHandlerǁclear_failed_operations__mutmut_4
    }
    
    def clear_failed_operations(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAutoFlushHandlerǁclear_failed_operations__mutmut_orig"), object.__getattribute__(self, "xǁAutoFlushHandlerǁclear_failed_operations__mutmut_mutants"), args, kwargs, self)
        return result 
    
    clear_failed_operations.__signature__ = _mutmut_signature(xǁAutoFlushHandlerǁclear_failed_operations__mutmut_orig)
    xǁAutoFlushHandlerǁclear_failed_operations__mutmut_orig.__name__ = 'xǁAutoFlushHandlerǁclear_failed_operations'


# <3 🧱🤝📄🪄
