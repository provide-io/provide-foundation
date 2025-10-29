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
    ...     print(f"{op.type}: {op.path}")
"""

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


def x__get_default_detector__mutmut_orig() -> OperationDetector:
    """Get or create the default detector instance."""
    global _default_detector
    if _default_detector is None:
        _default_detector = OperationDetector()
    return _default_detector


def x__get_default_detector__mutmut_1() -> OperationDetector:
    """Get or create the default detector instance."""
    global _default_detector
    if _default_detector is not None:
        _default_detector = OperationDetector()
    return _default_detector


def x__get_default_detector__mutmut_2() -> OperationDetector:
    """Get or create the default detector instance."""
    global _default_detector
    if _default_detector is None:
        _default_detector = None
    return _default_detector


x__get_default_detector__mutmut_mutants: ClassVar[MutantDict] = {
    "x__get_default_detector__mutmut_1": x__get_default_detector__mutmut_1,
    "x__get_default_detector__mutmut_2": x__get_default_detector__mutmut_2,
}


def _get_default_detector(*args, **kwargs):
    result = _mutmut_trampoline(
        x__get_default_detector__mutmut_orig, x__get_default_detector__mutmut_mutants, args, kwargs
    )
    return result


_get_default_detector.__signature__ = _mutmut_signature(x__get_default_detector__mutmut_orig)
x__get_default_detector__mutmut_orig.__name__ = "x__get_default_detector"


@overload
def detect(events: FileEvent) -> FileOperation | None: ...


@overload
def detect(events: list[FileEvent]) -> list[FileOperation]: ...


def x_detect__mutmut_orig(
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


def x_detect__mutmut_1(
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
    detector = None

    # Handle single event
    if isinstance(events, FileEvent):
        results = detector.detect([events])
        return results[0] if results else None

    # Handle list of events
    return detector.detect(events)


def x_detect__mutmut_2(
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
    detector = _get_default_detector() if config is not None else OperationDetector(config)

    # Handle single event
    if isinstance(events, FileEvent):
        results = detector.detect([events])
        return results[0] if results else None

    # Handle list of events
    return detector.detect(events)


def x_detect__mutmut_3(
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
    detector = _get_default_detector() if config is None else OperationDetector(None)

    # Handle single event
    if isinstance(events, FileEvent):
        results = detector.detect([events])
        return results[0] if results else None

    # Handle list of events
    return detector.detect(events)


def x_detect__mutmut_4(
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
        results = None
        return results[0] if results else None

    # Handle list of events
    return detector.detect(events)


def x_detect__mutmut_5(
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
        results = detector.detect(None)
        return results[0] if results else None

    # Handle list of events
    return detector.detect(events)


def x_detect__mutmut_6(
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
        return results[1] if results else None

    # Handle list of events
    return detector.detect(events)


def x_detect__mutmut_7(
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
    return detector.detect(None)


x_detect__mutmut_mutants: ClassVar[MutantDict] = {
    "x_detect__mutmut_1": x_detect__mutmut_1,
    "x_detect__mutmut_2": x_detect__mutmut_2,
    "x_detect__mutmut_3": x_detect__mutmut_3,
    "x_detect__mutmut_4": x_detect__mutmut_4,
    "x_detect__mutmut_5": x_detect__mutmut_5,
    "x_detect__mutmut_6": x_detect__mutmut_6,
    "x_detect__mutmut_7": x_detect__mutmut_7,
}


def detect(*args, **kwargs):
    result = _mutmut_trampoline(x_detect__mutmut_orig, x_detect__mutmut_mutants, args, kwargs)
    return result


detect.__signature__ = _mutmut_signature(x_detect__mutmut_orig)
x_detect__mutmut_orig.__name__ = "x_detect"


def x_detect_all__mutmut_orig(
    events: list[FileEvent], config: DetectorConfig | None = None
) -> list[FileOperation]:
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


def x_detect_all__mutmut_1(
    events: list[FileEvent], config: DetectorConfig | None = None
) -> list[FileOperation]:
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
    detector = None
    return detector.detect(events)


def x_detect_all__mutmut_2(
    events: list[FileEvent], config: DetectorConfig | None = None
) -> list[FileOperation]:
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
    detector = _get_default_detector() if config is not None else OperationDetector(config)
    return detector.detect(events)


def x_detect_all__mutmut_3(
    events: list[FileEvent], config: DetectorConfig | None = None
) -> list[FileOperation]:
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
    detector = _get_default_detector() if config is None else OperationDetector(None)
    return detector.detect(events)


def x_detect_all__mutmut_4(
    events: list[FileEvent], config: DetectorConfig | None = None
) -> list[FileOperation]:
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
    return detector.detect(None)


x_detect_all__mutmut_mutants: ClassVar[MutantDict] = {
    "x_detect_all__mutmut_1": x_detect_all__mutmut_1,
    "x_detect_all__mutmut_2": x_detect_all__mutmut_2,
    "x_detect_all__mutmut_3": x_detect_all__mutmut_3,
    "x_detect_all__mutmut_4": x_detect_all__mutmut_4,
}


def detect_all(*args, **kwargs):
    result = _mutmut_trampoline(x_detect_all__mutmut_orig, x_detect_all__mutmut_mutants, args, kwargs)
    return result


detect_all.__signature__ = _mutmut_signature(x_detect_all__mutmut_orig)
x_detect_all__mutmut_orig.__name__ = "x_detect_all"


def x_detect_streaming__mutmut_orig(
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


def x_detect_streaming__mutmut_1(
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
    if detector is not None:
        detector = _get_default_detector()

    return detector.detect_streaming(event)


def x_detect_streaming__mutmut_2(
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
        detector = None

    return detector.detect_streaming(event)


def x_detect_streaming__mutmut_3(
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

    return detector.detect_streaming(None)


x_detect_streaming__mutmut_mutants: ClassVar[MutantDict] = {
    "x_detect_streaming__mutmut_1": x_detect_streaming__mutmut_1,
    "x_detect_streaming__mutmut_2": x_detect_streaming__mutmut_2,
    "x_detect_streaming__mutmut_3": x_detect_streaming__mutmut_3,
}


def detect_streaming(*args, **kwargs):
    result = _mutmut_trampoline(
        x_detect_streaming__mutmut_orig, x_detect_streaming__mutmut_mutants, args, kwargs
    )
    return result


detect_streaming.__signature__ = _mutmut_signature(x_detect_streaming__mutmut_orig)
x_detect_streaming__mutmut_orig.__name__ = "x_detect_streaming"


# For backward compatibility and convenience
def x_create_detector__mutmut_orig(config: DetectorConfig | None = None) -> OperationDetector:
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


# For backward compatibility and convenience
def x_create_detector__mutmut_1(config: DetectorConfig | None = None) -> OperationDetector:
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
    return OperationDetector(None)


x_create_detector__mutmut_mutants: ClassVar[MutantDict] = {
    "x_create_detector__mutmut_1": x_create_detector__mutmut_1
}


def create_detector(*args, **kwargs):
    result = _mutmut_trampoline(
        x_create_detector__mutmut_orig, x_create_detector__mutmut_mutants, args, kwargs
    )
    return result


create_detector.__signature__ = _mutmut_signature(x_create_detector__mutmut_orig)
x_create_detector__mutmut_orig.__name__ = "x_create_detector"
