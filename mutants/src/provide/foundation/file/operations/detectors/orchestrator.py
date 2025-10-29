# provide/foundation/file/operations/detectors/orchestrator.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""File operation detector orchestrator.

Coordinates detector functions via registry to identify the best match for file events.
"""

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class OperationDetector:
    """Detects and classifies file operations from events."""

    def xǁOperationDetectorǁ__init____mutmut_orig(
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

    def xǁOperationDetectorǁ__init____mutmut_1(
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
        self.config = None
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

    def xǁOperationDetectorǁ__init____mutmut_2(
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
        self.config = config and DetectorConfig()
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

    def xǁOperationDetectorǁ__init____mutmut_3(
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
        self.on_operation_complete = None
        self.registry = registry or get_detector_registry()
        self._pending_events: list[FileEvent] = []
        self._last_flush = datetime.now()

        # Create auto-flush handler for streaming mode
        self._auto_flush_handler = AutoFlushHandler(
            time_window_ms=self.config.time_window_ms,
            on_operation_complete=on_operation_complete,
            analyze_func=self._analyze_event_group,
        )

    def xǁOperationDetectorǁ__init____mutmut_4(
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
        self.registry = None
        self._pending_events: list[FileEvent] = []
        self._last_flush = datetime.now()

        # Create auto-flush handler for streaming mode
        self._auto_flush_handler = AutoFlushHandler(
            time_window_ms=self.config.time_window_ms,
            on_operation_complete=on_operation_complete,
            analyze_func=self._analyze_event_group,
        )

    def xǁOperationDetectorǁ__init____mutmut_5(
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
        self.registry = registry and get_detector_registry()
        self._pending_events: list[FileEvent] = []
        self._last_flush = datetime.now()

        # Create auto-flush handler for streaming mode
        self._auto_flush_handler = AutoFlushHandler(
            time_window_ms=self.config.time_window_ms,
            on_operation_complete=on_operation_complete,
            analyze_func=self._analyze_event_group,
        )

    def xǁOperationDetectorǁ__init____mutmut_6(
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
        self._pending_events: list[FileEvent] = None
        self._last_flush = datetime.now()

        # Create auto-flush handler for streaming mode
        self._auto_flush_handler = AutoFlushHandler(
            time_window_ms=self.config.time_window_ms,
            on_operation_complete=on_operation_complete,
            analyze_func=self._analyze_event_group,
        )

    def xǁOperationDetectorǁ__init____mutmut_7(
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
        self._last_flush = None

        # Create auto-flush handler for streaming mode
        self._auto_flush_handler = AutoFlushHandler(
            time_window_ms=self.config.time_window_ms,
            on_operation_complete=on_operation_complete,
            analyze_func=self._analyze_event_group,
        )

    def xǁOperationDetectorǁ__init____mutmut_8(
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
        self._auto_flush_handler = None

    def xǁOperationDetectorǁ__init____mutmut_9(
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
            time_window_ms=None,
            on_operation_complete=on_operation_complete,
            analyze_func=self._analyze_event_group,
        )

    def xǁOperationDetectorǁ__init____mutmut_10(
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
            on_operation_complete=None,
            analyze_func=self._analyze_event_group,
        )

    def xǁOperationDetectorǁ__init____mutmut_11(
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
            analyze_func=None,
        )

    def xǁOperationDetectorǁ__init____mutmut_12(
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
            on_operation_complete=on_operation_complete,
            analyze_func=self._analyze_event_group,
        )

    def xǁOperationDetectorǁ__init____mutmut_13(
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
            analyze_func=self._analyze_event_group,
        )

    def xǁOperationDetectorǁ__init____mutmut_14(
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
        )

    xǁOperationDetectorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁOperationDetectorǁ__init____mutmut_1": xǁOperationDetectorǁ__init____mutmut_1,
        "xǁOperationDetectorǁ__init____mutmut_2": xǁOperationDetectorǁ__init____mutmut_2,
        "xǁOperationDetectorǁ__init____mutmut_3": xǁOperationDetectorǁ__init____mutmut_3,
        "xǁOperationDetectorǁ__init____mutmut_4": xǁOperationDetectorǁ__init____mutmut_4,
        "xǁOperationDetectorǁ__init____mutmut_5": xǁOperationDetectorǁ__init____mutmut_5,
        "xǁOperationDetectorǁ__init____mutmut_6": xǁOperationDetectorǁ__init____mutmut_6,
        "xǁOperationDetectorǁ__init____mutmut_7": xǁOperationDetectorǁ__init____mutmut_7,
        "xǁOperationDetectorǁ__init____mutmut_8": xǁOperationDetectorǁ__init____mutmut_8,
        "xǁOperationDetectorǁ__init____mutmut_9": xǁOperationDetectorǁ__init____mutmut_9,
        "xǁOperationDetectorǁ__init____mutmut_10": xǁOperationDetectorǁ__init____mutmut_10,
        "xǁOperationDetectorǁ__init____mutmut_11": xǁOperationDetectorǁ__init____mutmut_11,
        "xǁOperationDetectorǁ__init____mutmut_12": xǁOperationDetectorǁ__init____mutmut_12,
        "xǁOperationDetectorǁ__init____mutmut_13": xǁOperationDetectorǁ__init____mutmut_13,
        "xǁOperationDetectorǁ__init____mutmut_14": xǁOperationDetectorǁ__init____mutmut_14,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁOperationDetectorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁOperationDetectorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁOperationDetectorǁ__init____mutmut_orig)
    xǁOperationDetectorǁ__init____mutmut_orig.__name__ = "xǁOperationDetectorǁ__init__"

    def xǁOperationDetectorǁdetect__mutmut_orig(self, events: list[FileEvent]) -> list[FileOperation]:
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

    def xǁOperationDetectorǁdetect__mutmut_1(self, events: list[FileEvent]) -> list[FileOperation]:
        """Detect all operations from a list of events.

        Args:
            events: List of file events to analyze

        Returns:
            List of detected operations, ordered by start time
        """
        if events:
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

    def xǁOperationDetectorǁdetect__mutmut_2(self, events: list[FileEvent]) -> list[FileOperation]:
        """Detect all operations from a list of events.

        Args:
            events: List of file events to analyze

        Returns:
            List of detected operations, ordered by start time
        """
        if not events:
            return []

        # Sort events by timestamp
        sorted_events = None

        # Group events by time windows
        event_groups = self._group_events_by_time(sorted_events)

        operations = []
        for group in event_groups:
            operation = self._analyze_event_group(group)
            if operation:
                operations.append(operation)

        return operations

    def xǁOperationDetectorǁdetect__mutmut_3(self, events: list[FileEvent]) -> list[FileOperation]:
        """Detect all operations from a list of events.

        Args:
            events: List of file events to analyze

        Returns:
            List of detected operations, ordered by start time
        """
        if not events:
            return []

        # Sort events by timestamp
        sorted_events = sorted(None, key=lambda e: e.timestamp)

        # Group events by time windows
        event_groups = self._group_events_by_time(sorted_events)

        operations = []
        for group in event_groups:
            operation = self._analyze_event_group(group)
            if operation:
                operations.append(operation)

        return operations

    def xǁOperationDetectorǁdetect__mutmut_4(self, events: list[FileEvent]) -> list[FileOperation]:
        """Detect all operations from a list of events.

        Args:
            events: List of file events to analyze

        Returns:
            List of detected operations, ordered by start time
        """
        if not events:
            return []

        # Sort events by timestamp
        sorted_events = sorted(events, key=None)

        # Group events by time windows
        event_groups = self._group_events_by_time(sorted_events)

        operations = []
        for group in event_groups:
            operation = self._analyze_event_group(group)
            if operation:
                operations.append(operation)

        return operations

    def xǁOperationDetectorǁdetect__mutmut_5(self, events: list[FileEvent]) -> list[FileOperation]:
        """Detect all operations from a list of events.

        Args:
            events: List of file events to analyze

        Returns:
            List of detected operations, ordered by start time
        """
        if not events:
            return []

        # Sort events by timestamp
        sorted_events = sorted(key=lambda e: e.timestamp)

        # Group events by time windows
        event_groups = self._group_events_by_time(sorted_events)

        operations = []
        for group in event_groups:
            operation = self._analyze_event_group(group)
            if operation:
                operations.append(operation)

        return operations

    def xǁOperationDetectorǁdetect__mutmut_6(self, events: list[FileEvent]) -> list[FileOperation]:
        """Detect all operations from a list of events.

        Args:
            events: List of file events to analyze

        Returns:
            List of detected operations, ordered by start time
        """
        if not events:
            return []

        # Sort events by timestamp
        sorted_events = sorted(
            events,
        )

        # Group events by time windows
        event_groups = self._group_events_by_time(sorted_events)

        operations = []
        for group in event_groups:
            operation = self._analyze_event_group(group)
            if operation:
                operations.append(operation)

        return operations

    def xǁOperationDetectorǁdetect__mutmut_7(self, events: list[FileEvent]) -> list[FileOperation]:
        """Detect all operations from a list of events.

        Args:
            events: List of file events to analyze

        Returns:
            List of detected operations, ordered by start time
        """
        if not events:
            return []

        # Sort events by timestamp
        sorted_events = sorted(events, key=lambda e: None)

        # Group events by time windows
        event_groups = self._group_events_by_time(sorted_events)

        operations = []
        for group in event_groups:
            operation = self._analyze_event_group(group)
            if operation:
                operations.append(operation)

        return operations

    def xǁOperationDetectorǁdetect__mutmut_8(self, events: list[FileEvent]) -> list[FileOperation]:
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
        event_groups = None

        operations = []
        for group in event_groups:
            operation = self._analyze_event_group(group)
            if operation:
                operations.append(operation)

        return operations

    def xǁOperationDetectorǁdetect__mutmut_9(self, events: list[FileEvent]) -> list[FileOperation]:
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
        event_groups = self._group_events_by_time(None)

        operations = []
        for group in event_groups:
            operation = self._analyze_event_group(group)
            if operation:
                operations.append(operation)

        return operations

    def xǁOperationDetectorǁdetect__mutmut_10(self, events: list[FileEvent]) -> list[FileOperation]:
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

        operations = None
        for group in event_groups:
            operation = self._analyze_event_group(group)
            if operation:
                operations.append(operation)

        return operations

    def xǁOperationDetectorǁdetect__mutmut_11(self, events: list[FileEvent]) -> list[FileOperation]:
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
            operation = None
            if operation:
                operations.append(operation)

        return operations

    def xǁOperationDetectorǁdetect__mutmut_12(self, events: list[FileEvent]) -> list[FileOperation]:
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
            operation = self._analyze_event_group(None)
            if operation:
                operations.append(operation)

        return operations

    def xǁOperationDetectorǁdetect__mutmut_13(self, events: list[FileEvent]) -> list[FileOperation]:
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
                operations.append(None)

        return operations

    xǁOperationDetectorǁdetect__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁOperationDetectorǁdetect__mutmut_1": xǁOperationDetectorǁdetect__mutmut_1,
        "xǁOperationDetectorǁdetect__mutmut_2": xǁOperationDetectorǁdetect__mutmut_2,
        "xǁOperationDetectorǁdetect__mutmut_3": xǁOperationDetectorǁdetect__mutmut_3,
        "xǁOperationDetectorǁdetect__mutmut_4": xǁOperationDetectorǁdetect__mutmut_4,
        "xǁOperationDetectorǁdetect__mutmut_5": xǁOperationDetectorǁdetect__mutmut_5,
        "xǁOperationDetectorǁdetect__mutmut_6": xǁOperationDetectorǁdetect__mutmut_6,
        "xǁOperationDetectorǁdetect__mutmut_7": xǁOperationDetectorǁdetect__mutmut_7,
        "xǁOperationDetectorǁdetect__mutmut_8": xǁOperationDetectorǁdetect__mutmut_8,
        "xǁOperationDetectorǁdetect__mutmut_9": xǁOperationDetectorǁdetect__mutmut_9,
        "xǁOperationDetectorǁdetect__mutmut_10": xǁOperationDetectorǁdetect__mutmut_10,
        "xǁOperationDetectorǁdetect__mutmut_11": xǁOperationDetectorǁdetect__mutmut_11,
        "xǁOperationDetectorǁdetect__mutmut_12": xǁOperationDetectorǁdetect__mutmut_12,
        "xǁOperationDetectorǁdetect__mutmut_13": xǁOperationDetectorǁdetect__mutmut_13,
    }

    def detect(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁOperationDetectorǁdetect__mutmut_orig"),
            object.__getattribute__(self, "xǁOperationDetectorǁdetect__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    detect.__signature__ = _mutmut_signature(xǁOperationDetectorǁdetect__mutmut_orig)
    xǁOperationDetectorǁdetect__mutmut_orig.__name__ = "xǁOperationDetectorǁdetect"

    def xǁOperationDetectorǁdetect_streaming__mutmut_orig(self, event: FileEvent) -> FileOperation | None:
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

    def xǁOperationDetectorǁdetect_streaming__mutmut_1(self, event: FileEvent) -> FileOperation | None:
        """Process events in streaming fashion.

        Args:
            event: Single file event

        Returns:
            Completed operation if detected, None otherwise
        """
        self._pending_events.append(None)

        # Check if we should flush based on time window
        now = datetime.now()
        time_since_last = (now - self._last_flush).total_seconds() * 1000

        if time_since_last >= self.config.time_window_ms:
            return self._flush_pending()

        return None

    def xǁOperationDetectorǁdetect_streaming__mutmut_2(self, event: FileEvent) -> FileOperation | None:
        """Process events in streaming fashion.

        Args:
            event: Single file event

        Returns:
            Completed operation if detected, None otherwise
        """
        self._pending_events.append(event)

        # Check if we should flush based on time window
        now = None
        time_since_last = (now - self._last_flush).total_seconds() * 1000

        if time_since_last >= self.config.time_window_ms:
            return self._flush_pending()

        return None

    def xǁOperationDetectorǁdetect_streaming__mutmut_3(self, event: FileEvent) -> FileOperation | None:
        """Process events in streaming fashion.

        Args:
            event: Single file event

        Returns:
            Completed operation if detected, None otherwise
        """
        self._pending_events.append(event)

        # Check if we should flush based on time window
        now = datetime.now()
        time_since_last = None

        if time_since_last >= self.config.time_window_ms:
            return self._flush_pending()

        return None

    def xǁOperationDetectorǁdetect_streaming__mutmut_4(self, event: FileEvent) -> FileOperation | None:
        """Process events in streaming fashion.

        Args:
            event: Single file event

        Returns:
            Completed operation if detected, None otherwise
        """
        self._pending_events.append(event)

        # Check if we should flush based on time window
        now = datetime.now()
        time_since_last = (now - self._last_flush).total_seconds() / 1000

        if time_since_last >= self.config.time_window_ms:
            return self._flush_pending()

        return None

    def xǁOperationDetectorǁdetect_streaming__mutmut_5(self, event: FileEvent) -> FileOperation | None:
        """Process events in streaming fashion.

        Args:
            event: Single file event

        Returns:
            Completed operation if detected, None otherwise
        """
        self._pending_events.append(event)

        # Check if we should flush based on time window
        now = datetime.now()
        time_since_last = (now + self._last_flush).total_seconds() * 1000

        if time_since_last >= self.config.time_window_ms:
            return self._flush_pending()

        return None

    def xǁOperationDetectorǁdetect_streaming__mutmut_6(self, event: FileEvent) -> FileOperation | None:
        """Process events in streaming fashion.

        Args:
            event: Single file event

        Returns:
            Completed operation if detected, None otherwise
        """
        self._pending_events.append(event)

        # Check if we should flush based on time window
        now = datetime.now()
        time_since_last = (now - self._last_flush).total_seconds() * 1001

        if time_since_last >= self.config.time_window_ms:
            return self._flush_pending()

        return None

    def xǁOperationDetectorǁdetect_streaming__mutmut_7(self, event: FileEvent) -> FileOperation | None:
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

        if time_since_last > self.config.time_window_ms:
            return self._flush_pending()

        return None

    xǁOperationDetectorǁdetect_streaming__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁOperationDetectorǁdetect_streaming__mutmut_1": xǁOperationDetectorǁdetect_streaming__mutmut_1,
        "xǁOperationDetectorǁdetect_streaming__mutmut_2": xǁOperationDetectorǁdetect_streaming__mutmut_2,
        "xǁOperationDetectorǁdetect_streaming__mutmut_3": xǁOperationDetectorǁdetect_streaming__mutmut_3,
        "xǁOperationDetectorǁdetect_streaming__mutmut_4": xǁOperationDetectorǁdetect_streaming__mutmut_4,
        "xǁOperationDetectorǁdetect_streaming__mutmut_5": xǁOperationDetectorǁdetect_streaming__mutmut_5,
        "xǁOperationDetectorǁdetect_streaming__mutmut_6": xǁOperationDetectorǁdetect_streaming__mutmut_6,
        "xǁOperationDetectorǁdetect_streaming__mutmut_7": xǁOperationDetectorǁdetect_streaming__mutmut_7,
    }

    def detect_streaming(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁOperationDetectorǁdetect_streaming__mutmut_orig"),
            object.__getattribute__(self, "xǁOperationDetectorǁdetect_streaming__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    detect_streaming.__signature__ = _mutmut_signature(xǁOperationDetectorǁdetect_streaming__mutmut_orig)
    xǁOperationDetectorǁdetect_streaming__mutmut_orig.__name__ = "xǁOperationDetectorǁdetect_streaming"

    def xǁOperationDetectorǁadd_event__mutmut_orig(self, event: FileEvent) -> None:
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

    def xǁOperationDetectorǁadd_event__mutmut_1(self, event: FileEvent) -> None:
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
        self._auto_flush_handler.add_event(None)

    xǁOperationDetectorǁadd_event__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁOperationDetectorǁadd_event__mutmut_1": xǁOperationDetectorǁadd_event__mutmut_1
    }

    def add_event(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁOperationDetectorǁadd_event__mutmut_orig"),
            object.__getattribute__(self, "xǁOperationDetectorǁadd_event__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    add_event.__signature__ = _mutmut_signature(xǁOperationDetectorǁadd_event__mutmut_orig)
    xǁOperationDetectorǁadd_event__mutmut_orig.__name__ = "xǁOperationDetectorǁadd_event"

    def xǁOperationDetectorǁflush__mutmut_orig(self) -> list[FileOperation]:
        """Get any pending operations and clear buffer."""
        operations = []
        if self._pending_events:
            operation = self._flush_pending()
            if operation:
                operations.append(operation)
        return operations

    def xǁOperationDetectorǁflush__mutmut_1(self) -> list[FileOperation]:
        """Get any pending operations and clear buffer."""
        operations = None
        if self._pending_events:
            operation = self._flush_pending()
            if operation:
                operations.append(operation)
        return operations

    def xǁOperationDetectorǁflush__mutmut_2(self) -> list[FileOperation]:
        """Get any pending operations and clear buffer."""
        operations = []
        if self._pending_events:
            operation = None
            if operation:
                operations.append(operation)
        return operations

    def xǁOperationDetectorǁflush__mutmut_3(self) -> list[FileOperation]:
        """Get any pending operations and clear buffer."""
        operations = []
        if self._pending_events:
            operation = self._flush_pending()
            if operation:
                operations.append(None)
        return operations

    xǁOperationDetectorǁflush__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁOperationDetectorǁflush__mutmut_1": xǁOperationDetectorǁflush__mutmut_1,
        "xǁOperationDetectorǁflush__mutmut_2": xǁOperationDetectorǁflush__mutmut_2,
        "xǁOperationDetectorǁflush__mutmut_3": xǁOperationDetectorǁflush__mutmut_3,
    }

    def flush(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁOperationDetectorǁflush__mutmut_orig"),
            object.__getattribute__(self, "xǁOperationDetectorǁflush__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    flush.__signature__ = _mutmut_signature(xǁOperationDetectorǁflush__mutmut_orig)
    xǁOperationDetectorǁflush__mutmut_orig.__name__ = "xǁOperationDetectorǁflush"

    def xǁOperationDetectorǁ_flush_pending__mutmut_orig(self) -> FileOperation | None:
        """Analyze pending events and clear buffer."""
        if not self._pending_events:
            return None

        operation = self._analyze_event_group(self._pending_events)
        self._pending_events.clear()
        self._last_flush = datetime.now()
        return operation

    def xǁOperationDetectorǁ_flush_pending__mutmut_1(self) -> FileOperation | None:
        """Analyze pending events and clear buffer."""
        if self._pending_events:
            return None

        operation = self._analyze_event_group(self._pending_events)
        self._pending_events.clear()
        self._last_flush = datetime.now()
        return operation

    def xǁOperationDetectorǁ_flush_pending__mutmut_2(self) -> FileOperation | None:
        """Analyze pending events and clear buffer."""
        if not self._pending_events:
            return None

        operation = None
        self._pending_events.clear()
        self._last_flush = datetime.now()
        return operation

    def xǁOperationDetectorǁ_flush_pending__mutmut_3(self) -> FileOperation | None:
        """Analyze pending events and clear buffer."""
        if not self._pending_events:
            return None

        operation = self._analyze_event_group(None)
        self._pending_events.clear()
        self._last_flush = datetime.now()
        return operation

    def xǁOperationDetectorǁ_flush_pending__mutmut_4(self) -> FileOperation | None:
        """Analyze pending events and clear buffer."""
        if not self._pending_events:
            return None

        operation = self._analyze_event_group(self._pending_events)
        self._pending_events.clear()
        self._last_flush = None
        return operation

    xǁOperationDetectorǁ_flush_pending__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁOperationDetectorǁ_flush_pending__mutmut_1": xǁOperationDetectorǁ_flush_pending__mutmut_1,
        "xǁOperationDetectorǁ_flush_pending__mutmut_2": xǁOperationDetectorǁ_flush_pending__mutmut_2,
        "xǁOperationDetectorǁ_flush_pending__mutmut_3": xǁOperationDetectorǁ_flush_pending__mutmut_3,
        "xǁOperationDetectorǁ_flush_pending__mutmut_4": xǁOperationDetectorǁ_flush_pending__mutmut_4,
    }

    def _flush_pending(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁOperationDetectorǁ_flush_pending__mutmut_orig"),
            object.__getattribute__(self, "xǁOperationDetectorǁ_flush_pending__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _flush_pending.__signature__ = _mutmut_signature(xǁOperationDetectorǁ_flush_pending__mutmut_orig)
    xǁOperationDetectorǁ_flush_pending__mutmut_orig.__name__ = "xǁOperationDetectorǁ_flush_pending"

    def xǁOperationDetectorǁ_group_events_by_time__mutmut_orig(
        self, events: list[FileEvent]
    ) -> list[list[FileEvent]]:
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

    def xǁOperationDetectorǁ_group_events_by_time__mutmut_1(
        self, events: list[FileEvent]
    ) -> list[list[FileEvent]]:
        """Group events that occur within time windows.

        Uses a fixed time window from the first event in each group to ensure
        all related events are captured together, even if they span longer than
        the window between consecutive events.
        """
        if events:
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

    def xǁOperationDetectorǁ_group_events_by_time__mutmut_2(
        self, events: list[FileEvent]
    ) -> list[list[FileEvent]]:
        """Group events that occur within time windows.

        Uses a fixed time window from the first event in each group to ensure
        all related events are captured together, even if they span longer than
        the window between consecutive events.
        """
        if not events:
            return []

        groups = None
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

    def xǁOperationDetectorǁ_group_events_by_time__mutmut_3(
        self, events: list[FileEvent]
    ) -> list[list[FileEvent]]:
        """Group events that occur within time windows.

        Uses a fixed time window from the first event in each group to ensure
        all related events are captured together, even if they span longer than
        the window between consecutive events.
        """
        if not events:
            return []

        groups = []
        current_group = None
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

    def xǁOperationDetectorǁ_group_events_by_time__mutmut_4(
        self, events: list[FileEvent]
    ) -> list[list[FileEvent]]:
        """Group events that occur within time windows.

        Uses a fixed time window from the first event in each group to ensure
        all related events are captured together, even if they span longer than
        the window between consecutive events.
        """
        if not events:
            return []

        groups = []
        current_group = [events[1]]
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

    def xǁOperationDetectorǁ_group_events_by_time__mutmut_5(
        self, events: list[FileEvent]
    ) -> list[list[FileEvent]]:
        """Group events that occur within time windows.

        Uses a fixed time window from the first event in each group to ensure
        all related events are captured together, even if they span longer than
        the window between consecutive events.
        """
        if not events:
            return []

        groups = []
        current_group = [events[0]]
        group_start_time = None  # Track first event in group

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

    def xǁOperationDetectorǁ_group_events_by_time__mutmut_6(
        self, events: list[FileEvent]
    ) -> list[list[FileEvent]]:
        """Group events that occur within time windows.

        Uses a fixed time window from the first event in each group to ensure
        all related events are captured together, even if they span longer than
        the window between consecutive events.
        """
        if not events:
            return []

        groups = []
        current_group = [events[0]]
        group_start_time = events[1].timestamp  # Track first event in group

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

    def xǁOperationDetectorǁ_group_events_by_time__mutmut_7(
        self, events: list[FileEvent]
    ) -> list[list[FileEvent]]:
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

        for event in events[2:]:
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

    def xǁOperationDetectorǁ_group_events_by_time__mutmut_8(
        self, events: list[FileEvent]
    ) -> list[list[FileEvent]]:
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
            time_diff = None

            if time_diff <= self.config.time_window_ms:
                current_group.append(event)
            else:
                groups.append(current_group)
                current_group = [event]
                group_start_time = event.timestamp  # Reset for new group

        if current_group:
            groups.append(current_group)

        return groups

    def xǁOperationDetectorǁ_group_events_by_time__mutmut_9(
        self, events: list[FileEvent]
    ) -> list[list[FileEvent]]:
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
            time_diff = (event.timestamp - group_start_time).total_seconds() / 1000

            if time_diff <= self.config.time_window_ms:
                current_group.append(event)
            else:
                groups.append(current_group)
                current_group = [event]
                group_start_time = event.timestamp  # Reset for new group

        if current_group:
            groups.append(current_group)

        return groups

    def xǁOperationDetectorǁ_group_events_by_time__mutmut_10(
        self, events: list[FileEvent]
    ) -> list[list[FileEvent]]:
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
            time_diff = (event.timestamp + group_start_time).total_seconds() * 1000

            if time_diff <= self.config.time_window_ms:
                current_group.append(event)
            else:
                groups.append(current_group)
                current_group = [event]
                group_start_time = event.timestamp  # Reset for new group

        if current_group:
            groups.append(current_group)

        return groups

    def xǁOperationDetectorǁ_group_events_by_time__mutmut_11(
        self, events: list[FileEvent]
    ) -> list[list[FileEvent]]:
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
            time_diff = (event.timestamp - group_start_time).total_seconds() * 1001

            if time_diff <= self.config.time_window_ms:
                current_group.append(event)
            else:
                groups.append(current_group)
                current_group = [event]
                group_start_time = event.timestamp  # Reset for new group

        if current_group:
            groups.append(current_group)

        return groups

    def xǁOperationDetectorǁ_group_events_by_time__mutmut_12(
        self, events: list[FileEvent]
    ) -> list[list[FileEvent]]:
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

            if time_diff < self.config.time_window_ms:
                current_group.append(event)
            else:
                groups.append(current_group)
                current_group = [event]
                group_start_time = event.timestamp  # Reset for new group

        if current_group:
            groups.append(current_group)

        return groups

    def xǁOperationDetectorǁ_group_events_by_time__mutmut_13(
        self, events: list[FileEvent]
    ) -> list[list[FileEvent]]:
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
                current_group.append(None)
            else:
                groups.append(current_group)
                current_group = [event]
                group_start_time = event.timestamp  # Reset for new group

        if current_group:
            groups.append(current_group)

        return groups

    def xǁOperationDetectorǁ_group_events_by_time__mutmut_14(
        self, events: list[FileEvent]
    ) -> list[list[FileEvent]]:
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
                groups.append(None)
                current_group = [event]
                group_start_time = event.timestamp  # Reset for new group

        if current_group:
            groups.append(current_group)

        return groups

    def xǁOperationDetectorǁ_group_events_by_time__mutmut_15(
        self, events: list[FileEvent]
    ) -> list[list[FileEvent]]:
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
                current_group = None
                group_start_time = event.timestamp  # Reset for new group

        if current_group:
            groups.append(current_group)

        return groups

    def xǁOperationDetectorǁ_group_events_by_time__mutmut_16(
        self, events: list[FileEvent]
    ) -> list[list[FileEvent]]:
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
                group_start_time = None  # Reset for new group

        if current_group:
            groups.append(current_group)

        return groups

    def xǁOperationDetectorǁ_group_events_by_time__mutmut_17(
        self, events: list[FileEvent]
    ) -> list[list[FileEvent]]:
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
            groups.append(None)

        return groups

    xǁOperationDetectorǁ_group_events_by_time__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁOperationDetectorǁ_group_events_by_time__mutmut_1": xǁOperationDetectorǁ_group_events_by_time__mutmut_1,
        "xǁOperationDetectorǁ_group_events_by_time__mutmut_2": xǁOperationDetectorǁ_group_events_by_time__mutmut_2,
        "xǁOperationDetectorǁ_group_events_by_time__mutmut_3": xǁOperationDetectorǁ_group_events_by_time__mutmut_3,
        "xǁOperationDetectorǁ_group_events_by_time__mutmut_4": xǁOperationDetectorǁ_group_events_by_time__mutmut_4,
        "xǁOperationDetectorǁ_group_events_by_time__mutmut_5": xǁOperationDetectorǁ_group_events_by_time__mutmut_5,
        "xǁOperationDetectorǁ_group_events_by_time__mutmut_6": xǁOperationDetectorǁ_group_events_by_time__mutmut_6,
        "xǁOperationDetectorǁ_group_events_by_time__mutmut_7": xǁOperationDetectorǁ_group_events_by_time__mutmut_7,
        "xǁOperationDetectorǁ_group_events_by_time__mutmut_8": xǁOperationDetectorǁ_group_events_by_time__mutmut_8,
        "xǁOperationDetectorǁ_group_events_by_time__mutmut_9": xǁOperationDetectorǁ_group_events_by_time__mutmut_9,
        "xǁOperationDetectorǁ_group_events_by_time__mutmut_10": xǁOperationDetectorǁ_group_events_by_time__mutmut_10,
        "xǁOperationDetectorǁ_group_events_by_time__mutmut_11": xǁOperationDetectorǁ_group_events_by_time__mutmut_11,
        "xǁOperationDetectorǁ_group_events_by_time__mutmut_12": xǁOperationDetectorǁ_group_events_by_time__mutmut_12,
        "xǁOperationDetectorǁ_group_events_by_time__mutmut_13": xǁOperationDetectorǁ_group_events_by_time__mutmut_13,
        "xǁOperationDetectorǁ_group_events_by_time__mutmut_14": xǁOperationDetectorǁ_group_events_by_time__mutmut_14,
        "xǁOperationDetectorǁ_group_events_by_time__mutmut_15": xǁOperationDetectorǁ_group_events_by_time__mutmut_15,
        "xǁOperationDetectorǁ_group_events_by_time__mutmut_16": xǁOperationDetectorǁ_group_events_by_time__mutmut_16,
        "xǁOperationDetectorǁ_group_events_by_time__mutmut_17": xǁOperationDetectorǁ_group_events_by_time__mutmut_17,
    }

    def _group_events_by_time(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁOperationDetectorǁ_group_events_by_time__mutmut_orig"),
            object.__getattribute__(self, "xǁOperationDetectorǁ_group_events_by_time__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _group_events_by_time.__signature__ = _mutmut_signature(
        xǁOperationDetectorǁ_group_events_by_time__mutmut_orig
    )
    xǁOperationDetectorǁ_group_events_by_time__mutmut_orig.__name__ = (
        "xǁOperationDetectorǁ_group_events_by_time"
    )

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_orig(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_1(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Analyze a group of events to detect an operation using registry-based detectors.

        Performance optimizations:
        - Registry-based detector lookup (extensible)
        - Priority-ordered execution (highest priority first)
        - Early termination on high-confidence matches (>=0.95)
        """
        if events:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_2(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Analyze a group of events to detect an operation using registry-based detectors.

        Performance optimizations:
        - Registry-based detector lookup (extensible)
        - Priority-ordered execution (highest priority first)
        - Early termination on high-confidence matches (>=0.95)
        """
        if not events:
            return None

        # Get all registered detectors from the instance's registry, sorted by priority
        all_entries = None
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_3(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Analyze a group of events to detect an operation using registry-based detectors.

        Performance optimizations:
        - Registry-based detector lookup (extensible)
        - Priority-ordered execution (highest priority first)
        - Early termination on high-confidence matches (>=0.95)
        """
        if not events:
            return None

        # Get all registered detectors from the instance's registry, sorted by priority
        all_entries = [entry for entry in self.registry if entry.dimension != "file_operation_detector"]
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_4(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Analyze a group of events to detect an operation using registry-based detectors.

        Performance optimizations:
        - Registry-based detector lookup (extensible)
        - Priority-ordered execution (highest priority first)
        - Early termination on high-confidence matches (>=0.95)
        """
        if not events:
            return None

        # Get all registered detectors from the instance's registry, sorted by priority
        all_entries = [entry for entry in self.registry if entry.dimension == "XXfile_operation_detectorXX"]
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_5(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Analyze a group of events to detect an operation using registry-based detectors.

        Performance optimizations:
        - Registry-based detector lookup (extensible)
        - Priority-ordered execution (highest priority first)
        - Early termination on high-confidence matches (>=0.95)
        """
        if not events:
            return None

        # Get all registered detectors from the instance's registry, sorted by priority
        all_entries = [entry for entry in self.registry if entry.dimension == "FILE_OPERATION_DETECTOR"]
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_6(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        sorted_entries = None
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_7(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        sorted_entries = sorted(None, key=lambda e: e.metadata.get("priority", 0), reverse=True)
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_8(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        sorted_entries = sorted(all_entries, key=None, reverse=True)
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_9(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        sorted_entries = sorted(all_entries, key=lambda e: e.metadata.get("priority", 0), reverse=None)
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_10(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        sorted_entries = sorted(key=lambda e: e.metadata.get("priority", 0), reverse=True)
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_11(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        sorted_entries = sorted(all_entries, reverse=True)
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_12(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        sorted_entries = sorted(
            all_entries,
            key=lambda e: e.metadata.get("priority", 0),
        )
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_13(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        sorted_entries = sorted(all_entries, key=lambda e: None, reverse=True)
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_14(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        sorted_entries = sorted(all_entries, key=lambda e: e.metadata.get(None, 0), reverse=True)
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_15(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        sorted_entries = sorted(all_entries, key=lambda e: e.metadata.get("priority", None), reverse=True)
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_16(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        sorted_entries = sorted(all_entries, key=lambda e: e.metadata.get(0), reverse=True)
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_17(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        sorted_entries = sorted(
            all_entries,
            key=lambda e: e.metadata.get(
                "priority",
            ),
            reverse=True,
        )
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_18(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        sorted_entries = sorted(all_entries, key=lambda e: e.metadata.get("XXpriorityXX", 0), reverse=True)
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_19(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        sorted_entries = sorted(all_entries, key=lambda e: e.metadata.get("PRIORITY", 0), reverse=True)
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_20(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        sorted_entries = sorted(all_entries, key=lambda e: e.metadata.get("priority", 1), reverse=True)
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_21(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        sorted_entries = sorted(all_entries, key=lambda e: e.metadata.get("priority", 0), reverse=False)
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_22(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        detectors = None

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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_23(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        detectors = [(e.name, e.value, e.metadata.get(None, 0)) for e in sorted_entries]

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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_24(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        detectors = [(e.name, e.value, e.metadata.get("priority", None)) for e in sorted_entries]

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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_25(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        detectors = [(e.name, e.value, e.metadata.get(0)) for e in sorted_entries]

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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_26(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        detectors = [
            (
                e.name,
                e.value,
                e.metadata.get(
                    "priority",
                ),
            )
            for e in sorted_entries
        ]

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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_27(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        detectors = [(e.name, e.value, e.metadata.get("XXpriorityXX", 0)) for e in sorted_entries]

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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_28(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        detectors = [(e.name, e.value, e.metadata.get("PRIORITY", 0)) for e in sorted_entries]

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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_29(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        detectors = [(e.name, e.value, e.metadata.get("priority", 1)) for e in sorted_entries]

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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_30(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

        best_operation = ""
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_31(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        best_confidence = None
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_32(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        best_confidence = 1.0
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_33(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        HIGH_CONFIDENCE_THRESHOLD = None

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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_34(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
        HIGH_CONFIDENCE_THRESHOLD = 1.95

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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_35(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                operation = None
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_36(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                operation = detect_func(None)
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_37(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                if operation or operation.confidence > best_confidence:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_38(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                if operation and operation.confidence >= best_confidence:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_39(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                    best_operation = None
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_40(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                    best_confidence = None
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_41(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        None,
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_42(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        detector=None,
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_43(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        priority=None,
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_44(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        confidence=None,
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_45(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        operation_type=None,
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_46(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        primary_path=None,
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_47(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_48(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_49(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_50(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_51(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_52(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_53(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        "XXFound better operation matchXX",
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_54(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        "found better operation match",
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_55(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        "FOUND BETTER OPERATION MATCH",
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_56(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        primary_path=str(None),
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_57(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                    if best_confidence > HIGH_CONFIDENCE_THRESHOLD:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_58(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                            None,
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_59(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                            confidence=None,
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_60(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                            detector=None,
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_61(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_62(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_63(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_64(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                            "XXEarly termination on high confidence matchXX",
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_65(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                            "early termination on high confidence match",
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_66(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                            "EARLY TERMINATION ON HIGH CONFIDENCE MATCH",
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_67(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        return

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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_68(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                    None,
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_69(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                    detector=None,
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_70(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                    priority=None,
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_71(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                    error=None,
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_72(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_73(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_74(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_75(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_76(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                    "XXDetector failedXX",
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_77(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                    "detector failed",
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_78(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                    "DETECTOR FAILED",
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_79(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                    error=str(None),
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_80(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

        if best_operation or best_confidence >= self.config.min_confidence:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_81(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

        if best_operation and best_confidence > self.config.min_confidence:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_82(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
            if is_temp_file(None):
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_83(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                    None,
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_84(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                    temp_path=None,
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_85(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                    operation_type=None,
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_86(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_87(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_88(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_89(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                    "XXDetector returned temp file as primary_path, attempting to fixXX",
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_90(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                    "detector returned temp file as primary_path, attempting to fix",
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_91(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                    "DETECTOR RETURNED TEMP FILE AS PRIMARY_PATH, ATTEMPTING TO FIX",
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_92(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                    temp_path=str(None),
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_93(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                real_file = None
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_94(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                real_file = self._find_real_file_from_events(None)
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_95(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

                    best_operation = None
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_96(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

                    best_operation = evolve(None, primary_path=real_file)
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_97(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

                    best_operation = evolve(best_operation, primary_path=None)
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_98(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

                    best_operation = evolve(primary_path=real_file)
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_99(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

                    best_operation = evolve(
                        best_operation,
                    )
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_100(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        None,
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_101(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        corrected_path=None,
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_102(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_103(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_104(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        "XXCorrected primary_path from temp to real fileXX",
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_105(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        "corrected primary_path from temp to real file",
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_106(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        "CORRECTED PRIMARY_PATH FROM TEMP TO REAL FILE",
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_107(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        corrected_path=str(None),
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_108(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        None,
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_109(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        temp_path=None,
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_110(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_111(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_112(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        "XXCould not find real file, rejecting operationXX",
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_113(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        "could not find real file, rejecting operation",
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_114(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        "COULD NOT FIND REAL FILE, REJECTING OPERATION",
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_115(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                        temp_path=str(None),
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

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_116(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                None,
                operation_type=best_operation.operation_type.value,
                primary_path=str(best_operation.primary_path),
                confidence=best_confidence,
                is_temp=is_temp_file(best_operation.primary_path),
            )
            return best_operation

        return None

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_117(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                operation_type=None,
                primary_path=str(best_operation.primary_path),
                confidence=best_confidence,
                is_temp=is_temp_file(best_operation.primary_path),
            )
            return best_operation

        return None

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_118(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                primary_path=None,
                confidence=best_confidence,
                is_temp=is_temp_file(best_operation.primary_path),
            )
            return best_operation

        return None

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_119(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                confidence=None,
                is_temp=is_temp_file(best_operation.primary_path),
            )
            return best_operation

        return None

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_120(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                is_temp=None,
            )
            return best_operation

        return None

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_121(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                operation_type=best_operation.operation_type.value,
                primary_path=str(best_operation.primary_path),
                confidence=best_confidence,
                is_temp=is_temp_file(best_operation.primary_path),
            )
            return best_operation

        return None

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_122(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                primary_path=str(best_operation.primary_path),
                confidence=best_confidence,
                is_temp=is_temp_file(best_operation.primary_path),
            )
            return best_operation

        return None

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_123(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                confidence=best_confidence,
                is_temp=is_temp_file(best_operation.primary_path),
            )
            return best_operation

        return None

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_124(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                is_temp=is_temp_file(best_operation.primary_path),
            )
            return best_operation

        return None

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_125(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
            )
            return best_operation

        return None

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_126(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                "XXSelected operationXX",
                operation_type=best_operation.operation_type.value,
                primary_path=str(best_operation.primary_path),
                confidence=best_confidence,
                is_temp=is_temp_file(best_operation.primary_path),
            )
            return best_operation

        return None

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_127(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                "selected operation",
                operation_type=best_operation.operation_type.value,
                primary_path=str(best_operation.primary_path),
                confidence=best_confidence,
                is_temp=is_temp_file(best_operation.primary_path),
            )
            return best_operation

        return None

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_128(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                "SELECTED OPERATION",
                operation_type=best_operation.operation_type.value,
                primary_path=str(best_operation.primary_path),
                confidence=best_confidence,
                is_temp=is_temp_file(best_operation.primary_path),
            )
            return best_operation

        return None

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_129(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                primary_path=str(None),
                confidence=best_confidence,
                is_temp=is_temp_file(best_operation.primary_path),
            )
            return best_operation

        return None

    def xǁOperationDetectorǁ_analyze_event_group__mutmut_130(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
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
                is_temp=is_temp_file(None),
            )
            return best_operation

        return None

    xǁOperationDetectorǁ_analyze_event_group__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_1": xǁOperationDetectorǁ_analyze_event_group__mutmut_1,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_2": xǁOperationDetectorǁ_analyze_event_group__mutmut_2,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_3": xǁOperationDetectorǁ_analyze_event_group__mutmut_3,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_4": xǁOperationDetectorǁ_analyze_event_group__mutmut_4,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_5": xǁOperationDetectorǁ_analyze_event_group__mutmut_5,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_6": xǁOperationDetectorǁ_analyze_event_group__mutmut_6,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_7": xǁOperationDetectorǁ_analyze_event_group__mutmut_7,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_8": xǁOperationDetectorǁ_analyze_event_group__mutmut_8,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_9": xǁOperationDetectorǁ_analyze_event_group__mutmut_9,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_10": xǁOperationDetectorǁ_analyze_event_group__mutmut_10,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_11": xǁOperationDetectorǁ_analyze_event_group__mutmut_11,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_12": xǁOperationDetectorǁ_analyze_event_group__mutmut_12,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_13": xǁOperationDetectorǁ_analyze_event_group__mutmut_13,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_14": xǁOperationDetectorǁ_analyze_event_group__mutmut_14,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_15": xǁOperationDetectorǁ_analyze_event_group__mutmut_15,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_16": xǁOperationDetectorǁ_analyze_event_group__mutmut_16,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_17": xǁOperationDetectorǁ_analyze_event_group__mutmut_17,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_18": xǁOperationDetectorǁ_analyze_event_group__mutmut_18,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_19": xǁOperationDetectorǁ_analyze_event_group__mutmut_19,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_20": xǁOperationDetectorǁ_analyze_event_group__mutmut_20,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_21": xǁOperationDetectorǁ_analyze_event_group__mutmut_21,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_22": xǁOperationDetectorǁ_analyze_event_group__mutmut_22,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_23": xǁOperationDetectorǁ_analyze_event_group__mutmut_23,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_24": xǁOperationDetectorǁ_analyze_event_group__mutmut_24,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_25": xǁOperationDetectorǁ_analyze_event_group__mutmut_25,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_26": xǁOperationDetectorǁ_analyze_event_group__mutmut_26,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_27": xǁOperationDetectorǁ_analyze_event_group__mutmut_27,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_28": xǁOperationDetectorǁ_analyze_event_group__mutmut_28,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_29": xǁOperationDetectorǁ_analyze_event_group__mutmut_29,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_30": xǁOperationDetectorǁ_analyze_event_group__mutmut_30,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_31": xǁOperationDetectorǁ_analyze_event_group__mutmut_31,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_32": xǁOperationDetectorǁ_analyze_event_group__mutmut_32,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_33": xǁOperationDetectorǁ_analyze_event_group__mutmut_33,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_34": xǁOperationDetectorǁ_analyze_event_group__mutmut_34,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_35": xǁOperationDetectorǁ_analyze_event_group__mutmut_35,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_36": xǁOperationDetectorǁ_analyze_event_group__mutmut_36,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_37": xǁOperationDetectorǁ_analyze_event_group__mutmut_37,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_38": xǁOperationDetectorǁ_analyze_event_group__mutmut_38,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_39": xǁOperationDetectorǁ_analyze_event_group__mutmut_39,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_40": xǁOperationDetectorǁ_analyze_event_group__mutmut_40,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_41": xǁOperationDetectorǁ_analyze_event_group__mutmut_41,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_42": xǁOperationDetectorǁ_analyze_event_group__mutmut_42,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_43": xǁOperationDetectorǁ_analyze_event_group__mutmut_43,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_44": xǁOperationDetectorǁ_analyze_event_group__mutmut_44,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_45": xǁOperationDetectorǁ_analyze_event_group__mutmut_45,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_46": xǁOperationDetectorǁ_analyze_event_group__mutmut_46,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_47": xǁOperationDetectorǁ_analyze_event_group__mutmut_47,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_48": xǁOperationDetectorǁ_analyze_event_group__mutmut_48,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_49": xǁOperationDetectorǁ_analyze_event_group__mutmut_49,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_50": xǁOperationDetectorǁ_analyze_event_group__mutmut_50,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_51": xǁOperationDetectorǁ_analyze_event_group__mutmut_51,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_52": xǁOperationDetectorǁ_analyze_event_group__mutmut_52,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_53": xǁOperationDetectorǁ_analyze_event_group__mutmut_53,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_54": xǁOperationDetectorǁ_analyze_event_group__mutmut_54,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_55": xǁOperationDetectorǁ_analyze_event_group__mutmut_55,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_56": xǁOperationDetectorǁ_analyze_event_group__mutmut_56,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_57": xǁOperationDetectorǁ_analyze_event_group__mutmut_57,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_58": xǁOperationDetectorǁ_analyze_event_group__mutmut_58,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_59": xǁOperationDetectorǁ_analyze_event_group__mutmut_59,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_60": xǁOperationDetectorǁ_analyze_event_group__mutmut_60,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_61": xǁOperationDetectorǁ_analyze_event_group__mutmut_61,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_62": xǁOperationDetectorǁ_analyze_event_group__mutmut_62,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_63": xǁOperationDetectorǁ_analyze_event_group__mutmut_63,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_64": xǁOperationDetectorǁ_analyze_event_group__mutmut_64,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_65": xǁOperationDetectorǁ_analyze_event_group__mutmut_65,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_66": xǁOperationDetectorǁ_analyze_event_group__mutmut_66,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_67": xǁOperationDetectorǁ_analyze_event_group__mutmut_67,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_68": xǁOperationDetectorǁ_analyze_event_group__mutmut_68,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_69": xǁOperationDetectorǁ_analyze_event_group__mutmut_69,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_70": xǁOperationDetectorǁ_analyze_event_group__mutmut_70,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_71": xǁOperationDetectorǁ_analyze_event_group__mutmut_71,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_72": xǁOperationDetectorǁ_analyze_event_group__mutmut_72,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_73": xǁOperationDetectorǁ_analyze_event_group__mutmut_73,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_74": xǁOperationDetectorǁ_analyze_event_group__mutmut_74,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_75": xǁOperationDetectorǁ_analyze_event_group__mutmut_75,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_76": xǁOperationDetectorǁ_analyze_event_group__mutmut_76,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_77": xǁOperationDetectorǁ_analyze_event_group__mutmut_77,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_78": xǁOperationDetectorǁ_analyze_event_group__mutmut_78,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_79": xǁOperationDetectorǁ_analyze_event_group__mutmut_79,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_80": xǁOperationDetectorǁ_analyze_event_group__mutmut_80,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_81": xǁOperationDetectorǁ_analyze_event_group__mutmut_81,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_82": xǁOperationDetectorǁ_analyze_event_group__mutmut_82,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_83": xǁOperationDetectorǁ_analyze_event_group__mutmut_83,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_84": xǁOperationDetectorǁ_analyze_event_group__mutmut_84,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_85": xǁOperationDetectorǁ_analyze_event_group__mutmut_85,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_86": xǁOperationDetectorǁ_analyze_event_group__mutmut_86,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_87": xǁOperationDetectorǁ_analyze_event_group__mutmut_87,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_88": xǁOperationDetectorǁ_analyze_event_group__mutmut_88,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_89": xǁOperationDetectorǁ_analyze_event_group__mutmut_89,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_90": xǁOperationDetectorǁ_analyze_event_group__mutmut_90,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_91": xǁOperationDetectorǁ_analyze_event_group__mutmut_91,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_92": xǁOperationDetectorǁ_analyze_event_group__mutmut_92,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_93": xǁOperationDetectorǁ_analyze_event_group__mutmut_93,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_94": xǁOperationDetectorǁ_analyze_event_group__mutmut_94,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_95": xǁOperationDetectorǁ_analyze_event_group__mutmut_95,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_96": xǁOperationDetectorǁ_analyze_event_group__mutmut_96,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_97": xǁOperationDetectorǁ_analyze_event_group__mutmut_97,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_98": xǁOperationDetectorǁ_analyze_event_group__mutmut_98,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_99": xǁOperationDetectorǁ_analyze_event_group__mutmut_99,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_100": xǁOperationDetectorǁ_analyze_event_group__mutmut_100,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_101": xǁOperationDetectorǁ_analyze_event_group__mutmut_101,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_102": xǁOperationDetectorǁ_analyze_event_group__mutmut_102,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_103": xǁOperationDetectorǁ_analyze_event_group__mutmut_103,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_104": xǁOperationDetectorǁ_analyze_event_group__mutmut_104,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_105": xǁOperationDetectorǁ_analyze_event_group__mutmut_105,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_106": xǁOperationDetectorǁ_analyze_event_group__mutmut_106,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_107": xǁOperationDetectorǁ_analyze_event_group__mutmut_107,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_108": xǁOperationDetectorǁ_analyze_event_group__mutmut_108,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_109": xǁOperationDetectorǁ_analyze_event_group__mutmut_109,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_110": xǁOperationDetectorǁ_analyze_event_group__mutmut_110,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_111": xǁOperationDetectorǁ_analyze_event_group__mutmut_111,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_112": xǁOperationDetectorǁ_analyze_event_group__mutmut_112,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_113": xǁOperationDetectorǁ_analyze_event_group__mutmut_113,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_114": xǁOperationDetectorǁ_analyze_event_group__mutmut_114,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_115": xǁOperationDetectorǁ_analyze_event_group__mutmut_115,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_116": xǁOperationDetectorǁ_analyze_event_group__mutmut_116,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_117": xǁOperationDetectorǁ_analyze_event_group__mutmut_117,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_118": xǁOperationDetectorǁ_analyze_event_group__mutmut_118,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_119": xǁOperationDetectorǁ_analyze_event_group__mutmut_119,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_120": xǁOperationDetectorǁ_analyze_event_group__mutmut_120,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_121": xǁOperationDetectorǁ_analyze_event_group__mutmut_121,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_122": xǁOperationDetectorǁ_analyze_event_group__mutmut_122,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_123": xǁOperationDetectorǁ_analyze_event_group__mutmut_123,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_124": xǁOperationDetectorǁ_analyze_event_group__mutmut_124,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_125": xǁOperationDetectorǁ_analyze_event_group__mutmut_125,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_126": xǁOperationDetectorǁ_analyze_event_group__mutmut_126,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_127": xǁOperationDetectorǁ_analyze_event_group__mutmut_127,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_128": xǁOperationDetectorǁ_analyze_event_group__mutmut_128,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_129": xǁOperationDetectorǁ_analyze_event_group__mutmut_129,
        "xǁOperationDetectorǁ_analyze_event_group__mutmut_130": xǁOperationDetectorǁ_analyze_event_group__mutmut_130,
    }

    def _analyze_event_group(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁOperationDetectorǁ_analyze_event_group__mutmut_orig"),
            object.__getattribute__(self, "xǁOperationDetectorǁ_analyze_event_group__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _analyze_event_group.__signature__ = _mutmut_signature(
        xǁOperationDetectorǁ_analyze_event_group__mutmut_orig
    )
    xǁOperationDetectorǁ_analyze_event_group__mutmut_orig.__name__ = "xǁOperationDetectorǁ_analyze_event_group"

    def xǁOperationDetectorǁ_find_real_file_from_events__mutmut_orig(
        self, events: list[FileEvent]
    ) -> Path | None:
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

    def xǁOperationDetectorǁ_find_real_file_from_events__mutmut_1(
        self, events: list[FileEvent]
    ) -> Path | None:
        """Find the real (non-temp) file path from a list of events."""
        # Look for non-temp files in the events
        for event in reversed(None):  # Start from most recent
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

    def xǁOperationDetectorǁ_find_real_file_from_events__mutmut_2(
        self, events: list[FileEvent]
    ) -> Path | None:
        """Find the real (non-temp) file path from a list of events."""
        # Look for non-temp files in the events
        for event in reversed(events):  # Start from most recent
            # Check dest_path first (for move/rename operations)
            if event.dest_path or not is_temp_file(event.dest_path):
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

    def xǁOperationDetectorǁ_find_real_file_from_events__mutmut_3(
        self, events: list[FileEvent]
    ) -> Path | None:
        """Find the real (non-temp) file path from a list of events."""
        # Look for non-temp files in the events
        for event in reversed(events):  # Start from most recent
            # Check dest_path first (for move/rename operations)
            if event.dest_path and is_temp_file(event.dest_path):
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

    def xǁOperationDetectorǁ_find_real_file_from_events__mutmut_4(
        self, events: list[FileEvent]
    ) -> Path | None:
        """Find the real (non-temp) file path from a list of events."""
        # Look for non-temp files in the events
        for event in reversed(events):  # Start from most recent
            # Check dest_path first (for move/rename operations)
            if event.dest_path and not is_temp_file(None):
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

    def xǁOperationDetectorǁ_find_real_file_from_events__mutmut_5(
        self, events: list[FileEvent]
    ) -> Path | None:
        """Find the real (non-temp) file path from a list of events."""
        # Look for non-temp files in the events
        for event in reversed(events):  # Start from most recent
            # Check dest_path first (for move/rename operations)
            if event.dest_path and not is_temp_file(event.dest_path):
                return event.dest_path
            # Then check regular path
            if is_temp_file(event.path):
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

    def xǁOperationDetectorǁ_find_real_file_from_events__mutmut_6(
        self, events: list[FileEvent]
    ) -> Path | None:
        """Find the real (non-temp) file path from a list of events."""
        # Look for non-temp files in the events
        for event in reversed(events):  # Start from most recent
            # Check dest_path first (for move/rename operations)
            if event.dest_path and not is_temp_file(event.dest_path):
                return event.dest_path
            # Then check regular path
            if not is_temp_file(None):
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

    def xǁOperationDetectorǁ_find_real_file_from_events__mutmut_7(
        self, events: list[FileEvent]
    ) -> Path | None:
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
                base_name = None
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

    def xǁOperationDetectorǁ_find_real_file_from_events__mutmut_8(
        self, events: list[FileEvent]
    ) -> Path | None:
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
                base_name = extract_base_name(None)
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

    def xǁOperationDetectorǁ_find_real_file_from_events__mutmut_9(
        self, events: list[FileEvent]
    ) -> Path | None:
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
                    real_path = None
                    if real_path != event.dest_path:
                        return real_path

            base_name = extract_base_name(event.path)
            if base_name:
                real_path = event.path.parent / base_name
                if real_path != event.path:
                    return real_path

        return None

    def xǁOperationDetectorǁ_find_real_file_from_events__mutmut_10(
        self, events: list[FileEvent]
    ) -> Path | None:
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
                    real_path = event.dest_path.parent * base_name
                    if real_path != event.dest_path:
                        return real_path

            base_name = extract_base_name(event.path)
            if base_name:
                real_path = event.path.parent / base_name
                if real_path != event.path:
                    return real_path

        return None

    def xǁOperationDetectorǁ_find_real_file_from_events__mutmut_11(
        self, events: list[FileEvent]
    ) -> Path | None:
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
                    if real_path == event.dest_path:
                        return real_path

            base_name = extract_base_name(event.path)
            if base_name:
                real_path = event.path.parent / base_name
                if real_path != event.path:
                    return real_path

        return None

    def xǁOperationDetectorǁ_find_real_file_from_events__mutmut_12(
        self, events: list[FileEvent]
    ) -> Path | None:
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

            base_name = None
            if base_name:
                real_path = event.path.parent / base_name
                if real_path != event.path:
                    return real_path

        return None

    def xǁOperationDetectorǁ_find_real_file_from_events__mutmut_13(
        self, events: list[FileEvent]
    ) -> Path | None:
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

            base_name = extract_base_name(None)
            if base_name:
                real_path = event.path.parent / base_name
                if real_path != event.path:
                    return real_path

        return None

    def xǁOperationDetectorǁ_find_real_file_from_events__mutmut_14(
        self, events: list[FileEvent]
    ) -> Path | None:
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
                real_path = None
                if real_path != event.path:
                    return real_path

        return None

    def xǁOperationDetectorǁ_find_real_file_from_events__mutmut_15(
        self, events: list[FileEvent]
    ) -> Path | None:
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
                real_path = event.path.parent * base_name
                if real_path != event.path:
                    return real_path

        return None

    def xǁOperationDetectorǁ_find_real_file_from_events__mutmut_16(
        self, events: list[FileEvent]
    ) -> Path | None:
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
                if real_path == event.path:
                    return real_path

        return None

    xǁOperationDetectorǁ_find_real_file_from_events__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁOperationDetectorǁ_find_real_file_from_events__mutmut_1": xǁOperationDetectorǁ_find_real_file_from_events__mutmut_1,
        "xǁOperationDetectorǁ_find_real_file_from_events__mutmut_2": xǁOperationDetectorǁ_find_real_file_from_events__mutmut_2,
        "xǁOperationDetectorǁ_find_real_file_from_events__mutmut_3": xǁOperationDetectorǁ_find_real_file_from_events__mutmut_3,
        "xǁOperationDetectorǁ_find_real_file_from_events__mutmut_4": xǁOperationDetectorǁ_find_real_file_from_events__mutmut_4,
        "xǁOperationDetectorǁ_find_real_file_from_events__mutmut_5": xǁOperationDetectorǁ_find_real_file_from_events__mutmut_5,
        "xǁOperationDetectorǁ_find_real_file_from_events__mutmut_6": xǁOperationDetectorǁ_find_real_file_from_events__mutmut_6,
        "xǁOperationDetectorǁ_find_real_file_from_events__mutmut_7": xǁOperationDetectorǁ_find_real_file_from_events__mutmut_7,
        "xǁOperationDetectorǁ_find_real_file_from_events__mutmut_8": xǁOperationDetectorǁ_find_real_file_from_events__mutmut_8,
        "xǁOperationDetectorǁ_find_real_file_from_events__mutmut_9": xǁOperationDetectorǁ_find_real_file_from_events__mutmut_9,
        "xǁOperationDetectorǁ_find_real_file_from_events__mutmut_10": xǁOperationDetectorǁ_find_real_file_from_events__mutmut_10,
        "xǁOperationDetectorǁ_find_real_file_from_events__mutmut_11": xǁOperationDetectorǁ_find_real_file_from_events__mutmut_11,
        "xǁOperationDetectorǁ_find_real_file_from_events__mutmut_12": xǁOperationDetectorǁ_find_real_file_from_events__mutmut_12,
        "xǁOperationDetectorǁ_find_real_file_from_events__mutmut_13": xǁOperationDetectorǁ_find_real_file_from_events__mutmut_13,
        "xǁOperationDetectorǁ_find_real_file_from_events__mutmut_14": xǁOperationDetectorǁ_find_real_file_from_events__mutmut_14,
        "xǁOperationDetectorǁ_find_real_file_from_events__mutmut_15": xǁOperationDetectorǁ_find_real_file_from_events__mutmut_15,
        "xǁOperationDetectorǁ_find_real_file_from_events__mutmut_16": xǁOperationDetectorǁ_find_real_file_from_events__mutmut_16,
    }

    def _find_real_file_from_events(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁOperationDetectorǁ_find_real_file_from_events__mutmut_orig"),
            object.__getattribute__(self, "xǁOperationDetectorǁ_find_real_file_from_events__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _find_real_file_from_events.__signature__ = _mutmut_signature(
        xǁOperationDetectorǁ_find_real_file_from_events__mutmut_orig
    )
    xǁOperationDetectorǁ_find_real_file_from_events__mutmut_orig.__name__ = (
        "xǁOperationDetectorǁ_find_real_file_from_events"
    )


# <3 🧱🤝📄🪄
