#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Simple functional API for file operation detection.

This module provides a minimal, user-friendly API for detecting file operations
from filesystem events. It hides the complexity of the underlying detector system
while providing all necessary functionality.

Examples:
    >>> from provide.foundation.file.operations import detect, Event
    >>>
    >>> # Single operation detection
    >>> events = [Event(...), Event(...)]
    >>> operation = detect(events)
    >>> if operation:
    ...     print(f"{operation.type}: {operation.path}")
    >>>
    >>> # Multiple operations detection
    >>> operations = detect_all(events)
    >>> for op in operations:
    ...     print(f"{op.type}: {op.path}")"""

from __future__ import annotations

from typing import overload

from provide.foundation.file.operations.detectors.orchestrator import OperationDetector
from provide.foundation.file.operations.types import (
    DetectorConfig,
    FileEvent,
    FileOperation,
)

# Create module-level detector for simple usage
_default_detector: OperationDetector | None = None


def _get_default_detector() -> OperationDetector:
    """Get or create the default detector instance."""
    global _default_detector
    if _default_detector is None:
        _default_detector = OperationDetector()
    return _default_detector


@overload
def detect(events: FileEvent) -> FileOperation | None: ...


@overload
def detect(events: list[FileEvent]) -> list[FileOperation]: ...


def detect(
    events: FileEvent | list[FileEvent], config: DetectorConfig | None = None
) -> FileOperation | list[FileOperation] | None:
    """Detect file operations from event(s).

    This is the primary API for operation detection. It automatically determines
    whether to return a single operation or a list based on the input type.

    Args:
        events: Single event or list of events to analyze
        config: Optional detector configuration (uses defaults if not provided)

    Returns:
        - If single event provided: FileOperation | None
        - If list provided: list[FileOperation] (may be empty)

    Examples:
        >>> # Single event
        >>> operation = detect(event)
        >>> if operation:
        ...     print(f"Found: {operation.operation_type}")
        >>>
        >>> # Multiple events
        >>> operations = detect(event_list)
        >>> print(f"Found {len(operations)} operations")
    """
    # Create detector (use cached default or new one with custom config)
    detector = _get_default_detector() if config is None else OperationDetector(config)

    # Handle single event
    if isinstance(events, FileEvent):
        results = detector.detect([events])
        return results[0] if results else None

    # Handle list of events
    return detector.detect(events)


def detect_all(events: list[FileEvent], config: DetectorConfig | None = None) -> list[FileOperation]:
    """Detect all operations from a list of events.

    Explicit function for when you always want a list result, even for single events.

    Args:
        events: List of events to analyze
        config: Optional detector configuration

    Returns:
        List of detected operations (may be empty)

    Examples:
        >>> operations = detect_all(events)
        >>> for op in operations:
        ...     print(f"{op.operation_type}: {op.primary_path}")
    """
    detector = _get_default_detector() if config is None else OperationDetector(config)
    return detector.detect(events)


def detect_streaming(
    event: FileEvent,
    detector: OperationDetector | None = None,
) -> FileOperation | None:
    """Process a single event in streaming mode.

    For real-time detection, use this with a persistent OperationDetector instance.
    Operations are returned when patterns are detected based on time windows.

    Args:
        event: Single file event to process
        detector: Optional persistent detector instance (required for stateful detection)

    Returns:
        Completed operation if detected, None otherwise

    Examples:
        >>> # Create persistent detector for streaming
        >>> from provide.foundation.file.operations import OperationDetector
        >>> detector = OperationDetector()
        >>>
        >>> # Feed events as they arrive
        >>> for event in event_stream:
        ...     operation = detect_streaming(event, detector)
        ...     if operation:
        ...         print(f"Operation detected: {operation.operation_type}")
        >>>
        >>> # Flush at end
        >>> remaining = detector.flush()

    Note:
        This is a lower-level API. For most use cases, the batch `detect()` function
        is simpler and sufficient.
    """
    if detector is None:
        detector = _get_default_detector()

    return detector.detect_streaming(event)


# For backward compatibility and convenience
def create_detector(config: DetectorConfig | None = None) -> OperationDetector:
    """Create a new operation detector instance.

    Use this when you need a persistent detector for streaming detection
    or want custom configuration.

    Args:
        config: Optional detector configuration

    Returns:
        New OperationDetector instance

    Examples:
        >>> from provide.foundation.file.operations import create_detector, DetectorConfig
        >>>
        >>> # Custom configuration
        >>> config = DetectorConfig(time_window_ms=1000, min_confidence=0.8)
        >>> detector = create_detector(config)
        >>>
        >>> # Use for streaming
        >>> for event in events:
        ...     operation = detector.detect_streaming(event)
    """
    return OperationDetector(config)


# 🧱🏗️🔚
