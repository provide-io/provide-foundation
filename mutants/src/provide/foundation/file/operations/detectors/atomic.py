# provide/foundation/file/operations/detectors/atomic.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Atomic operation detectors."""

from __future__ import annotations

from provide.foundation.file.operations.detectors.helpers import (
    extract_base_name,
    is_backup_file,
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


class AtomicOperationDetector:
    """Detects atomic file operations like safe writes and atomic saves."""

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_orig(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_1(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) <= 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_2(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 3:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_3(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(None):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_4(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) + 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_5(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 2):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_6(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = None
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_7(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = None

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_8(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i - 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_9(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 2]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_10(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                or not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_11(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                or next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_12(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                or next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_13(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                or next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_14(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                or current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_15(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(None)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_16(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type not in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_17(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"XXcreatedXX", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_18(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"CREATED", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_19(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "XXmodifiedXX"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_20(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "MODIFIED"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_21(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type != "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_22(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "XXmovedXX"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_23(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "MOVED"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_24(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path != current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_25(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_26(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(None)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_27(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = None

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_28(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = None
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_29(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(None):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_30(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 or event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_31(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i or j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_32(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j == i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_33(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j == i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_34(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i - 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_35(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 2 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_36(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path != current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_37(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(None)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_38(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=None)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_39(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: None)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_40(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=None,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_41(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=None,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_42(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=None,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_43(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=None,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_44(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=None,
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_45(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=None,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_46(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=None,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_47(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=None,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_48(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=None,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_49(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=None,
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_50(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata=None,
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_51(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_52(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_53(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_54(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_55(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_56(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_57(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_58(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_59(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_60(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_61(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_62(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=1.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_63(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[1].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_64(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[+1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_65(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-2].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_66(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_67(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=False,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_68(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "XXtemp_fileXX": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_69(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "TEMP_FILE": str(current.path),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_70(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(None),
                        "pattern": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_71(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "XXpatternXX": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_72(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "PATTERN": "atomic_save",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_73(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "XXatomic_saveXX",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_74(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect atomic save pattern (write to temp file, then rename).

        Common pattern: create temp -> write temp -> rename temp to target
        """
        if len(events) < 2:
            return None

        # Look for create/modify temp file followed by rename to target
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]

            if (
                is_temp_file(current.path)
                and current.event_type in {"created", "modified"}
                and next_event.event_type == "moved"
                and next_event.path == current.path
                and next_event.dest_path
                and not is_temp_file(next_event.dest_path)
            ):
                # Found atomic save pattern
                target_path = next_event.dest_path

                # Look for other related events (additional writes to temp)
                related_events = [current, next_event]
                for j, event in enumerate(events):
                    if j != i and j != i + 1 and event.path == current.path:
                        related_events.append(event)

                related_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=target_path,
                    events=related_events,
                    confidence=0.95,
                    description=f"Atomic save to {target_path.name}",
                    start_time=related_events[0].timestamp,
                    end_time=related_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[target_path],
                    metadata={
                        "temp_file": str(current.path),
                        "pattern": "ATOMIC_SAVE",
                    },
                )

        return None

    xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_1": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_1,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_2": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_2,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_3": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_3,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_4": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_4,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_5": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_5,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_6": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_6,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_7": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_7,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_8": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_8,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_9": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_9,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_10": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_10,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_11": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_11,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_12": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_12,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_13": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_13,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_14": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_14,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_15": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_15,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_16": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_16,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_17": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_17,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_18": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_18,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_19": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_19,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_20": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_20,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_21": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_21,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_22": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_22,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_23": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_23,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_24": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_24,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_25": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_25,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_26": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_26,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_27": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_27,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_28": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_28,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_29": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_29,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_30": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_30,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_31": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_31,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_32": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_32,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_33": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_33,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_34": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_34,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_35": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_35,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_36": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_36,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_37": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_37,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_38": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_38,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_39": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_39,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_40": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_40,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_41": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_41,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_42": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_42,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_43": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_43,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_44": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_44,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_45": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_45,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_46": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_46,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_47": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_47,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_48": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_48,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_49": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_49,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_50": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_50,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_51": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_51,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_52": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_52,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_53": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_53,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_54": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_54,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_55": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_55,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_56": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_56,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_57": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_57,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_58": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_58,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_59": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_59,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_60": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_60,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_61": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_61,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_62": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_62,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_63": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_63,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_64": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_64,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_65": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_65,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_66": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_66,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_67": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_67,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_68": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_68,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_69": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_69,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_70": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_70,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_71": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_71,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_72": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_72,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_73": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_73,
        "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_74": xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_74,
    }

    def detect_atomic_save(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_orig"),
            object.__getattribute__(self, "xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    detect_atomic_save.__signature__ = _mutmut_signature(
        xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_orig
    )
    xǁAtomicOperationDetectorǁdetect_atomic_save__mutmut_orig.__name__ = (
        "xǁAtomicOperationDetectorǁdetect_atomic_save"
    )

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_orig(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_1(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) <= 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_2(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 3:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_3(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = None
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_4(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = None

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_5(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(None):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_6(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(None)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_7(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(None)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_8(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_9(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"XXmovedXX", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_10(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"MOVED", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_11(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "XXcreatedXX"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_12(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "CREATED"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_13(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                break

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_14(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = None
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_15(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(None)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_16(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_17(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                break

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_18(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = None
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_19(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = None

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_20(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent * base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_21(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = None

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_22(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original or e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_23(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path != expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_24(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type not in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_25(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"XXcreatedXX", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_26(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"CREATED", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_27(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "XXmodifiedXX"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_28(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "MODIFIED"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_29(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = None
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_30(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[1]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_31(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = None
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_32(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=None)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_33(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: None)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_34(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=None,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_35(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=None,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_36(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=None,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_37(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=None,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_38(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=None,
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_39(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=None,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_40(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=None,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_41(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=None,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_42(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=None,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_43(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=None,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_44(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=None,
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_45(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata=None,
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_46(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_47(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_48(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_49(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_50(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_51(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_52(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_53(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_54(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_55(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_56(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_57(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_58(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=1.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_59(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[1].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_60(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[+1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_61(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-2].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_62(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_63(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=False,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_64(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=False,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_65(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "XXbackup_fileXX": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_66(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "BACKUP_FILE": str(backup_event.path),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_67(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(None),
                        "pattern": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_68(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "XXpatternXX": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_69(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "PATTERN": "safe_write",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_70(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "XXsafe_writeXX",
                    },
                )

        return None

    def xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_71(
        self, events: list[FileEvent]
    ) -> FileOperation | None:
        """Detect safe write pattern (backup original, write new, cleanup).

        Common pattern: create backup -> modify original OR rename original to backup -> create new
        """
        if len(events) < 2:
            return None

        # Find backup files and match them with original files
        backup_events = []
        regular_events = []

        for event in events:
            if is_backup_file(event.path):
                backup_events.append(event)
            else:
                regular_events.append(event)

        # Try to match backup files with regular files
        for backup_event in backup_events:
            if backup_event.event_type not in {"moved", "created"}:
                continue

            # Extract base name from backup
            base_name = extract_base_name(backup_event.path)
            if not base_name:
                continue

            backup_parent = backup_event.path.parent
            expected_original = backup_parent / base_name

            # Find matching original file events
            matching_events = [
                e
                for e in regular_events
                if e.path == expected_original and e.event_type in {"created", "modified"}
            ]

            if matching_events:
                # Found safe write pattern
                original_event = matching_events[0]
                all_events = [backup_event, original_event]
                all_events.sort(key=lambda e: e.timestamp)

                return FileOperation(
                    operation_type=OperationType.SAFE_WRITE,
                    primary_path=original_event.path,
                    events=all_events,
                    confidence=0.95,
                    description=f"Safe write to {original_event.path.name}",
                    start_time=all_events[0].timestamp,
                    end_time=all_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    has_backup=True,
                    files_affected=[original_event.path],
                    metadata={
                        "backup_file": str(backup_event.path),
                        "pattern": "SAFE_WRITE",
                    },
                )

        return None

    xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_1": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_1,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_2": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_2,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_3": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_3,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_4": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_4,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_5": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_5,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_6": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_6,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_7": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_7,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_8": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_8,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_9": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_9,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_10": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_10,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_11": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_11,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_12": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_12,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_13": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_13,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_14": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_14,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_15": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_15,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_16": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_16,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_17": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_17,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_18": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_18,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_19": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_19,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_20": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_20,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_21": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_21,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_22": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_22,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_23": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_23,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_24": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_24,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_25": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_25,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_26": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_26,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_27": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_27,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_28": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_28,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_29": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_29,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_30": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_30,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_31": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_31,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_32": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_32,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_33": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_33,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_34": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_34,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_35": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_35,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_36": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_36,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_37": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_37,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_38": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_38,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_39": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_39,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_40": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_40,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_41": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_41,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_42": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_42,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_43": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_43,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_44": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_44,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_45": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_45,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_46": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_46,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_47": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_47,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_48": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_48,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_49": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_49,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_50": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_50,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_51": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_51,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_52": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_52,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_53": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_53,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_54": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_54,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_55": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_55,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_56": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_56,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_57": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_57,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_58": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_58,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_59": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_59,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_60": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_60,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_61": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_61,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_62": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_62,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_63": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_63,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_64": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_64,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_65": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_65,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_66": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_66,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_67": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_67,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_68": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_68,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_69": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_69,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_70": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_70,
        "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_71": xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_71,
    }

    def detect_safe_write(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_orig"),
            object.__getattribute__(self, "xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    detect_safe_write.__signature__ = _mutmut_signature(
        xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_orig
    )
    xǁAtomicOperationDetectorǁdetect_safe_write__mutmut_orig.__name__ = (
        "xǁAtomicOperationDetectorǁdetect_safe_write"
    )


# <3 🧱🤝📄🪄
