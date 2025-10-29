# provide/foundation/file/operations/detectors/temp.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Temporary file pattern detectors."""

from __future__ import annotations

from pathlib import Path

from provide.foundation.file.operations.detectors.helpers import (
    extract_base_name,
    is_temp_file,
)
from provide.foundation.file.operations.types import (
    FileEvent,
    FileOperation,
    OperationType,
)
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


class TempPatternDetector:
    """Detects patterns involving temporary files."""

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_orig(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_1(
        self, events: list[FileEvent], temp_window_ms: int = 1001
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_2(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) <= 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_3(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 3:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_4(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(None):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_5(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) + 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_6(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 2):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_7(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = None
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_8(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = None

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_9(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i - 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_10(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 2]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_11(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = None

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_12(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() / 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_13(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp + current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_14(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1001

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_15(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                or time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_16(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                or next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_17(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                or next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_18(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                or next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_19(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                or is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_20(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type != "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_21(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "XXcreatedXX"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_22(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "CREATED"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_23(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(None)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_24(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type != "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_25(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "XXmovedXX"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_26(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "MOVED"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_27(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path != current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_28(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff < temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_29(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=None,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_30(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=None,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_31(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=None,
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_32(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=None,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_33(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=None,
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_34(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=None,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_35(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=None,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_36(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=None,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_37(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=None,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_38(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=None,
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_39(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata=None,
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_40(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_41(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_42(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_43(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_44(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_45(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_46(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_47(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_48(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_49(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_50(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_51(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=1.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_52(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_53(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=False,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_54(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "XXtemp_fileXX": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_55(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "TEMP_FILE": str(current.path),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_56(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(None),
                        "pattern": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_57(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "XXpatternXX": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_58(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "PATTERN": "temp_rename",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_59(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "XXtemp_renameXX",
                    },
                )

        return None

    def xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_60(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect temp file rename pattern: create temp -> rename to final."""
        if len(events) < 2:
            return None

        # Look for temp file creation followed by rename
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            time_diff = (next_event.timestamp - current.timestamp).total_seconds() * 1000

            if (
                current.event_type == "created"
                and is_temp_file(current.path)
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and time_diff <= temp_window_ms
            ):
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=next_event.dest_path,
                    events=[current, next_event],
                    confidence=0.95,
                    description=f"Atomic save to {next_event.dest_path.name}",
                    start_time=current.timestamp,
                    end_time=next_event.timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[next_event.dest_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "TEMP_RENAME",
                    },
                )

        return None

    xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_1": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_1,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_2": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_2,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_3": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_3,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_4": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_4,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_5": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_5,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_6": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_6,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_7": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_7,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_8": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_8,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_9": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_9,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_10": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_10,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_11": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_11,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_12": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_12,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_13": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_13,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_14": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_14,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_15": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_15,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_16": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_16,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_17": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_17,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_18": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_18,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_19": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_19,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_20": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_20,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_21": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_21,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_22": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_22,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_23": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_23,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_24": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_24,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_25": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_25,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_26": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_26,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_27": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_27,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_28": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_28,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_29": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_29,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_30": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_30,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_31": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_31,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_32": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_32,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_33": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_33,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_34": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_34,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_35": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_35,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_36": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_36,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_37": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_37,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_38": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_38,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_39": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_39,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_40": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_40,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_41": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_41,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_42": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_42,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_43": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_43,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_44": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_44,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_45": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_45,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_46": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_46,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_47": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_47,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_48": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_48,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_49": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_49,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_50": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_50,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_51": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_51,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_52": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_52,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_53": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_53,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_54": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_54,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_55": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_55,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_56": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_56,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_57": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_57,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_58": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_58,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_59": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_59,
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_60": xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_60,
    }

    def detect_temp_rename_pattern(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_orig"),
            object.__getattribute__(self, "xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    detect_temp_rename_pattern.__signature__ = _mutmut_signature(
        xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_orig
    )
    xǁTempPatternDetectorǁdetect_temp_rename_pattern__mutmut_orig.__name__ = (
        "xǁTempPatternDetectorǁdetect_temp_rename_pattern"
    )

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_orig(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_1(
        self, events: list[FileEvent], temp_window_ms: int = 1001
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_2(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) <= 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_3(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 4:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_4(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(None):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_5(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) + 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_6(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 3):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_7(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = None
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_8(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = None
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_9(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i - 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_10(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 2]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_11(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = None

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_12(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i - 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_13(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 3]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_14(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                or temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_15(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                or temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_16(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                or temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_17(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                or is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_18(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                or temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_19(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type != "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_20(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "XXdeletedXX"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_21(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "DELETED"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_22(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type != "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_23(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "XXcreatedXX"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_24(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "CREATED"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_25(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(None)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_26(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type != "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_27(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "XXmovedXX"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_28(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "MOVED"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_29(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path != temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_30(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path != delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_31(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = None

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_32(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() / 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_33(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp + delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_34(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1001

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_35(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span < temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_36(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=None,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_37(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=None,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_38(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=None,
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_39(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=None,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_40(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=None,
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_41(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=None,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_42(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=None,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_43(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=None,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_44(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=None,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_45(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=None,
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_46(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata=None,
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_47(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_48(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_49(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_50(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_51(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_52(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_53(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_54(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_55(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_56(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_57(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_58(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=1.9,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_59(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=False,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_60(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=False,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_61(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "XXtemp_fileXX": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_62(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "TEMP_FILE": str(temp_create.path),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_63(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(None),
                            "pattern": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_64(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "XXpatternXX": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_65(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "PATTERN": "delete_temp_rename",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_66(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "XXdelete_temp_renameXX",
                        },
                    )

        return None

    def xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_67(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: delete original -> create temp -> rename temp."""
        if len(events) < 3:
            return None

        for i in range(len(events) - 2):
            delete_event = events[i]
            temp_create = events[i + 1]
            temp_rename = events[i + 2]

            if (
                delete_event.event_type == "deleted"
                and temp_create.event_type == "created"
                and is_temp_file(temp_create.path)
                and temp_rename.event_type == "moved"
                and temp_rename.path == temp_create.path
                and temp_rename.dest_path == delete_event.path
            ):
                time_span = (temp_rename.timestamp - delete_event.timestamp).total_seconds() * 1000

                if time_span <= temp_window_ms:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=delete_event.path,
                        events=[delete_event, temp_create, temp_rename],
                        confidence=0.90,
                        description=f"File atomically saved via temp: {delete_event.path.name}",
                        start_time=delete_event.timestamp,
                        end_time=temp_rename.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[delete_event.path],
                        metadata={
                            "temp_file": str(temp_create.path),
                            "pattern": "DELETE_TEMP_RENAME",
                        },
                    )

        return None

    xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_1": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_1,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_2": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_2,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_3": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_3,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_4": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_4,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_5": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_5,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_6": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_6,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_7": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_7,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_8": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_8,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_9": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_9,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_10": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_10,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_11": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_11,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_12": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_12,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_13": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_13,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_14": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_14,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_15": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_15,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_16": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_16,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_17": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_17,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_18": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_18,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_19": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_19,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_20": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_20,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_21": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_21,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_22": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_22,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_23": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_23,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_24": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_24,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_25": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_25,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_26": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_26,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_27": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_27,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_28": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_28,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_29": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_29,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_30": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_30,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_31": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_31,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_32": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_32,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_33": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_33,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_34": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_34,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_35": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_35,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_36": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_36,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_37": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_37,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_38": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_38,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_39": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_39,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_40": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_40,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_41": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_41,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_42": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_42,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_43": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_43,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_44": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_44,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_45": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_45,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_46": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_46,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_47": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_47,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_48": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_48,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_49": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_49,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_50": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_50,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_51": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_51,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_52": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_52,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_53": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_53,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_54": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_54,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_55": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_55,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_56": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_56,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_57": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_57,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_58": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_58,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_59": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_59,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_60": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_60,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_61": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_61,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_62": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_62,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_63": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_63,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_64": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_64,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_65": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_65,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_66": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_66,
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_67": xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_67,
    }

    def detect_delete_temp_pattern(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_orig"),
            object.__getattribute__(self, "xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    detect_delete_temp_pattern.__signature__ = _mutmut_signature(
        xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_orig
    )
    xǁTempPatternDetectorǁdetect_delete_temp_pattern__mutmut_orig.__name__ = (
        "xǁTempPatternDetectorǁdetect_delete_temp_pattern"
    )

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_orig(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_1(
        self, events: list[FileEvent], temp_window_ms: int = 1001
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_2(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) <= 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_3(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 4:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_4(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = None
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_5(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(None):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_6(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = None
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_7(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(None)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_8(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_9(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = None
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_10(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(None)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_11(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) <= 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_12(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 3:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_13(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                break

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_14(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=None)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_15(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: None)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_16(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" or any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_17(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[1].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_18(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type != "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_19(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "XXcreatedXX" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_20(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "CREATED" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_21(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(None):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_22(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type != "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_23(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "XXmodifiedXX" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_24(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "MODIFIED" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_25(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[2:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_26(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = None
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_27(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(None)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_28(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = None

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_29(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" or e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_30(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type != "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_31(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "XXmovedXX" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_32(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "MOVED" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_33(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path != temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_34(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = None
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_35(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[1]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_36(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = None
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_37(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=None)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_38(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: None)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_39(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = None

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_40(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() / 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_41(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp + all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_42(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[+1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_43(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-2].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_44(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[1].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_45(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1001

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_46(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span < temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_47(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = None
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_48(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path and rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_49(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=None,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_50(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=None,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_51(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=None,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_52(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=None,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_53(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=None,
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_54(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=None,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_55(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=None,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_56(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=None,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_57(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=None,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_58(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=None,
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_59(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata=None,
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_60(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_61(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_62(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_63(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_64(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_65(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_66(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_67(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_68(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_69(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_70(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_71(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=1.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_72(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[1].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_73(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[+1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_74(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-2].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_75(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=False,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_76(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=False,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_77(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "XXtemp_fileXX": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_78(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "TEMP_FILE": temp_path_str,
                                "pattern": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_79(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "XXpatternXX": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_80(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "PATTERN": "temp_modify_rename",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_81(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "XXtemp_modify_renameXX",
                            },
                        )

        return None

    def xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_82(
        self, events: list[FileEvent], temp_window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> modify temp -> rename to final."""
        if len(events) < 3:
            return None

        # Group events by temp files
        temp_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_groups:
                    temp_groups[path_str] = []
                temp_groups[path_str].append(event)

        for temp_path_str, temp_events in temp_groups.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Look for create -> modify -> rename sequence
            if temp_events[0].event_type == "created" and any(
                e.event_type == "modified" for e in temp_events[1:]
            ):
                # Find corresponding rename event
                temp_path = Path(temp_path_str)
                rename_events = [e for e in events if e.event_type == "moved" and e.path == temp_path]

                if rename_events:
                    rename_event = rename_events[0]
                    all_events = [*temp_events, rename_event]
                    all_events.sort(key=lambda e: e.timestamp)

                    time_span = (all_events[-1].timestamp - all_events[0].timestamp).total_seconds() * 1000

                    if time_span <= temp_window_ms:
                        final_path = rename_event.dest_path or rename_event.path
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=final_path,
                            events=all_events,
                            confidence=0.92,
                            description=f"Atomic save to {final_path.name}",
                            start_time=all_events[0].timestamp,
                            end_time=all_events[-1].timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[final_path],
                            metadata={
                                "temp_file": temp_path_str,
                                "pattern": "TEMP_MODIFY_RENAME",
                            },
                        )

        return None

    xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_1": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_1,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_2": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_2,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_3": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_3,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_4": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_4,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_5": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_5,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_6": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_6,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_7": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_7,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_8": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_8,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_9": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_9,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_10": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_10,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_11": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_11,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_12": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_12,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_13": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_13,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_14": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_14,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_15": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_15,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_16": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_16,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_17": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_17,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_18": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_18,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_19": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_19,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_20": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_20,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_21": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_21,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_22": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_22,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_23": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_23,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_24": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_24,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_25": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_25,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_26": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_26,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_27": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_27,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_28": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_28,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_29": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_29,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_30": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_30,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_31": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_31,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_32": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_32,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_33": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_33,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_34": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_34,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_35": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_35,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_36": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_36,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_37": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_37,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_38": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_38,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_39": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_39,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_40": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_40,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_41": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_41,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_42": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_42,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_43": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_43,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_44": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_44,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_45": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_45,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_46": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_46,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_47": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_47,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_48": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_48,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_49": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_49,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_50": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_50,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_51": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_51,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_52": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_52,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_53": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_53,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_54": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_54,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_55": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_55,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_56": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_56,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_57": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_57,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_58": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_58,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_59": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_59,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_60": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_60,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_61": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_61,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_62": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_62,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_63": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_63,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_64": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_64,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_65": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_65,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_66": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_66,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_67": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_67,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_68": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_68,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_69": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_69,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_70": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_70,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_71": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_71,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_72": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_72,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_73": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_73,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_74": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_74,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_75": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_75,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_76": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_76,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_77": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_77,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_78": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_78,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_79": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_79,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_80": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_80,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_81": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_81,
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_82": xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_82,
    }

    def detect_temp_modify_pattern(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_orig"),
            object.__getattribute__(self, "xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    detect_temp_modify_pattern.__signature__ = _mutmut_signature(
        xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_orig
    )
    xǁTempPatternDetectorǁdetect_temp_modify_pattern__mutmut_orig.__name__ = (
        "xǁTempPatternDetectorǁdetect_temp_modify_pattern"
    )

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_orig(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_1(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5001
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_2(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) <= 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_3(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 3:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_4(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = None
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_5(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = None

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_6(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(None):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_7(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = None
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_8(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(None)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_9(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_10(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = None
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_11(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(None)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_12(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = None
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_13(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(None)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_14(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_15(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = None
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_16(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(None)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_17(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) <= 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_18(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 3:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_19(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                break

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_20(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=None)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_21(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: None)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_22(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" or temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_23(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[1].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_24(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type != "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_25(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "XXcreatedXX" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_26(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "CREATED" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_27(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[+1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_28(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-2].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_29(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type != "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_30(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "XXdeletedXX":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_31(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "DELETED":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_32(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = None
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_33(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(None)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_34(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = None

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_35(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(None)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_36(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = None
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_37(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent * base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_38(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = None

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_39(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(None)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_40(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str not in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_41(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = None
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_42(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                or real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_43(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type != "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_44(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "XXcreatedXX"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_45(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "CREATED"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_46(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp > temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_47(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[+1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_48(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-2].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_49(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = None

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_50(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() / 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_51(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp + temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_52(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[1].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_53(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1001

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_54(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span < temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_55(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = None
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_56(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=None)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_57(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: None)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_58(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=None,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_59(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=None,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_60(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=None,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_61(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=None,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_62(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=None,
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_63(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=None,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_64(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=None,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_65(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=None,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_66(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=None,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_67(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=None,
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_68(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata=None,
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_69(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_70(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_71(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_72(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_73(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_74(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_75(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_76(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_77(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_78(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_79(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_80(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=1.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_81(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[1].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_82(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[+1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_83(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-2].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_84(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=False,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_85(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=False,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_86(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "XXtemp_fileXX": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_87(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "TEMP_FILE": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_88(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "XXpatternXX": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_89(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "PATTERN": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_90(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "XXtemp_create_delete_create_realXX",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_91(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "TEMP_CREATE_DELETE_CREATE_REAL",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_92(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    None,
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_93(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=None,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_94(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=None,
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_95(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_96(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_97(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "Temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_98(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "XXTemp file created and deleted with no real file - not returning operationXX",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_99(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "temp file created and deleted with no real file - not returning operation",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    def xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_100(  # noqa: C901
        self, events: list[FileEvent], temp_window_ms: int = 5000
    ) -> FileOperation | None:
        """Detect pattern: create temp -> delete temp -> create real file.

        Note: High complexity is intentional to handle all temp file patterns.
        """
        if len(events) < 2:
            return None

        # Look for temp file creation followed by deletion, then real file creation
        temp_files: dict[str, list[FileEvent]] = {}
        real_files: dict[str, list[FileEvent]] = {}

        for event in events:
            if is_temp_file(event.path):
                path_str = str(event.path)
                if path_str not in temp_files:
                    temp_files[path_str] = []
                temp_files[path_str].append(event)
            else:
                path_str = str(event.path)
                if path_str not in real_files:
                    real_files[path_str] = []
                real_files[path_str].append(event)

        # Check for create temp -> delete temp -> create real pattern
        for temp_path_str, temp_events in temp_files.items():
            if len(temp_events) < 2:
                continue

            temp_events.sort(key=lambda e: e.timestamp)

            # Check for create -> delete pattern on temp file
            if temp_events[0].event_type == "created" and temp_events[-1].event_type == "deleted":
                # Extract base name from temp file
                temp_path = Path(temp_path_str)
                base_name = extract_base_name(temp_path)

                # Look for real file creation after temp deletion
                if base_name:
                    real_path = temp_path.parent / base_name
                    real_path_str = str(real_path)

                    if real_path_str in real_files:
                        real_events = real_files[real_path_str]
                        # Find create events after temp deletion
                        for real_event in real_events:
                            if (
                                real_event.event_type == "created"
                                and real_event.timestamp >= temp_events[-1].timestamp
                            ):
                                time_span = (
                                    real_event.timestamp - temp_events[0].timestamp
                                ).total_seconds() * 1000

                                if time_span <= temp_window_ms:
                                    all_events = [*temp_events, real_event]
                                    all_events.sort(key=lambda e: e.timestamp)

                                    return FileOperation(
                                        operation_type=OperationType.ATOMIC_SAVE,
                                        primary_path=real_path,
                                        events=all_events,
                                        confidence=0.92,
                                        description=f"Atomic save to {real_path.name}",
                                        start_time=all_events[0].timestamp,
                                        end_time=all_events[-1].timestamp,
                                        is_atomic=True,
                                        is_safe=True,
                                        files_affected=[real_path],
                                        metadata={
                                            "temp_file": temp_path_str,
                                            "pattern": "temp_create_delete_create_real",
                                        },
                                    )

                # If no real file found, don't return an operation
                # Pure temp file operations (create→delete with no real file) should be
                # filtered by the auto-flush handler, not returned as invalid operations
                log.debug(
                    "TEMP FILE CREATED AND DELETED WITH NO REAL FILE - NOT RETURNING OPERATION",
                    temp_file=temp_path_str,
                    event_count=len(temp_events),
                )
                # Return None - let auto-flush handler filter these temp-only events

        return None

    xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_1": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_1,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_2": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_2,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_3": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_3,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_4": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_4,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_5": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_5,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_6": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_6,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_7": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_7,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_8": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_8,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_9": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_9,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_10": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_10,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_11": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_11,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_12": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_12,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_13": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_13,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_14": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_14,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_15": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_15,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_16": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_16,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_17": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_17,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_18": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_18,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_19": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_19,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_20": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_20,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_21": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_21,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_22": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_22,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_23": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_23,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_24": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_24,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_25": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_25,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_26": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_26,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_27": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_27,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_28": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_28,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_29": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_29,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_30": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_30,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_31": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_31,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_32": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_32,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_33": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_33,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_34": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_34,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_35": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_35,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_36": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_36,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_37": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_37,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_38": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_38,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_39": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_39,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_40": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_40,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_41": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_41,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_42": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_42,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_43": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_43,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_44": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_44,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_45": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_45,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_46": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_46,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_47": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_47,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_48": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_48,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_49": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_49,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_50": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_50,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_51": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_51,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_52": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_52,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_53": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_53,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_54": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_54,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_55": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_55,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_56": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_56,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_57": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_57,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_58": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_58,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_59": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_59,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_60": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_60,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_61": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_61,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_62": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_62,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_63": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_63,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_64": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_64,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_65": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_65,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_66": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_66,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_67": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_67,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_68": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_68,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_69": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_69,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_70": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_70,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_71": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_71,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_72": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_72,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_73": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_73,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_74": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_74,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_75": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_75,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_76": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_76,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_77": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_77,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_78": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_78,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_79": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_79,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_80": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_80,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_81": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_81,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_82": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_82,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_83": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_83,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_84": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_84,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_85": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_85,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_86": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_86,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_87": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_87,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_88": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_88,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_89": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_89,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_90": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_90,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_91": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_91,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_92": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_92,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_93": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_93,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_94": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_94,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_95": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_95,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_96": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_96,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_97": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_97,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_98": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_98,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_99": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_99,
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_100": xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_100,
    }

    def detect_temp_create_delete_pattern(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    detect_temp_create_delete_pattern.__signature__ = _mutmut_signature(
        xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_orig
    )
    xǁTempPatternDetectorǁdetect_temp_create_delete_pattern__mutmut_orig.__name__ = (
        "xǁTempPatternDetectorǁdetect_temp_create_delete_pattern"
    )


# <3 🧱🤝📄🪄
