# provide/foundation/file/operations/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""File operation detection and analysis.

This module provides intelligent detection and grouping of file system events
into logical operations (e.g., atomic saves, batch updates, rename sequences).

## Simple API (Recommended)

For most use cases, use the simple functional API:

    >>> from provide.foundation.file.operations import detect, Event, Operation
    >>>
    >>> events = [Event(...), Event(...)]
    >>> operation = detect(events)
    >>> if operation:
    ...     print(f"{operation.type}: {operation.path}")

## Advanced API

For streaming detection or custom configuration:

    >>> from provide.foundation.file.operations import create_detector, DetectorConfig
    >>>
    >>> config = DetectorConfig(time_window_ms=1000)
    >>> detector = create_detector(config)
    >>>
    >>> for event in event_stream:
    ...     if operation := detector.detect_streaming(event):
    ...         handle_operation(operation)
"""

from __future__ import annotations

# ============================================================================
# SIMPLE API (Recommended for most users)
# ============================================================================
# Simple detection functions
from provide.foundation.file.operations.detect import (
    create_detector,
    detect,
    detect_all,
    detect_streaming,
)

# ============================================================================
# FULL API (For backward compatibility and advanced usage)
# ============================================================================
# Original detector class
from provide.foundation.file.operations.detectors import OperationDetector

# Simplified type aliases
# Complete type system
from provide.foundation.file.operations.types import (
    DetectorConfig,
    FileEvent,
    FileEvent as Event,
    FileEventMetadata,
    FileOperation,
    FileOperation as Operation,
    OperationType,
)

# Utility functions
from provide.foundation.file.operations.utils import (
    detect_atomic_save,
    extract_original_path,
    group_related_events,
    is_temp_file,
)

__all__ = [
    "DetectorConfig",
    "Event",
    "FileEvent",
    "FileEventMetadata",
    "FileOperation",
    "Operation",
    "OperationDetector",
    "OperationType",
    "create_detector",
    "detect",
    "detect_all",
    "detect_atomic_save",
    "detect_streaming",
    "extract_original_path",
    "group_related_events",
    "is_temp_file",
]
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


# <3 🧱🤝📄🪄
