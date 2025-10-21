# provide/foundation/file/operations/utils.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Utility functions for file operation detection."""

from __future__ import annotations

from pathlib import Path

from provide.foundation.file.operations.types import DetectorConfig, FileEvent, FileOperation, OperationType
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


def x_detect_atomic_save__mutmut_orig(events: list[FileEvent]) -> FileOperation | None:
    """Detect if events represent an atomic save operation."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    detector = OperationDetector()
    operations = detector.detect(events)
    return next((op for op in operations if op.operation_type == OperationType.ATOMIC_SAVE), None)


def x_detect_atomic_save__mutmut_1(events: list[FileEvent]) -> FileOperation | None:
    """Detect if events represent an atomic save operation."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    detector = None
    operations = detector.detect(events)
    return next((op for op in operations if op.operation_type == OperationType.ATOMIC_SAVE), None)


def x_detect_atomic_save__mutmut_2(events: list[FileEvent]) -> FileOperation | None:
    """Detect if events represent an atomic save operation."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    detector = OperationDetector()
    operations = None
    return next((op for op in operations if op.operation_type == OperationType.ATOMIC_SAVE), None)


def x_detect_atomic_save__mutmut_3(events: list[FileEvent]) -> FileOperation | None:
    """Detect if events represent an atomic save operation."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    detector = OperationDetector()
    operations = detector.detect(None)
    return next((op for op in operations if op.operation_type == OperationType.ATOMIC_SAVE), None)


def x_detect_atomic_save__mutmut_4(events: list[FileEvent]) -> FileOperation | None:
    """Detect if events represent an atomic save operation."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    detector = OperationDetector()
    operations = detector.detect(events)
    return next(None, None)


def x_detect_atomic_save__mutmut_5(events: list[FileEvent]) -> FileOperation | None:
    """Detect if events represent an atomic save operation."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    detector = OperationDetector()
    operations = detector.detect(events)
    return next(None)


def x_detect_atomic_save__mutmut_6(events: list[FileEvent]) -> FileOperation | None:
    """Detect if events represent an atomic save operation."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    detector = OperationDetector()
    operations = detector.detect(events)
    return next((op for op in operations if op.operation_type == OperationType.ATOMIC_SAVE), )


def x_detect_atomic_save__mutmut_7(events: list[FileEvent]) -> FileOperation | None:
    """Detect if events represent an atomic save operation."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    detector = OperationDetector()
    operations = detector.detect(events)
    return next((op for op in operations if op.operation_type != OperationType.ATOMIC_SAVE), None)

x_detect_atomic_save__mutmut_mutants : ClassVar[MutantDict] = {
'x_detect_atomic_save__mutmut_1': x_detect_atomic_save__mutmut_1, 
    'x_detect_atomic_save__mutmut_2': x_detect_atomic_save__mutmut_2, 
    'x_detect_atomic_save__mutmut_3': x_detect_atomic_save__mutmut_3, 
    'x_detect_atomic_save__mutmut_4': x_detect_atomic_save__mutmut_4, 
    'x_detect_atomic_save__mutmut_5': x_detect_atomic_save__mutmut_5, 
    'x_detect_atomic_save__mutmut_6': x_detect_atomic_save__mutmut_6, 
    'x_detect_atomic_save__mutmut_7': x_detect_atomic_save__mutmut_7
}

def detect_atomic_save(*args, **kwargs):
    result = _mutmut_trampoline(x_detect_atomic_save__mutmut_orig, x_detect_atomic_save__mutmut_mutants, args, kwargs)
    return result 

detect_atomic_save.__signature__ = _mutmut_signature(x_detect_atomic_save__mutmut_orig)
x_detect_atomic_save__mutmut_orig.__name__ = 'x_detect_atomic_save'


def x_is_temp_file__mutmut_orig(path: Path) -> bool:
    """Check if a path represents a temporary file."""
    from provide.foundation.file.operations.detectors.helpers import is_temp_file as helper_is_temp_file

    return helper_is_temp_file(path)


def x_is_temp_file__mutmut_1(path: Path) -> bool:
    """Check if a path represents a temporary file."""
    from provide.foundation.file.operations.detectors.helpers import is_temp_file as helper_is_temp_file

    return helper_is_temp_file(None)

x_is_temp_file__mutmut_mutants : ClassVar[MutantDict] = {
'x_is_temp_file__mutmut_1': x_is_temp_file__mutmut_1
}

def is_temp_file(*args, **kwargs):
    result = _mutmut_trampoline(x_is_temp_file__mutmut_orig, x_is_temp_file__mutmut_mutants, args, kwargs)
    return result 

is_temp_file.__signature__ = _mutmut_signature(x_is_temp_file__mutmut_orig)
x_is_temp_file__mutmut_orig.__name__ = 'x_is_temp_file'


def x_extract_original_path__mutmut_orig(temp_path: Path) -> Path | None:
    """Extract the original filename from a temp file path."""
    from provide.foundation.file.operations.detectors.helpers import extract_base_name

    base_name = extract_base_name(temp_path)
    if base_name:
        return temp_path.parent / base_name
    else:
        # If no temp pattern matches, return the original path
        return temp_path


def x_extract_original_path__mutmut_1(temp_path: Path) -> Path | None:
    """Extract the original filename from a temp file path."""
    from provide.foundation.file.operations.detectors.helpers import extract_base_name

    base_name = None
    if base_name:
        return temp_path.parent / base_name
    else:
        # If no temp pattern matches, return the original path
        return temp_path


def x_extract_original_path__mutmut_2(temp_path: Path) -> Path | None:
    """Extract the original filename from a temp file path."""
    from provide.foundation.file.operations.detectors.helpers import extract_base_name

    base_name = extract_base_name(None)
    if base_name:
        return temp_path.parent / base_name
    else:
        # If no temp pattern matches, return the original path
        return temp_path


def x_extract_original_path__mutmut_3(temp_path: Path) -> Path | None:
    """Extract the original filename from a temp file path."""
    from provide.foundation.file.operations.detectors.helpers import extract_base_name

    base_name = extract_base_name(temp_path)
    if base_name:
        return temp_path.parent * base_name
    else:
        # If no temp pattern matches, return the original path
        return temp_path

x_extract_original_path__mutmut_mutants : ClassVar[MutantDict] = {
'x_extract_original_path__mutmut_1': x_extract_original_path__mutmut_1, 
    'x_extract_original_path__mutmut_2': x_extract_original_path__mutmut_2, 
    'x_extract_original_path__mutmut_3': x_extract_original_path__mutmut_3
}

def extract_original_path(*args, **kwargs):
    result = _mutmut_trampoline(x_extract_original_path__mutmut_orig, x_extract_original_path__mutmut_mutants, args, kwargs)
    return result 

extract_original_path.__signature__ = _mutmut_signature(x_extract_original_path__mutmut_orig)
x_extract_original_path__mutmut_orig.__name__ = 'x_extract_original_path'


def x_group_related_events__mutmut_orig(events: list[FileEvent], time_window_ms: int = 500) -> list[list[FileEvent]]:
    """Group events that occur within a time window."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    config = DetectorConfig(time_window_ms=time_window_ms)
    detector = OperationDetector(config)
    return detector._group_events_by_time(sorted(events, key=lambda e: e.timestamp))


def x_group_related_events__mutmut_1(events: list[FileEvent], time_window_ms: int = 501) -> list[list[FileEvent]]:
    """Group events that occur within a time window."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    config = DetectorConfig(time_window_ms=time_window_ms)
    detector = OperationDetector(config)
    return detector._group_events_by_time(sorted(events, key=lambda e: e.timestamp))


def x_group_related_events__mutmut_2(events: list[FileEvent], time_window_ms: int = 500) -> list[list[FileEvent]]:
    """Group events that occur within a time window."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    config = None
    detector = OperationDetector(config)
    return detector._group_events_by_time(sorted(events, key=lambda e: e.timestamp))


def x_group_related_events__mutmut_3(events: list[FileEvent], time_window_ms: int = 500) -> list[list[FileEvent]]:
    """Group events that occur within a time window."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    config = DetectorConfig(time_window_ms=None)
    detector = OperationDetector(config)
    return detector._group_events_by_time(sorted(events, key=lambda e: e.timestamp))


def x_group_related_events__mutmut_4(events: list[FileEvent], time_window_ms: int = 500) -> list[list[FileEvent]]:
    """Group events that occur within a time window."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    config = DetectorConfig(time_window_ms=time_window_ms)
    detector = None
    return detector._group_events_by_time(sorted(events, key=lambda e: e.timestamp))


def x_group_related_events__mutmut_5(events: list[FileEvent], time_window_ms: int = 500) -> list[list[FileEvent]]:
    """Group events that occur within a time window."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    config = DetectorConfig(time_window_ms=time_window_ms)
    detector = OperationDetector(None)
    return detector._group_events_by_time(sorted(events, key=lambda e: e.timestamp))


def x_group_related_events__mutmut_6(events: list[FileEvent], time_window_ms: int = 500) -> list[list[FileEvent]]:
    """Group events that occur within a time window."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    config = DetectorConfig(time_window_ms=time_window_ms)
    detector = OperationDetector(config)
    return detector._group_events_by_time(None)


def x_group_related_events__mutmut_7(events: list[FileEvent], time_window_ms: int = 500) -> list[list[FileEvent]]:
    """Group events that occur within a time window."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    config = DetectorConfig(time_window_ms=time_window_ms)
    detector = OperationDetector(config)
    return detector._group_events_by_time(sorted(None, key=lambda e: e.timestamp))


def x_group_related_events__mutmut_8(events: list[FileEvent], time_window_ms: int = 500) -> list[list[FileEvent]]:
    """Group events that occur within a time window."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    config = DetectorConfig(time_window_ms=time_window_ms)
    detector = OperationDetector(config)
    return detector._group_events_by_time(sorted(events, key=None))


def x_group_related_events__mutmut_9(events: list[FileEvent], time_window_ms: int = 500) -> list[list[FileEvent]]:
    """Group events that occur within a time window."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    config = DetectorConfig(time_window_ms=time_window_ms)
    detector = OperationDetector(config)
    return detector._group_events_by_time(sorted(key=lambda e: e.timestamp))


def x_group_related_events__mutmut_10(events: list[FileEvent], time_window_ms: int = 500) -> list[list[FileEvent]]:
    """Group events that occur within a time window."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    config = DetectorConfig(time_window_ms=time_window_ms)
    detector = OperationDetector(config)
    return detector._group_events_by_time(sorted(events, ))


def x_group_related_events__mutmut_11(events: list[FileEvent], time_window_ms: int = 500) -> list[list[FileEvent]]:
    """Group events that occur within a time window."""
    from provide.foundation.file.operations.detectors.orchestrator import OperationDetector

    config = DetectorConfig(time_window_ms=time_window_ms)
    detector = OperationDetector(config)
    return detector._group_events_by_time(sorted(events, key=lambda e: None))

x_group_related_events__mutmut_mutants : ClassVar[MutantDict] = {
'x_group_related_events__mutmut_1': x_group_related_events__mutmut_1, 
    'x_group_related_events__mutmut_2': x_group_related_events__mutmut_2, 
    'x_group_related_events__mutmut_3': x_group_related_events__mutmut_3, 
    'x_group_related_events__mutmut_4': x_group_related_events__mutmut_4, 
    'x_group_related_events__mutmut_5': x_group_related_events__mutmut_5, 
    'x_group_related_events__mutmut_6': x_group_related_events__mutmut_6, 
    'x_group_related_events__mutmut_7': x_group_related_events__mutmut_7, 
    'x_group_related_events__mutmut_8': x_group_related_events__mutmut_8, 
    'x_group_related_events__mutmut_9': x_group_related_events__mutmut_9, 
    'x_group_related_events__mutmut_10': x_group_related_events__mutmut_10, 
    'x_group_related_events__mutmut_11': x_group_related_events__mutmut_11
}

def group_related_events(*args, **kwargs):
    result = _mutmut_trampoline(x_group_related_events__mutmut_orig, x_group_related_events__mutmut_mutants, args, kwargs)
    return result 

group_related_events.__signature__ = _mutmut_signature(x_group_related_events__mutmut_orig)
x_group_related_events__mutmut_orig.__name__ = 'x_group_related_events'


# <3 🧱🤝📄🪄
